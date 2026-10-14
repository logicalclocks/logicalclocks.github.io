// Provenance highlight for schema diagrams. Elements that carry the same
// data-prov key light up together when one is hovered, so a derived column
// (e.g. a feature-view column) reveals which source columns it comes from.
//
// Hover is handled by delegation on the document, so it works for the inline
// diagram AND for the cloned copy the zoom overlay builds (the earlier
// per-element listeners never reached the clone). Progressive enhancement:
// without JS the rows still render, they just do not light up.
//
// A figure opts into a slow auto demo with data-prov-cycle on its <svg>: the
// driver walks the distinct keys one at a time. It pauses while the reader
// hovers that figure, runs only while on screen, and honours reduced-motion.
(function () {
  "use strict";

  var CYCLE_MS = 1800;
  var hoverSvg = null; // svg currently under the reader's pointer

  function paint(svg, key) {
    svg.querySelectorAll(".prov-active").forEach(function (el) {
      el.classList.remove("prov-active");
    });
    if (key) {
      svg.querySelectorAll('[data-prov="' + key + '"]').forEach(function (el) {
        el.classList.add("prov-active");
      });
    }
  }

  // Delegated hover: covers inline diagrams and cloned (zoomed) copies alike.
  document.addEventListener("mouseover", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var row = t.closest("[data-prov]");
    if (!row) return;
    var svg = row.closest("svg");
    if (!svg) return;
    hoverSvg = svg;
    paint(svg, row.getAttribute("data-prov"));
  });
  document.addEventListener("mouseout", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var row = t.closest("[data-prov]");
    if (!row) return;
    var svg = row.closest("svg");
    if (!svg) return;
    var rel = e.relatedTarget;
    var toRow = rel && rel.closest ? rel.closest("[data-prov]") : null;
    if (toRow && toRow.closest("svg") === svg) return; // still inside this svg
    if (hoverSvg === svg) hoverSvg = null;
    paint(svg, null);
  });

  function wireAuto(root) {
    (root || document).querySelectorAll(".hops-viz svg[data-prov-cycle]")
      .forEach(function (svg) {
        if (svg.dataset.provAuto) return;
        if (!svg.querySelector("[data-prov]")) return;
        if (window.matchMedia &&
            window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
        svg.dataset.provAuto = "1";

        var keys = [];
        svg.querySelectorAll("[data-prov]").forEach(function (r) {
          var k = r.getAttribute("data-prov");
          if (keys.indexOf(k) === -1) keys.push(k);
        });
        var i = 0;
        var timer = null;
        function tick() {
          if (hoverSvg === svg) return;
          paint(svg, keys[i % keys.length]);
          i++;
        }
        function start() { if (!timer) { tick(); timer = setInterval(tick, CYCLE_MS); } }
        function stop() {
          if (timer) { clearInterval(timer); timer = null; }
          if (hoverSvg !== svg) paint(svg, null);
        }
        if ("IntersectionObserver" in window) {
          new IntersectionObserver(function (entries) {
            entries.forEach(function (en) { en.isIntersecting ? start() : stop(); });
          }, { threshold: 0.25 }).observe(svg);
        } else {
          start();
        }
      });
  }

  function init() {
    wireAuto(document);
    // The zoom overlay clones a figure into the DOM later; wire that copy too.
    if ("MutationObserver" in window) {
      new MutationObserver(function (muts) {
        muts.forEach(function (m) {
          m.addedNodes.forEach(function (n) {
            if (n.nodeType === 1) wireAuto(n);
          });
        });
      }).observe(document.body, { childList: true, subtree: true });
    }
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
