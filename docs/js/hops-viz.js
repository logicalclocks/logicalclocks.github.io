// Timeline driver for the hops-viz animated diagram kit (custom.css).
// A diagram opts in with <figure class="hops-diagram hops-viz"> holding an
// inline SVG plus a <script type="application/json" data-viz-scene> timeline:
//   {"interval": 1000, "steps": [...]}  // add "loop": true to loop forever
// Each step maps a CSS selector to ops applied to every match inside the SVG:
//   state  -> data-state attribute (null removes it; CSS renders the state)
//   tone   -> data-tone attribute (resolves --viz-tone for the subtree)
//   active -> data-active boolean attribute
//   text   -> textContent (set at once)
//   type   -> textContent revealed character by character (typewriter), for
//             code and values that read better as written
//   x / y  -> style.transform translate in px, tweened by CSS transitions
//   w      -> style.width in px (SVG geometry property, e.g. progress fills)
//   opacity -> style.opacity
// "$ms" on a step overrides the pause after it. "$label" on a step opens a
// named chapter: the driver renders one chip per chapter under the figure, the
// active chip follows playback, and clicking a chip jumps to that chapter's
// first frame (steps applied instantly, no tween) and pauses there.
// The scene plays once while the
// figure is on screen, then holds the final frame; the button turns into a
// replay control that restarts from the pristine SVG. Set "loop": true to loop
// continuously instead (restarting from pristine after loopDelay). With
// prefers-reduced-motion every step is applied at once: the final state renders
// as a static diagram, no motion.
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var TYPE_MS = 45; // per-character reveal speed for the `type` op

  // Pristine SVG markup per figure, captured before the first step runs, so
  // a zoomed clone can restart from the beginning instead of mid-animation.
  var pristine = new WeakMap();

  function clearTypers(svg) {
    if (svg._typers) {
      svg._typers.forEach(function (id) { clearInterval(id); });
      svg._typers.clear();
    }
  }

  function startType(svg, el, full) {
    el.textContent = "";
    var n = 0;
    var id = setInterval(function () {
      n += 1;
      el.textContent = full.slice(0, n);
      if (n >= full.length) {
        clearInterval(id);
        if (svg._typers) svg._typers.delete(id);
      }
    }, TYPE_MS);
    if (!svg._typers) svg._typers = new Set();
    svg._typers.add(id);
  }

  function applyStep(svg, step, instant) {
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
        if ("type" in ops) {
          if (reduced || instant) el.textContent = ops.type;
          else startType(svg, el, ops.type);
        }
        if ("x" in ops || "y" in ops) {
          el.style.transform =
            "translate(" + (ops.x || 0) + "px," + (ops.y || 0) + "px)";
        }
        if ("w" in ops) el.style.width = ops.w + "px";
        if ("opacity" in ops) el.style.opacity = ops.opacity;
      });
    });
  }

  var ICON = {
    play: '<svg viewBox="0 0 16 16" width="9" height="9" aria-hidden="true"><path d="M4 3 L13 8 L4 13 Z"/></svg>',
    pause:
      '<svg viewBox="0 0 16 16" width="9" height="9" aria-hidden="true"><rect x="3.5" y="3" width="3" height="10" rx="1"/><rect x="9.5" y="3" width="3" height="10" rx="1"/></svg>',
    // Replay is a stroked circular arrow; inline fill:none beats the toggle's
    // `svg { fill: currentColor }` rule so the glyph reads as an outline.
    replay:
      '<svg viewBox="0 0 16 16" width="10" height="10" aria-hidden="true" style="fill:none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M13.5 8a5.5 5.5 0 1 1-1.7-3.95"/><path d="M13.8 2.6V5.2H11.2"/></svg>',
  };

  function addToggle(fig, ctrl) {
    var btn = document.createElement("button");
    btn.className = "hops-viz-toggle";
    btn.type = "button";
    function render() {
      var ended = ctrl.ended();
      var paused = ctrl.paused();
      btn.setAttribute(
        "aria-label",
        ended ? "Replay animation" : paused ? "Play animation" : "Pause animation",
      );
      btn.setAttribute("data-paused", paused ? "1" : "0");
      btn.setAttribute("data-ended", ended ? "1" : "0");
      btn.innerHTML = ended ? ICON.replay : paused ? ICON.play : ICON.pause;
    }
    btn.addEventListener("click", function () {
      ctrl.toggle();
      render();
    });
    // The scene switches itself to the ended state when it finishes; re-render
    // the icon then, without waiting for a click.
    ctrl.onChange(render);
    render();
    fig.appendChild(btn);
  }

  function addSteps(fig, ctrl) {
    if (!ctrl.chapters.length) return;
    var ol = document.createElement("ol");
    ol.className = "hops-viz-steps";
    ol.setAttribute("aria-label", "Animation steps");
    var buttons = ctrl.chapters.map(function (ch, k) {
      var li = document.createElement("li");
      var b = document.createElement("button");
      b.type = "button";
      b.className = "hops-viz-step";
      var l = document.createElement("span");
      l.className = "hops-viz-step-l";
      var n = document.createElement("span");
      n.className = "hops-viz-step-n";
      n.textContent = String(k + 1);
      l.appendChild(n);
      l.appendChild(document.createTextNode(ch.label));
      b.appendChild(l);
      var bar = document.createElement("span");
      bar.className = "hops-viz-step-bar";
      b.appendChild(bar);
      b.addEventListener("click", function () { ctrl.jumpTo(k); });
      li.appendChild(b);
      ol.appendChild(li);
      return b;
    });
    function render() {
      var cur = ctrl.current();
      buttons.forEach(function (b, k) {
        var state = k === cur ? "active" : k < cur ? "visited" : "pending";
        b.setAttribute("data-state", state);
        b.parentNode.setAttribute("data-state", state);
        if (k === cur) b.setAttribute("aria-current", "step");
        else b.removeAttribute("aria-current");
      });
    }
    ctrl.onChange(render);
    render();
    fig.appendChild(ol);
  }

  function play(fig) {
    var script = fig.querySelector("script[data-viz-scene]");
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
    pristine.set(fig, svg.innerHTML);

    if (reduced) {
      steps.forEach(function (step) { applyStep(svg, step); });
      return;
    }

    var interval = scene.interval || 1000;
    var initial = svg.innerHTML;
    var chapters = [];
    steps.forEach(function (step, k) {
      if (step.$label) chapters.push({ label: String(step.$label), start: k });
    });
    var i = 0;
    var timer = null;
    var visible = false;
    var userPaused = false;
    var ended = false;
    var listeners = [];

    function emit() {
      listeners.forEach(function (fn) { fn(); });
    }
    function resetPristine() {
      clearTypers(svg);
      svg.innerHTML = initial;
    }

    function tick() {
      if (!svg.isConnected) return;
      applyStep(svg, steps[i]);
      var wait = steps[i].$ms || interval;
      i += 1;
      emit();
      if (i >= steps.length) {
        if (scene.loop === true) {
          i = 0;
          timer = setTimeout(function () {
            resetPristine();
            // Let the pristine DOM paint once before step 1 re-applies, so the
            // restart does not tween from the last frame.
            timer = setTimeout(tick, 80);
          }, scene.loopDelay || 2 * interval);
          return;
        }
        // Default: play once, hold the final frame, offer replay.
        ended = true;
        emit();
        return;
      }
      timer = setTimeout(tick, wait);
    }

    // Jump to a chapter: rebuild from pristine, apply every step up to and
    // including the chapter's first one with tweens suppressed, then hold.
    function jumpTo(k) {
      var ch = chapters[k];
      if (!ch) return;
      clearTimeout(timer);
      resetPristine();
      svg.classList.add("viz-jump");
      for (var s = 0; s <= ch.start; s++) applyStep(svg, steps[s], true);
      void svg.getBoundingClientRect(); // flush styles while transitions are off
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { svg.classList.remove("viz-jump"); });
      });
      i = ch.start + 1;
      ended = false;
      userPaused = true;
      emit();
    }

    var ctrl = {
      chapters: chapters,
      jumpTo: jumpTo,
      // Index of the chapter the last applied step belongs to, -1 before play.
      current: function () {
        var last = i - 1;
        var cur = -1;
        chapters.forEach(function (ch, k) { if (ch.start <= last) cur = k; });
        return cur;
      },
      paused: function () { return userPaused; },
      ended: function () { return ended; },
      onChange: function (fn) { listeners.push(fn); },
      toggle: function () {
        if (ended) {
          // Replay from the pristine SVG.
          clearTimeout(timer);
          resetPristine();
          i = 0;
          ended = false;
          userPaused = false;
          timer = setTimeout(tick, 80);
          emit();
          return;
        }
        if (userPaused) {
          userPaused = false;
          if (visible) timer = setTimeout(tick, 200);
        } else {
          userPaused = true;
          clearTimeout(timer);
        }
        emit();
      },
    };

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !visible) {
            visible = true;
            // Autoplay on first view; a finished scene holds its final frame
            // and waits for an explicit replay instead of restarting on scroll.
            if (!userPaused && !ended) timer = setTimeout(tick, 300);
          } else if (!entry.isIntersecting && visible) {
            visible = false;
            clearTimeout(timer);
            clearTypers(svg);
          }
        });
      },
      { threshold: 0.25 },
    );
    io.observe(fig);

    return ctrl;
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".md-typeset .hops-viz").forEach(function (fig) {
      var ctrl = play(fig);
      if (ctrl) {
        addToggle(fig, ctrl);
        addSteps(fig, ctrl);
      }
    });
  });

  // Zoom overlay (diagram-zoom.js) clones a figure into document.body and
  // announces it here. Reset the clone to the pristine SVG and give it its
  // own player; the isConnected guard stops it once the overlay is reused.
  document.addEventListener("hops-zoom-open", function (e) {
    var clone = e.detail && e.detail.clone;
    var source = e.detail && e.detail.source;
    if (!clone || !clone.classList.contains("hops-viz")) return;
    // The clone copies the source figure's toggle button but not its listener,
    // so drop the dead button; the overlay has its own controls.
    clone.querySelectorAll(".hops-viz-toggle, .hops-viz-steps").forEach(function (b) { b.remove(); });
    var svg = clone.querySelector("svg");
    var initial = pristine.get(source);
    if (svg && initial) svg.innerHTML = initial;
    var ctrl = play(clone);
    if (ctrl) {
      addToggle(clone, ctrl);
      addSteps(clone, ctrl);
    }
  });
})();
