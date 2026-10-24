# Money and Elections: Aggregate Comparison Lab R0

**24 October 2026 | Public research candidate**

## Lead

**Money in elections is measurable. An individual ballot is not a commodity.**

This public, nonpartisan source-based educational experience helps readers explore a limited descriptive statistic: **reported spending or public administration expense divided by counted ballots**. It does not identify who voted for whom, infer an individual political preference, assign election-integrity rankings, show that votes were purchased, or campaign for political choices.

- [HTML experiment](./index.html)
- [Machine-readable scope and sources](./discovery.json)
- [Exact-source mock runtime receipt](./test_receipt_r0.json)
- [Civic Integrity home](../)
- [Post-election evidence protocol](../POST_ELECTION_CONTINUITY_R0.md)

## Three distinct questions

| Question | Proper evidence | Invalid inference |
| --- | --- | --- |
| How much reported spending per counted ballot? | Financial statements for an explicitly defined scope, paired with official counted-ballot totals for the same jurisdiction/election | This is what it costs to *buy* a vote or determines why voters voted |
| How much does it cost to administer an election? | Comparable government budget outturn for all relevant responsible authorities, with shared cost categories and a matched ballot denominator | Higher cost proves waste, misconduct or a worse election |
| Has unlawful vote buying, intimidation or coercion occurred? | Credible specific records, applicable law, authorized review/investigation, due process, distinction between allegation and finding | Campaign spending divided by turnout diagnoses illegal payments |

**U.S. ballot secrecy:** EAC states voter files do not tell whom an individual voted for. Participation records may be available under state rules and have privacy protections. https://www.eac.gov/election-officials/voter-lists-registration-confidentiality-and-voter-list-maintenance

**Campaign reporting:** FEC source tables distinguish committee classes, coverage periods, disbursements and transfers. Adding all categories blindly can double count activity. https://www.fec.gov/campaign-finance-data/campaign-finance-statistics/ and https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology/

**2024 turnout:** EAC's June 30, 2025 release says more than 158 million ballots were counted in the 2024 general election. EAVS corrected Version 2.0 datasets were published February 12, 2026. The published national figure does not automatically match a federal-campaign-only expenditure numerator. https://www.eac.gov/research-and-data/studies-and-reports

**Administration spending:** state/county/municipal responsibility varies significantly and a statewide aggregate may omit local costs. https://www.ncsl.org/elections-and-campaigns/funding-election-administration

**Global:** International IDEA's Political Finance Database compares laws on funding, spending, disclosure, oversight and sanctions. Reported regulations should not be confused with verified enforcement or compliance. https://www.idea.int/data-tools/data/political-finance-database

**Federal bribery law:** 52 U.S.C. § 10307(c) prohibits specified payments connected to registration or voting in federal contests. A spending-per-ballot ratio is not a test of violations of this provision. https://uscode.house.gov/us/usc/119-118/t52/s10307/

## How to reproduce a responsible aggregate comparison

1. Choose a precisely defined election, observation year, government jurisdiction and financial reporting boundary.
2. Find an authoritative **spent** amount, not receipts or unrelated donations. List what is included and excluded; address intra-committee transfers, in-kind activity, outside groups, geography, currency and overlapping scopes.
3. Find official counted ballots for the **same** election and area. Ballots counted are not the same thing as registered voters, vote share, population or individual ballot choices.
4. Record original URLs, publication time, accessed time, exact table or field, amendments and candidate alternative sources.
5. Show the arithmetic with explicit data source and denomination: `reported spending USD / aggregate counted ballots`.
6. Label any unverifiable or reader-provided figures as `UNVERIFIED_READER_INPUT`. Fictional examples carry `SYNTHETIC_NOT_ELECTION_DATA`.
7. Never infer causal efficacy, individual preferences, corruption, group susceptibility or influence from the ratio.
8. Before comparing across states, countries or years, reconcile currencies, price levels, campaign laws, reporting coverage, election type and administrative finance responsibilities.

**2026 incompleteness:** before the November 3 general election and official reporting periods close, do not present current-cycle spending or turnout as final.

## Non-targeted public dissemination

Every person sees the same resource; the reader may voluntarily type a public jurisdiction label. No location inference, voter record, email push, campaign targeting or segmentation occurs. Source URLs are entered as text and **not** retrieved or validated by the tool. Copy to clipboard requires explicit action. Browser/host networking may have its own ordinary connection metadata; the site script does not send the entered values.

A minimum of 1,000 ballots is a coarse demonstration safeguard; it does not prove anonymity or make all smaller datasets inappropriate for unrelated legitimate public research.

## CoEvoAll and CoPatterna: accelerate verified learning

High-frequency repetitions do not multiply independent evidence. A genuinely different primary source, contradictory record, legal interpretation, accessibility observation or measured user outcome can be more valuable than thousands of duplicate tests.

The loop is:

`HYPOTHESIS -> SOURCE -> INDEPENDENT CHALLENGE -> TEST -> EXPLAINABLE RESULT -> REPAIR/REFRAME/RETRACT -> VERSIONED RECORD -> NEXT INDEPENDENT TEST`

Permitted resolutions are `REPAIR`, `REFRAME`, `RETRY_BOUNDED`, `REFER`, `STOP_RETRACT`, and `DORMANT`. Some experimental lines must stop rather than be repeated forever. Multiple AI sessions may propose views, but identity, permissions, distinct evidence lineage and receiver acknowledgements still matter.

## Verification limits

- **GitHub source:** committed and exact readback verified.
- **Mock runtime:** 30/30 source and isolated V8 DOM/clipboard checks passed on the initial page source.
- **Actual host reachability:** not established by independent browser fetch.
- **Screen reader, native browser and first-time public use:** not yet tested.
- **Real official spending datasets or active data connectors:** not ingested.
- **Political personalization, bulk messages, external sharing:** not used.
- **Election or public integrity result:** no such conclusion.

Published source is a research artifact, not evidence of a finished AI operating system, registered election service, official government relationship, or demonstrated human benefit.

`RATIO_NE_PRICE | SOURCE_NE_INDEPENDENT_VERIFICATION | MANY_MODELS_NE_MANY_WITNESSES | MORE_CYCLES_NE_FASTER_PROGRESS | PRIVACY_FIRST | STOP_WHEN_HARMFUL`
