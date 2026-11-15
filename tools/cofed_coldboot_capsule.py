#!/usr/bin/env python3
"""Deterministic, public-only CoGibber cold-boot capsule.

The result is a candidate portability artifact for offline testing, not
independent-provider recovery, a license grant, or CoAll runtime acceptance.
No external dependencies, network access, credentials, or private files.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".ci" / "coldboot"
ARCHIVE = OUT / "cofed-cogibber-coldboot-r0.zip"
MAPPING = {
    "site/index.html": "docs/cogibber/index.html",
    "site/discovery.json": "docs/cogibber/discovery.json",
    "site/README.md": "docs/cogibber/README.md",
}
NONCLAIMS = [
    "REPRODUCIBLE_ARCHIVE_NE_INDEPENDENT_PROVIDER",
    "LOOPBACK_COLD_BOOT_NE_REMOTE_FAILURE_DOMAIN",
    "LOCAL_FILE_BUNDLE_NE_PUBLIC_RECEIVER_ACK",
    "NO_COCIVIUM_OR_COALL_CANON_RUNTIME",
    "COACADEMY_RIGHTS_NE_BLANKET_RELICENSE",
    "NO_REAL_USER_ACCEPTANCE",
    "NO_CREDENTIALS_NO_NETWORK_NO_DEPLOYMENT",
]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def zipinfo(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    return info

def main() -> None:
    source_commit = os.environ.get("GITHUB_SHA", "UNBOUND_LOCAL_SOURCE")
    if source_commit != "UNBOUND_LOCAL_SOURCE":
        if len(source_commit) != 40 or any(c not in "0123456789abcdef" for c in source_commit.lower()):
            raise SystemExit("HOLD: invalid source commit")
    objects: dict[str, bytes] = {}
    records = []
    for dest, src in sorted(MAPPING.items()):
        full_path = ROOT / src
        if not full_path.is_file():
            raise SystemExit("HOLD: missing source " + src)
        data = full_path.read_bytes()
        if not data:
            raise SystemExit("HOLD: empty source " + src)
        objects[dest] = data
        records.append({
            "bundled_path": dest,
            "source_path": src,
            "sha256": sha(data),
            "bytes": len(data),
        })
    html = objects["site/index.html"].decode("utf-8")
    banned = ('<script src=', '<iframe', '<object', '<embed', 'navigator.sendBeacon(', 'XMLHttpRequest(', 'fetch(')
    if any(token.lower() in html.lower() for token in banned):
        raise SystemExit("HOLD: unexpected potential network/external embed")
    for needed in ("connect-src 'none'", "form-action 'none'", '<form id="inputForm"', 'id="downloadJson"'):
        if needed not in html:
            raise SystemExit("HOLD: HTML boundary or task element missing: " + needed)
    data = json.loads(objects["site/discovery.json"])
    if data.get("schema") != "CoGibber.PublicDiscovery.R0" or data.get("implementation", {}).get("model_calls") is not False:
        raise SystemExit("HOLD: unexpected machine twin")
    manifest = {
        "schema": "CoFed.ColdBootCapsule.R0",
        "edition": "2026-11-15",
        "state": "PUBLIC_OFFLINE_SOURCE_CAPSULE__NOT_INDEPENDENT_HOST_PROOF",
        "source_repository": "CoCivium/CoAcademy",
        "source_commit": source_commit,
        "entrypoint": "site/index.html",
        "machine_companion": "site/discovery.json",
        "files": records,
        "licenses": "CoAcademy root license audit incomplete. Packaging for source review/testing is not a new license grant.",
        "runtime": "Any static HTTPS or local loopback server; no model, database, service worker or remote API required for first task",
        "authority": "READ_AND_LOCAL_EDIT_ONLY__ZERO_EXTERNAL_EFFECTS",
        "limits": "One task copied from a public repo, not a whole site or independent second-provider recovery",
        "nonclaims": NONCLAIMS,
    }
    objects["manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    objects["SHA256SUMS"] = "".join(
        f"{sha(body)}  {name}\n" for name, body in sorted(objects.items())
    ).encode("ascii")
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, mode="w") as archive:
        for name, body in sorted(objects.items()):
            archive.writestr(zipinfo(name), body)
    result = {
        "schema": "CoFed.CapsuleBuildReceipt.R0",
        "source_commit": source_commit,
        "archive_path": str(ARCHIVE.relative_to(ROOT)),
        "archive_sha256": sha(ARCHIVE.read_bytes()),
        "archive_bytes": ARCHIVE.stat().st_size,
        "payload_file_count": len(MAPPING),
        "report": "BUILT_NOT_BOOTED",
        "nonclaims": NONCLAIMS,
    }
    (OUT / "build-receipt.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("archive_sha256", "archive_bytes", "payload_file_count", "report")}))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        sys.exit("HOLD: " + str(exc))
