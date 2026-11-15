#!/usr/bin/env python3
"""CoPatterna source-only grammar validator. No sockets, model, writes outside CI receipt.

Checks source-linked pattern families, bounded case selection, embedded human/machine
data parity and deliberately invalid mutations. Does not execute an operator.
"""
from __future__ import annotations
import copy
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/"docs/constellation/patterns/registry.json"
PAGE=ROOT/"docs/constellation/patterns/index.html"
REPORT=ROOT/".ci/patterns/registry-proof.json"
EXPECTED_CASES={
  "missing_ack":"HOLD_RECEIVER_ACK_UNKNOWN",
  "duplicate_work":"NOOP_EXACT_REPLAY",
  "source_changed":"HOLD_SOURCE_CONFLICT",
  "two_writers":"HOLD_ELECTED_WRITER",
  "provider_down":"HOLD_SECOND_HOST_PROOF",
  "no_delta":"QUIESCE_NO_EFFECT",
  "visitor_confused":"HOLD_HUMAN_ACCEPTANCE",
  "too_many_branches":"BOUND_TO_ONE_CANARY",
}
REQUIRED_NEGATIVE={
  "UNKNOWN_NE_ACK","DUPLICATE_NE_SECOND_EFFECT","SOURCE_DRIFT_NE_UPDATE",
  "DUPLICATE_WRITER_NE_LAST_WRITE_WINS","NO_DELTA_NE_WORK","G_DSIDE_NE_AUTHORITY"
}

class EmbeddedParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.active=False
        self.chunks=[]
        self.matches=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="script" and d.get("id")=="patternSource":
            if self.matches: raise AssertionError("duplicate script ID")
            if d.get("type")!="application/json": raise AssertionError("unsafe embedding type")
            self.matches+=1
            self.active=True
    def handle_data(self,data):
        if self.active:self.chunks.append(data)
    def handle_endtag(self,tag):
        if tag=="script" and self.active:self.active=False

def check(reg):
    if reg.get("schema")!="CoAll.CoPatterna.LazyRelationalTestRegistry.R0":
        raise AssertionError("registry schema mismatch")
    families=reg.get("families",[])
    patterns=reg.get("patterns",[])
    cases=reg.get("cases",[])
    if (len(families),len(patterns),len(cases))!=(7,28,8):
        raise AssertionError("unbounded family/pattern/case scope")
    ids=[x["id"] for x in patterns]
    fids=[x["id"] for x in families]
    cids=[x["id"] for x in cases]
    if any(len(xs)!=len(set(xs)) for xs in (ids,fids,cids)):
        raise AssertionError("duplicate id")
    if set(cids)!=set(EXPECTED_CASES):
        raise AssertionError("different scenario set")
    if reg["selection"]["generate_all_combinations"] is not False:
        raise AssertionError("unbounded eager generation")
    if reg["selection"]["operators_per_case"]!=4 or reg["selection"]["max_turtle_depth"]!=2:
        raise AssertionError("changed resource envelope")
    if reg["selection"]["active_case_max"]!=1:
        raise AssertionError("multiple active scenarios allowed")
    if not REQUIRED_NEGATIVE.issubset(set(reg["selection"]["required_negative_controls"])):
        raise AssertionError("required negative case omitted")
    for p in patterns:
        if p["family"] not in fids:
            raise AssertionError("unknown family")
        if p["effect_authority"]!="NONE":
            raise AssertionError("operator self-authorized")
        if p["privacy"]!="PUBLIC_SAFE_EXEMPLAR":
            raise AssertionError("privacy not fenced")
        if not p["source_ref"].startswith(
            "https://github.com/CoCivium/CoCivium/blob/main/"):
            raise AssertionError("unsupported source authority")
        for key in ("label","plain","probe","boundary"):
            if not isinstance(p[key],str) or len(p[key])<6:
                raise AssertionError("empty/meaningless operator")
    for c in cases:
        if c["expected_state"]!=EXPECTED_CASES[c["id"]]:
            raise AssertionError("case state overwritten")
        if c["external_effects"]!=0:
            raise AssertionError("scenario claims an effect")
        if len(c["operators"])!=4 or len(set(c["operators"]))!=4:
            raise AssertionError("scenario not bounded")
        if not all(p in ids for p in c["operators"]):
            raise AssertionError("unknown operator")
        if len(c["next_safe"])<20 or len(c["blocked"])<20:
            raise AssertionError("case without rails")
    return {"family_count":len(families),"pattern_count":len(patterns),
            "case_count":len(cases),"suggestions_if_each_selected":sum(len(c["operators"]) for c in cases),
            "simultaneously_active_cases":1,"effect_authority_granted":0}

def negatives(reg):
    failures={}
    def must_reject(name,mutate):
        bad=copy.deepcopy(reg)
        mutate(bad)
        try:check(bad)
        except (AssertionError,KeyError,TypeError,ValueError):
            failures[name]="PASS_MUTATION_REJECTED"
        else:raise AssertionError("negative case silently accepted: "+name)
    must_reject("UNKNOWN_CANNOT_BECOME_ACK",lambda d:d["cases"][0].update(expected_state="ACKNOWLEDGED"))
    must_reject("DUPLICATE_CANNOT_CREATE_SECOND_EFFECT",lambda d:d["cases"][1].update(external_effects=1))
    must_reject("SOURCE_DRIFT_CANNOT_SILENTLY_UPDATE",lambda d:d["cases"][2].update(expected_state="SUCCESS"))
    must_reject("SPLIT_WRITER_CANNOT_AUTOGRANT",lambda d:d["patterns"][10].update(effect_authority="DEPLOY"))
    must_reject("OPTIONAL_RELATIONS_CANNOT_ACTIVATE_ALL",lambda d:d["selection"].update(generate_all_combinations=True))
    must_reject("REVIEW_CANNOT_TURTLE_INDEFINITELY",lambda d:d["selection"].update(max_turtle_depth=10))
    must_reject("UNKNOWN_PATTERN_CANNOT_BE_SELECTED",lambda d:d["cases"][7]["operators"].__setitem__(0,"NEW_UNVERIFIED_OPERATOR"))
    must_reject("PUBLIC_PATTERN_CANNOT_LINK_PRIVATE_SOURCE",lambda d:d["patterns"][2].update(source_ref="file:///private/source"))
    must_reject("OPERATOR_IDS_MUST_BE_UNIQUE",lambda d:d["patterns"][1].update(id=d["patterns"][0]["id"]))
    must_reject("HUMAN_PRIORITY_CANNOT_DROP_NO_DELTA",lambda d:d["cases"].pop(5))
    return failures

def main():
    raw=DATA.read_bytes()
    reg=json.loads(raw)
    stats=check(reg)
    negative=negatives(reg)
    parser=EmbeddedParser()
    html=PAGE.read_text(encoding="utf-8")
    parser.feed(html)
    if parser.matches!=1 or not parser.chunks:
        raise AssertionError("embedded pattern source missing")
    embedded=json.loads("".join(parser.chunks))
    for k in ("schema","patterns","cases","families"):
        if embedded[k]!=reg[k]:
            raise AssertionError("human/machine JSON source diverged: "+k)
    if "aria-pressed" not in html or "prefers-reduced-motion:reduce" not in html:
        raise AssertionError("basic UX boundaries missing")
    if "<form" in html or "localStorage" in html or "new WebSocket" in html:
        raise AssertionError("unexpected interaction/input mechanism")
    if html.count('class="selected-card"')!=4:
        raise AssertionError("initial four static fallback cards missing")
    receipt={
      "schema":"CoPatterna.SourceRegistryCanary.R0",
      "source_commit":os.getenv("GITHUB_SHA","UNBOUND_SOURCE"),
      "source_registry":"docs/constellation/patterns/registry.json",
      "registry_sha256":hashlib.sha256(raw).hexdigest(),
      "human_page":"docs/constellation/patterns/index.html",
      "human_page_sha256":hashlib.sha256(PAGE.read_bytes()).hexdigest(),
      "result":"PASS_SCOPED_SOURCE_PATTERNS",
      "scope":stats,
      "negative_controls":negative,
      "negative_count":len(negative),
      "human_machine_embedded_source_parity":True,
      "external_effects":0,
      "actual_receiver_ack":False,
      "real_pattern_automation":False,
      "independent_human_acceptance":False,
      "nonclaims":[
        "SOURCE_REGISTRY_NE_NEW_COTERMS","PATTERN_IDEAS_NE_EXECUTABLE_WORKERS",
        "METAMORPHIC_FIXTURE_NE_EXTERNAL_EFFECT","SOURCE_PARITY_NE_HUMAN_COMPREHENSION",
        "NO_COEX_CANON_RUNTIME","NO_INDEPENDENT_COOWNEDWORK_RECEIVER_ACK"
      ]
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    again=json.loads(REPORT.read_text(encoding="utf-8"))
    assert again["result"]=="PASS_SCOPED_SOURCE_PATTERNS"
    print(json.dumps({"result":receipt["result"],"families":stats["family_count"],
      "operators":stats["pattern_count"],"scenarios":stats["case_count"],
      "negative_tests":receipt["negative_count"],"human_machine_parity":True}))

if __name__=="__main__":
    main()
