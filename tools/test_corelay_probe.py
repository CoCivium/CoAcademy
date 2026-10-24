"""Deterministic tests; no network requests."""
import unittest
import tempfile
from pathlib import Path
from corelay_probe import TARGETS, SOURCE_PATHS, assess_content, classify, verify_source_bytes

def result(name, state):
    return {"id": name, "state": state}

class CoRelayPublicProbeTests(unittest.TestCase):
    def test_accepts_verified_html(self):
        self.assertEqual(assess_content(200, b"Try it. Challenge it. Improve it. CoRelay+", ("CoRelay+",))[0], "PASS")
    def test_rejects_wrong_http(self):
        self.assertEqual(assess_content(404, b"CoRelay+", ("CoRelay+",))[0], "FAIL")
    def test_rejects_missing_marker(self):
        self.assertEqual(assess_content(200, b"Something else", ("CoRelay+",))[0], "FAIL")
    def test_rejects_excess_size(self):
        self.assertEqual(assess_content(200, b"x" * 400001, ("x",))[0], "FAIL")
    def test_all_targets_https(self):
        self.assertTrue(all(t[1].startswith("https://") for t in TARGETS))
    def test_all_targets_same_failure_domain(self):
        self.assertEqual({t[3] for t in TARGETS}, {"GITHUB"})
    def test_source_path_for_every_target(self):
        self.assertEqual({t[0] for t in TARGETS}, set(SOURCE_PATHS))

    def test_source_byte_match_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / SOURCE_PATHS["relay"]
            path.parent.mkdir(parents=True)
            path.write_bytes(b"alpha omega")
            state, reason, expected, served = verify_source_bytes("relay", b"alpha omega", root)
            self.assertEqual((state, reason), ("PASS", "SOURCE_SHA256_MATCH"))
            self.assertEqual(expected, served)

    def test_stale_page_with_same_markers_fails_sha(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / SOURCE_PATHS["relay"]
            path.parent.mkdir(parents=True)
            path.write_bytes(b"CoRelay+ current")
            older = b"CoRelay+ older"
            self.assertEqual(assess_content(200, older, ("CoRelay+",))[0], "PASS")
            state, reason, expected, served = verify_source_bytes("relay", older, root)
            self.assertEqual((state, reason), ("FAIL", "SOURCE_VERSION_MISMATCH"))
            self.assertNotEqual(expected, served)

    def test_missing_checked_out_source_is_not_success(self):
        with tempfile.TemporaryDirectory() as folder:
            state, reason, expected, served = verify_source_bytes("relay", b"known body", Path(folder))
            self.assertEqual((state, reason), ("INCONCLUSIVE", "CHECKED_OUT_SOURCE_UNAVAILABLE"))
            self.assertIsNone(expected)
            self.assertEqual(len(served), 64)

    def test_unlisted_source_is_a_failure(self):
        state, reason, _, _ = verify_source_bytes("unqualified_external_host", b"public")
        self.assertEqual((state, reason), ("FAIL", "UNLISTED_TARGET"))

    def test_pages_success_raw_failure_does_not_show_green(self):
        checks = [result(t[0], "PASS") for t in TARGETS]
        checks[-1]["state"] = "FAIL"
        self.assertEqual(classify(checks), "PAGES_MATCH_BUT_RAW_SOURCE_UNAVAILABLE")
    def test_phoenix_is_separately_scoped(self):
        by_id = {t[0]: t for t in TARGETS}
        self.assertEqual(set(("phoenix", "phoenix_contract")).issubset(by_id), True)
        self.assertEqual(by_id["phoenix"][3], "GITHUB")
        self.assertEqual(by_id["phoenix_contract"][3], "GITHUB")
    def test_phoenix_contract_has_nonclaim(self):
        by_id = {t[0]: t for t in TARGETS}
        self.assertIn('"public_capsule_hosted": false', by_id["phoenix_contract"][2])
    def test_new_page_missing_is_failure_even_if_fallback_passes(self):
        checks = [result(t[0], "PASS") for t in TARGETS]
        for item in checks:
            if item["id"] == "phoenix":
                item["state"] = "FAIL"
        self.assertEqual(classify(checks), "DEGRADED_WITH_SAME_PROVIDER_SOURCE")
    def test_passing_independent_readback(self):
        checks = [result(t[0], "PASS") for t in TARGETS]
        self.assertEqual(classify(checks), "PASS_PUBLIC_HTTP_SOURCE_MATCH")
    def test_fallback_is_not_independent_redundancy(self):
        checks = [result(t[0], "FAIL") for t in TARGETS]
        checks[-1]["state"] = "PASS"
        self.assertEqual(classify(checks), "DEGRADED_WITH_SAME_PROVIDER_SOURCE")
    def test_no_source_fallback(self):
        checks = [result(t[0], "FAIL") for t in TARGETS]
        self.assertEqual(classify(checks), "PUBLIC_READPROOF_FAILED_OR_INCONCLUSIVE")

if __name__ == "__main__":
    unittest.main()
