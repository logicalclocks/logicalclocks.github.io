// Filter box for the generated Helm values pages: narrows every .hops-values
// list to the entries whose key or description contains the query, and hides
// the sections left empty. Without this script every entry stays visible.
document.addEventListener("DOMContentLoaded", function () {
  var lists = document.querySelectorAll(".md-typeset .hops-values");
  var terms = document.querySelectorAll(".md-typeset .hops-values dt");
  if (terms.length < 25) return;

  var bar = document.createElement("div");
  bar.className = "hops-values-filterbar";
  var input = document.createElement("input");
  input.type = "search";
  input.className = "hops-values-filter";
  input.placeholder = "Filter " + terms.length + " values by key or description";
  input.setAttribute("aria-label", "Filter values");
  var count = document.createElement("span");
  count.className = "hops-values-count";
  count.setAttribute("aria-live", "polite");
  bar.append(input, count);

  // A list's section is the heading and the "Defaults as YAML" block before it.
  function sectionOf(list) {
    var parts = [];
    var el = list.previousElementSibling;
    while (el && el.tagName === "DETAILS") {
      parts.push(el);
      el = el.previousElementSibling;
    }
    if (el && /^H[23]$/.test(el.tagName)) parts.push(el);
    return parts;
  }

  var first = lists[0];
  var firstSection = sectionOf(first);
  var before = firstSection.length ? firstSection[firstSection.length - 1] : first;
  before.parentNode.insertBefore(bar, before);

  input.addEventListener("input", function () {
    var query = input.value.trim().toLowerCase();
    var shown = 0;
    terms.forEach(function (dt) {
      var dd = dt.nextElementSibling;
      var text = (dt.textContent + " " + (dd ? dd.textContent : "")).toLowerCase();
      var match = !query || text.indexOf(query) !== -1;
      dt.hidden = !match;
      if (dd) dd.hidden = !match;
      if (match) shown++;
    });
    lists.forEach(function (list) {
      var empty = list.querySelector("dt:not([hidden])") === null;
      list.hidden = empty;
      sectionOf(list).forEach(function (el) {
        el.hidden = empty;
      });
    });
    count.textContent = query ? shown + " of " + terms.length + " values" : "";
  });
});
