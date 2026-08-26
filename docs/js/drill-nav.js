// Column drill navigation. The rail shows exactly two adjacent levels: the level
// the active page lives on (indented, with a guide rail) and the level directly
// above it (its parent section's siblings, flat at the left margin). You always
// see "yours and above": your own level plus the one it hangs from. Everything
// shallower than the parent level collapses into the up-header and the breadcrumb
// (navigation.path). Going deeper or up slides the column left or right.
//
// Levels come from Material's nested nav DOM; we only choose which two lists to
// show and where "up" points, then hide everything else. Progressive
// enhancement: without JS the full nested tree stays visible.
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

  // The <li>'s own child list (its sub-pages), excluding the page-heading TOC
  // that Material nests under the active leaf. Null when the item is a leaf page.
  function childListOf(li) {
    if (!li) return null;
    return li.querySelector(
      ":scope > nav.md-nav:not(.md-nav--secondary) > .md-nav__list",
    );
  }

  function sectionAncestor(el) {
    var li = el.parentElement && el.parentElement.closest(".md-nav__item");
    return li || null;
  }

  // Site root, used as the "up" target when the flat level already is the top of
  // the tree (its parent section's index page IS the current context).
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

    // The active SECTION is the section that holds the current page: the active
    // item itself when it is a section (navigation.indexes gives every section an
    // index page), otherwise the nearest ancestor section. Its own child list is
    // the level you are in (indented); the list it sits in is the level above
    // (flat). When the active page is at the top of the tree it has no section
    // above, and only the one flat level shows.
    var activeSection = childListOf(activeLi)
      ? activeLi
      : sectionAncestor(activeLi);

    var indentedList = activeSection ? childListOf(activeSection) : null;
    var flatList = activeSection
      ? activeSection.parentElement
      : activeLi.parentElement;
    if (!flatList) return;

    var flatItems = Array.prototype.slice.call(flatList.children);
    var indentedItems = indentedList
      ? Array.prototype.slice.call(indentedList.children)
      : [];

    var keep = new Set(flatItems);
    indentedItems.forEach(function (li) {
      keep.add(li);
    });
    // Keep ancestor wrappers for DOM structure; their own labels are hidden below
    // (they live in the up-header / breadcrumb).
    var node = flatList.parentElement;
    while (node && !node.classList.contains("md-nav--primary")) {
      if (node.tagName === "LI") keep.add(node);
      node = node.parentElement;
    }

    primary.querySelectorAll(".md-nav__item").forEach(function (li) {
      if (!keep.has(li)) li.classList.add(HIDDEN);
    });
    // Kept items that are neither the flat level nor the indented level are
    // structural wrappers above the shown levels: hide their own label row.
    keep.forEach(function (li) {
      if (flatItems.indexOf(li) !== -1) return;
      if (indentedItems.indexOf(li) !== -1) return;
      var own = li.querySelector(
        ":scope > .md-nav__link, :scope > .md-nav__container",
      );
      if (own) own.classList.add(HIDDEN);
    });
    // Mark the indented list so CSS indents exactly that one step under its
    // section (the flat level stays at the left margin).
    if (indentedList) indentedList.classList.add("hops-drill-children");

    // Up-header: names the section ABOVE the flat level and walks up to it. When
    // the flat level is the top of the tree there is nothing above, so no header.
    var parentSection = sectionAncestor(flatList);
    var label, upHref, depth;
    if (parentSection) {
      label = textOf(parentSection);
      // Up goes to the parent section's own page, or the site root. A different
      // page from the current one, so the button is never a no-op.
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
