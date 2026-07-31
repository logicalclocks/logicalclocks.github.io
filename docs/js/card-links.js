// Make single-link grid cards fully clickable, matching the platform's
// hoverable cards (honest pointer + click). Cards with zero or several
// links stay plain containers, so the pointer is never misleading.
document.addEventListener("DOMContentLoaded", function () {
  var cards = document.querySelectorAll(
    ".md-typeset .grid.cards > ul > li, .md-typeset .grid.cards > ol > li"
  );
  cards.forEach(function (card) {
    var links = card.querySelectorAll("a[href]");
    if (links.length !== 1) return;
    var href = links[0].getAttribute("href");
    var external = links[0].getAttribute("target") === "_blank";
    card.classList.add("card-clickable");
    card.addEventListener("click", function (e) {
      if (e.target.closest("a")) return;
      if (external) window.open(href, "_blank", "noopener");
      else window.location.href = href;
    });
  });
});
