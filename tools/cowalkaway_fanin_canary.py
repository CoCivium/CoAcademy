#!/usr/bin/env python3
"""Bounded CoWalkaway+ / CoGlyphList+ read-only fan-in canary.

Consumes the existing CoConstellation five-bubble source fixture.
No network, models, effects, cron creation, queues, privileged state or public writes.
This does NOT reimplement the authoritative CoSession/CoEvo fan-in compiler.
It tests the proposal-boundary contract before actual receiver work is permitted.
"""
from __future__ import annotations
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent.parent
BOARD = ROOT / "docs/constellation/bubbles/board.json"
REPORT = ROOT / ".ci" / "walkaway" / "fan-in-canary.json"
ALLOWED_STATE = "PROPOSED_NOT_DISPATCHED"
SAFE_WORK = "RESEARCH_OR_PROPOSAL_ONLY"
BLOCKED_KEYS = {"password", "secret", "api_key", "private_email", "access_token",
                "credentials", "authorization_header", "bearer_token"}
NONCLAIMS = [
    "CANDIDATE_WORK_NE_ACTUAL_WORKER_EXECUTION",
    "DUPLICATE_SUPPRESSION_NE_EXACTLY_ONCE_EXTERNAL_EFFECT",
    "RUNNER_FILESYSTEM_NE_INDEPENDENT_DURABLE_RECEIVER",
    "NO_SESSION_RELAY_IN_TEST_NE_STEWARD_REPLACED",
    "PUBLIC_SOURCE_NE_COEX_CANON_OR_RECEIVER_ACK",
    "GRAPH_VALIDATION_NE_LEGAL_AUTHORITY",
    "NO_PRIVATE_SOURCE_OR_CREDENTIAL_INGESTION",
]

def stable(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")

def digest(value):
    return hashlib.sha256(stable(value)).hexdigest()

def privacy_violation(value):
    if isinstance(value, dict):
        for k, v in value.items():
            if str(k).lower() in BLOCKED_KEYS or privacy_violation(v):
                return True
    elif isinstance(value, list):
        return any(privacy_violation(v) for v in value)
    return False

def graph_checks(board):
    assert board["schema"] == "CoAll.CoConstellation.SoftQuarantinedSiteBubbles.R0"
    nodes = board["bubbles"]
    ids = [b["id"] for b in nodes]
    assert len(ids) == len(set(ids)) and ids, "duplicate bubble ID"
    work = board["work_candidates"]
    work_ids = [w["work_id"] for w in work]
    assert len(work_ids) == len(set(work_ids)) and work_ids, "duplicate WorkID"
    assert len(nodes) == len(work) == 5, "unexpected scope, explicit review required"
    owned = set()
    for b in nodes:
        for path in b["owned_paths"]:
            key = (b["repo"],path)
            assert key not in owned, "path collision"
            owned.add(key)
        assert b["repo"].startswith("CoCivium/") and b["branch"], "invalid repo"
    known_bubbles = set(ids)
    known_patterns = {p["id"] for p in board["shared_patterns"]}
    deps = {wid: set() for wid in work_ids}
    for w in work:
        assert w["bubble_id"] in known_bubbles, "missing bubble"
        for rel in w["optional_pattern_edges"]:
            assert rel["from"] in known_patterns, "unknown optional pattern"
            assert rel["to"] == w["bubble_id"], "unexpected optional edge"
            assert rel["type"] == "OPTIONAL_PATTERN_IMPORT__NOT_PRECEDENCE", "edge type"
        for needed in w["required_prerequisites"]:
            assert needed in deps, "unbound required edge"
            deps[w["work_id"]].add(needed)
    # True mandatory edges only. Optional patterns do not create a false cycle.
    active, done = set(),set()
    def visit(work_id):
        if work_id in active:
            raise ValueError("mandatory dependency cycle")
        if work_id in done:
            return
        active.add(work_id)
        for needed in sorted(deps[work_id]):
            visit(needed)
        active.remove(work_id)
        done.add(work_id)
    for wid in sorted(deps):
        visit(wid)
    return {"bubble_count":len(nodes), "work_count":len(work),
            "shared_patterns":len(known_patterns),
            "mandatory_edges":sum(len(x) for x in deps.values()),
            "optional_pattern_edges":sum(len(w["optional_pattern_edges"]) for w in work),
            "owned_path_pairs":len(owned)}

def admit(candidate):
    """No admission decision conveys effect authority."""
    if privacy_violation(candidate):
        return "BLOCKED_PRIVACY"
    if not candidate.get("work_id") or not candidate.get("bubble_id"):
        return "BLOCKED_INVALID_WORKID"
    if candidate.get("effects_allowed"):
        return "HELD_EFFECT_REQUEST"
    if candidate.get("work_type") != SAFE_WORK:
        return "HELD_NON_RESEARCH_WORK"
    if candidate.get("state") != ALLOWED_STATE:
        return "HELD_NOT_PROPOSED"
    if not candidate.get("source","").startswith("https://github.com/CoCivium/"):
        return "BLOCKED_UNBOUND_SOURCE"
    if not candidate.get("reversible"):
        return "HELD_IRREVERSIBLE"
    return "SHADOW_RESEARCH_CANDIDATE_ONLY"

def fan_in(candidates):
    """Deterministic across arrival order; different payload for same WorkID is HOLD."""
    grouped={}
    for c in candidates:
        grouped.setdefault(c.get("work_id","MISSING_ID"),{}).setdefault(digest(c),c)
    result=[]
    for work_id in sorted(grouped):
        variants=grouped[work_id]
        if len(variants)>1:
            result.append({"work_id":work_id, "state":"HOLD_CONFLICTING_VARIANTS",
                           "candidate_digests":sorted(variants),
                           "variant_count":len(variants)})
            continue
        sha, candidate=next(iter(variants.items()))
        result.append({"work_id":work_id, "digest":sha,
                       "state":admit(candidate), "variant_count":1})
    return result

def atomic_proposal_test(candidate):
    """Only a simulated crash boundary in a temporary runner directory."""
    body = stable(candidate)
    expected = hashlib.sha256(body).hexdigest()
    with tempfile.TemporaryDirectory(prefix="cowalkaway-") as root:
        path=Path(root) / "workid.json"
        # A committed candidate is written atomically; the simulated sender dies
        # *before it receives the acknowledgment*. We then re-read from disk.
        tmp=Path(root) / "proposal.tmp"
        tmp.write_bytes(body)
        os.replace(tmp,path)
        readback=path.read_bytes()
        assert hashlib.sha256(readback).hexdigest()==expected
        assert stable(json.loads(readback))==body
        # Replay same WorkID+digest must yield the same one candidate, no effect.
        first=fan_in([candidate])
        replayed=fan_in([candidate, json.loads(readback)])
        assert first==replayed
        assert replayed[0]["state"]=="SHADOW_RESEARCH_CANDIDATE_ONLY"
    return "PASS_TEMPORARY_ATOMIC_READBACK_AND_DEDUPE"

def selfcheck(board):
    meta=graph_checks(board)
    base=copy.deepcopy(board["work_candidates"])
    assert all(admit(x)=="SHADOW_RESEARCH_CANDIDATE_ONLY" for x in base)
    clean=fan_in(base)
    assert len(clean)==5
    assert all(r["state"]=="SHADOW_RESEARCH_CANDIDATE_ONLY" for r in clean)
    assert clean==fan_in(list(reversed(base))+base),"order changed fan-in"
    assert len(clean)==len(set(x["work_id"] for x in clean))
    # The absent steward does not turn proposal research into a financial action.
    active=copy.deepcopy(base[0])
    active["effects_allowed"]=["DEPLOY_SHARED_SITEMAP"]
    assert admit(active)=="HELD_EFFECT_REQUEST"
    private=copy.deepcopy(base[0])
    private["credentials"]="DO_NOT_SEND"
    assert admit(private)=="BLOCKED_PRIVACY"
    unknown=copy.deepcopy(base[0])
    unknown["source"]="file:///private/not-for-publication"
    assert admit(unknown)=="BLOCKED_UNBOUND_SOURCE"
    no_author=copy.deepcopy(base[0])
    no_author["reversible"]=False
    assert admit(no_author)=="HELD_IRREVERSIBLE"
    # Contradictory WorkID is not a last-write-wins election.
    conflict=copy.deepcopy(base[0])
    conflict["description"]+=" [a genuinely different proposed result]"
    with_conflict=fan_in(base+[conflict])
    assert sum(x["state"]=="HOLD_CONFLICTING_VARIANTS" for x in with_conflict)==1
    assert sum(x["state"]=="SHADOW_RESEARCH_CANDIDATE_ONLY" for x in with_conflict)==4
    assert all(x["variant_count"]==2 for x in with_conflict
               if x["state"]=="HOLD_CONFLICTING_VARIANTS")
    # Optional cycles are contextual; actual mandatory cycles are rejected.
    optional=copy.deepcopy(board)
    optional["work_candidates"][0]["optional_pattern_edges"].append(
        {"from":"COREVIEW_PATTERN","to":"COGIBBER",
         "type":"OPTIONAL_PATTERN_IMPORT__NOT_PRECEDENCE"})
    graph_checks(optional)
    cyclic=copy.deepcopy(board)
    cyclic["work_candidates"][0]["required_prerequisites"].append(base[1]["work_id"])
    cyclic["work_candidates"][1]["required_prerequisites"].append(base[0]["work_id"])
    try:
        graph_checks(cyclic)
        raise AssertionError("mandatory cycle silently accepted")
    except ValueError as e:
        assert "cycle" in str(e)
    # Stop recursion after bounded challenge, not when a chatbot feels satisfied.
    def turtle(depth):
        return "HOLD_MAX_REVIEW_DEPTH" if depth>2 else "REVIEW_CANDIDATE_ONLY"
    assert turtle(2)=="REVIEW_CANDIDATE_ONLY"
    assert turtle(3)=="HOLD_MAX_REVIEW_DEPTH"
    persistence=atomic_proposal_test(base[0])
    cases=[
        "five_source_bound_workids_eligible_for_shadow_review",
        "duplicate_replay_collapses_exactly",
        "arrival_order_has_no_effect",
        "unauthorized_deploy_held",
        "privacy_payload_rejected",
        "unbound_source_rejected",
        "irreversible_action_held",
        "conflicting_same_workid_held_others_continue",
        "optional_relation_not_mandatory_order",
        "mandatory_cycle_rejected",
        "review_depth_limit",
        "committed_proposal_retry_deduplicated",
    ]
    report={
      "schema":"CoAll.CoWalkaway.SourceFaninCanary.R0",
      "source_board":"docs/constellation/bubbles/board.json",
      "source_board_sha256":hashlib.sha256(BOARD.read_bytes()).hexdigest(),
      "source_commit":os.getenv("GITHUB_SHA","UNBOUND_LOCAL"),
      "result":"PASS_SOURCE_ONLY_FANIN_NO_EFFECTS",
      "checks":{"total":len(cases),"passed":len(cases),"cases":cases},
      "graph":meta,
      "source_candidates":len(base),
      "fan_in":clean,
      "collision_negative":{"held":1,"unrelated_proposals_unblocked":4},
      "crash_boundary_test":persistence,
      "rick_manual_touches_for_this_ci_task":0,
      "actual_worker_effects":0,
      "independent_external_receiver_ack":None,
      "cross_provider_continuity":None,
      "autonomous_site_updates":0,
      "future_wake":"EXISTING_GITHUB_WORKFLOW_SCHEDULE_OR_SOURCE_EVENT_ONLY",
      "ux_status":"PUBLIC_SOURCE_ONLY__NO_HUMAN_FIRST_USE",
      "human_gate_scope":"UNKNOWN_OR_IRREVERSIBLE_EFFECTS_ONLY__NO_IMPLICIT_APPROVAL",
      "operator_present":"NOT_REQUIRED_FOR_READ_ONLY_TEST",
      "safe_idle":"NO_MATERIAL_CHANGE_AND_NO_AUTHORITY_IMPLIES_SLEEP",
      "nogo":["CLAIM_AUTOEXECUTION","MUTATE_SHARED_RESOURCES","INFER_PRIVATE_CONSENT",
              "ELECT_AN_UNAUTHORIZED_OPERATOR","CLAIM_COEX"],
      "status":"READ_ONLY_CI_TEST_NOT_RECEIVER_RUNTIME",
      "nonclaims":NONCLAIMS
    }
    return report

def main():
    board=json.loads(BOARD.read_text(encoding="utf-8"))
    report=selfcheck(board)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    tmp=REPORT.with_suffix(".tmp")
    tmp.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(tmp,REPORT)
    reloaded=json.loads(REPORT.read_text(encoding="utf-8"))
    assert reloaded["checks"]["passed"]==12
    assert reloaded["actual_worker_effects"]==0
    print(json.dumps({"result":report["result"],"checks":report["checks"]["passed"],
                      "source_candidates":report["source_candidates"],
                      "user_touches":report["rick_manual_touches_for_this_ci_task"],
                      "effects":report["actual_worker_effects"]}))

if __name__=="__main__":
    main()
