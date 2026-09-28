# UI Captures

How screenshots and GIFs of the Hopsworks app are taken for the docs.
Diagrams are a different species, see the Diagrams section of `design-system.md`; this file is only about pixels of the real product.
Read it before replacing a screenshot, and follow `parity-review.md` for which pages still carry old-UI captures.

## Where the pixels come from

A dev cluster running the target release, never a mock-up and never an older release than the docs version.
The demo project should look like a real project (a `fraud_detection` style project with feature groups, a deployment, an app, a couple of jobs) so that lists are not empty and names read as real.
When the state a page describes does not exist, fake it on the cluster or in the browser rather than drawing it: create the object through the SDK or the REST API, stub a response with `agent-browser network route`, or write rows straight into the metadata database.
Leave harmless fixtures in place for the next agent and write them down in memory; revert anything that changes cluster behaviour (admin variables, auth toggles, Helm values).

## Browser session

Use `agent-browser` with a dedicated session and profile directory, headed, ignoring the self-signed certificate:

```bash
agent-browser --session hopsdocs --profile "$SCRATCH/chrome-profile" --headed --ignore-https-errors open https://<app>/
agent-browser --session hopsdocs set viewport 1440 900 2
```

Never capture from the user's personal Chrome profile: its active tab moves under you.
The viewport is 1440 css wide at device scale 2, so every capture is 2x; raise the height (1440 by 1500) when a card must fit in one shot.
A restart of the app (Helm, Payara) logs the session out; ask the user to log in again in the headed window rather than storing credentials.

Read the page with `eval`, click with native `click` on an element you gave an id to in a prior `eval`, and use `find role button click --name "..."` for primary buttons that ignore untrusted clicks (the wizard "Next" buttons do).
Radix radio groups switch on a click of their `label`, or with arrow keys after focusing a radio.
Custom dropdowns: click the combobox input, then click the `[role=option]`.

## What a capture shows

Scope the capture to the panel the prose talks about, with some UI around it so the reader sees it is inside the app: never a full app shell, never a bare widget on white.
Rules that have held on every page so far:

- A form or card: the card from its header to the last relevant block, plus about 3 percent margin on each side; clamp the top to the sticky header's bottom edge so the header never bleeds in.
- A row range inside a long form (a settings block): cut at the midpoint of the gap to the neighbouring rows so no neighbour is sliced.
- A modal: the dialog with an 18 percent margin so the blurred page behind it shows it is a modal.
- A list: the toolbar (primary button and filter) and the table, nothing else.
- Blur the focused control before shooting (`document.activeElement.blur()`), or the caret and focus ring end up in the docs.
- Fill placeholders with values that read as real (`transactions`, `fraud_source`, a cursor field, a job name), never `test` or `asdf`.

Measure the rectangle in the page, take a viewport screenshot, and crop:

```bash
R=$(agent-browser --session hopsdocs eval '(()=>{const e=document.querySelector("#the-card");e.scrollIntoView({block:"start"});window.scrollBy(0,-60);const r=e.getBoundingClientRect();return JSON.stringify({x:r.x,y:r.y,w:r.width,h:r.height,iw:innerWidth})})()' | tail -1)
R=${R#\"}; R=${R%\"}; R=${R//\\/}
agent-browser --session hopsdocs screenshot /tmp/vp.png
python3 .claude/docs/capture_crop.py /tmp/vp.png docs/assets/images/<section>/<name>.png "$R" --margin 0.03 --top-min 72
```

`capture_crop.py` derives the device scale from the rectangle's `iw`, so it works for any viewport.
The rectangle is measured after scrolling, because element screenshots lose their target when React re-renders.

## GIFs

A GIF is for a sequence the reader would otherwise have to imagine (a server starting, a job moving through states).
Record one viewport screenshot per state and, next to it, the rectangle of the card in that frame (the card moves when a sidebar collapses), then assemble:

```bash
python3 .claude/docs/capture_gif.py "$FRAMES_DIR" docs/assets/images/<section>/<name>.gif 0.05
```

Frames are cropped around the largest card rectangle, halved to 1x and quantised, so a five-frame GIF stays under a few hundred kilobytes.
The first frame holds longer, the last one longest.

## Naming and placement

Images live in `docs/assets/images/<section>/` mirroring the page (`guides/fs/feature_group/`, `guides/jobs/`, `admin/oauth2/`).
Keep the existing file name when replacing an old capture so no page reference changes; delete captures you cannot redo rather than leaving the old UI in, and drop their figure from the page.
Alt text says what the reader is looking at, one sentence, no "screenshot of".

## Faking states, worked examples

- A feature the cluster does not enable: stub the availability check in the browser, `agent-browser network route "**/isAvailable*" --body '{"enabled":true}'`, then create the objects through the API.
- Feature monitoring results: register synthetic statistics per commit window through the SDK so the chart has distinct points.
- A data source that browses tables: the built-in HopsFS and JDBC sources never enable "Next: Select Tables"; create a `SQL` source against the cluster's own MySQL (`mysqld.hopsworks.svc.cluster.local`) with a dedicated read-only user and a small database of realistic tables.
- Session-capacity badges, alerts, admin panels: the memory file for the dev cluster lists the switches; check it before searching.

## Before you are done

Open the page on the served site and look at the capture in the column: if the text is not readable at the docs width, the scope was too wide, not the resolution too low.
Tick the page in `parity-review.md` with a note on what was redone.
