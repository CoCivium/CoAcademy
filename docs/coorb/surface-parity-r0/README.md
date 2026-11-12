# CoOrb+ Surface Parity R0 | One work, four surfaces

**State:** `PUBLIC_SAFE_OFFLINE_CANARY__BROWSER_AND_PURE_PROJECTION_TESTED__NO_X2_RUNTIME__NO_RECEIVER_PICKUP`.

This is **not another daybook or desktop controller**. It isolates one cross-substrate question: can an unchanged work identity and its evidence, authority, privacy, currentness and receiver limits survive projection into four receiver-specific surfaces?

- `work-object.json`: one **fictional, public-safe** work object. The subject is generic coordination between publishing, research and recovery. The user's screenshot, private chats and real account contents were **not** imported.
- `project.py`: Python 3 standard-library, read-only projector to `glance`, `orb`, `map` and `machine` JSON. Every view carries the same deep-copied invariants, exact source SHA-256 of canonical JSON and explicit `projection_omissions`.
- `index.html`: self-contained accessible browser projection of the *same* fixture, embedded for offline `file://` support; switches between Glance, CoOrb, CoMap and full headless JSON. Responsive layout, visible keyboard focus, reduced-motion support and no network or storage APIs.
- `test_parity.py`: regression on exact embedded-source parity, four-view invariants, no fake receiver pickup/live state, typed omissions, fail-closed privacy, no effects.
- `test_browser.py`: optional browser fixture using Playwright and a system Chromium binary. Authoring test ran at 360, 390 and 1280 CSS pixels via `page.set_content` and verified 4 views, keyboard activation, JSON equality, no horizontal overflow, zero page errors and zero requests. Direct `file://` navigation on X2/user browsers was **not** tested.

## Run

Open `index.html` locally (does not require ChatGPT, Claude, a user account, server or Internet), or inspect the entire work object in `work-object.json`.

```sh
python3 project.py --view glance
python3 project.py --view orb
python3 project.py --view map
python3 project.py --view machine
python3 -m unittest discover -s . -p 'test_parity.py' -v
```

`test_browser.py` is optional. On the authoring system it required `playwright` and `/usr/bin/chromium`; no general browser availability is inferred.

## What success does and does not mean

The offline invariant: every view preserves the exact identity, source/provenance, currentness, evidence, authority, privacy and receiver state, **even when its display collapses other fields**. A reduced projection explicitly tells you what was omitted. Screen space and an app's native chat history are not the source of truth.

The caveats: fixture identity is synthetic; `UNVERIFIED_LIVE` is not live; no user task, source-verification, physical middle-button, OS overlay, CoStead receiver, independent browser, provider API, actual session synchronization or human benefit has been established. No auto-import of accounts, screenshot scraping or bulk agent fan-out.

## Integration boundary

Existing CoCivium architecture and review candidates should be reused: `COORBWARE_BEYOND_COSOFTWARE_R0_20261024`, `COORB_LOCAL_UX_REGENERATIVE_R0_20261026`, CoOrbWare First Look, CoOrb/CoCopy Daybook (CoAcademy PR #4), and CoOrb DayTrail (CoCivium PR #288). This canary is a **parity test donor**, not a competing event store or a replacement renderer.

**Next gate:** one authorized actual work object through at least two independent implementation receivers, with separate hash-bound readproof and a genuinely consenting human's task-completion record. Deploying the static page or passing local tests alone does not cross that gate.

`SYNTHETIC_NE_LIVE` · `RENDER_NE_RECEIVER_ACK` · `VIEW_NE_TRUTH_STORE` · `LAYOUT_NE_AUTHORITY` · `PROJECTION_LOSS_MUST_BE_EXPLICIT`.