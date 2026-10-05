# Zoom overlay clones escape .md-typeset scoping

The diagram zoom overlay (`diagram-zoom.js`) clones the whole figure into `document.body`, outside `.md-typeset`.
Any CSS scoped under `.md-typeset` (design tokens especially) stops matching the clone, and a failed `var()` in an SVG `fill` computes to black, so the zoomed diagram renders as black boxes while the inline one looks fine.

Scope diagram tokens and component rules to the figure class alone (`.hops-viz`, `.hops-diagram`), never through `.md-typeset`, and pin theme-dependent values inside `.hops-zoom-stage` because the overlay panel is always dark whatever the page scheme.
Animated figures get restarted on the clone by `hops-viz.js` listening for the `hops-zoom-open` event; keep that event dispatch when touching `diagram-zoom.js`.
