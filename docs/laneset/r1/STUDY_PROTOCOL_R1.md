# CoAthene LaneSet R1 | Counterbalanced pilot protocol

**State:** PUBLIC RESEARCH PROTOCOL CANDIDATE. No registered participants, validated outcomes or human-study findings.

## Research question

Does a typed cross-lane grouping help independently consenting readers locate source-backed claims more accurately or quickly than the same records shown as a date-ordered list, after accounting for order, task set and complexity?

## Competing explanations

- **H0:** Timeline is equally usable or better. Grouping adds jargon and navigation overhead.
- **H1:** Grouping by relation or other declared dimensions improves traceability or correct first selections enough to justify extra effort.
- **H2 (confounder):** Any difference arises from question wording, card position, familiarity, order, reading strategies or prior experience rather than the lane representation.

## What R1 actually does

The R1 browser canary displays the same eight public-source cards under Timeline and CoLaneSets. It selects one of **four assignment arms** using browser cryptographic randomness:

| Arm | Phase 1 | Phase 2 |
| --- | --- | --- |
| 0 | Timeline, set A (Q0 Q2 Q4 Q6) | CoLaneSets, set B (Q1 Q3 Q5 Q7) |
| 1 | CoLaneSets, set A | Timeline, set B |
| 2 | Timeline, set B | CoLaneSets, set A |
| 3 | CoLaneSets, set B | Timeline, set A |

Each participant sees different questions in the two representations; **no single-person head-to-head superiority inference is valid**. A set appears under both representations *across participants*. Random assignment is not quota balancing and small voluntary samples may be uneven.

Result export records arm, question indices, task set, view, selected card, answer correctness and first-choice milliseconds. It is local to the browser until a participant explicitly copies it. No identifiers, cookies, automatic results upload, account access or tracking scripts are provided by this experiment.

## Synthetic verification

On 15 November 2026 a local isolated Chromium test exercised all four arms: 8 correct selections per arm, 32 total, phase changes, result completeness, restart, browser page errors and narrow mobile overflow. **Four arms passing is a software test, not human evidence.** It does not measure independent page accessibility, comprehension, retention or educational benefit.

## Study readiness gate

Before recruiting consenting participants or claiming a quantitative result:

1. Pre-register outcomes and exclusion criteria, including negative and null findings.
2. Add a plain notebook or simple list comparator, not merely Timeline versus CoLaneSets.
3. Calibrate task difficulty and avoid exposing answers to a later phase through training effects.
4. Measure accuracy, task time, delayed source comprehension, confidence calibration, cognitive load, accessibility and qualitative reasons for confusion.
5. Counterbalance across a meaningful sample; document assignment arm and deviations.
6. Preserve incomplete runs, mistakes, any participant objections, dropouts and corrections.
7. For minors or vulnerable users use specific independent safeguards, age-appropriate assent and required guardian permission. Do not automatically profile anyone or infer clinical traits, general intelligence, consciousness or moral merit.

## Analysis rule

Report descriptive per-arm and per-view outcomes with explicit denominators, uncertainty and missing data. Treat H0 as a real possibility. The system is judged by better task outcomes and fewer unsupported claims, not by its vocabulary or design attractiveness.

**Nonclaims:** No participant recruitment, no validated learning effect, no global CoScendence score, no clinical/cognitive diagnosis, no independent receiver acceptance, no CoAll canon, no runtime service activation. Source in GitHub is not proof that Pages has deployed. All public and private release boundaries remain independently scoped.

## Provenance

- [R0 browser canary](../index.html), preserved unchanged.
- [R1 source](index.html), four-arm browser assignment.
- [Public Ocean and Minds journal](https://github.com/CoCivium/CoCivium/blob/main/docs/Journal/2026-11-15-ocean-and-minds-that-study.md).
- [CoAthene learner rail](../LEARNER_INQUIRY_R0.md).
