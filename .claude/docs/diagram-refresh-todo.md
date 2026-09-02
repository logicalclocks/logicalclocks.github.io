# Diagram + Nav Refresh TODO

Worklist for the visual refresh. Per-page ticking lives in `diagram-inventory.md`;
this file holds the locked standard, the cross-cutting items, and what is deferred.

## The locked standard (from the home FTI diagram)

One kit for every figure: `hops-diagram hops-viz` (+ `hops-viz-static` when the
figure is navigable, no animation). Rules baked into the home FTI template:

- Icons: minimalist line, normalized to fill the 24-grid, `scale(0.85)` around
  their centre (aids, not heroes), stroke inherits the node tone.
- Never an icon that reads as a competitor logo (Databricks stacked diamonds).
- Grid ground on every figure (`--hops-grid-cell: 9px`, faint).
- Connectors curved, docked on the node border (no standoff gap).
- Tone = accent on stroke + icon, never a colour flood.
- Inbox text always centred, H and V; icon placement follows box proportion
  (icon on top for narrow, icon left for wide); consistent top/bottom padding.
- Tight viewBox = the figure padding is the only spacing (auto, uniform).
- Radius small (node 4, zone 6). Title token 13px.

## Orientation rule (locked)

Infinite vertical, limited horizontal: a figure fits the container width and
grows downward. Horizontal scroll is a failure mode, not a feature. The kit no
longer forces a min-width pan (`.hops-viz svg` is `width:100%`, `max-width:52rem`,
no `min-width`); every diagram is authored **portrait** (sections stacked, flow
top to bottom) so fitting a TOC'd column stays legible. Wide landscape charts
get re-flowed to portrait, they are not left to pan.

## Open

- [ ] Convert the last 4 old-kit fragments: `concepts/dev/inside`,
      `concepts/dev/outside`, `mlops/registry/model-registry`,
      `mlops/training/training-pipelines-on-hopsworks`.
      (grep: `grep -rL hops-viz diagrams --include='*.html'`.)
      Verify edge routing with `agent-browser screenshot` (working again).
- [ ] Icon retrofit pass on the dense diagrams converted WITHOUT icons before Lex
      asked for iconography (the data_transformations page, feature-views x2,
      real-time-ai, batch-ai, the versioning grids, taxonomies). governance +
      data-storage already carry node icons (person, CI-loop, table, store, cube,
      server, magnifier) at `scale(0.7)`, icon-left with centred text.
- [ ] Codify the standard + orientation rule into `.claude/docs/design-system.md`.
- [ ] Nav: decide the Python/Java API `</>` marker indent (gutter-align vs leave).

## Done

- Home `index/one-architecture-three-pipelines`: rebuilt as the viz-static
  template. Kit primitives added (viz-icon, viz-zone, hops-viz-static, grid
  ground). Committed `7956cf169`.
- `concepts/hopsworks/the-hopsworks-platform`: rebuilt onto the viz kit and
  re-flowed **portrait** (sections stacked, vertical flow). Fits the column,
  no horizontal scroll. First application of the orientation rule.
- Kit: dropped the min-width pan floor; diagrams now fit width and grow vertical.
- Kit: the zoom overlay now bounds the figure to the stage height, so tall
  portrait diagrams fit in full view instead of overflowing / needing a pan.
- 18 of 25 old-kit fragments converted (plus the provenance screenshot →
  viz lineage diagram). Batches: 5 concepts, data_transformations page (4),
  feature-view + pipeline (3), prediction services (2), projects/cicd (4).
- Shared-asset pattern (data-storage): a dashed backing box reaches from the
  owned node to the shared consumer, labelled SHARED in the gap.
- Nav cleanup: Tutorials out of the menu (kept via `not_in_nav`), section
  renamed **Administration**, REST status codes moved under a **Reference**
  group, `</>` API marker on Python/Java API, drill-nav back buttons fixed
  (up to parent or site root, never self), sidebar divider now full-height.
  Uncommitted.

## Per-page conversion

See `diagram-inventory.md`: 148 pages / ~494 visuals. Old-kit `.hops-diagram`
figures and mermaid/image remnants convert to the viz standard one at a time.
