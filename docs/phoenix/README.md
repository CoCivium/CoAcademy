# CoPhoenix R0: public source-backed cold-start contract

October 24, 2026. The capsule itself is a chat-only private download, not a public ZIP release.

## Verified
Three previous self-contained browser prototypes, one 47,275-byte ZIP, 13 pinned member files, 26/26 local cold-start checks and a full SHA-256 outside this public source in the user's downloadable checksum.
Zip digest: 868a2f8f9ca9276e359917b526c24cc178639b19a600e2c358b514e8f82f0d9f
Test details: ./test_receipt_r0.json

## Recover a verified local capsule
1. Find the actual ZIP in a separately authorized durable location. The current chat download is not a proven CoStead copy.
2. Compare the complete ZIP hash to the separately retained reference. An embedded checksum by itself cannot authenticate an attacker-replaced archive.
3. Extract in a fresh directory, run python VERIFY.py, and stop on any missing or mismatched member.
4. Open index.html in a compatible browser or run python RUN_LOCAL.py, which serves only on 127.0.0.1:8765 until Ctrl-C.
5. Check one useful interaction per required page and source currentness before any further publication. Never infer service identity or effect authority from restored bytes.
6. To promote a second public origin, separately verify privacy/rights, actual destination, DNS and HTTPS, independent receiver GET, rollback, and end-to-end usefulness.

## Important negative result from the test harness
The sandbox browser blocked direct file:// navigation. The passing checks used separately extracted document rendering in offline Chromium and four distinct loopback HTTP 200 tests. Therefore do not claim direct file-link navigation was independently browser-tested.

## Known failure-domain debt
GitHub source, Pages, Raw, issue intake and the existing six-hour probe share one provider. CoStead, CoGateway, CoPolitic alias DNS, independent forge or public host, CoVIA and Wayback snapshots have not been restored, installed or verified by this experiment. Do not confuse configured monitors with live tasks or a private chat file with independent offsite custody.

## Existing donors, not reinvention
RepoZipper design: https://github.com/CoCivium/CoCivium/blob/main/docs/Product/COPLATFORM_HELPER_ECOLOGY_REPOZIPPER_R0.md
CoRelay public probe: https://github.com/CoCivium/CoAcademy/blob/master/.github/workflows/corelay-public-probe.yml
Wayback help: https://archivesupport.zendesk.com/hc/en-us/articles/360004651732-Using-The-Wayback-Machine
CoRelay: ../relay/

## Feedback about feedback
A correction route is a dependency, not an infinite source of truth. If GitHub Issues is lost, the fallback intake is UNKNOWN, not received. Preserve a nonpersonal local note until a verified alternate approved receiver exists. A harmful, unverified or stale source should stop propagation, not be replicated everywhere.

All recurring, experimental or recursive review is bounded by material information gain, authority and cost. Wake only on changed source, contradiction, expiry, receiver proof or available alternative failure domain.

BACKUP_NE_RESTORE | ARCHIVE_NE_CURRENT | FAILURE_NE_DELETE | REPEAT_NE_LEARN | REPAIR_NE_PERMISSION | RECEIPT_BEATS_ASSERTION
