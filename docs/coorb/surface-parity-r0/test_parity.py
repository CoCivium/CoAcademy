import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('project',ROOT/'project.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class Parity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj=json.loads((ROOT/'work-object.json').read_text(encoding='utf-8'))
        cls.html=(ROOT/'index.html').read_text(encoding='utf-8')
    def test_embedded_source_identical_to_json(self):
        m=re.search(r'<script type="application/json" id="source-object">\s*(.*?)\s*</script>',self.html,re.S)
        self.assertIsNotNone(m)
        self.assertEqual(json.loads(m.group(1)),self.obj)
    def test_bounded_views(self):self.assertEqual(mod.VIEWS,('glance','orb','map','machine'))
    def test_same_invariants_all_views(self):
        projected=[mod.project(self.obj,v) for v in mod.VIEWS]
        self.assertTrue(all(p['shared_invariants']==projected[0]['shared_invariants'] for p in projected))
    def test_same_source_hash_all_views(self):
        a=[mod.project(self.obj,v)['source_sha256'] for v in mod.VIEWS]
        self.assertEqual(len(set(a)),1)
    def test_machine_lossless(self):
        p=mod.project(self.obj,'machine');self.assertEqual(p['projection_omissions'],[])
        self.assertEqual({**p['shared_invariants'],**p['visible']},self.obj)
    def test_glance_explicitly_omits_details(self):
        p=mod.project(self.obj,'glance');self.assertIn('lanes',p['projection_omissions']);self.assertIn('unknowns',p['projection_omissions'])
    def test_preserves_unknown(self):
        self.assertEqual(mod.project(self.obj,'orb')['shared_invariants']['currentness']['state'],'UNVERIFIED_LIVE')
        self.assertFalse(mod.project(self.obj,'map')['shared_invariants']['receiver']['independent_ack'])
    def test_no_effects(self):
        self.assertEqual(mod.project(self.obj,'machine')['effects'],dict(network=0,provider_calls=0,workers_spawned=0,source_mutations=0))
    def test_rejects_private_object(self):
        a=copy.deepcopy(self.obj);a['privacy']['personal_content_included']=True
        with self.assertRaises(ValueError):mod.project(a,'machine')
    def test_rejects_fake_receiver_ack(self):
        a=copy.deepcopy(self.obj);a['receiver']['independent_ack']=True
        with self.assertRaises(ValueError):mod.project(a,'glance')
    def test_rejects_fake_live_state(self):
        a=copy.deepcopy(self.obj);a['currentness']['state']='LIVE_CONFIRMED'
        with self.assertRaises(ValueError):mod.project(a,'orb')
    def test_source_immutable(self):
        a=copy.deepcopy(self.obj)
        for v in mod.VIEWS:mod.project(a,v)
        self.assertEqual(self.obj,a)
    def test_no_external_network_or_storage_api(self):
        for forbidden in ('fetch(', 'XMLHttpRequest', 'localStorage', 'sessionStorage', 'navigator.clipboard', '<iframe','<img','addEventListener("paste"','document.cookie'):
            self.assertNotIn(forbidden,self.html)
        self.assertIn("connect-src 'none'",self.html)
    def test_bounded_fixture(self):self.assertLess(len(self.obj['lanes']),13)

if __name__=='__main__':unittest.main()
