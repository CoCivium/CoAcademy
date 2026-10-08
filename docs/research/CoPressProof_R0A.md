# CoPressProof+ R0A

State: PUBLIC-SAFE CANDIDATE · NOT CANON · NOT MEDIA CLAIM · NOT PRESS ENDORSEMENT

Machine-readable twin: [CoPressProof_R0A.json](CoPressProof_R0A.json)

## Purpose

Provide a small evidence register for external media/public-attention claims about CoCivium.

The register exists to prevent accidental inflation from:

- self-published material
- search/AI summaries
- aggregators
- forum mentions
- citations
- independent articles
- interviews
- editorial coverage

into one undifferentiated claim of "media coverage".

## Evidence classes

```
SELF_PUBLISHED
AGGREGATOR_OR_DIRECTORY
PUBLIC_FORUM_OR_THREAD
INDEPENDENT_CITATION
INDEPENDENT_ARTICLE
INTERVIEW_OR_APPEARANCE
EDITORIAL_COVERAGE
SEARCH_OR_AI_SUMMARY
UNVERIFIED_REFERENCE
```

## Required fields

Each candidate row should carry:

- source/outlet
- URL or stable native identifier
- title
- publication/observation date
- evidence class
- independence assessment
- direct source bound? yes/no
- archive/snapshot/hash if available
- what is actually said
- what is not established
- currentness
- correction/challenge path

## Current bounded posture — 2026-10-06

### Verified project-owned/public material

CoCivium has public project-controlled GitHub and publication surfaces.

Class: `SELF_PUBLISHED`

Meaning: public visibility exists.

Nonclaim: this is not independent media coverage.

### Aggregation / public-reference footprint

Some project references appear in public aggregation/discovery surfaces and historical community links.

Class: `AGGREGATOR_OR_DIRECTORY` or `PUBLIC_FORUM_OR_THREAD` when directly bound.

Meaning: discoverability/mention evidence only.

Nonclaim: aggregation is not newsroom reporting or editorial endorsement.

### Search/AI-summary reference mentioning media coverage

An internal evidence record preserves a screenshot of a search/AI-style summary that referenced "Main Media Coverage & Exposure Points" and LAVX News.

Class: `UNVERIFIED_REFERENCE` / `SEARCH_OR_AI_SUMMARY`

Meaning: a lead for source recovery.

Nonclaim: until the underlying article/source is directly bound and inspected, it must not be counted as verified independent coverage.

### Major mass-media/editorial coverage

Current state: `UNPROVEN_IN_BOUNDED_REVIEW`

This does not assert zero coverage. It means no directly bound, independently verified major-newsroom article/interview was established by the bounded evidence used for this candidate.

## Rails

```
MENTION_NE_COVERAGE
AGGREGATION_NE_EDITORIAL_REPORTING
SEARCH_SUMMARY_NE_SOURCE_ARTICLE
PUBLICITY_NE_VALIDATION
CITATION_NE_ENDORSEMENT
INTERVIEW_NE_APPROVAL
OUTLET_NAME_NE_VERIFIED_ARTICLE
ABSENCE_IN_BOUNDED_SEARCH_NE_GLOBAL_ABSENCE
```

## Promotion ladder

```
DISCOVERED_LEAD
-> SOURCE_BOUND
-> CONTENT_INSPECTED
-> INDEPENDENCE_CLASSIFIED
-> DATE_AND_IDENTITY_VERIFIED
-> CLAIMS/NONCLAIMS_EXTRACTED
-> VERIFIED_PRESS_REGISTER_ROW
```

No step may be skipped merely because a search engine, AI answer, repost, or screenshot sounds authoritative.

## Relation to CoPublicationAdaptiveLens+

CoPressProof+ supplies external-attention evidence to the publication/public-signal layer.

It does not authorize outreach, replies, press releases, targeting, promotion, or publication.

Press/outreach effects remain separately gated.


## Bounded currentness check — 2026-10-08

A fresh read-only public-web scan checked project-specific terms including CoCivium, CoCivia, CoTheoryAll, BeAxaKitten, Cognocarta Consenti, and Headless Magic Dragon.

Observed in the bounded result set:

- project-controlled GitHub/public material;
- no fresh independently verified major-newsroom article, interview, or editorial feature.

Disposition: `NO_NEW_VERIFIED_INDEPENDENT_COVERAGE_IN_BOUNDED_CHECK`

This is negative bounded evidence only. It does not establish global absence of coverage, and it should be superseded whenever a directly bound independent source appears.

Preserve:

```
NO_RESULT_IN_BOUNDED_CHECK_NE_GLOBAL_ABSENCE
PROJECT_OWNED_RESULT_NE_INDEPENDENT_PRESS
CURRENTNESS_CHECK_NE_MONITORING_COVERAGE
```
