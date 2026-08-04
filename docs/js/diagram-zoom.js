// Click-to-zoom for the inline-SVG diagram kit (.hops-diagram) and content
// images. A small ⤢ handle in the top-right corner opens a full-screen
// overlay with wheel-zoom + drag-pan, so the navigational diagrams keep their
// clickable links (the handle is the only zoom trigger, no conflict).
// Progressive enhancement: without JS the diagrams still render inline.
(function () {
  "use strict";

  function buildOverlay() {
    var overlay = document.createElement("div");
    overlay.className = "hops-zoom-overlay";
    overlay.innerHTML =
      '<button class="hops-zoom-close" aria-label="Close">✕</button>' +
      '<div class="hops-zoom-hint">scroll to zoom · drag to pan · Esc to close</div>' +
      '<div class="hops-zoom-stage"></div>';
    document.body.appendChild(overlay);
    return overlay;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var overlay = null;
    var stage = null;
    var scale = 1;
    var tx = 0;
    var ty = 0;
    var dragging = false;
    var sx = 0;
    var sy = 0;

    function apply() {
      stage.style.transform =
        "translate(" + tx + "px," + ty + "px) scale(" + scale + ")";
    }

    function open(node) {
      if (!overlay) {
        overlay = buildOverlay();
        stage = overlay.querySelector(".hops-zoom-stage");
        overlay
          .querySelector(".hops-zoom-close")
          .addEventListener("click", close);
        overlay.addEventListener("click", function (e) {
          if (e.target === overlay) close();
        });
        overlay.addEventListener(
          "wheel",
          function (e) {
            e.preventDefault();
            var f = e.deltaY < 0 ? 1.12 : 1 / 1.12;
            scale = Math.min(8, Math.max(0.4, scale * f));
            apply();
          },
          { passive: false },
        );
        stage.addEventListener("mousedown", function (e) {
          dragging = true;
          sx = e.clientX - tx;
          sy = e.clientY - ty;
          stage.classList.add("is-grabbing");
        });
        window.addEventListener("mousemove", function (e) {
          if (!dragging) return;
          tx = e.clientX - sx;
          ty = e.clientY - sy;
          apply();
        });
        window.addEventListener("mouseup", function () {
          dragging = false;
          if (stage) stage.classList.remove("is-grabbing");
        });
      }
      stage.innerHTML = "";
      // Clone the whole .hops-diagram wrapper so the kit's CSS (which is
      // scoped to `.hops-diagram .d-*`) still applies to the clone; strip the
      // zoom handle from the copy. Cloning the bare <svg> would drop the fills.
      var clone = node.cloneNode(true);
      var h = clone.querySelector(".hops-zoom-handle");
      if (h) h.remove();
      stage.appendChild(clone);
      scale = 1;
      tx = 0;
      ty = 0;
      apply();
      overlay.classList.add("is-open");
      document.body.classList.add("hops-zoom-lock");
    }

    function close() {
      if (!overlay) return;
      overlay.classList.remove("is-open");
      document.body.classList.remove("hops-zoom-lock");
    }

    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });

    // Zoom the whole diagram wrapper (SVG kit or image inside it).
    var wraps = document.querySelectorAll(".md-typeset .hops-diagram");
    wraps.forEach(function (wrap) {
      if (!wrap.querySelector("svg, img")) return;
      if (wrap.querySelector(".hops-zoom-handle")) return;
      wrap.classList.add("hops-zoomable");
      var btn = document.createElement("button");
      btn.className = "hops-zoom-handle";
      btn.setAttribute("aria-label", "Zoom diagram");
      btn.textContent = "⤢";
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        open(wrap);
      });
      wrap.appendChild(btn);
    });
  });
})();
