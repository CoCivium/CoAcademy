# CoFed+ failure isolation R0

**Public browser-local simulation only. No federation, CivOS runtime, CoStax fleet, identity authority, independent hosting, or CoEx installed.**

This exercise reuses the [Civ2+ federated cell contract](https://github.com/CoCivium/CoCivium/blob/main/docs/Architecture/CIV2_FEDERATED_CELL_HOSTING_R0.md), the [CoAll GitHub Evolution Fabric](https://github.com/CoCivium/CoCivium/blob/main/docs/Evolution/COALL_GITHUB_EVOLUTION_FABRIC_R0.md), and the [CoOrbWare projection grammar](https://github.com/CoCivium/CoCivium/blob/main/docs/Architecture/COORBWARE_BEYOND_COSOFTWARE_R0_20261024.md).

Choose an outage or authority challenge on the [human page](https://cocivium.github.io/CoAcademy/constellation/federation/), then inspect the [typed machine fixture](https://cocivium.github.io/CoAcademy/constellation/federation/fixture.json). No AI model or network request runs when scenarios are selected. A loaded page may remain interactive offline, but this is not proof that a cold independent host can boot a service after provider failure.

A single cloud-hosted CI invocation should verify exact public/source bytes and the local fixture's invariants, including deliberately failing revoked-authority, two-writer and stale-manifest cases. Its browser counterpart exercises real Chromium at desktop/mobile sizes and network-off after load.

One next receiver test: a clean second host operated under separate authority serves a source-pinned release with GitHub intentionally unavailable at receiver time, followed by a second browser exact readproof. Measure RTO, RPO, human relay count and failure classification. Do not claim success before that receiver acts.

Status: `STATIC_TEST_FIXTURE_NOT_A_REAL_FEDERATION`. No DNS, private node, commercial partner or token runtime is touched.


## Portable first-use recovery capsule | bounded next test

A source-controlled [capsule builder](https://github.com/CoCivium/CoAcademy/blob/master/tools/cofed_coldboot_capsule.py) packages only CoGibber's public static page, machine description and README into a deterministic ZIP, with file SHA-256 checksums and an explicit nonclaim manifest.

The existing [public readback workflow](https://github.com/CoCivium/CoAcademy/blob/master/.github/workflows/public-pages-readback.yml) runs a separate `verify-coldboot-capsule` job on authorized source changes: build archive → clean extraction → verify checksums → boot via localhost in hosted Chromium → turn networking off after loading → test the first note-to-structured-result deed on desktop and reduced-motion mobile → retain machine receipts. It must complete successfully before the capsule is described as tested.

This test deliberately uses a GitHub-hosted CI runner. **Clean archive extraction and localhost cold start are not proof of a second independently administered provider**. Nor do they prove that the browser can cold-load with the provider unavailable. The next real federation acceptance gate remains a distinct second-host cold boot with GitHub inaccessible at receiver time, independently signed/read-back evidence and measured recovery time.

This capsule is source-review/test material. The CoAcademy repository's site-wide licensing has not been fully audited, so archive packaging does not grant new redistribution rights.

