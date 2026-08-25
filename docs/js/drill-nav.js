// Column drill navigation (Miller-column style). The rail shows exactly one
// level at a time: the items that sit alongside the current page, as a flat
// list with no indentation. A header row at the top names the level you are in
// and, clicked, walks up one level. Going deeper or up slides the column left or
// right. The breadcrumb (navigation.path) is the redundant, always-there path.
//
// Levels come from Material's nested nav DOM; we only choose which list to show
// and where "up" points, then hide everything else. Progressive enhancement:
// without JS the full nested tree stays visible.
(function () {
  "use strict";

  var HIDDEN = "hops-drill-hidden";
  var ON = "hops-drill-on";
  var DEPTH_KEY = "hops-drill-depth";

  function textOf(li) {
    var link = li.querySelector(
      ":scope > .md-nav__link, :scope > .md-nav__container > .md-nav__link",
    );
    if (!link) return "";
    var clone = link.cloneNode(true);
    clone.querySelectorAll(".md-nav__icon, svg").forEach(function (n) {
      n.remove();
    });
    return (clone.textContent || "").trim();
  }

  // The index page link of a nav item (the <li>'s own link), used as the target
  // when walking up a level. Returns null for label-only sections.
  function hrefOf(li) {
    if (!li) return null;
    var link = li.querySelector(
      ":scope > .md-nav__link[href], :scope > .md-nav__container > .md-nav__link[href]",
    );
    var href = link && link.getAttribute("href");
    if (!href || href.charAt(0) === "#") return null;
    return href;
  }

  function sectionAncestor(el) {
    var li = el.parentElement && el.parentElement.closest(".md-nav__item");
    return li || null;
  }

  // Site root, used as the "up" target from a top-level section (whose own
  // index page IS the current page, so it must never point at itself).
  function homeHref() {
    var logo = document.querySelector("a.md-logo, .md-header__button.md-logo");
    var href = logo && logo.getAttribute("href");
    return href || ".";
  }

  function buildUpButton(label, href) {
    var btn = document.createElement(href ? "a" : "div");
    btn.className = "hops-nav-up";
    if (href) btn.setAttribute("href", href);
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" ' +
      'stroke="currentColor" stroke-width="2" stroke-linecap="round" ' +
      'stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/>' +
      "</svg><span></span>";
    btn.querySelector("span").textContent = label;
    return btn;
  }

  function drill() {
    var primary = document.querySelector(".md-nav--primary");
    if (!primary) return;

    // Reset any previous run.
    primary.querySelectorAll("." + HIDDEN).forEach(function (el) {
      el.classList.remove(HIDDEN);
    });
    primary.querySelectorAll(".hops-drill-children").forEach(function (el) {
      el.classList.remove("hops-drill-children");
    });
    var oldUp = primary.querySelector(".hops-nav-up");
    if (oldUp) oldUp.remove();
    document.body.classList.remove(ON);

    var active = primary.querySelector(".md-nav__link--active");
    if (!active) return;
    var activeLi = active.closest(".md-nav__item");
    if (!activeLi) return;

    // Two adjacent levels are shown: the level the active item lives on (its
    // siblings) and, when the active item is a section, that section's children
    // one step down. Hiding is about DEPTH, not siblings: everything shallower
    // than the sibling level collapses into the up-header / breadcrumb, and
    // everything deeper than the child level stays hidden. Never the page's own
    // heading TOC (.md-nav--secondary).
    var siblingList = activeLi.parentElement;
    if (!siblingList) return;
    var siblingItems = Array.prototype.slice.call(siblingList.children);

    var childNav = activeLi.querySelector(
      ":scope > nav.md-nav:not(.md-nav--secondary) > .md-nav__list",
    );
    var childItems = childNav
      ? Array.prototype.slice.call(childNav.children)
      : [];

    var keep = new Set(siblingItems);
    childItems.forEach(function (li) {
      keep.add(li);
    });
    // Keep ancestor wrappers for structure; their labels are hidden below.
    var node = siblingList.parentElement;
    while (node && !node.classList.contains("md-nav--primary")) {
      if (node.tagName === "LI") keep.add(node);
      node = node.parentElement;
    }

    primary.querySelectorAll(".md-nav__item").forEach(function (li) {
      if (!keep.has(li)) li.classList.add(HIDDEN);
    });
    // Ancestor wrappers above the shown levels: hide their own label, they live
    // in the up-header / breadcrumb. Sibling and child labels stay visible.
    keep.forEach(function (li) {
      if (siblingItems.indexOf(li) !== -1) return;
      if (childItems.indexOf(li) !== -1) return;
      var own = li.querySelector(
        ":scope > .md-nav__link, :scope > .md-nav__container",
      );
      if (own) own.classList.add(HIDDEN);
    });
    // Mark the child list so CSS indents exactly that one step under its
    // section (the sibling level stays flat at the left margin).
    if (childNav) childNav.classList.add("hops-drill-children");

    // Up-header: names the level ABOVE the siblings (the parent section) and
    // walks up to it. A top-level active item has no section above it, so no
    // header: the whole top level already is the current level.
    var parentSection = sectionAncestor(siblingList);
    var label, upHref, depth;
    if (parentSection) {
      label = textOf(parentSection);
      // Up goes to the parent section's own page, or the site root. This is a
      // different page from the current one, so the button is never a no-op.
      upHref = hrefOf(parentSection) || homeHref();
      depth = 1;
      var d = parentSection;
      while ((d = sectionAncestor(d.parentElement))) depth++;
    } else {
      label = "";
      upHref = null;
      depth = 0;
    }

    if (label) {
      var up = buildUpButton(label, upHref);
      var scrollwrap = primary.closest(".md-sidebar__scrollwrap") || primary;
      scrollwrap.insertBefore(up, scrollwrap.firstChild);
    }

    // Slide direction from the depth change since the last page.
    var prev = parseInt(sessionStorage.getItem(DEPTH_KEY) || "-1", 10);
    var dir = depth > prev ? "in" : depth < prev ? "out" : "";
    sessionStorage.setItem(DEPTH_KEY, String(depth));

    document.body.classList.add(ON);
    if (dir) {
      var col = primary.closest(".md-sidebar__scrollwrap") || primary;
      var cls = dir === "in" ? "hops-slide-in" : "hops-slide-out";
      col.classList.remove("hops-slide-in", "hops-slide-out");
      // reflow so the animation restarts even on same class
      void col.offsetWidth;
      col.classList.add(cls);
    }
  }

  document.addEventListener("DOMContentLoaded", drill);
})();
