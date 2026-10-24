# CoObserverMap R0: who can see, influence, interact or disrupt?

**Date:** 2026-10-24  
**State:** `PUBLIC_SOURCE_CANDIDATE__NOT_A_LIVE_OBSERVER_CENSUS__NO_INCIDENT_ASSERTED`

## Lead

**An observer is not necessarily a watcher; a watcher is not necessarily an attacker; a critic is not an enemy.**

CoCivium has public pages and machine-readable data, connected tools, human and synthetic collaborators, candidate domains, platform dependencies, and potential backup routes. All have relationships to what can be seen, changed, indexed, blocked, archived or misrepresented. The job of this inventory is to document **classes, scopes, permissions and evidence**, not name unknown people or label ordinary disagreement as hostility.

- [Readable evidence filter](./index.html)
- [Machine registry (15 classes)](./registry.json)
- [28-check isolated validation](./test_receipt_r0.json)
- [CoRelay opt-in public front door](../)
- [Existing CoCivium machine discovery boundaries](https://github.com/CoCivium/CoCivium/blob/main/docs/AI_DISCOVERY_POLICY.md)
- [CoWaitlessExecution and watcher/actuator separation](https://github.com/CoCivium/CoCivium/blob/main/docs/Architecture/COWAITLESS_EXECUTION_R0.md)
- [CoSession shadow observer limitations](https://github.com/CoCivium/CoCivium/blob/main/docs/Operations/COSESSION_SHADOW_LEDGER_R1.md)

## What is actually inventoried

The public registry describes 15 **classes**, not 15 observed visitors or connected services. They include:

- Public source readers, actual GitHub hosting/source controls, and potential normal visitors.
- Search and AI crawlers, public feed readers, voluntarily participating reviewers, GitHub Issues and platform moderation.
- Candidate registrars, DNS, hosts, social channels, recommendation systems and connected-app dependencies.
- Archives and backups (candidate preservation routes, not verified running replicas).
- CoStead, CoGateway, X2 and future private device resources, all unprobed in this wave.
- Software supply chain failure domains and generic potential abuse classes.
- Existing CoSession logical observer patterns and **unknown/unrepresented classes**.

Use `VERIFIED_SOURCE` for a directly inspected document or setting. Even that **does not** establish a human visited, a bot fetched it, or a particular actor is watching. `ARCHITECTURAL_CAPABILITY` indicates plausible capability without a matching event. `CANDIDATE` is planned, not live; `HELD` prohibits probing; `NOT_OBSERVED` reserves unknowns.

**An official public service, a journalist, a skeptical volunteer or an adversarial testing agent is not automatically a threat.** Neither is a government organization assumed to monitor or endorse this work because election information appears on the site.

## CoPhoenix+ as a dependency and restoration *proof* protocol

An "all copies run and live" system is neither demonstrated nor desirable by default. Public artifacts can be stored in many places, but source, access, execution, custody, currency and authorization are different properties.

| Substrate | Could preserve | Does **not** automatically provide |
| --- | --- | --- |
| Git repository and tags | Exact versioned source | Independent host/CDN uptime, secret custody, or audience acceptance |
| GitHub Pages | Public static HTML/CSS/JS when served successfully | Connected local models, privileged agents or own-device backups |
| Wayback / third-party archive | Public snapshot if independently captured and retrievable | Guaranteed current content, active back-end, private files, scheduling or application state |
| Offline package | Rebuildable local artifacts when the verified bytes exist | Public findability, live account access or data freshness |
| Independent mirror | Read availability *after host/domain/source checks* | Guaranteed different failure domain merely by changing domain alias |
| CoStead/CoGateway | Potential durable custody / authenticated relay | Connection, ACK, authority or deployment until tested and accepted |
| Future FOSS local AI | Some qualified local processing | Infinite compute, provider independence of every component, or permission to access other systems |

A *real* continuity drill would begin with a permitted, non-sensitive static public artifact; record a pinned source SHA; deliberately prevent use of its primary URL in a sandbox; fetch and validate a separately hosted copy from an independent client; verify content integrity and version; then simulate allowed recovery. It must not modify X2 or assume CoStead availability.

**Recovery PASS** requires independent readback and scope-correct functionality. `COPY_EXISTS`, `DNS_RESOLVES`, `REQUEST_200`, `CONTENT_MATCHES`, `ACTION_WORKS`, and `RECEIVER_ACK` are separate results.

## Security: what to watch when an authorized sensor exists

Prefer least-invasive, scoped **service-owned** audit records and public changes:
- Domain and certificate expiration, DNS and redirect changes, signed publication changes.
- Authorized account login and permission changes; content or branch changes and provenance.
- Dependence on hosting/provider accounts and rate limits, not presumed hostile surveillance.
- Actual issue spam, false claims or impersonation reports only after independent source review.
- Vulnerability reports, suspicious administrative actions, data leak indicators or lost access.
- Actual receiver downtime and the availability of a verified restore path.

Do **not** build a system for covertly identifying site visitors, mining private contacts, guessing political opinions, searching personal devices without permission, or publicly ranking people as "bad guys." Such activity would undermine the fairness and privacy the project is meant to support.

## Private incident object: schema, not a published dossier

`incident_id | privately_held_evidence | observed_utc | source_authenticity | exact_affected_asset | detected_behavior | scope | legitimate_access_baseline | plausible_nonmalicious_explanations | observed_impact | evidence_status | reviewer | confidentiality | containment | appeal_and_correction | retention_deadline | recovery_readproof`

Keep it in **actually authorized private custody** if an event occurs. Never open a public Github Issue with private system logs, names, access tokens, IP addresses tied to individuals, secret endpoints or unverified allegations.

No such private incident log has been created or populated by this release. The public machine registry contains **no identified malicious person, no event log, and no surveillance data**.

## CoPatterna+ on observer claims

Repeated reports from dependent providers, mirrors, AI summaries and news syndications may all trace back to **one** original assertion. Deduplicate source lineage before counting corroboration. A copied screenshot is not a new witness. Preserve credible contrary reports and the ability to retract a mistaken attribution.

No full census is possible from bounded public signals. If network logging and analytics are absent, that means `NO_OBSERVATION`, not `NO_VISITORS`, `NO_ATTACK` or `NO_RISK`.

## Turtles, autocycles and feedback

One useful loop is:

`PUBLIC_ASSET -> PERMITTED_OBSERVATION -> SOURCE_BOUND_CHANGE -> EVIDENCE_CLASS -> COUNTEREXAMPLE -> RISK_EVALUATION -> AUTHORIZED_REPAIR_OR_STOP -> INDEPENDENT_READBACK -> VERSIONED_RECEIPT -> QUIESCE`

Each loop must have real resources, a trigger, permission and a bounded budget. Reversible shadow investigations may proceed when an unrelated external action is gated. A report pointer is not proof of pickup; a replica does not gain additional authority; many logical watchers should not spawn thousands of provider tabs.

**Trigger ideas:** new public source mismatch, documented official-policy change, actual third-party security advisory affecting a known component, explicit participant report, authorized domain expiration notice, or failed independent source readback. A scheduled task or receiver is required for actual background monitoring; **none was deployed here**.

Failure dispositions: `FIX`, `HOLD`, `REFER`, `RETRACT`, `DORMANT` and `BOUNDED_RETRY`. Some exposure can be reduced, not eliminated. A false accusation must be corrected, not "solved" by repeating it.

## Current proof ledger

| Claim | Status |
| --- | --- |
| Public machine class register and source pointers | EXACT_GITHUB_READBACK |
| Human-readable filter view | SOURCE_COMMITTED |
| Isolated JS filtering and static privacy checks | PASS 28/28; no native browser |
| Specific hidden watchers or malicious actors discovered | NONE ASSERTED |
| Independent public host/browser readback | NOT_YET_VERIFIED |
| Private devices, DNS provider controls or CoStead/CoGateway queried | NOT_DONE |
| Backup or archive failover drill | NOT_DONE |
| Cross-provider subscriber pickup | NOT_OBSERVED |
| Always-on security watchers, liveness or monitor | NOT_DEPLOYED |

`POTENTIAL_ACCESS_NE_OBSERVED_MONITORING | CRITIC_NE_ATTACKER | MANY_MODEL_OPINIONS_NE_MANY_WITNESSES | BACKUP_NE_ACTIVE_RUNTIME | MORE_OBSERVERS_NE_MORE_AUTHORITY | SOURCE_NE_RECEIVER_ACK | X2_HELD`
