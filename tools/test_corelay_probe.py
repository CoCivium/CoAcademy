"""Deterministic tests; no network requests."""
import unittest
from corelay_probe import TARGETS, assess_content, classify

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
    def test_passing_independent_readback(self):
        checks = [result(t[0], "PASS") for t in TARGETS]
        self.assertEqual(classify(checks), "PASS_PUBLIC_RENDER")
    def test_fallback_is_not_independent_redundancy(self):
        checks = [result(t[0], "FAIL") for t in TARGETS]
        checks[-1]["state"] = "PASS"
        self.assertEqual(classify(checks), "DEGRADED_WITH_SAME_PROVIDER_SOURCE")
    def test_no_source_fallback(self):
        checks = [result(t[0], "FAIL") for t in TARGETS]
        self.assertEqual(classify(checks), "PUBLIC_READPROOF_FAILED_OR_INCONCLUSIVE")

if __name__ == "__main__":
    unittest.main()
