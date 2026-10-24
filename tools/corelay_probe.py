#!/usr/bin/env python3
"""Public-only CoRelay readproof. Never scans private hosts or accepts dynamic URLs."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib import error, request

TARGETS = (
    ("relay", "https://cocivium.github.io/CoAcademy/relay/", ("Try it. Challenge it. Improve it.", "CoRelay+"), "GITHUB"),
    ("beacon", "https://cocivium.github.io/CoAcademy/relay/beacon.json", ('"schema": "CoRelay.AIBeacon.R1"',), "GITHUB"),
    ("feed", "https://cocivium.github.io/CoAcademy/relay/feed.xml", ('<rss version="2.0"', "CoRelay public source updates"), "GITHUB"),
    ("civic", "https://cocivium.github.io/CoAcademy/civic-integrity/", ("Understand the process.", "Report concerns responsibly."), "GITHUB"),
    ("phoenix", "https://cocivium.github.io/CoAcademy/phoenix/", ("CoPhoenix R0", "26/26", "Wayback"), "GITHUB"),
    ("phoenix_contract", "https://cocivium.github.io/CoAcademy/phoenix/discovery.json", ('"schema": "CoCivium.CoPhoenix.RecoverabilityProduct.R0"', '"public_capsule_hosted": false'), "GITHUB"),
    ("source_fallback", "https://raw.githubusercontent.com/CoCivium/CoAcademy/master/docs/relay/index.html", ("Try it. Challenge it. Improve it.",), "GITHUB"),
)
USER_AGENT = "CoCivium-CoRelay-PublicReadproof/1.0"
LIMIT = 400_000
SOURCE_PATHS = {
    "relay": "docs/relay/index.html",
    "beacon": "docs/relay/beacon.json",
    "feed": "docs/relay/feed.xml",
    "civic": "docs/civic-integrity/index.html",
    "phoenix": "docs/phoenix/index.html",
    "phoenix_contract": "docs/phoenix/discovery.json",
    "source_fallback": "docs/relay/index.html",
}

def verify_source_bytes(name, received, root=Path(".")):
    """Check the actual served public bytes against the checked-out Git source."""
    served_sha = hashlib.sha256(received).hexdigest()
    rel = SOURCE_PATHS.get(name)
    if rel is None:
        return "FAIL", "UNLISTED_TARGET", None, served_sha
    try:
        expected = (root / rel).read_bytes()
    except OSError:
        return "INCONCLUSIVE", "CHECKED_OUT_SOURCE_UNAVAILABLE", None, served_sha
    expected_sha = hashlib.sha256(expected).hexdigest()
    if served_sha != expected_sha:
        return "FAIL", "SOURCE_VERSION_MISMATCH", expected_sha, served_sha
    return "PASS", "SOURCE_SHA256_MATCH", expected_sha, served_sha


def assess_content(status, body, expected):
    if status != 200:
        return "FAIL", "HTTP_STATUS_" + str(status)
    if len(body) > LIMIT:
        return "FAIL", "RESPONSE_EXCEEDS_BOUNDED_LIMIT"
    text = body.decode("utf-8", "replace")
    for marker in expected:
        if marker not in text:
            return "FAIL", "EXPECTED_MARKER_ABSENT"
    return "PASS", "MARKERS_PRESENT"

def probe(target, timeout=9):
    name, url, markers, domain = target
    if not url.startswith("https://") or domain != "GITHUB":
        raise ValueError("Public HTTPS allowlist only")
    req = request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/json,application/xml,text/xml"})
    result = {"id": name, "url": url, "failure_domain": domain, "state": "INCONCLUSIVE", "reason": "NOT_RUN"}
    try:
        with request.urlopen(req, timeout=timeout) as response:
            status = response.getcode()
            payload = response.read(LIMIT + 1)
        result["state"], result["reason"] = assess_content(status, payload, markers)
        result["http_status"] = status
        result["bytes_inspected"] = len(payload)
        if result["state"] == "PASS":
            state, reason, expected_sha, served_sha = verify_source_bytes(name, payload)
            result["state"], result["reason"] = state, reason
            result["expected_source_sha256"] = expected_sha
            result["served_sha256"] = served_sha
    except error.HTTPError as exc:
        result["state"], result["reason"] = "FAIL", "HTTP_STATUS_" + str(exc.code)
        result["http_status"] = exc.code
    except (error.URLError, TimeoutError, OSError) as exc:
        result["state"], result["reason"] = "INCONCLUSIVE", type(exc).__name__
    return result

def classify(checks):
    pages = [p for p in checks if p["id"] != "source_fallback"]
    fallback = next(p for p in checks if p["id"] == "source_fallback")
    if all(p["state"] == "PASS" for p in checks):
        return "PASS_PUBLIC_HTTP_SOURCE_MATCH"
    if all(p["state"] == "PASS" for p in pages):
        return "PAGES_MATCH_BUT_RAW_SOURCE_UNAVAILABLE"
    if fallback["state"] == "PASS":
        return "DEGRADED_WITH_SAME_PROVIDER_SOURCE"
    return "PUBLIC_READPROOF_FAILED_OR_INCONCLUSIVE"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/corelay-readproof.json")
    parser.add_argument("--summary", default="")
    options = parser.parse_args()
    checks = [probe(target) for target in TARGETS]
    state = classify(checks)
    report = {
        "schema": "CoRelay.ExternalHostReadproof.R1",
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_commit": os.getenv("GITHUB_SHA", "UNBOUND_LOCAL_PROBE"),
        "runner": "GitHub Actions" if os.getenv("GITHUB_ACTIONS") else "LOCAL_EXPLICIT_EXECUTION",
        "state": state,
        "readproof": checks,
        "note": "PASS requires every public target to match exact checked-out Git source bytes by SHA-256. GitHub Pages and Raw remain ONE common provider failure domain. HTTP checks are not a full browser, accessibility, real audience, or independent provider restoration test.",
        "never_checked": ["copolitic.org", "copolitic.com", "CoStead", "CoVIA", "CoGateway", "Metricool private profiles", "real election systems"]
    }
    out = Path(options.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if options.summary:
        summary = Path(options.summary)
        with summary.open("a", encoding="utf-8") as fp:
            fp.write("## CoRelay public source readproof\n\n")
            fp.write("Result: **" + state + "**\n\n")
            fp.write("| Target | State | Reason |\n|---|---|---|\n")
            for result in checks:
                fp.write("| " + result["id"] + " | " + result["state"] + " | " + result["reason"] + " |\n")
            fp.write("\nProvider caveat: GitHub Pages and GitHub Raw share a failure domain.\n")
    print(json.dumps({"state": state, "targets": [{"id": x["id"], "state": x["state"]} for x in checks]}))
    return 0 if state == "PASS_PUBLIC_HTTP_SOURCE_MATCH" else 1

if __name__ == "__main__":
    sys.exit(main())
