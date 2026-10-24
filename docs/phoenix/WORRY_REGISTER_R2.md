# CoPhoenix R2: bounded automated public worry register

**24 October 2026.** This extends the previously verified [CoPhoenix public HTTP readproof](./probe_public.py) without creating a separate fleet of observers.

## What automatically happens

The existing CoPhoenix GitHub Actions workflow is scheduled daily and runs whenever its own checker or workflow files change. The R2 stage reads the exact same-run JSON receipt and produces:

- co_phoenix_worries.json: typed priorities, observable states, uncertainty, source/run identity and proposed wake conditions.
- co_phoenix_worries.md: human-readable issue table, attached to the same workflow run.
- A concise GitHub Actions step summary for that run.

These outputs are workflow **artifacts**, not permanent Git commits or proof that someone saw the warning. Retention is 14 days and GitHub can disable or delay schedules.

## Worries that can be detected now

Confirmed HTTP failures, missing expected text, inconclusive network reads, an unparseable or incomplete 5-target receipt, and failure of the same-provider public-source fallback.

## Worries that remain open regardless of successful HTTP checks

GitHub common-failure-domain concentration; no qualified second-host recovery; the monitor's own possibility of stopping; real accessibility and first-time usability; domain alias and private CoStead/CoGateway/CoVIA health; currentness of official civic guidance; and absence of measured public learning.

A successful test may close the *observed public-page reachability* concern but not these wider risks.

## How much "AutoEvo" actually exists?

The bounded cycle is:

OBSERVE -> CLASSIFY -> DEDUPE WITHIN_RUN -> RANK -> PROPOSE_SAFE_TEST -> VERSIONED_WORKFLOW_RECEIPT -> NEXT_SCHEDULE.

No runtime auto-commit, DNS change, credential mutation, public accusation, messaging or deployment cutover follows a worry. This is deliberate: generated suggestions require fresh source-level qualification, relevant approvals, regression tests and verified outcome before a production repair. The checker cannot certify its own future runs. Another existing CoRelay six-hour checker provides related source-byte observations within the same GitHub vendor; that still isn't independent provider redundancy.

Risk definitions are a candidate contract. Changing the register or triage source goes through normal reviewed versioning; producing more risk labels is not measured improvement.

## Severity meaning

- P0: direct observed public-page failure or missing/invalid readproof critical to knowing what happened.
- P1: inconclusive current proof, source fallback failure or shared-service failure-domain concern requiring a bounded follow-up.
- P2: meaningful unverified capability or outcome, not necessarily an active outage.
- P3: reserved for low-importance items with an appropriate wake condition.

An actual attacker, government monitor or unauthorized observer is never inferred from an HTTP failure. An election-information error needs original-source confirmation and must not be broadcast as misconduct.

## Next proofs

1. Confirm a real GitHub Actions R2 run and download/inspect its JSON/Markdown artifacts.
2. Independently confirm a representative public route in a native mobile/keyboard/screenreader browser.
3. Prove a separate-provider public restoration, not merely GitHub Pages plus GitHub Raw.
4. Integrate one independent consent-based first-use correction into a source-versioned issue and demonstrate a closed fix.
5. If the checker misses its own cadence, detect that with a separately authorized receiver that does not depend entirely on the same GitHub schedule.

X2 and all private nodes remain untouched. This is a public monitoring product, not full autonomous evolution.

SOURCE_NE_HOST | PASS_NE_NO_WORRIES | UNKNOWN_NE_FAIL | WORRY_NE_REAL_ATTACKER | REPAIR_SUGGESTION_NE_PERMISSION | RUN_ONCE_NE_FOREVER
