# CoMegaScroller public viewer | source and limits

**State:** PUBLIC-SAFE STATIC WEB CANDIDATE; not a new semantic source or production CoOrbWare service.

- Canonical generator: [CoNavNestedAtlasR0.cjs](https://github.com/CoCivium/CoCivium/blob/main/scripts/CoNavNestedAtlasR0.cjs)
- Canonical self-contained HTML: [CoMegaScroller source](https://github.com/CoCivium/CoCivium/blob/main/examples/comap/megascroller-r0.html)
- Exact source HTML Git blob at first mirroring: `f027f0999075ef7429b8ec8777a806e41b436333` (preserved predecessor)
- First mobile long-relation wrap revision: `552d75fd5d79484d66697c0cf069f65ecd2f6b3c` (preserved predecessor), from [canonical PR #479](https://github.com/CoCivium/CoCivium/pull/479)
- Current canonical and mirrored Git blob: `d2f27d07da5cfbfaea47a9da10ff2ab9a5ab3d13`, from [canonical PR #480](https://github.com/CoCivium/CoCivium/pull/480), which also wraps intrinsically overwide `.meta` and `.card` fields.
- Cause: actual Chromium 390px test found a 433px page due to a non-wrapping `PROPOSED_PROJECTION_FAMILY` relation. The source generator and mirror now allow long relation names to wrap without truncation. **Second live mobile browser recheck pending post-merge deployment**; do not infer from a CSS diff.
- Reuse basis: original CoCivium source and illustrations, subject to [GPLv3 source license](https://github.com/CoCivium/CoCivium/blob/main/LICENSE); no private media embedded
- All ten conceptual thumbnails represent candidates and exploratory designs, not verified screenshots, user uptake, independently reviewed science, or automatic rights clearance for future assets
- This viewer is a projection: each successor must be rebased from the same canonical generator and exact generated HTML, never independently edited in place
- Same-provider GitHub source and GitHub Pages are not independent archival failure domains. Public URL and search index coverage require separate readproof.
- Expected public URL if GitHub Pages serves the site's `docs/` root: `https://cocivium.github.io/CoAcademy/megascroller/`.

**Publishing gate:** Verify exact HTML readback, source blob parity, keyboard/mobile first-use and actual HTTPS display before calling it a deployed page. No account creation, tracking, public post, webhook or scheduled task is initiated by this file.
