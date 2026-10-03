"""Run deterministic tests. Optional jsonschema/PyYAML provide full format checks."""
from pathlib import Path
import copy, importlib.util, json, re, subprocess, sys, unittest, tempfile, zipfile
ROOT = Path(__file__).resolve().parents[1]
P = ROOT
S = P/'skills/revenue-leak-audit'
spec = importlib.util.spec_from_file_location('calc', S/'scripts/calculate.py')
calc = importlib.util.module_from_spec(spec); spec.loader.exec_module(calc)

def fixture():
    vals={'eligible_leads':40,'recovery_rate':0.5,'booking_rate':0.5,'completion_rate':0.8,'sale_rate':0.5,'job_value':1000,'capacity_jobs':10}
    return {'period':'2026-09','cohort':'unique unresolved qualified prospects','currency':'USD','inputs':{k:{'value':v,'status':'KNOWN','basis':'Synthetic business-record fixture'} for k,v in vals.items()}}

class MathTests(unittest.TestCase):
    def test_full_funnel(self):
        r=calc.calculate(fixture()); self.assertEqual(r['potential_jobs'],'4');self.assertEqual(r['potential_revenue'],'4000');self.assertEqual(r['output_kind'],'POTENTIAL OPPORTUNITY')
    def test_call_attempts_distinct(self):
        f=fixture();f['inputs'].update(inbound_calls={'value':200,'status':'KNOWN','basis':'call log'},missed_rate={'value':0.2,'status':'KNOWN','basis':'call log'})
        r=calc.calculate(f);self.assertEqual(r['unanswered_call_attempts']['value'],'40');self.assertEqual(r['potential_jobs'],'4')
    def test_known(self): self.assertEqual(calc.calculate(fixture())['projection_confidence'],'HIGH')
    def test_owner_estimate(self):
        f=fixture();f['inputs']['job_value']['status']='ESTIMATED';self.assertEqual(calc.calculate(f)['projection_confidence'],'MEDIUM')
    def test_assumption_preserved(self):
        f=fixture();f['inputs']['recovery_rate']['status']='ASSUMED';r=calc.calculate(f);self.assertEqual(r['projection_confidence'],'LOW');self.assertEqual(r['inputs']['recovery_rate']['status'],'ASSUMED')
    def test_unknown_capacity(self):
        f=fixture();del f['inputs']['capacity_jobs'];r=calc.calculate(f);self.assertEqual(r['projection_confidence'],'LOW');self.assertIn('UNCONSTRAINED',r['capacity_status'])
    def test_capacity_caps(self):
        f=fixture();f['inputs']['capacity_jobs']['value']=2;r=calc.calculate(f);self.assertEqual(r['potential_jobs_before_capacity'],'4');self.assertEqual(r['potential_revenue'],'2000')
    def test_zero_capacity(self):
        f=fixture();f['inputs']['capacity_jobs']['value']=0;self.assertEqual(calc.calculate(f)['potential_revenue'],'0')
    def test_zero_rate(self):
        f=fixture();f['inputs']['recovery_rate']['value']=0;self.assertEqual(calc.calculate(f)['potential_jobs'],'0')
    def test_decimal_exactness(self):
        f=fixture();f['inputs']['job_value']['value']='1000.10';self.assertEqual(calc.calculate(f)['potential_revenue'],'4000.4')
    def test_missing_never_defaults(self):
        for n in calc.REQUIRED:
            with self.subTest(n=n):
                f=fixture();del f['inputs'][n]
                with self.assertRaises(ValueError):calc.calculate(f)
    def test_bad_numbers(self):
        for x in [None,True,-1,'NaN','Infinity','-Infinity','not a number']:
            with self.subTest(value=x):
                f=fixture();f['inputs']['eligible_leads']['value']=x
                with self.assertRaises(ValueError):calc.calculate(f)
    def test_percent_not_fraction(self):
        f=fixture();f['inputs']['recovery_rate']['value']=50
        with self.assertRaises(ValueError):calc.calculate(f)
    def test_missing_basis(self):
        f=fixture();f['inputs']['job_value']['basis']=' '
        with self.assertRaises(ValueError):calc.calculate(f)
    def test_unknown_status(self):
        f=fixture();f['inputs']['job_value']['status']='UNKNOWN'
        with self.assertRaises(ValueError):calc.calculate(f)
    def test_period_required(self):
        f=fixture();f['period']=''
        with self.assertRaises(ValueError):calc.calculate(f)
    def test_calls_pair(self):
        f=fixture();f['inputs']['inbound_calls']={'value':100,'status':'KNOWN','basis':'log'}
        with self.assertRaises(ValueError):calc.calculate(f)
    def test_no_overlap_total(self):
        r=calc.calculate(fixture())
        with self.assertRaises(ValueError):calc.aggregate([r,r])
        with self.assertRaises(ValueError):calc.aggregate([r,r],disjoint_cohorts=True)
    def test_disjoint_total(self):
        a=calc.calculate(fixture());f=fixture();f['cohort']='separate other qualified prospects';b=calc.calculate(f)
        self.assertEqual(calc.aggregate([a,b],disjoint_cohorts=True)['potential_revenue'],'8000')
    def test_currency_and_period_mismatch(self):
        a=calc.calculate(fixture())
        for field,value in [('period','2026-08'),('currency','EUR')]:
            with self.subTest(field=field):
                f=fixture();f['cohort']='another';f[field]=value;b=calc.calculate(f)
                with self.assertRaises(ValueError):calc.aggregate([a,b],disjoint_cohorts=True)
    def test_scenarios(self):
        expected=['2000','4000','6000']
        for recovery,want in zip([0.25,0.5,0.75],expected):
            f=fixture();f['inputs']['recovery_rate'].update(value=recovery,status='ASSUMED',basis='Illustrative sensitivity case');r=calc.calculate(f)
            self.assertEqual(r['potential_revenue'],want);self.assertEqual(r['projection_confidence'],'LOW')
    def test_strong_replay_math(self):
        f=fixture();f['inputs']['booking_rate']['value']=0.75;f['inputs']['completion_rate']['value']=0.9;f['inputs']['capacity_jobs']['value']=20
        self.assertEqual(calc.calculate(f)['potential_revenue'],'6750')
    def test_rounding(self):
        f=fixture();f['inputs']['job_value']['value']='1000.125';r=calc.calculate(f);self.assertEqual(r['potential_revenue'],'4000.5');self.assertEqual(r['display_revenue_whole_units'],'4001')
    def test_cli_valid(self):
        p=subprocess.run([sys.executable,str(S/'scripts/calculate.py'),str(ROOT/'tests/math-input.json')],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['potential_revenue'],'4000')
    def test_cli_invalid(self):
        p=subprocess.run([sys.executable,str(S/'scripts/calculate.py'),str(ROOT/'tests/no-such-input.json')],capture_output=True,text=True)
        self.assertEqual(p.returncode,2);self.assertIn('Cannot calculate',p.stderr)

class StructureTests(unittest.TestCase):
    def test_portable_discovery(self):
        manifest=json.loads((P/'plugin.json').read_text())
        self.assertEqual(manifest['name'],'ai-growth-studio')
        self.assertNotIn('skills',manifest)
        self.assertEqual({p.parent.name for p in (P/'skills').glob('*/SKILL.md')},
                         {'revenue-leak-audit','missed-call-revenue-calculator','unsold-estimate-follow-up-audit'})
    def test_no_mcp(self):
        self.assertFalse(list(P.rglob('*mcp*.json')));self.assertFalse((P/'.app.json').exists())
    def test_presentation(self):
        a=json.loads((P/'plugin.json').read_text())['extensions']['com.openai']['interface']
        self.assertLessEqual(len(a['displayName']),30);self.assertLessEqual(len(a['shortDescription']),30);self.assertLessEqual(len(a['defaultPrompt']),3)
        for prompt in a['defaultPrompt']:self.assertLessEqual(len(prompt),128)
        for field in ['logo','composerIcon']:self.assertTrue((P/a[field]).is_file())
    def test_links(self):
        for path in S.rglob('*.md'):
            for dest in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                if '://' not in dest:self.assertTrue((path.parent/dest).resolve().is_file(),f'{path}: {dest}')
    def test_marketplace(self):
        m=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text());self.assertEqual((ROOT/m['plugins'][0]['source']['path']).resolve(),P.resolve())
    def test_prompt_counts(self):
        rows=[json.loads(l) for l in (ROOT/'tests/golden-prompts.jsonl').read_text().splitlines()]
        self.assertEqual({c:sum(r['category']==c for r in rows) for c in ['direct','indirect','negative']},{'direct':20,'indirect':30,'negative':20})
        self.assertEqual(len({r['prompt'] for r in rows}),70);self.assertEqual(len({r['id'] for r in rows}),70)
    def test_review_coverage(self):
        rows=[json.loads(l) for l in (ROOT/'tests/golden-prompts.jsonl').read_text().splitlines()];review=json.loads((ROOT/'tests/replays/activation-review.json').read_text())['decisions'];self.assertEqual({r['id'] for r in rows},{r['id'] for r in review})
        # This checks saved review consistency, NOT host activation accuracy.
        for r,d in zip(rows,review):self.assertEqual(r['expected_activation'],d['observed_decision'])
    def test_behavior_coverage(self):
        cases=json.loads((ROOT/'tests/behavior-cases.json').read_text());res=json.loads((ROOT/'tests/replays/developer-responses.json').read_text())['responses'];self.assertEqual({c['id'] for c in cases},set(res)|{'strong-data','abandonment'})
    def test_portable_schema(self):
        try:import jsonschema
        except ImportError:self.skipTest('Install jsonschema for full manifest schema validation')
        jsonschema.Draft202012Validator(json.loads((ROOT/'tests/schemas/plugin.schema.json').read_text())).validate(json.loads((P/'plugin.json').read_text()))
    def test_runtime_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            run=subprocess.run([sys.executable,str(ROOT/'scripts/package.py'),'--output-dir',directory],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            result=json.loads(run.stdout)
            with zipfile.ZipFile(Path(directory)/result[0]['file']) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('plugin.json',archive.namelist())
                self.assertFalse(any(n.startswith(('tests/','scripts/','.git/')) or '__pycache__' in n for n in archive.namelist()))
                for path in (ROOT/'skills').rglob('*'):
                    if path.is_file() and '__pycache__' not in path.parts:
                        self.assertEqual(archive.read(path.relative_to(ROOT).as_posix()),path.read_bytes())
    def test_yaml(self):
        try:import yaml
        except ImportError:self.skipTest('Install PyYAML for full YAML validation')
        parts=(S/'SKILL.md').read_text().split('---',2);front=yaml.safe_load(parts[1]);self.assertEqual(front['name'],'revenue-leak-audit');self.assertIsInstance(front['description'],str)
        a=yaml.safe_load((S/'agents/openai.yaml').read_text());self.assertTrue(a['policy']['allow_implicit_invocation']);self.assertIn('$revenue-leak-audit',a['interface']['default_prompt'])

class RoutingScorerTests(unittest.TestCase):
    def run_score(self, rows):
        import score_activation
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'observed.jsonl';p.write_text('\n'.join(json.dumps(r) for r in rows))
            return score_activation.score(p)
    def test_empty_is_uncovered(self):
        r=self.run_score([]);self.assertEqual(r['observed'],0);self.assertEqual(len(r['missing']),70);self.assertFalse(r['release_criterion_met'])
    def test_unobservable_is_not_pass(self):
        r=self.run_score([{'id':'D01','activated':None}]);self.assertEqual(r['observed'],0);self.assertEqual(r['unobservable'],['D01'])
    def test_false_routing_measured(self):
        r=self.run_score([{'id':'D01','activated':False,'evidence':'host did not load skill'},{'id':'N01','activated':True,'evidence':'host skill indicator'}]);self.assertEqual(r['counts']['false_negative'],1);self.assertEqual(r['counts']['false_positive'],1)
    def test_evidence_required(self):
        with self.assertRaises(ValueError):self.run_score([{'id':'D01','activated':True}])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]);suite.addTests(unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_branding.py'));result=unittest.TextTestRunner(verbosity=2).run(suite)
    data={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'success':result.wasSuccessful(),'scope':'Deterministic arithmetic, package structure and saved review consistency; not native ChatGPT behavior.'}
    (ROOT/'tests/automated-results.json').write_text(json.dumps(data,indent=2)+'\n')
    sys.exit(0 if result.wasSuccessful() else 1)
