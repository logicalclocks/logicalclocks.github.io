// Off-site links open in a new tab: nav entries (MLOps Dictionary), the header
// repo link, and content links alike. Same-host links, anchors and mailto stay
// in place. Attribute-only, so the links still work with scripting off.
document.addEventListener("DOMContentLoaded", function () {
  var links = document.querySelectorAll('a[href^="http://"], a[href^="https://"]');
  links.forEach(function (a) {
    if (a.host === location.host) return;
    a.target = "_blank";
    a.rel = "noopener";
  });
});
