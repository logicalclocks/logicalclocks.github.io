# Content tabs inside raw HTML blocks

A `=== "Tab"` set placed in a `<div markdown>` that sits inside an outer raw HTML block without its own `markdown` attribute renders as literal text: md_in_html only parses nested `markdown` divs when the outermost raw block carries the attribute too. Code fences still render there because superfences is a preprocessor, so the breakage is easy to miss (the home stepper looked fine until tabs went in).

Put `markdown` on the outermost wrapper as well (`<div class="hops-steps" markdown>`); raw children without the attribute, such as the stepper's button rail, pass through untouched.
