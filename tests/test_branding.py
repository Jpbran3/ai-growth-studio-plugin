from pathlib import Path
import importlib.util,tempfile,json,unittest
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'skills/revenue-leak-audit'
spec=importlib.util.spec_from_file_location('branding',S/'scripts/brand_report.py');branding=importlib.util.module_from_spec(spec);spec.loader.exec_module(branding)
class BrandingTests(unittest.TestCase):
    def test_trade_palettes(self):
        for trade,color in [('plumbing','#1565C0'),('HVAC','#62B5E5'),('med spa','#006039'),('roofing','#7BAFD4')]:self.assertEqual(branding.fallback(trade),color)
    def test_mixed_palette(self):self.assertEqual(branding.fallback('Plumbing and HVAC'),'#7BAFD4')
    def test_unverified_site_uses_fallback(self):
        b=branding.brand({'trade':'HVAC','website':'https://example.com'})
        self.assertEqual(b['source'],'FALLBACK');self.assertIn('Skill fallback',b['basis']);self.assertNotIn('Owner-specified',b['basis'])
    def test_verified_brand(self):
        b=branding.brand({'trade':'HVAC','website':'https://example.com','branding':{'source':'WEBSITE VERIFIED','basis':'Synthetic CSS fixture on provided URL','primary_color':'#112233','font_family':"'Open Sans', sans-serif"}});self.assertEqual(b['primary_color'],'#112233');self.assertIn('Open Sans',b['font_family'])
    def test_owner_override(self):
        b=branding.brand({'trade':'HVAC','branding':{'source':'OWNER PROVIDED','basis':'Owner stated brand preference','primary_color':'#123456','font_family':'Georgia, serif'}});self.assertEqual(b['primary_color'],'#123456')
    def test_bad_color(self):
        with self.assertRaises(ValueError):branding.brand({'trade':'plumbing','branding':{'source':'OWNER PROVIDED','basis':'Test','primary_color':'red;}</style>','font_family':'Arial'}})
    def test_bad_font(self):
        with self.assertRaises(ValueError):branding.brand({'trade':'plumbing','branding':{'source':'OWNER PROVIDED','basis':'Test','primary_color':'#123456','font_family':'Arial; background:url(https://evil)'}})
    def test_verified_requires_site(self):
        with self.assertRaises(ValueError):branding.brand({'trade':'plumbing','branding':{'source':'WEBSITE VERIFIED','basis':'Test','primary_color':'#123456','font_family':'Arial'}})
    def test_raw_html_and_bad_link_escaped(self):
        t=branding.render('<script>alert(1)</script>\n\n[bad](javascript:alert)');self.assertNotIn('<script>',t);self.assertNotIn('href="javascript:',t);self.assertIn('&lt;script&gt;',t)
    def test_tables_render(self):self.assertIn('<table>',branding.render('| Metric | Value |\n|---|---|\n| potential | $7,200 |'))
    def test_actual_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);(p/'body.md').write_text('# Acme Plumbing\n\n**POTENTIAL OPPORTUNITY**: $7,200, LOW confidence.\n')
            r=branding.generate({'business_name':'Acme Plumbing','trade':'plumbing','report_path':str(p/'body.md'),'output_dir':str(p/'out')});md=Path(r['markdown']).read_text();ht=Path(r['html']).read_text();self.assertIn('brand_color: "#1565C0"',md);self.assertIn('LOW confidence',md);self.assertIn('#1565C0',ht);self.assertIn('<h1>Acme Plumbing</h1>',ht);self.assertNotIn('@import',ht)
    def test_preserve_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);(p/'body.md').write_text('# Test\n');c={'business_name':'Test','trade':'other','report_path':str(p/'body.md'),'output_dir':str(p/'out')};branding.generate(c)
            with self.assertRaises(ValueError):branding.generate(c)

    def test_complete_and_preliminary_report_pairs(self):
        import html
        for name,company,trade,disclosures in [('strong-data','Example Home Services','mixed',1),('abandonment','Oak Electrical','electrical',0)]:
            with self.subTest(report=name), tempfile.TemporaryDirectory() as directory:
                body=ROOT/'tests/replays'/(name+'-report.md')
                result=branding.generate({'business_name':company,'trade':trade,'report_path':str(body),'output_dir':directory})
                markdown=Path(result['markdown']).read_text()
                document=Path(result['html']).read_text()
                self.assertEqual(markdown.split('---',2)[2].lstrip(),body.read_text())
                self.assertEqual(len(__import__('re').findall(r'<h3>\d+\.',document)),10)
                self.assertEqual(document.count('AI Growth Studio'),disclosures)
                self.assertIn('UNKNOWN' if name=='abandonment' else '$6,750',document)
                self.assertNotIn('<script',document)
                # Every prose paragraph survives HTML escaping and inline styling.
                for paragraph in body.read_text().split('\n\n'):
                    if paragraph.startswith(('#','|')):continue
                    self.assertIn(html.escape(' '.join(paragraph.splitlines())),document)
