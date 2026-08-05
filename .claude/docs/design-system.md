# Design System

The visual language of docs.hopsworks.ai.
Read this before changing anything visual (CSS, nav, logo, diagrams) so the site stays one coherent system.

## Principle

Match the Hopsworks product app, not a generic docs theme.
The reference is `hopsworks-front` (Quartz design system, `tailwind-quartz`): flat, restrained, grid-aligned, brand green confined to the logo and small accents.
When in doubt, open the app and copy its treatment rather than inventing one.

Two hard lessons already learned, do not repeat them:

- Do not invent per-section nav icons. The docs navigate by content type (Concepts, Guides, API), the app navigates by entity (Feature Group, Model, Deployment). There is no icon mapping between them, so any guessed glyph reads as foreign. The app's visual language is the rail plus the green active pill plus the mark plus the typography, not a glyph per category.
- The "same visual language" is achieved with structure and color, not decoration.

## Where the design lives

| Concern | File | Notes |
| ------- | ---- | ----- |
| Tokens + all component styling | `docs/css/custom.css` | Single stylesheet. Tokens at the top, components below. |
| Nav collapse toggle | `docs/js/nav-collapse.js` | Header button, hides the sidebar, widens content. |
| Drill-in navigation | `docs/js/drill-nav.js` | Shows only the current level; ancestors live in the breadcrumb. |
| Diagram zoom | `docs/js/diagram-zoom.js` | Corner handle + full-screen overlay for `.hops-diagram` and all content images (wrapped in `.hops-img-zoom` at runtime; inline images under 200px are left alone). Content images also carry a 1px `--hops-border-strong` border via CSS. |
| Code language labels | `docs/js/code-lang.js` | Language tag on code blocks. |
| Theme features + assets wiring | `mkdocs.yml` | `theme.features`, `extra_javascript`, `extra_css`. |

## Color tokens

One palette, defined once for light and once for dark (`[data-md-color-scheme="slate"]`), in `docs/css/custom.css`.
Never hardcode a hex in a rule. Use a token so light and dark both track.

| Token | Light | Dark | Use |
| ----- | ----- | ---- | --- |
| `--hops-accent` | `#21b182` | `#1eb182` | Non-text accents: logo tint, active markers, focus rings. |
| `--hops-accent-text` | `#0e8a63` | `#3ccd9f` | Links and active nav text (AA contrast). |
| `--hops-surface` | `#f5f5f5` | dark grey | Raised fills (search field, code inline). |
| `--hops-border` | `#e2e2e2` | white 9% | 1px separators. |
| `--hops-border-strong` | `#cbcbcb` | white 18% | Card and hover borders. |
| `--hops-tint` | green 8% | green 16% | Active-nav wash behind the pill. |
| `--hops-nav-fg` | `#4b5563` | fg--light | Nav item at rest. |
| `--hops-sidebar-bg` | `#f6f7f9` | near-black | The nav panel fill. |

Brand green is an accent, not a fill. Do not paint bands or large surfaces green.

## Logo

`docs/assets/images/hops-mark-green.png`, the green hop mark alone (the wordmark is the header title text).
Size it `height: 1.5rem; width: auto`. Never force a square: the mark is 142x150, a fixed width/height compresses it.

## Header

Flat, near-white, no shadow. The only chrome is a 1px bottom border (`--hops-border`).
Header icons and the repo link ride a muted foreground so the logo leads.

## Left navigation

The rail is the spine of the site. Rules, in order of importance:

- It is a text rail, no per-section icons (see the lesson above).
- The active item is a single green pill (`--hops-tint` wash, `--hops-accent-text` text), never two split boxes; the pill is on the `.md-nav__container`.
- Deep trees (up to ~5 levels, e.g. `concepts/fs/feature_group/...`) are handled by showing one level at a time, not by exposing the whole tree:
    - `navigation.indexes`: every section has an Overview/index page acting as a hub.
    - `navigation.prune`: only the active branch is rendered.
    - `navigation.path`: breadcrumbs above the H1 carry the hierarchy above the current level.
    - `drill-nav.js`: the rail shows only the current level (active item plus siblings, or children on a section page); ancestors collapse into the breadcrumb, which is the way back up.
- Collapse toggle (`nav-collapse.js`): a header button hides the whole sidebar and lets the content reclaim the width. It is a plain show/hide, not an icon rail. Desktop only; mobile uses the drawer. State persists in localStorage.
- The sidebar is its own panel (`--hops-sidebar-bg`). The panel fill and the right divider are painted by `.md-sidebar--primary::before` (full-bleed, spanning past the header) so the divider is flush with the header, not notched 30px below it. Do not put the divider border back on the `.md-sidebar--primary` box.

## Search

Header search (not sidebar). Bordered pill on `--hops-surface`.
The magnifier icon inherits the header's white by default and vanishes on the light field; it is forced to the muted foreground in `.md-header .md-search__form .md-search__icon`. Keep that override.

## Diagrams

Two kinds, do not mix them up:

- Navigational / architecture charts: clickable inline SVG built on the shared `.hops-diagram` CSS kit. Use `currentColor` plus tinted brand fills so they adapt to light/dark, and version-safe relative `href`s for the clickable nodes.
- Illustrations only: mermaid. Mermaid's `click` directives break rendering under Material's strict `securityLevel`, so mermaid is never used for clickable navigation.

`diagram-zoom.js` adds a corner handle and full-screen overlay to any `.hops-diagram`.

## Theme features

Set in `mkdocs.yml` under `theme.features`. Current set and why:
`navigation.indexes` (section hubs), `navigation.prune` (render active branch only), `navigation.path` (breadcrumbs), `navigation.top` (back to top), `toc.follow` (right TOC tracks scroll), `content.code.copy`.
Note the absence of `navigation.sections` (keeps sections collapsible) and `navigation.expand` (collapse by default). Keep both absent.

## Content tone

Covered in `content.md`: one sentence per line, reference not editorial, and no em dashes (a commit hook enforces the last one). This charter is visual; that one is editorial.
