# Diagram fragments inside content tabs

A `--8<--` diagram include placed inside a `=== "Tab"` block is re-parsed as Markdown by the tabbed extension, unlike a top-level include which passes through as one raw HTML block. Two things break: a blank line inside the fragment ends the HTML block, so the SVG's inner tags render as paragraph text; and a `$` inside the scene JSON (`$label`, `$ms`) is picked up by the arithmatex math extension, which injects a `<span>` into the script and the scene fails to parse (no toggle, no step bar).

Write tabbed fragments with no blank lines, and spell the scene's dollar keys as JSON unicode escapes, `"\u0024label"` and `"\u0024ms"`, which decode to the same keys. The flywheel figures on the AI Systems page are the reference. Top-level includes need neither.
