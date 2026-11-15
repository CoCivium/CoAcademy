# CoGibber R0 | One functional vertical slice

Status: BOUNDED STATIC BROWSER EXPERIMENT. No live CoGibber domain activation or CoAll canon.

## User task

A first-time user can choose a sample or paste a short note, structure it into candidate actions, questions and statements, correct each interpretation, add/remove items, and export a readable checklist or structured JSON. The original source stays attached to the JSON and all edits are explicit.

## What does not happen

No AI model, semantic understanding, browser storage, telemetry, login, backend or automatic external effect. No deadline is interpreted as a real scheduled obligation. No item grants permission for the system to execute it. Reject notes that are empty, more than 6000 characters or produce more than 30 segments instead of silently omitting material.

## Source and related surfaces

- Human page: `index.html` / `https://cocivium.github.io/CoAcademy/cogibber/`
- Machine twin: `discovery.json`
- Existing local seed: `D:\CoCivium\CoFarm\CoCloudSites261018-S1\R0B_private_preview_20261018\sites\CoGibber.html`
- Public discovery: `https://cocivium.github.io/CoAcademy/discover/`
- CoGibber family: domain mapping and DNS remain separately gated.

## H0/H1 comparison

H0: An ordinary note editor or hand-written checklist is at least as useful as this parser with less correction burden.
H1: Candidate structuring plus visible uncertainty produces more complete and inspectable outputs for specified tasks, measured by independent consenting users.

Do not infer H1 from unit/browser smoke tests. Preserve wrong classifications, unfinished items and negative feedback. Run keyboard, screen reader, mobile, copy, export, input safety and no-network checks before calling it accessible.