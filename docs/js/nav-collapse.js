// Collapsible left navigation. A toggle button at the far left of the header
// hides the primary sidebar and lets the content reclaim the width; click again
// to restore. The choice persists in localStorage. Desktop only (on mobile the
// hamburger drawer already owns the nav). Progressive enhancement: without JS
// the nav stays fully visible.
(function () {
  "use strict";

  var KEY = "hops-nav-collapsed";

  document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector(".md-header__inner");
    if (!header || header.querySelector(".hops-nav-toggle")) return;

    var btn = document.createElement("button");
    btn.className = "hops-nav-toggle md-header__button md-icon";
    btn.type = "button";
    btn.setAttribute("aria-label", "Toggle navigation");
    // Lucide "panel-left": a sidebar glyph, reads as a nav toggle.
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" ' +
      'stroke="currentColor" stroke-width="2" stroke-linecap="round" ' +
      'stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/>' +
      '<path d="M9 3v18"/></svg>';

    function restore() {
      document.body.classList.toggle(
        "hops-nav-collapsed",
        localStorage.getItem(KEY) === "1",
      );
    }

    btn.addEventListener("click", function () {
      var on = !document.body.classList.contains("hops-nav-collapsed");
      document.body.classList.toggle("hops-nav-collapsed", on);
      localStorage.setItem(KEY, on ? "1" : "0");
    });

    header.insertBefore(btn, header.firstChild);
    restore();
  });
})();
