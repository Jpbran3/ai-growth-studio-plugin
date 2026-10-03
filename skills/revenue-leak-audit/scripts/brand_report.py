"""Save branded Markdown and HTML with no external dependencies or network."""
from pathlib import Path
import html,json,re,sys
from urllib.parse import urlsplit
PALETTES={'plumbing':'#1565C0','hvac':'#62B5E5','med spa':'#006039','other':'#7BAFD4'}
FONT='Arial, Helvetica, sans-serif'
def fallback(trade):
    t=trade.strip().lower()
    # Multiple trades intentionally remain soft blue unless a primary trade is supplied.
    if any(x in t for x in [' and ',' & ','/',',','multi-trade']):return PALETTES['other']
    if 'plumb' in t:return PALETTES['plumbing']
    if any(x in t for x in ['hvac','heating','air conditioning','air-conditioning']):return PALETTES['hvac']
    if any(x in t for x in ['med spa','medspa','medical spa']):return PALETTES['med spa']
    return PALETTES['other']
def brand(config):
    supplied=config.get('branding')
    if supplied is None:
        return {'source':'FALLBACK','basis':'Skill fallback trade palette; website style not verified' if config.get('website') else 'Skill fallback trade palette; no website supplied','primary_color':fallback(config['trade']),'secondary_color':'#EAF2F8','font_family':FONT}
    if not isinstance(supplied,dict) or set(supplied)-{'source','basis','primary_color','secondary_color','font_family'}:raise ValueError('Unsupported branding fields')
    if supplied.get('source') not in ['WEBSITE VERIFIED','OWNER PROVIDED']:raise ValueError('Branding must be verified website evidence or owner provided')
    for key in ['basis','primary_color','font_family']:
        if not isinstance(supplied.get(key),str) or not supplied[key].strip():raise ValueError(key+' required')
    if supplied['source']=='WEBSITE VERIFIED' and not config.get('website'):raise ValueError('Verified website branding requires website URL and evidence basis')
    for c in ['primary_color','secondary_color']:
        if c in supplied and not re.fullmatch(r'#[0-9A-Fa-f]{6}',supplied[c]):raise ValueError('Colors must use #RRGGBB')
    font=supplied['font_family']
    if len(font)>200 or not re.fullmatch(r'[A-Za-z0-9 ,\-\'\"]+',font) or any(x in font.lower() for x in ['url','expression','import']):raise ValueError('Unsupported font-family value')
    if 'sans-serif' not in font.lower() and 'serif' not in font.lower():font+=', Arial, Helvetica, sans-serif'
    return {**supplied,'font_family':font,'secondary_color':supplied.get('secondary_color','#EAF2F8')}
def inline(text):
    text=html.escape(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    def link(m):
        url=html.unescape(m.group(2))
        if urlsplit(url).scheme.lower() not in ['https','http']:return m.group(1)+' ('+html.escape(url)+')'
        return '<a href="'+html.escape(url,quote=True)+'">'+m.group(1)+'</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
def render(text):
    lines=text.splitlines();out=[];i=0
    def table_cells(line):return [p.strip() for p in line.strip().strip('|').split('|')]
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
        h=re.match(r'^(#{1,6})\s+(.+)',line)
        if h:out.append(f'<h{len(h[1])}>'+inline(h[2])+f'</h{len(h[1])}>');i+=1;continue
        if i+1<len(lines) and '|' in line and re.fullmatch(r'[\s|:\-]+',lines[i+1]) and '-' in lines[i+1]:
            headers=table_cells(line);out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in headers)+'</tr></thead><tbody>');i+=2
            while i<len(lines) and '|' in lines[i] and lines[i].strip():
                cells=table_cells(lines[i]);out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in cells)+'</tr>');i+=1
            out.append('</tbody></table></div>');continue
        m=re.match(r'^\s*(?:[-*]|\d+\.)\s+(.+)',line)
        if m:
            ordered=bool(re.match(r'^\s*\d+\.',line));tag='ol' if ordered else 'ul';out.append('<'+tag+'>')
            while i<len(lines):
                m=re.match(r'^\s*(?:[-*]|\d+\.)\s+(.+)',lines[i])
                if not m:break
                out.append('<li>'+inline(m[1])+'</li>');i+=1
            out.append('</'+tag+'>');continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|```|[-*] |\d+\. )',lines[i]) and '|' not in lines[i]:paragraph.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return '\n'.join(out)
def generate(config):
    for key in ['business_name','trade','report_path','output_dir']:
        if not isinstance(config.get(key),str) or not config[key].strip():raise ValueError(key+' required')
    text=Path(config['report_path']).read_text(encoding='utf-8')
    if text.startswith('---\n'):raise ValueError('Supply report body without existing YAML metadata')
    if not text.strip():raise ValueError('Report is empty')
    b=brand(config);slug=re.sub(r'[^a-z0-9]+','-',config['business_name'].lower()).strip('-') or 'business'
    suffix=config.get('report_slug','audit')
    if not isinstance(suffix,str) or not re.fullmatch(r'[a-z0-9-]+',suffix):raise ValueError('report_slug must be lowercase filename characters')
    directory=Path(config['output_dir']);md=directory/(slug+'-'+suffix+'.md');ht=md.with_suffix('.html')
    if md.exists() or ht.exists():raise ValueError('Output exists; choose a distinct report_slug or output_dir')
    metadata={'company':config['business_name'],'brand_source':b['source'],'brand_basis':b['basis'],'brand_font':b['font_family'],'brand_color':b['primary_color'],'brand_secondary':b['secondary_color']}
    front='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in metadata.items())+'\n---\n\n'
    font=b['font_family'];color=b['primary_color'];secondary=b['secondary_color']
    css=f'body{{margin:0;background:#f4f7fa;color:#173042;font-family:{font};line-height:1.6}}main{{max-width:960px;margin:36px auto;padding:40px;background:white;border-top:10px solid {color};border-radius:10px}}h1{{font-size:2.1rem;line-height:1.2}}h2,h3{{border-left:5px solid {color};padding-left:12px}}h1,h2,h3{{color:#173042}}table{{border-collapse:collapse;width:100%;font-size:.94rem}}th{{background:{secondary}}}td,th{{padding:10px;border:1px solid #cddae3;text-align:left;vertical-align:top}}.table-wrap{{overflow-x:auto}}a{{color:#125b91}}pre{{white-space:pre-wrap;background:#eef3f7;padding:16px}}code{{font-family:monospace}}footer{{font-size:.85rem;color:#42596a;border-top:1px solid #cddae3;margin-top:30px;padding-top:14px}}@media(max-width:650px){{main{{margin:0;padding:20px;border-radius:0}}h1{{font-size:1.7rem}}}}@media print{{body{{background:white}}main{{margin:0;padding:20px;max-width:none}}}}'
    source_note=html.escape(b['source']+': '+b['basis'])
    document='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(config['business_name'])+' Audit</title><style>'+css+'</style></head><body><main>'+render(text)+'<footer>Presentation: '+source_note+'. Typography uses available local fonts.</footer></main></body></html>'
    directory.mkdir(parents=True,exist_ok=True);md.write_text(front+text,encoding='utf-8');ht.write_text(document,encoding='utf-8')
    return {'markdown':str(md.resolve()),'html':str(ht.resolve()),'branding':b,'rendering_note':'Markdown appearance depends on viewer; HTML carries font/color styles. Website verification asserted by input, not performed by helper.'}
def main():
    if len(sys.argv)!=2:print('Usage: python3 brand_report.py CONFIG.json',file=sys.stderr);return 2
    try:
        with open(sys.argv[1]) as f:config=json.load(f)
        print(json.dumps(generate(config),indent=2));return 0
    except (OSError,ValueError,TypeError) as e:print('Cannot generate report: '+str(e),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
