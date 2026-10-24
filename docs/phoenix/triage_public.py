#!/usr/bin/env python3
"""CoPhoenix R2: deterministic public-surface worry register, NOT self-repair."""
import datetime
import json
import os
import pathlib
import sys

INPUT="co_phoenix_public_readproof.json"
OUT_JSON="co_phoenix_worries.json"
OUT_MD="co_phoenix_worries.md"
PAGE_STATES=("PASS","FAIL","INCONCLUSIVE")

BASELINE=[
 ("SHARED_GITHUB_PROVIDER","P1","OPEN_KNOWN_LIMIT",
  "Pages, raw source, workflows, issue intake and core repository depend on GitHub.",
  "Prove a cold recovery from a separate authorized vendor and independent custody; no alias-only replica.",
  "OWNER_GATE_EXTERNAL_HOST_AND_CUSTODY"),
 ("MONITOR_MONITOR_UNVERIFIED","P1","OPEN_KNOWN_LIMIT",
  "A scheduled workflow cannot certify that its own future runs will keep occurring.",
  "Use the existing independent observer if available to check the last completed run; escalate a missed window.",
  "WAKE_WHEN_GITHUB_ACTIONS_RUN_EXPIRES"),
 ("OFF_PROVIDER_RESTORE_UNVERIFIED","P1","NOT_VERIFIED",
  "The verified offline capsule and GitHub receipts do not prove a current restored public service on another provider.",
  "Run a permissioned source-pinned restoration drill on independent custody; no production cutover.",
  "HOLD_UNTIL_SEPARATE_RECEIVER_OR_HOST"),
 ("BROWSER_ACCESSIBILITY_UNVERIFIED","P2","NOT_VERIFIED",
  "HTTP 200 with an expected string does not prove mobile, keyboard or screen-reader usability.",
  "Arrange opt-in independent browser and accessibility test, retain version-specific repro steps.",
  "WAKE_ON_ACTUAL_TEST_OR_RELEVANT_RELEASE"),
 ("DOMAINS_AND_PRIVATE_NODES_UNVERIFIED","P2","NOT_VERIFIED",
  "CoPolitic aliases, CoStead, CoGateway, CoVIA and private node health were not checked here.",
  "Verify separately with their legitimate owners and consent; do not probe private systems.",
  "HOLD_NO_AUTHENTICATED_READER"),
 ("PUBLIC_OUTCOME_AND_REVIEW_UNVERIFIED","P2","NOT_VERIFIED",
  "Public source, deployment and HTTP checks do not measure independent user comprehension or benefit.",
  "Invite consent-based nonpartisan first-use and factual review, preserve negative findings.",
  "WAKE_ON_VOLUNTARY_PUBLIC_FEEDBACK"),
 ("CIVIC_SOURCE_FRESHNESS_UNVERIFIED","P2","NOT_VERIFIED",
  "This probe cannot confirm that third-party election guidance remains current for every jurisdiction.",
  "Review original dated official publications; avoid election incident intake or automated accusations.",
  "WAKE_ON_OFFICIAL_SOURCE_REVISION"),
]

def put(items,risk_id,priority,state,why,next_step,wake,source):
 items.append({
  "id":risk_id,"priority":priority,"state":state,
  "evidence":why,"proposed_next_step":next_step,"wake_condition":wake,
  "source_scope":source,"executed_repair":False
 })

def evaluate(readproof):
 risks=[]
 if readproof is None:
  put(risks,"RECEIPT_UNAVAILABLE","P0","INCONCLUSIVE",
      "No parseable readproof file was present at this run.",
      "Inspect this workflow and recover exact run logs before relying on green history.",
      "NEXT_COMPLETED_INDEPENDENT_READPROOF","WORKFLOW_ARTIFACT")
  known={}
  evidence_time=None
  prior_commit=None
 else:
  evidence_time=readproof.get("checked_utc")
  prior_commit=readproof.get("commit")
  readings=readproof.get("readings")
  if not isinstance(readings,list) or len(readings)!=5:
   put(risks,"RECEIPT_SCOPE_INCOMPLETE","P0","INCONCLUSIVE",
       "Expected five source-bound public targets; data shape or target count differs.",
       "Recheck runner input and exact allowlist; do not certify complete coverage.",
       "AFTER_VALID_INPUT_SHAPE","WORKFLOW_ARTIFACT")
   readings=[]
  known={}
  for x in readings:
   if not isinstance(x,dict) or not isinstance(x.get("target"),str):
    continue
   target=x["target"]
   if target in known:
    put(risks,"DUPLICATE_TARGET_"+target,"P1","INCONCLUSIVE",
        "The same public target appears twice in one receipt.",
        "Review duplicate target identities, do not double-count observations.",
        "AFTER_TARGET_IDENTITY_REVIEW",target)
    continue
   known[target]=x
   for field,label in (("page","PUBLIC_PAGE"),("raw","GITHUB_RAW")):
    part=x.get(field)
    state=part.get("status") if isinstance(part,dict) else None
    if state=="PASS": continue
    if state=="FAIL":
     severity="P0" if field=="page" else "P1"
     outcome="CONFIRMED_FAILURE_FROM_RUNNER"
     next_step=("Inspect deployment/marker and compare exact canonical source before any change."
      if field=="page" else "Inspect GitHub Raw response; this is same-provider source loss, not proven offsite loss.")
    else:
     severity="P1"
     outcome="INCONCLUSIVE"
     next_step="Check runner network, redirect, DNS and source status before diagnosing a site outage."
    put(risks,label+"_"+target,severity,outcome,
        label+" observed "+str(state or "MISSING")+"; reason="+str(part.get("error") if isinstance(part,dict) else "NO_SUBRECORD"),
        next_step,"NEXT_BOUNDED_SOURCE_READPROOF",target)
  if len(known)!=5 and not any(x["id"]=="RECEIPT_SCOPE_INCOMPLETE" for x in risks):
   put(risks,"RECEIPT_TARGET_IDENTITY_INCOMPLETE","P0","INCONCLUSIVE",
       "Target identities are absent, malformed or duplicated.",
       "Review artifact and fix only the monitoring fixture after source-qualified correction.",
       "AFTER_TARGET_IDENTITY_REVIEW","WORKFLOW_ARTIFACT")
 for rid,priority,state,why,next_step,wake in BASELINE:
  put(risks,rid,priority,state,why,next_step,wake,"ARCHITECTURE_OR_EXTERNAL_PROOF")
 order={"P0":0,"P1":1,"P2":2,"P3":3}
 risks.sort(key=lambda r:(order.get(r["priority"],9),r["id"]))
 result={
  "schema":"CoPhoenix.PublicWorryRegister.R2",
  "compiled_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "source_readproof_created_utc":evidence_time,
  "source_commit":prior_commit,
  "runner_workflow":os.environ.get("GITHUB_WORKFLOW","LOCAL_REVIEW"),
  "run_id":os.environ.get("GITHUB_RUN_ID"),
  "source_valid":len(known)==5 and readproof is not None,
  "automatic_detection_scope":"Five public pages and their same-vendor GitHub Raw pointers, plus known structural unverified relations.",
  "automatic_effects":["WRITE_JSON_REPORT","WRITE_MARKDOWN_REPORT","PRESERVE_GITHUB_ARTIFACT","SUGGEST_NEXT_GATED_TEST"],
  "blocked_effects":["AUTOMATIC_PRODUCTION_CODE_REWRITE","DOMAIN_REDIRECT_CHANGE","EXTERNAL_OUTREACH","POLITICAL_TARGETING","DEVICE_ACCESS","SECRET_OR_ACCOUNT_ACCESS","DEPLOYMENT_CUTOVER","ASSERTING_UNKNOWN_ACTOR"],
  "worries":risks,
  "counts_by_priority":{p:sum(x["priority"]==p for x in risks) for p in ("P0","P1","P2","P3")},
  "observable_current_passes":sum(x.get("page",{}).get("status")=="PASS" for x in known.values()),
  "interpretation":"The risk list includes known architectural debt even when 5/5 public readbacks pass. Missing data is UNKNOWN, not healthy.",
  "cross_run_trend":"UNMEASURED_WITHOUT_A_BOUND_PREVIOUS_RECEIPT",
  "auto_repair":"NOT_ENABLED",
  "receipts_are_not":["VOTER_OR_AUDIENCE_TRACKING","INDEPENDENT_PROVIDER_BACKUP","UNIVERSAL_NODE_HEALTH","HUMAN_READER_ACCEPTANCE"]
 }
 return result

def selftest():
 good={"checked_utc":"fixture","commit":"fixture",
       "readings":[{"target":s,"page":{"status":"PASS"},"raw":{"status":"PASS"}} for s in ("relay","phoenix","observer","civic","satire")]}
 a=evaluate(good)
 assert a["observable_current_passes"]==5
 assert a["counts_by_priority"]["P0"]==0
 assert a["counts_by_priority"]["P1"]>=3
 assert a["auto_repair"]=="NOT_ENABLED"
 bad=json.loads(json.dumps(good))
 bad["readings"][0]["page"]={"status":"FAIL","error":"CONTENT_MARKER_MISSING"}
 b=evaluate(bad)
 assert any(x["id"]=="PUBLIC_PAGE_relay" and x["priority"]=="P0" for x in b["worries"])
 bad["readings"][0]["page"]={"status":"INCONCLUSIVE","error":"URLError"}
 c=evaluate(bad)
 assert any(x["id"]=="PUBLIC_PAGE_relay" and x["state"]=="INCONCLUSIVE" for x in c["worries"])
 missing=evaluate(None)
 assert any(x["id"]=="RECEIPT_UNAVAILABLE" for x in missing["worries"])
 duplicated=json.loads(json.dumps(good))
 duplicated["readings"][4]["target"]="relay"
 d=evaluate(duplicated)
 assert not d["source_valid"]
 assert len({x["id"] for x in d["worries"]})==len(d["worries"])
 print("CoPhoenix worry triage fixtures: PASS",flush=True)

def main():
 selftest()
 if "--selftest" in sys.argv: return 0
 try:
  evidence=json.loads(pathlib.Path(INPUT).read_text(encoding="utf-8"))
 except (OSError,ValueError):
  evidence=None
 report=evaluate(evidence)
 pathlib.Path(OUT_JSON).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 lines=[
  "## CoPhoenix public worry register (run-specific)",
  "",
  "Run: "+str(report["run_id"])+"; observed source time: "+str(report["source_readproof_created_utc"]),
  "",
  "Public Pages PASS: "+str(report["observable_current_passes"])+"/5; unknown domains, private nodes and real-user outcomes remain outside scope.",
  "",
  "| Priority | Status | Worry | Evidence and next bounded step |",
  "| --- | --- | --- | --- |",
 ]
 for risk in report["worries"]:
  summary=(risk["evidence"]+" NEXT: "+risk["proposed_next_step"]).replace("|","/")
  lines.append("| "+risk["priority"]+" | "+risk["state"]+" | "+risk["id"]+" | "+summary+" |")
 lines.extend(["","This run only classified and proposed. It made no repairs or external contact.",
                "All Pages and Raw source checks share GitHub as a provider."])
 pathlib.Path(OUT_MD).write_text("\n".join(lines)+"\n",encoding="utf-8")
 print("CoPhoenix worry register emitted: "+str(report["counts_by_priority"]),flush=True)
 return 0 if report["source_valid"] else 1

if __name__=="__main__":
 sys.exit(main())
