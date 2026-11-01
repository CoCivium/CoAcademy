import tempfile
import unittest
from cofirstuse_compare import analyze_source, run, SOURCES


class FirstUseTests(unittest.TestCase):
    def test_basic_pass(self):
        html = '<!doctype html><html><head><meta name="viewport" content="width=device-width"></head><body><h1>Welcome</h1><a href="next/">Explore</a><svg></svg><style>:focus-visible{} @media(prefers-reduced-motion:reduce){}</style><p>Prototype</p></body></html>'
        p = analyze_source(html, 'example', 'docs/index.html')
        self.assertEqual(p['source_checks_passed'], 10)
        self.assertEqual(p['duplicate_href_values'], [])
        self.assertEqual(p['real_person_outcome'], 'UNVERIFIED')

    def test_regressions_are_exposed(self):
        html = '<!doctype html><html><h1>One</h1><h1>Two</h1><a href="a">A</a><a href="a">B</a><img src="photo"><script src="https://tracker.example/a.js"></script></html>'
        p = analyze_source(html, 'bad', 'docs/bad.html')
        self.assertFalse(p['source_checks']['one_h1'])
        self.assertFalse(p['source_checks']['all_img_have_alt'])
        self.assertFalse(p['source_checks']['no_external_script_src'])
        self.assertEqual(p['duplicate_href_values'], ['a'])

    def test_missing_sources_not_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run(tmp, live=False)
            self.assertEqual(len(report['targets']), len(SOURCES))
            self.assertEqual(sum('source_status' in x for x in report['targets']), len(SOURCES))
            self.assertEqual(report['live_checks'], [])


if __name__ == '__main__':
    unittest.main()
