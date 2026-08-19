// Timeline driver for the hops-viz animated diagram kit (custom.css).
// A diagram opts in with <figure class="hops-diagram hops-viz"> holding an
// inline SVG plus a <script type="application/json" data-viz-scene> timeline:
//   {"interval": 800, "loop": true, "loopDelay": 2400, "steps": [...]}
// Each step maps a CSS selector to ops applied to every match inside the SVG:
//   state  -> data-state attribute (null removes it; CSS renders the state)
//   tone   -> data-tone attribute (resolves --viz-tone for the subtree)
//   active -> data-active boolean attribute
//   text   -> textContent
//   x / y  -> style.transform translate in px, tweened by CSS transitions
//            (style.transform overrides any transform= attribute, so give a
//            moving element its own inner group and keep static placement on
//            the outer one)
//   w      -> style.width in px (SVG geometry property, e.g. progress fills)
//   opacity -> style.opacity
// "$ms" on a step overrides the pause after it. The scene plays only while
// the figure is on screen and restarts from the pristine SVG after loopDelay.
// With prefers-reduced-motion every step is applied at once: the final state
// renders as a static diagram, no loop.
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function applyStep(svg, step) {
    Object.keys(step).forEach(function (sel) {
      if (sel.charAt(0) === "$") return;
      var ops = step[sel];
      svg.querySelectorAll(sel).forEach(function (el) {
        if ("state" in ops) {
          if (ops.state === null) el.removeAttribute("data-state");
          else el.setAttribute("data-state", ops.state);
        }
        if ("tone" in ops) {
          if (ops.tone === null) el.removeAttribute("data-tone");
          else el.setAttribute("data-tone", ops.tone);
        }
        if ("active" in ops) {
          if (ops.active) el.setAttribute("data-active", "");
          else el.removeAttribute("data-active");
        }
        if ("text" in ops) el.textContent = ops.text;
        if ("x" in ops || "y" in ops) {
          el.style.transform =
            "translate(" + (ops.x || 0) + "px," + (ops.y || 0) + "px)";
        }
        if ("w" in ops) el.style.width = ops.w + "px";
        if ("opacity" in ops) el.style.opacity = ops.opacity;
      });
    });
  }

  function play(fig) {
    var script = fig.querySelector('script[data-viz-scene]');
    var svg = fig.querySelector("svg");
    if (!script || !svg) return;
    var scene;
    try {
      scene = JSON.parse(script.textContent);
    } catch (e) {
      return;
    }
    var steps = scene.steps || [];
    if (!steps.length) return;

    if (reduced) {
      steps.forEach(function (step) {
        applyStep(svg, step);
      });
      return;
    }

    var interval = scene.interval || 800;
    var initial = svg.innerHTML;
    var i = 0;
    var timer = null;
    var visible = false;

    function tick() {
      applyStep(svg, steps[i]);
      var wait = steps[i].$ms || interval;
      i += 1;
      if (i >= steps.length) {
        if (scene.loop === false) return;
        i = 0;
        timer = setTimeout(function () {
          svg.innerHTML = initial;
          // Let the pristine DOM paint once before step 1 re-applies, so
          // the restart does not tween from the last frame.
          timer = setTimeout(tick, 80);
        }, scene.loopDelay || 2 * interval);
        return;
      }
      timer = setTimeout(tick, wait);
    }

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !visible) {
            visible = true;
            timer = setTimeout(tick, 300);
          } else if (!entry.isIntersecting && visible) {
            visible = false;
            clearTimeout(timer);
          }
        });
      },
      { threshold: 0.25 },
    );
    io.observe(fig);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".md-typeset .hops-viz").forEach(play);
  });
})();
