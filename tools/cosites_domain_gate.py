#!/usr/bin/env python3
"""Read-only public-branded-domain gate observer. Never mutates DNS or logs credentials."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import ssl
import sys
import time
from urllib import error, parse, request

# Fixed public allowlist only. No account URLs, private nodes, tracking or user-provided hosts.
TARGETS = (
    ("copolitic_apex", "https://copolitic.org/", "copolitic.org", "CoPolitic"),
    ("copolitic_www", "https://www.copolitic.org/", "copolitic.org", "CoPolitic"),
    ("costonk_org", "https://costonk.org/", "costonk.org", "CoStonk"),
    ("costonk_com", "https://costonk.com/", "costonk.org", "CoStonk"),
    ("groupbuild_org", "https://groupbuild.org/", "groupbuild.org", "GroupBuild"),
    ("cogbx_org", "https://cogbx.org/", "cogbx.org", "CoGbx"),
)
MAX_BODY = 320_000
USER_AGENT = "CoCiviumPublicDomainGateReadback/0.1"
_ALLOWED_REDIRECT_HOSTS = {
    "copolitic_apex": {"copolitic.org", "www.copolitic.org", "cocivium.github.io"},
    "copolitic_www": {"copolitic.org", "www.copolitic.org", "cocivium.github.io"},
    "costonk_org": {"costonk.org"},
    "costonk_com": {"costonk.com", "costonk.org"},
    "groupbuild_org": {"groupbuild.org", "www.groupbuild.org"},
    "cogbx_org": {"cogbx.org", "www.cogbx.org"},
}

class StrictPublicRedirect(request.HTTPRedirectHandler):
    def __init__(self, allowed):
        super().__init__()
        self.allowed = allowed

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        u = parse.urlsplit(newurl)
        if u.scheme != "https" or u.hostname not in self.allowed:
            raise ValueError("REDIRECT_OUTSIDE_HTTPS_HOST_ALLOWLIST")
        # Bound the external CoPolitic destination to one project root, not GitHub Pages generally.
        if u.hostname == "cocivium.github.io" and (u.path != "/CoPolitic-site/" or u.query or u.fragment):
            raise ValueError("REDIRECT_OUTSIDE_COPOLITIC_PAGES_PROJECT_ROOT")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def classify(http, body, final_host, expected_host, marker, name):
    """States are observations; no state grants domain ownership or user acceptance."""
    if http == 404:
        return "BRANDED_HTTP_404"
    if http == 525:
        return "CLOUDFLARE_ORIGIN_TLS_525"
    if http is None:
        return "INCONCLUSIVE_TRANSPORT"
    if http != 200:
        return "NON_200_HTTP_" + str(http)
    text = body[:MAX_BODY].decode("utf-8", "replace")
    park = bool(re.search(
        r"GoDaddy|Afternic|is parked|Related Search Topics|/lander|domain (?:is )?for sale",
        text, re.I,
    ))
    if park:
        return "PARKED_NOT_PUBLIC_SITE"
    if final_host != expected_host:
        if name in ("copolitic_apex", "copolitic_www") and final_host == "cocivium.github.io":
            return "COPOLITIC_PAGES_REDIRECT_CONTENT_CANDIDATE_NOT_OWNER_PROOF"
        return "REDIRECT_TARGET_NOT_QUALIFIED"
    if marker.lower() in text.lower() and len(text) >= 200:
        # A source marker may be spoofed, so this is deliberately only a candidate.
        if name == "costonk_com":
            return "REDIRECT_TARGET_CONTENT_CANDIDATE_NOT_OWNER_PROOF"
        return "HUMAN_CONTENT_CANDIDATE_NOT_OWNER_PROOF"
    return "HTTP_200_UNQUALIFIED_CONTENT"


def read_one(target, timeout=8):
    name, url, expect_host, marker = target
    before = time.monotonic()
    result = {
        "id": name, "root": url, "http": None, "final_url": None,
        "state": "INCONCLUSIVE_TRANSPORT", "error_class": None,
        "bytes_examined": 0, "domain_owner_verified": False,
        "certificate_validation_disabled": False, "site_maturity_verified": False,
    }
    opener = request.build_opener(StrictPublicRedirect(_ALLOWED_REDIRECT_HOSTS[name]),
                                  request.HTTPSHandler(context=ssl.create_default_context()))
    try:
        req = request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
        with opener.open(req, timeout=timeout) as response:
            body = response.read(MAX_BODY + 1)
            host = parse.urlsplit(response.geturl()).hostname
            result.update(http=response.status, final_url=response.geturl(),
                          bytes_examined=len(body),
                          state=classify(response.status, body, host, expect_host, marker, name))
            if len(body) > MAX_BODY:
                result["state"] = "RESPONSE_TOO_LARGE_UNQUALIFIED"
    except error.HTTPError as exc:
        result.update(http=exc.code, state=classify(exc.code, b"", None, expect_host, marker, name),
                      final_url=url, error_class="HTTPError")
    except ValueError as exc:
        result.update(state="REDIRECT_OUT_OF_SCOPE", error_class=str(exc)[:100])
    except (error.URLError, TimeoutError, OSError, ssl.SSLError) as exc:
        r = repr(getattr(exc, "reason", exc))
        is_tls = any(x in r.upper() for x in ("CERTIFICATE_VERIFY_FAILED", "WRONG_PRINCIPAL", "HOSTNAME MISMATCH", "SSLCERTVERIFICATIONERROR"))
        result.update(state="TLS_CERTIFICATE_HOLD" if is_tls else "INCONCLUSIVE_TRANSPORT",
                      error_class=type(exc).__name__)
    result["elapsed_ms"] = int((time.monotonic() - before) * 1000)
    return result


def selftest():
    assert len(TARGETS) == 6
    assert len({t[0] for t in TARGETS}) == 6
    assert all(parse.urlsplit(t[1]).scheme == "https" for t in TARGETS)
    assert all(set(_ALLOWED_REDIRECT_HOSTS[t[0]]) for t in TARGETS)
    assert classify(404, b"", None, "copolitic.org", "CoPolitic", "copolitic_apex") == "BRANDED_HTTP_404"
    assert classify(525, b"", None, "cogbx.org", "CoGbx", "cogbx_org") == "CLOUDFLARE_ORIGIN_TLS_525"
    assert classify(200, b"<title>GoDaddy</title> /lander", "costonk.org", "costonk.org", "CoStonk", "costonk_org") == "PARKED_NOT_PUBLIC_SITE"
    assert classify(200, b"<h1>CoPolitic</h1>" + b" content" * 100, "copolitic.org", "copolitic.org", "CoPolitic", "copolitic_apex") == "HUMAN_CONTENT_CANDIDATE_NOT_OWNER_PROOF"
    assert classify(200, b"<h1>CoStonk</h1>" + b" content" * 100, "costonk.org", "costonk.org", "CoStonk", "costonk_com") == "REDIRECT_TARGET_CONTENT_CANDIDATE_NOT_OWNER_PROOF"
    assert classify(200, b"some html" * 100, "costonk.com", "costonk.org", "CoStonk", "costonk_com") == "REDIRECT_TARGET_NOT_QUALIFIED"
    assert classify(None, b"", None, "copolitic.org", "CoPolitic", "copolitic_apex") == "INCONCLUSIVE_TRANSPORT"
    assert classify(200, b"<h1>CoPolitic</h1>" + b" content" * 100, "cocivium.github.io", "copolitic.org", "CoPolitic", "copolitic_apex") == "COPOLITIC_PAGES_REDIRECT_CONTENT_CANDIDATE_NOT_OWNER_PROOF"
    handler = StrictPublicRedirect(_ALLOWED_REDIRECT_HOSTS["copolitic_apex"])
    origin = request.Request("https://copolitic.org/")
    assert handler.redirect_request(origin, None, 302, "Found", {}, "https://cocivium.github.io/CoPolitic-site/") is not None
    for disallowed in ("https://cocivium.github.io/other/", "http://cocivium.github.io/CoPolitic-site/", "https://cocivium.github.io/CoPolitic-site/?q=1"):
        try:
            handler.redirect_request(origin, None, 302, "Found", {}, disallowed)
        except ValueError:
            pass
        else:
            raise AssertionError("UNSAFE_REDIRECT_ACCEPTED")
    assert not any(t[1].startswith("http://") for t in TARGETS)
    print("PASS_DOMAIN_GATE_EIGHT_NEGATIVE_AND_POSITIVE_FIXTURES")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--output", default="cosites-domain-gate-readback.json")
    ap.add_argument("--summary", default="")
    args = ap.parse_args()
    selftest()
    if args.selftest:
        return 0
    readings = [read_one(t) for t in TARGETS]
    report = {
        "schema": "CoSites.PublicBrandedDomainGateObservation.R0",
        "checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_commit": os.getenv("GITHUB_SHA", "LOCAL_READ_ONLY"),
        "runner": "GITHUB_ACTIONS" if os.getenv("GITHUB_ACTIONS") else "EXPLICIT_LOCAL",
        "scope": "Six fixed public HTTPS entrypoints; no private nodes, no registrar or other-account API",
        "states": readings,
        "ready_verified": 0,  # No owner / independent human acceptance was checked.
        "no_claims": [
            "OBSERVED_HTTP_NE_DOMAIN_OWNERSHIP", "HTTP_200_NE_MATURE_PRODUCT",
            "DOMAIN_GATE_RUN_NE_DOMAIN_REPAIR", "COSTONK_IS_NOT_A_VERIFIED_FINANCIAL_SERVICE",
            "NO_PUBLIC_TLD_NODE", "GITHUB_RUNNER_NE_INDEPENDENT_PROVIDER",
            "NO_SECRETS_COOKIES_OR_CREDENTIALS", "NO_BACKGROUND_SELF_REPAIR",
        ],
    }
    pathlib.Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.summary:
        with pathlib.Path(args.summary).open("a", encoding="utf-8") as fp:
            fp.write("## CoSites six-domain branded-gate observation\n\n")
            fp.write("Observed at: " + report["checked_utc"] + " (single GitHub runner; not account or DNS authority).\n\n")
            fp.write("| Name | HTTP | Observation |\n| --- | --- | --- |\n")
            for item in readings:
                fp.write("| " + item["id"] + " | " + str(item["http"] or "unknown")
                         + " | " + item["state"] + " |\n")
            fp.write("\nA successful workflow is **not** a branded-domain PASS. Static snapshots cannot repair DNS or TLS.\n")
    print(json.dumps({"states": {x["id"]: x["state"] for x in readings},
                      "count": len(readings), "receipt": args.output}, separators=(",", ":")))
    # Known domain holds are observation outcomes, not failed tests of the observer.
    return 0


if __name__ == "__main__":
    sys.exit(main())
