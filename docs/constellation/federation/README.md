# CoFed+ failure isolation R0

**Public browser-local simulation only. No federation, CivOS runtime, CoStax fleet, identity authority, independent hosting, or CoEx installed.**

This exercise reuses the [Civ2+ federated cell contract](https://github.com/CoCivium/CoCivium/blob/main/docs/Architecture/CIV2_FEDERATED_CELL_HOSTING_R0.md), the [CoAll GitHub Evolution Fabric](https://github.com/CoCivium/CoCivium/blob/main/docs/Evolution/COALL_GITHUB_EVOLUTION_FABRIC_R0.md), and the [CoOrbWare projection grammar](https://github.com/CoCivium/CoCivium/blob/main/docs/Architecture/COORBWARE_BEYOND_COSOFTWARE_R0_20261024.md).

Choose an outage or authority challenge on the [human page](https://cocivium.github.io/CoAcademy/constellation/federation/), then inspect the [typed machine fixture](https://cocivium.github.io/CoAcademy/constellation/federation/fixture.json). No AI model or network request runs when scenarios are selected. A loaded page may remain interactive offline, but this is not proof that a cold independent host can boot a service after provider failure.

A single cloud-hosted CI invocation should verify exact public/source bytes and the local fixture's invariants, including deliberately failing revoked-authority, two-writer and stale-manifest cases. Its browser counterpart exercises real Chromium at desktop/mobile sizes and network-off after load.

One next receiver test: a clean second host operated under separate authority serves a source-pinned release with GitHub intentionally unavailable at receiver time, followed by a second browser exact readproof. Measure RTO, RPO, human relay count and failure classification. Do not claim success before that receiver acts.

Status: `STATIC_TEST_FIXTURE_NOT_A_REAL_FEDERATION`. No DNS, private node, commercial partner or token runtime is touched.
