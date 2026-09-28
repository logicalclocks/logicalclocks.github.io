// Hover cards for diagram tool nodes.
//
// Any element inside a .hops-diagram carrying data-tt-title gets a compact
// "social-card"-style hover card: an optional logo (data-tt-logo references an
// SVG <symbol> id already in the figure), a title, a one-line description, and
// a domain. Content is authored on the element; nothing is fetched at runtime.
//
// The card is a single reused DOM node appended to <body>, positioned by the
// hovered element's bounding box and clamped to the viewport. Keyboard focus
// (the elements are focusable via tabindex) shows it too, for a11y.
(function () {
  "use strict";
  var card, titleEl, descEl, domEl, logoWrap, hideTimer, current;

  function build() {
    card = document.createElement("div");
    card.className = "hviz-tt";
    card.setAttribute("role", "tooltip");
    card.hidden = true;
    logoWrap = document.createElement("div");
    logoWrap.className = "hviz-tt-logo";
    var body = document.createElement("div");
    body.className = "hviz-tt-body";
    titleEl = document.createElement("span");
    titleEl.className = "hviz-tt-title";
    descEl = document.createElement("span");
    descEl.className = "hviz-tt-desc";
    domEl = document.createElement("span");
    domEl.className = "hviz-tt-domain";
    body.appendChild(titleEl);
    body.appendChild(descEl);
    body.appendChild(domEl);
    card.appendChild(logoWrap);
    card.appendChild(body);
    document.body.appendChild(card);
  }

  function show(el) {
    if (!card) build();
    clearTimeout(hideTimer);
    current = el;
    var logo = el.getAttribute("data-tt-logo");
    if (logo) {
      logoWrap.innerHTML =
        '<svg aria-hidden="true"><use href="#' + logo + '"></use></svg>';
      logoWrap.hidden = false;
    } else {
      logoWrap.innerHTML = "";
      logoWrap.hidden = true;
    }
    titleEl.textContent = el.getAttribute("data-tt-title") || "";
    descEl.textContent = el.getAttribute("data-tt-desc") || "";
    var dom = el.getAttribute("data-tt-domain") || "";
    domEl.textContent = dom;
    domEl.hidden = !dom;
    card.hidden = false;
    position(el);
  }

  function position(el) {
    var r = el.getBoundingClientRect();
    var c = card.getBoundingClientRect();
    var pad = 8;
    // prefer above the element, flip below if it would clip the top
    var top = r.top - c.height - pad;
    if (top < pad) top = r.bottom + pad;
    var left = r.left + r.width / 2 - c.width / 2;
    left = Math.max(pad, Math.min(left, window.innerWidth - c.width - pad));
    card.style.top = Math.round(top) + "px";
    card.style.left = Math.round(left) + "px";
  }

  function hide() {
    if (!card) return;
    hideTimer = setTimeout(function () {
      card.hidden = true;
      current = null;
    }, 60);
  }

  function wire(el) {
    el.addEventListener("mouseenter", function () { show(el); });
    el.addEventListener("mouseleave", hide);
    el.addEventListener("focus", function () { show(el); });
    el.addEventListener("blur", hide);
    if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "0");
  }

  function init() {
    var nodes = document.querySelectorAll(".hops-diagram [data-tt-title]");
    if (!nodes.length) return;
    nodes.forEach(wire);
    window.addEventListener("scroll", function () { if (current) position(current); }, true);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
  // Material for MkDocs instant navigation: re-init on page swap.
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  }
})();
