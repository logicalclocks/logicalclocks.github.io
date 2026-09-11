// Home-page stepper: clicking a step in the rail shows its code panel.
// Progressive enhancement only: without JS every panel stays visible, so the
// content is always in the payload. The `hops-steps--js` class is what arms
// the one-panel-at-a-time CSS.
document.addEventListener("DOMContentLoaded", function () {
  var root = document.querySelector(".hops-steps");
  if (!root) return;
  root.classList.add("hops-steps--js");
  var steps = root.querySelectorAll(".hops-step");
  var panels = root.querySelectorAll(".hops-step-panel");
  steps.forEach(function (step) {
    step.addEventListener("click", function () {
      var id = step.getAttribute("data-step");
      steps.forEach(function (s) {
        s.classList.toggle("is-active", s === step);
        s.setAttribute("aria-selected", s === step ? "true" : "false");
      });
      panels.forEach(function (p) {
        p.classList.toggle("is-active", p.getAttribute("data-step") === id);
      });
    });
  });
});
