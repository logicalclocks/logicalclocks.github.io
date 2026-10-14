// Label each code block with its language, in the block's nav bar next to the
// copy button. Reads the pygments `language-*` class (pymdownx.highlight with
// pygments_lang_class), so it works for any language with no per-language map.
// Progressive enhancement only: the code itself is already in the payload.
document.addEventListener("DOMContentLoaded", function () {
  var blocks = document.querySelectorAll(".md-typeset .highlight");
  blocks.forEach(function (block) {
    var match = block.className.match(/language-([\w+-]+)/);
    if (!match) return;
    var nav = block.querySelector(".md-code__nav");
    if (!nav || nav.querySelector(".md-code__lang")) return;
    var label = document.createElement("span");
    label.className = "md-code__lang";
    label.textContent = match[1];
    nav.insertBefore(label, nav.firstChild);
  });
});
