# CoCivicLens+ First-Use and Civic Learning Acceptance R0

**Date:** October 24, 2026  
**State:** `PUBLIC_TEST_PROTOCOL__NO_READER_STUDY_PERFORMED`  
**Scope:** Nonpartisan information-literacy and site usability. No candidate, party, voting-preference, or outcome persuasion measurements.

## Lead

**A successful source commit and a million repeated synthetic checks are not evidence that a real person found accurate information.**

This evaluation tests independent access, neutral factual quality, the ability to find official state/local election sources, and actual transfer of source-checking skills. Synthetic tests and volunteer observations are distinct evidence classes.

## Official references, checked on October 24, 2026

- FEC confirms the regularly scheduled 2026 U.S. federal general election on Tuesday, November 3, 2026, and notes that the FEC does **not** administer elections: https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/
- Vote.gov says deadlines vary by state or territory and links to state-specific instructions: https://vote.gov/register
- Vote.gov summarizes in-person, early, and mail voting possibilities, subject to jurisdiction: https://vote.gov/guide-to-voting
- USAGov advises checking the state/local election office for polling places and hours: https://www.usa.gov/find-polling-place
- EAC provides state election-office references and specifically cautions that state/local sources must be checked for current rules: https://www.eac.gov/vote
- EAC explains unofficial election-night reports versus final canvass and certification: https://www.eac.gov/voters/voter-faqs
- W3C WAI preliminary accessibility checks: https://www.w3.org/WAI/test-evaluate/preliminary/ (not a substitute for comprehensive evaluation).

## Gate A: Independently reachable, or explicitly NOT VERIFIED

- From an independently networked client, request `https://cocivium.github.io/CoAcademy/civiclens/`.
- Capture timestamp, response status, final URL after redirects, content-type, version marker, meaningful HTML title, and expected source/manifest version.
- Confirm public sources lead to the *correct* official resources without requesting the reader's address or identity on CoCivium pages.
- Check a static/no-JS browser, mobile-width browser, keyboard navigation, meaningful headings, visible focus, zoom, reduced motion, and at least one screen reader.
- Maintain distinct receipts: `PUBLIC_SOURCE`, `HOST_DEPLOY`, `INDEPENDENT_HTTP`, `BROWSER_RENDER`, `REAL_PARTICIPANT_OUTCOME`.
- Fail closed on broken official links or jurisdictionally misleading claims. A tool's inability to fetch a URL is `INCONCLUSIVE`, not automatic evidence that the live site is down.

## Gate B: Voluntary exploratory first-use observations

A small initial group of **five consenting, varied first-time participants** may reveal common usability problems, but it is *not* a statistically representative measure of nationwide outcomes. Seek accessibility and device diversity without collecting demographic or political profiles.

Give participants the page link without briefing them on CoCivium terminology. Ask them to attempt these neutral tasks in their own time:

1. Find the appropriate **official** state/local election office route, without entering an address into CoCivium.
2. Explain why an apparently national registration deadline might not apply to all states, citing the official source.
3. Distinguish an election-night unofficial total from certified results using the EAC voter FAQ.
4. Describe one question still unknown from the page and where they would check it.
5. Say, if they wish, which confusing phrase or unnecessary step caused difficulty.

Record **only voluntary, minimally necessary site-usability outcomes**, such as pass / blocked / unclear, independent source reached yes/no, elapsed time if freely observed with consent, and anonymized error category. Do not record how anyone votes, party affinity, ballot choices, personal registration state, IP addresses, voice recordings, biometric data, inferred politics, or identifying free-text by default.

No covert A/B testing, psychological profiling, artificial urgency, dark patterns, or claim of a verified learning gain without genuine pre/post evidence. One person can opt out or delete a voluntary note without losing access to official information.

## Gate C: Independent learning and counterexample checks

Run a neutral pre/post knowledge probe on *general* principles (e.g., whether polling-place rules are national or state/local) only with participant consent and with stable equivalent questions. Report the **number and diversity of observations, missed items, and limitations**, not a grand national impact statistic.

Challenge the project with:
- incorrect and outdated external search results;
- official source redirects;
- expired/cached page versions;
- low-connectivity and JS-disabled browsing;
- keyboard-only and screen-reader navigation;
- multilingual source needs (point to authoritative translations rather than fabricating them);
- a skeptical participant who rejects the CoCivium framing entirely;
- a participant who wants official information immediately and skips the interactive experience;
- an independent AI asked to separate actual source code, working deployment evidence, and unproved adoption.

Re-run representative tests when official references or the page code change. Do not conflate test repetition with independent coverage.

## Gate D: Review/stop/repair

A release remains **EXPERIMENTAL** until independent readback, factual validation, accessibility checks and consenting user observations support a narrower release claim. Immediately fix any critical wrong official route, confusing election rule, privacy leakage or accessibility blocker found in testing.

If humans find the project interface irrelevant, it is still a valuable result: the official source links may be enough. Do not obstruct direct access.

## Acceptance ledger

| Claim | Current evidence | State |
|---|---|---|
| HTML source publicly committed | GitHub contents readback | VERIFIED_SOURCE |
| Official sources placed first on page | Commit `bb5d1d8b160da383e07af257a93dbd9b3f936c23` | VERIFIED_SOURCE |
| GitHub Pages deployment of latest revision | Workflow success must be checked for relevant commit | NOT_YET_VERIFIED |
| Independent external browser readback | No independent successful request in this wave | UNKNOWN |
| Real-person first-use outcome | No volunteer observation conducted | NOT_MEASURED |
| Learning transfer / civic impact | No independent participant outcome data | NOT_MEASURED |
| Political persuasion effect | Not a project objective or measurement | OUT_OF_SCOPE |

`CYCLES_NE_COVERAGE | SOURCE_NE_RECEIVER | FIRST_USE_NE_GENERALIZATION | AUTHORITATIVE_SOURCES_FIRST | HUMAN_AGENCY_FIRST`
