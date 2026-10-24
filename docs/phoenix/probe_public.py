#!/usr/bin/env python3
"""CoPhoenix R1: fixed, read-only, public HTTP tests. No secrets or user data."""
import datetime
import json
import os
import pathlib
import sys
import time
from urllib import request, parse, error

PAGE="https://cocivium.github.io/CoAcademy/"
RAW="https://raw.githubusercontent.com/CoCivium/CoAcademy/master/docs/"
TARGETS=[
 ("relay","relay/","relay/index.html","Try it. Challenge it. Improve it."),
 ("phoenix","phoenix/","phoenix/index.html","CoPhoenix R0"),
 ("observer","relay/observer-map/","relay/observer-map/index.html","Who can see what?"),
 ("civic","civic-integrity/","civic-integrity/index.html","Understand the process."),
 ("satire","coplay/votes-for-sale/","coplay/votes-for-sale/index.html","VOTES FOR SALE?"),
]
OUT="co_phoenix_public_readproof.json"

def classify(a,b):
 if a=="PASS" and b=="PASS": return "PAGES_AND_RAW_PASS_GITHUB_ONLY"
 if a=="PASS": return "PAGES_PASS_RAW_UNVERIFIED"
 if a=="FAIL" and b=="PASS": return "PAGES_DEGRADED_RAW_AVAILABLE_SAME_VENDOR"
 if a=="FAIL": return "PAGES_FAIL_REVIEW"
 if b=="PASS": return "PAGES_INCONCLUSIVE_RAW_AVAILABLE_SAME_VENDOR"
 return "INCONCLUSIVE"

def probe(url,host,marker):
 start=time.monotonic()
 r={"status":"INCONCLUSIVE","http":None,"marker":False,"error":None}
 try:
  req=request.Request(url,headers={"User-Agent":"CoPhoenixPublicReadproof/1.0"})
  with request.urlopen(req,timeout=7) as response:
   r["http"]=response.status
   final=parse.urlsplit(response.geturl())
   body=response.read(400001)
   if final.scheme!="https" or final.hostname!=host:
    r.update(status="FAIL",error="REDIRECT_HOST_MISMATCH")
   elif len(body)>400000:
    r.update(status="FAIL",error="OVER_SIZE_LIMIT")
   elif response.status!=200:
    r.update(status="FAIL",error="NON_200")
   elif marker not in body.decode("utf-8",errors="replace"):
    r.update(status="FAIL",error="CONTENT_MARKER_MISSING")
   else: r.update(status="PASS",marker=True)
 except error.HTTPError as ex:
  r.update(status="FAIL",http=ex.code,error="HTTP_ERROR")
 except (error.URLError,TimeoutError,OSError) as ex:
  r.update(status="INCONCLUSIVE",error=type(ex).__name__)
 r["elapsed_ms"]=int((time.monotonic()-start)*1000)
 return r

def selftest():
 assert len(TARGETS)==5
 assert len({r[0] for r in TARGETS})==5
 assert all(row[1].endswith("/") and row[2].endswith("/index.html") for row in TARGETS)
 assert all(".." not in row[1]+row[2] for row in TARGETS)
 assert classify("PASS","PASS")=="PAGES_AND_RAW_PASS_GITHUB_ONLY"
 assert classify("FAIL","PASS")=="PAGES_DEGRADED_RAW_AVAILABLE_SAME_VENDOR"
 assert classify("INCONCLUSIVE","INCONCLUSIVE")=="INCONCLUSIVE"
 print("CoPhoenix allowlist and classification selftest PASS")

def main():
 selftest()
 if "--selftest" in sys.argv: return 0
 readings=[]
 for name,public,source,marker in TARGETS:
  page=probe(PAGE+public,"cocivium.github.io",marker)
  raw=probe(RAW+source,"raw.githubusercontent.com",marker)
  state=classify(page["status"],raw["status"])
  readings.append({"target":name,"page_url":PAGE+public,"raw_url":RAW+source,"page":page,"raw":raw,"classification":state})
  print(name+": "+state,flush=True)
 overall="PAGES_PASS_FROM_GITHUB_RUNNER"
 if any(x["page"]["status"]=="FAIL" for x in readings): overall="PAGE_FAILURE_NEEDS_REVIEW"
 elif any(x["page"]["status"]!="PASS" for x in readings): overall="INCONCLUSIVE_RUNNER_NETWORK"
 report={
  "schema":"CoPhoenix.GitHubRunnerPublicHTTP.R1",
  "checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "commit":os.getenv("GITHUB_SHA"),
  "event":os.getenv("GITHUB_EVENT_NAME","unknown"),
  "overall":overall,
  "scope":"Five fixed public Pages URLs and five Raw files; 7-second timeout each",
  "readings":readings,
  "limits":["Both origins are GitHub; no off-provider recovery is established.",
            "HTTP and expected text do not prove accessibility, AI pickup or actual user benefit.",
            "A workflow schedule does not prove continued monitoring.",
            "A DNS or timeout failure is inconclusive rather than proof that a page is down.",
            "No user accounts, private nodes, election infrastructure or visitor records were inspected."]
 }
 pathlib.Path(OUT).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 print("Overall: "+overall+"; receipt: "+OUT)
 return 1 if overall=="PAGE_FAILURE_NEEDS_REVIEW" else 0

if __name__=="__main__":
 sys.exit(main())
