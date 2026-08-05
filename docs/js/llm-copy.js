// Adds a "Copy for LLM" action to each page header.
// The button fetches the raw-Markdown sibling emitted by scripts/llms_hook.py
// (`<page>.md`) and copies it to the clipboard. Pure progressive enhancement:
// the Markdown artifacts, llms.txt and llms-full.txt exist server-side without
// any JavaScript, so no content depends on this running.

(function () {
  "use strict";

  function mdUrl() {
    var path = window.location.pathname;
    if (path.endsWith("/")) return path + "index.md";
    if (path.endsWith(".html")) return path.slice(0, -5) + ".md";
    return path + ".md";
  }

  function build() {
    var title = document.querySelector(".md-content__inner h1");
    if (!title || document.querySelector(".md-llm-copy")) return;

    var btn = document.createElement("button");
    btn.className = "md-llm-copy";
    btn.type = "button";
    btn.title = "Fetch this page as Markdown and copy it to the clipboard";
    btn.textContent = "Copy for LLM";

    btn.addEventListener("click", function () {
      fetch(mdUrl())
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.text();
        })
        .then(function (text) {
          return navigator.clipboard.writeText(text);
        })
        .then(function () {
          btn.textContent = "Copied";
          setTimeout(function () {
            btn.textContent = "Copy for LLM";
          }, 2000);
        })
        .catch(function () {
          btn.textContent = "Unavailable";
          setTimeout(function () {
            btn.textContent = "Copy for LLM";
          }, 2000);
        });
    });

    title.appendChild(btn);
  }

  // Material for MkDocs swaps content via instant navigation; rebuild each time.
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(build);
  } else {
    document.addEventListener("DOMContentLoaded", build);
  }
})();
