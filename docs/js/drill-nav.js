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
    var oldUp = primary.querySelector(".hops-nav-up");
    if (oldUp) oldUp.remove();
    document.body.classList.remove(ON);

    var active = primary.querySelector(".md-nav__link--active");
    if (!active) return;
    var activeLi = active.closest(".md-nav__item");
    if (!activeLi) return;

    // Which list is the current level? A section index page drills INTO its
    // children; a leaf shows the level it lives on (its siblings). Never the
    // page's own heading TOC (.md-nav--secondary).
    var childNav = activeLi.querySelector(
      ":scope > nav.md-nav:not(.md-nav--secondary) > .md-nav__list",
    );
    var currentList, ownerLi;
    if (childNav) {
      currentList = childNav;
      ownerLi = activeLi; // we are inside the active section
    } else {
      currentList = activeLi.parentElement;
      ownerLi = sectionAncestor(currentList); // the section holding this list
    }
    if (!currentList) return;

    var currentItems = Array.prototype.slice.call(currentList.children);
    var keep = new Set(currentItems);
    var node = currentList.parentElement;
    while (node && !node.classList.contains("md-nav--primary")) {
      if (node.tagName === "LI") keep.add(node);
      node = node.parentElement;
    }

    primary.querySelectorAll(".md-nav__item").forEach(function (li) {
      if (!keep.has(li)) li.classList.add(HIDDEN);
    });
    // Ancestor wrappers we kept for structure: hide their own label, they are
    // above the current level and belong to the up-header / breadcrumb.
    keep.forEach(function (li) {
      if (currentItems.indexOf(li) !== -1) return;
      var own = li.querySelector(
        ":scope > .md-nav__link, :scope > .md-nav__container",
      );
      if (own) own.classList.add(HIDDEN);
    });

    // Up-header: names the level you are in, walks up one level when clicked.
    // Inside a section -> that section's name, up goes to its parent's page.
    // On a leaf level -> the holding section's name, up goes to its parent.
    var label, upHref, depth;
    if (ownerLi) {
      label = textOf(ownerLi);
      var parentSection = sectionAncestor(ownerLi.parentElement);
      upHref = hrefOf(parentSection) || hrefOf(ownerLi) || ".";
      depth = 1;
      var d = ownerLi;
      while ((d = sectionAncestor(d.parentElement))) depth++;
    } else {
      // Top-level list: no section above it.
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
