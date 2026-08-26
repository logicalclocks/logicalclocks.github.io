// Diagram edge router + paint-order lift for the hops-diagram kit.
//
// Two jobs, run once at load, in order, before hops-viz.js snapshots the SVG:
//
// 1. ROUTE. An edge may declare its endpoints instead of hand-drawing them:
//      <path class="viz-edge" data-from="fg-a" data-to="def-box"
//            data-from-side="bottom" data-to-side="top" data-to-x="380">
//    The router reads the two node boxes and computes a path that always exits
//    the source perpendicular to its side, bends in the middle, and enters the
//    target perpendicular to its side with the endpoint ON the target border
//    (the arrow marker's refX docks the tip there). One rule, every diagram:
//    change the routing here and all declared edges follow. Coordinates are read
//    from the static <rect> attributes, so this is layout-independent and the
//    computed `d` is deterministic. Edges that hand-author `d` (no data-from/to)
//    are left untouched, so migration is incremental.
//      - data-from / data-to: node ids (a <rect> or a <g> wrapping one).
//      - data-from-side / data-to-side: top|bottom|left|right. Omitted -> the
//        side facing the other node.
//      - data-from-x/-y, data-to-x/-y: absolute anchor coord along that side
//        (x for top/bottom, y for left/right). Omitted -> centered on the side.
//      - data-route: "smooth" (default) or "straight".
//
// 2. LIFT. SVG paint order is document order, and the kit authors every edge
//    before its destination node, so the node painted over the arrowhead/knob.
//    We lift every top-level .viz-edge to the end of its <svg> so heads and knobs
//    dock on top of the border. Only direct-child edges move; an edge nested in
//    an animated transform group is left where it is.
//
// Registered before hops-viz.js (mkdocs.yml order) so the driver captures the
// routed, reordered SVG as its pristine snapshot and replay/loop stay consistent.
(function () {
  "use strict";

  function num(v) {
    if (v == null) return null;
    var n = parseFloat(v);
    return isNaN(n) ? null : n;
  }

  function round(n) {
    return Math.round(n * 10) / 10;
  }

  // The node's box in SVG user space, read from its primary <rect>.
  function nodeBox(svg, id) {
    var el = svg.getElementById(id);
    if (!el) return null;
    var rect =
      el.tagName && el.tagName.toLowerCase() === "rect"
        ? el
        : el.querySelector(
            "rect.viz-node, rect.viz-code-box, rect.viz-kv-frame, rect.viz-zone, rect",
          );
    if (!rect) return null;
    var x = num(rect.getAttribute("x")) || 0;
    var y = num(rect.getAttribute("y")) || 0;
    var w = num(rect.getAttribute("width")) || 0;
    var h = num(rect.getAttribute("height")) || 0;
    return { x: x, y: y, w: w, h: h, cx: x + w / 2, cy: y + h / 2 };
  }

  // A docking point on one side of a box, with the outward normal for that side.
  // `at` is the absolute coord along the side (x for top/bottom, y for left/right).
  function anchor(box, side, at) {
    switch (side) {
      case "top":
        return { x: at == null ? box.cx : at, y: box.y, nx: 0, ny: -1 };
      case "bottom":
        return { x: at == null ? box.cx : at, y: box.y + box.h, nx: 0, ny: 1 };
      case "left":
        return { x: box.x, y: at == null ? box.cy : at, nx: -1, ny: 0 };
      case "right":
        return { x: box.x + box.w, y: at == null ? box.cy : at, nx: 1, ny: 0 };
      default:
        return null;
    }
  }

  // Pick the facing sides when the author does not name them: whichever axis
  // separates the two centers more decides top/bottom vs left/right.
  function inferSides(from, to) {
    var dx = to.cx - from.cx;
    var dy = to.cy - from.cy;
    if (Math.abs(dy) >= Math.abs(dx)) {
      return dy >= 0 ? ["bottom", "top"] : ["top", "bottom"];
    }
    return dx >= 0 ? ["right", "left"] : ["left", "right"];
  }

  // Minimum straight run-in into the head, in user units. The arrow marker needs
  // a straight segment to align to; without it the head meets the curve on a
  // tangent and reads as floating off the border (mechanic M1, "earned
  // approach"). This is the min distance the line reserves so the head docks
  // square. Kept in step with viz_overlap_check.py RUN_IN.
  var RUN_IN = 16;

  // Perpendicular exit, bend, then a STRAIGHT run-in into the head. The curve
  // reaches an approach point set back RUN_IN from the target along its normal,
  // then a straight line covers the last leg so the arrow aligns to the border.
  // When the gap is tighter than RUN_IN the run-in shrinks to fit and the curve
  // takes the extra distance; a straight-on edge collapses to a plain line.
  function buildPath(S, T, mode) {
    if (mode === "straight") {
      return "M" + round(S.x) + " " + round(S.y) + " L" + round(T.x) + " " + round(T.y);
    }
    // how far the source sits out from the target's border, along that normal;
    // the run-in can never exceed it or the approach point falls behind the source.
    var perpGap = Math.abs((S.x - T.x) * T.nx + (S.y - T.y) * T.ny);
    var runIn = Math.min(RUN_IN, perpGap * 0.6);
    var Ax = T.x + T.nx * runIn;
    var Ay = T.y + T.ny * runIn;
    var dx = Ax - S.x;
    var dy = Ay - S.y;
    var dist = Math.hypot(dx, dy);
    var projS = Math.abs(dx * S.nx + dy * S.ny);
    var projA = Math.abs(-dx * T.nx - dy * T.ny);
    var perp = Math.min(projS, projA);
    var k = Math.min(Math.max(12, 0.4 * dist), 0.45 * perp, 64);
    if (!(k > 0)) k = Math.max(2, 0.4 * dist);
    var p1x = S.x + S.nx * k;
    var p1y = S.y + S.ny * k;
    var p2x = Ax + T.nx * k;
    var p2y = Ay + T.ny * k;
    return (
      "M" + round(S.x) + " " + round(S.y) +
      " C" + round(p1x) + " " + round(p1y) +
      " " + round(p2x) + " " + round(p2y) +
      " " + round(Ax) + " " + round(Ay) +
      " L" + round(T.x) + " " + round(T.y)
    );
  }

  function route(svg) {
    svg.querySelectorAll(".viz-edge[data-from][data-to]").forEach(function (edge) {
      try {
        var from = nodeBox(svg, edge.getAttribute("data-from"));
        var to = nodeBox(svg, edge.getAttribute("data-to"));
        if (!from || !to) return;
        var sides = inferSides(from, to);
        var fs = edge.getAttribute("data-from-side") || sides[0];
        var ts = edge.getAttribute("data-to-side") || sides[1];
        var fAt =
          fs === "left" || fs === "right"
            ? num(edge.getAttribute("data-from-y"))
            : num(edge.getAttribute("data-from-x"));
        var tAt =
          ts === "left" || ts === "right"
            ? num(edge.getAttribute("data-to-y"))
            : num(edge.getAttribute("data-to-x"));
        var S = anchor(from, fs, fAt);
        var T = anchor(to, ts, tAt);
        if (!S || !T) return;
        edge.setAttribute("d", buildPath(S, T, edge.getAttribute("data-route") || "smooth"));
      } catch (e) {
        /* one malformed edge must not break the rest of the diagram */
      }
    });
  }

  function lift(svg) {
    svg.querySelectorAll(":scope > .viz-edge").forEach(function (edge) {
      svg.appendChild(edge);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".md-typeset .hops-diagram svg").forEach(function (svg) {
      route(svg);
      lift(svg);
    });
  });
})();
