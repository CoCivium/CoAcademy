#!/usr/bin/env python3
"""CoFirstUse+ R0: source inspection and opt-in, narrow public front-door probes.

Does not collect visitors, download project indexes, call analytics or mutate sites.
Zero external dependencies. Source mode is deterministic; live mode is observational.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPSHandler, HTTPRedirectHandler

SOURCES = {
    "cocivium-home": "docs/index.html",
    "living-world": "docs/experience/index.html",
    "beaxa-kit": "docs/kitten/index.html",
    "about": "docs/about/index.html",
    "groupbuild": "docs/groupbuild/index.html",
}
LIVE_URLS = {
    "cocivium-home": "https://cocivium.github.io/CoAcademy/",
    "living-world": "https://cocivium.github.io/CoAcademy/experience/",
    "beaxa-kit": "https://cocivium.github.io/CoAcademy/kitten/",
    "about": "https://cocivium.github.io/CoAcademy/about/",
    "groupbuild": "https://cocivium.github.io/CoAcademy/groupbuild/",
    "cocivium-apex": "https://cocivium.org/",
    "cocivium-www": "https://www.cocivium.org/",
}


class PageScanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = set()
        self.links = []
        self.script_sources = []
        self.headings = []
        self.in_heading = False
        self.viewport = False
        self.buttons = 0
        self.forms = 0
        self.h1 = 0
        self.image_alt_missing = 0
        self.canvas_fallbacks = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.add(tag)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "script" and attrs.get("src"):
            self.script_sources.append(attrs["src"])
        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.viewport = bool(attrs.get("content"))
        if tag == "h1":
            self.h1 += 1
        if tag == "button":
            self.buttons += 1
        if tag == "form":
            self.forms += 1
        if tag == "img" and not attrs.get("alt"):
            self.image_alt_missing += 1


def analyze_source(src, identifier, relpath):
    h = hashlib.sha256(src.encode("utf-8")).hexdigest()
    parser = PageScanner()
    parser.feed(src)
    external_scripts = [s for s in parser.script_sources if s.startswith(("https://", "http://"))]
    unique = set(parser.links)
    duplicates = sorted({p for p in unique if parser.links.count(p) > 1})
    internal = [p for p in parser.links if not p.startswith(("http://", "https://", "mailto:"))]
    first_use = any(p for p in internal if not p.startswith("#")) or bool(parser.buttons)
    flags = {
        "html": bool(re.search(r"<!doctype html>", src, re.I)),
        "viewport": parser.viewport,
        "one_h1": parser.h1 == 1,
        "visual_surface": bool(re.search(r"<svg\b|<canvas\b|radial-gradient|linear-gradient", src, re.I)),
        "navigation_or_task": first_use,
        "keyboard_focus_css": ":focus-visible" in src,
        "reduced_motion_css": "prefers-reduced-motion" in src,
        "limitations_disclosed": bool(re.search(r"prototype|preview|research|experiment|not a live|not a functioning|not immersive", src, re.I)),
        "no_external_script_src": len(external_scripts) == 0,
        "all_img_have_alt": parser.image_alt_missing == 0,
    }
    return {
        "id": identifier,
        "path": relpath,
        "source_sha256": h,
        "source_checks": flags,
        "source_checks_passed": sum(flags.values()),
        "source_checks_total": len(flags),
        "links_total": len(parser.links),
        "links_unique": len(unique),
        "duplicate_href_values": duplicates[:10],
        "interactive_buttons": parser.buttons,
        "external_script_count": len(external_scripts),
        "live_http": "NOT_TESTED_BY_SOURCE_MODE",
        "real_person_outcome": "UNVERIFIED",
        "device_accessibility": "UNVERIFIED",
    }


class NoRedirectHandler(HTTPRedirectHandler):
    """Reject redirects so live probes cannot leave their allowlisted URL."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def inspect_live(identifier, url):
    # Request ONLY the allowlisted landing document. Never follow its internal links,
    # consume shards, inspect private data, or persist response bodies.
    req = Request(url, headers={"User-Agent": "CoFirstUse-R0-ReadOnly/0.1", "Accept": "text/html"})
    try:
        opener = build_opener(HTTPSHandler(context=ssl.create_default_context()), NoRedirectHandler())
        with opener.open(req, timeout=8) as res:
            result = {"id": identifier, "url": url, "status": int(res.status), "final_url": res.geturl(), "content_type": (res.headers.get("Content-Type") or "").split(";")[0], "observation": "ONE_VANTAGE_ONLY"}
            res.read(0)
            return result
    except HTTPError as exc:
        return {"id": identifier, "url": url, "status": exc.code, "observation": "REDIRECT_NOT_FOLLOWED" if exc.code in (301, 302, 303, 307, 308) else "ONE_VANTAGE_ONLY"}
    except (URLError, TimeoutError, OSError) as exc:
        return {"id": identifier, "url": url, "status": "UNKNOWN", "error_class": exc.__class__.__name__, "observation": "NETWORK_FAILURE_NOT_SITE_FAILURE"}


def run(root, live=False):
    result = {
        "schema": "CoFirstUse.Comparator.R0",
        "epistemic_status": "STATIC_CODE_INSPECTION_WITH_OPTIONAL_ONE_VANTAGE_HTTP",
        "scope": "Specified public landing documents only, no deep crawl, no user data",
        "targets": [],
        "live_checks": [],
        "limits": ["SOURCE_CHECK_NE_BROWSER_USER_ACCEPTANCE", "NO_SECOND_VANTAGE", "NOT_SECURITY_AUDIT", "SCORES_ARE_CHECK_COUNTS_NOT_PRODUCT_QUALITY", "NO_AUTONOMOUS_FIX_OR_PUBLICATION"],
    }
    root = Path(root).resolve()
    for identifier, relpath in SOURCES.items():
        path = root / relpath
        if not path.is_file():
            result["targets"].append({"id": identifier, "path": relpath, "source_status": "MISSING_OR_NOT_MOUNTED"})
            continue
        text = path.read_text(encoding="utf-8")
        result["targets"].append(analyze_source(text, identifier, relpath))
    if live:
        for identifier, url in LIVE_URLS.items():
            result["live_checks"].append(inspect_live(identifier, url))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Checkout root containing docs/")
    parser.add_argument("--live", action="store_true", help="Opt in to read-only HTTP HEAD-like GET of allowlisted landing pages")
    parser.add_argument("--output", help="Write bounded JSON report; refuses overwriting an existing file")
    opts = parser.parse_args()
    report = json.dumps(run(opts.repo_root, opts.live), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if opts.output:
        path = Path(opts.output)
        with path.open("x", encoding="utf-8") as f:
            f.write(report)
        print("Wrote", path)
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
