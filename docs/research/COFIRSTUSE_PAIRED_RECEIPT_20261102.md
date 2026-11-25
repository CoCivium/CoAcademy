# CoFirstUse paired public first-use receipt | 2026-11-02

State: SOURCE_OBSERVED__ONE_VANTAGE_PUBLIC_FETCH__NO_RELEASE_OR_RUNTIME_CLAIM

## Bound sources
- CoAcademy comparator: scripts/cofirstuse_compare.py; source-only 10 feature checks, optional allowlisted one-vantage HTTP; not user acceptance or an accessibility audit.
- Paired surfaces: docs/index.html and docs/groupbuild/index.html; supporting docs/experience/index.html, docs/kitten/index.html, docs/about/index.html.
- GroupBuild planning references: CoCivium/CoCivium docs/Architecture/GROUPBUILD_COTEAMING_COPAYBACK_R0_20261101.md and COTEAMING_COPROJECTFIELD_R0_20261101.md, linked from GroupBuild page.
- Existing hostname incident: CoCivium/CoSteward#60. Do not duplicate or close without current binding proof.

## Bounded independent public fetches
One web vantage on 2026-11-02; a web fetch failure is not an authoritative DNS or TLS diagnosis.
- https://cocivium.org/ : fetched 404.
- https://www.cocivium.org/ : fetched 200 HTML headed "CoInfra260610 Bulk Static Direct-View Site Candidate", not the CoAcademy human-first site. Page labels itself LOCAL_STATIC_SITE / NOT_PUBLIC_HOSTED, despite public response. It lists shard links and metadata counts. No shard or sitemap link opened; do not infer exposure of private records from a metadata page alone. Review public classification and release authority before any origin change.
- https://cocivium.github.io/CoAcademy/ and /groupbuild/ : web tool could not access; no success/failure HTTP assertion.
- https://groupbuild.org/ : web tool returned 502; one-vantage only.
- https://groupbuild.com/ : web tool could not access; no authoritative reachability conclusion.

## Source review, not runtime acceptance
| Trait | CoCivium | GroupBuild |
|---|---|---|
| Human-first visual | Dark luminous hero, page-local themes, linked exploration/creator doors | Illustrated constellation, paired community and managed-services doors |
| Task | Navigate to Living World/CoTime or sketch with BeaxaKitten | Choose fictional park/game/skills project; generate/copy fictional brief |
| Accessibility | Focus-visible, reduced-motion styles, keyboard-described canvas controls | Focus-visible, reduced-motion styles, semantic buttons and aria-live results |
| Privacy | No login on entry; BeaxaKitten journal is opt-in browser-local | No login or data transmission by the sample project code |
| Evidence | Source/limitation links; no verified outcome | Architecture/limitation links; no real team creation or promised service |
| Recovery | Reset visual view, browser-local export/delete for kitten sketches | Re-select scenario and re-copy brief; no durable project state |
| Burden | Multiple concepts and doorways | Clear task but fictional output; no route to real consensual project intake |

## Specific source findings
- Initially docs/index.html had TWO h1 elements (hero and research catalogue), failing comparator's one_h1 rule. Corrected ONLY the catalogue heading to h2 in branch commit 480e87da2da82f0e592434a4310bc27b3e112ad2; fresh source readback blob d41f3ba9bed4072f49614512404e93a7699e1629 confirms exactly ONE h1. Not merged or deployed; tests not executed.
- Repeated destination links on CoAcademy and About pages do not by themselves prove broken paths: some appear in optional depth views, as expected navigation. Comparator reports duplicate href strings but does not resolve targets.
- Real-device accessibility, contrast, screen-reader reading order, clipboard success, physical-device claims, real participant task outcomes, and recovery after provider loss are UNVERIFIED.
- Do not treat source availability, browser fetch status, proposed domains, or this document as ACK, operational deployment, legal incorporation, independent acceptance, or canon.

## Next wake / highest-value proof
1. Recheck intended cocivium.org apex and www origins, source owner, confidentiality, release authorization, and rollback; existing CoSteward#60 stays HOLD. Do not touch DNS.
2. On the isolated development branch, execute comparator and unit tests against the corrected homepage; obtain release-owner review before any merge/publish. The source correction is committed but not runtime-tested.
3. Repeat the allowlisted GET-only live matrix from two independent vantage points and preserve response/status evidence; no shard traversal.
4. Test one newcomer finishing a GroupBuild fictional brief and exporting/retaining it, and one visitor finishing CoCivium discovery, with consent and accessibility observations. No human success claim until observed.

## Targeted link source existence (2026-11-02 follow-up)
Eleven direct link destinations were fetched from the same branch, without a web crawl: docs/rickbar/index.html, docs/coorb/index.html, docs/device-first/index.html, docs/coplay/votes-for-sale/index.html, docs/relay/index.html, docs/relay/feed.xml, docs/relay/discovery.json, docs/relay/observer-map/registry.json, docs/LATEST.md, docs/AGENT_INDEX.json, docs/research/CIV2_TO_CIV3_BOUNDARY_READINESS_R0.json. All eleven returned source blobs. This checks repository path existence only, not successful public navigation, full-link coverage, or absence of broken redirects.

Effects of this branch: research receipt and exactly one h1->h2 source correction, with commit/readback evidence. No DNS, payment, outreach, origin, canon, runtime, private shard, or hosted site mutation.
## Source-test and probe safety follow-up (2026-11-02)
- The exact original comparator and unit-test files were retrieved through the GitHub connector, recreated in a disposable offline runner, and verified by Git blob hashes 1328fddc3b34aba256e8eae838158c9e6f2a0e6a and eececd639c4638b8a762e0b787bdd49939eb43e1. The three pre-existing Python unittest cases passed. This is not a full repository checkout or hosted runtime test.
- The original live probe used urllib.request.urlopen, which follows HTTP redirects by default. This conflicted with the allowlisted landing-document-only constraint. On this isolated branch, fixed by installing NoRedirectHandler and reporting HTTP 301/302/303/307/308 as REDIRECT_NOT_FOLLOWED. Implementation commit 56a382179f55dc862f62755b0f41fd7d2286ff1f, verified blob 44ac16514bc431078525f8558f3cb617e967d306.
- Added two no-network unittest regression cases for redirect rejection and response reporting. Test commit 5293839786a2a71edbad6e73012eba3c83792dc1, verified blob cf39407fc25e4284902a0f5beb8c02ca1de29119. All five tests passed in the disposable runner before GitHub writes, with resulting blobs matching the tested files.
- A source-level reimplementation of the ten named comparator predicates across the five fetched public pages found 10/10 static flags for each. This is supporting evidence, NOT an execution of the full comparator over the five page files. The checked source locations are unchanged except the homepage h1 fix. The comparator in the disposable runner was separately executed against an empty local docs tree and correctly reported five MISSING_OR_NOT_MOUNTED entries.
- No opt-in live probe performed here; DNS, HTTP origins, redirects in production, browser UX, human task completion, and deployment remain unverified. Release process and dual-vantage checks remain outstanding.
