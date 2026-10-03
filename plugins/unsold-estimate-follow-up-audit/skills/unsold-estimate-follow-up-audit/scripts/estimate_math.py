"""Quote screening and incremental opportunity; no defaults, network or writes."""
from decimal import Decimal,InvalidOperation
import json,sys
RANK={'KNOWN':0,'ESTIMATED':1,'ASSUMED':2};CONF={'KNOWN':'HIGH','ESTIMATED':'MEDIUM','ASSUMED':'LOW'}
SCREEN=('estimate_records','excess_revisions','undelivered_unique','closed_or_ineligible_unique','pending_not_due_unique')
PROJECTION=('eligible_estimates','baseline_close_rate','proposed_close_rate','completion_rate','job_value')
def exact(n):return format(n.normalize(),'f')
def weakest(inputs):return max((m['status'] for m in inputs),key=RANK.__getitem__)
def metric(item,name):
    if not isinstance(item,dict) or set(item)!={'value','status','basis'}:raise ValueError(name+': value, status and basis required')
    if not isinstance(item['status'],str) or item['status'] not in RANK:raise ValueError(name+': KNOWN, ESTIMATED or ASSUMED status required')
    if not isinstance(item['basis'],str) or not item['basis'].strip():raise ValueError(name+': source/assumption basis required')
    v=item['value']
    if v is None or isinstance(v,bool) or not isinstance(v,(int,float,str,Decimal)):raise ValueError(name+': numeric input required; unknown is not zero')
    try:n=Decimal(str(v))
    except InvalidOperation as e:raise ValueError(name+': invalid number') from e
    if not n.is_finite() or n<0:raise ValueError(name+': finite nonnegative input required')
    if name.endswith('_rate') and n>1:raise ValueError(name+': fraction 0–1 required')
    return n
def common(p,keys):
    if not isinstance(p,dict) or set(p)!=keys:raise ValueError('Required fields: '+', '.join(sorted(keys)))
    for k in ('period','cohort'):
        if not isinstance(p[k],str) or not p[k].strip():raise ValueError(k+': definition required')
def screen(p):
    common(p,{'mode','period','cohort','definitions_confirmed','screening_basis','inputs'})
    if p['mode']!='screen':raise ValueError('screen mode required')
    if p['definitions_confirmed'] is not True:raise ValueError('Sequential disjoint exclusions must be reconciled')
    if not isinstance(p['screening_basis'],str) or not p['screening_basis'].strip():raise ValueError('screening_basis required')
    inputs=p['inputs']
    if not isinstance(inputs,dict) or set(inputs)!=set(SCREEN):raise ValueError('All five screening metrics required; no zero defaults')
    v={n:metric(inputs[n],n) for n in SCREEN};status=weakest(inputs.values())
    unique=v['estimate_records']-v['excess_revisions'];delivered=unique-v['undelivered_unique'];open_quotes=delivered-v['closed_or_ineligible_unique'];eligible=open_quotes-v['pending_not_due_unique']
    if min(unique,delivered,open_quotes,eligible)<0:raise ValueError('Exclusion exceeds available stage pool')
    return {'period':p['period'],'cohort':p['cohort'],'inputs':{n:{**inputs[n],'value':exact(v[n])} for n in inputs},'unique_opportunities':exact(unique),'delivered_quotes':exact(delivered),'still_open_delivered':exact(open_quotes),'eligible_estimates':{'value':exact(eligible),'status':status,'basis':p['screening_basis']+'; derived sequential screening inputs'},'screening_confidence':CONF[status],'formula':'estimate_records - excess_revisions - undelivered_unique - closed_or_ineligible_unique - pending_not_due_unique','warning':'Caller asserted reconciled disjoint groups; calculator cannot verify truth or eligibility. Eligible quotes are not guaranteed wins.'}
def opportunity(p):
    common(p,{'mode','period','cohort','currency','inputs'})
    if p['mode']!='opportunity':raise ValueError('opportunity mode required')
    if not isinstance(p['currency'],str) or not p['currency'].strip():raise ValueError('currency required')
    inputs=p['inputs']
    if not isinstance(inputs,dict) or set(PROJECTION)-set(inputs) or set(inputs)-(set(PROJECTION)|{'capacity_jobs'}):raise ValueError('Explicit projection inputs required; no defaults')
    v={n:metric(inputs[n],n) for n in inputs};delta=v['proposed_close_rate']-v['baseline_close_rate']
    if delta<0:raise ValueError('Proposed rate below baseline does not support positive opportunity')
    accepted=v['eligible_estimates']*delta;completed=accepted*v['completion_rate'];has_capacity='capacity_jobs' in v;adjusted=min(completed,v['capacity_jobs']) if has_capacity else completed;money=adjusted*v['job_value'];status=weakest(inputs.values())
    return {'period':p['period'],'cohort':p['cohort'],'currency':p['currency'],'output_kind':'POTENTIAL OPPORTUNITY','inputs':{n:{**inputs[n],'value':exact(v[n])} for n in inputs},'absolute_incremental_close_fraction':exact(delta),'percentage_point_change':exact(delta*100),'incremental_accepted_jobs':exact(accepted),'potential_completed_jobs_before_capacity':exact(completed),'potential_deliverable_jobs':exact(adjusted),'potential_revenue':exact(money),'capacity_status':'UNCONSTRAINED — CAPACITY UNKNOWN' if not has_capacity else 'CAPPED' if adjusted<completed else 'WITHIN SUPPLIED CAPACITY','projection_confidence':CONF[status] if has_capacity else 'LOW','confidence_reason':'Weakest input: '+status+('; capacity unknown' if not has_capacity else ''),'formula':'eligible_estimates × (proposed_close_rate - baseline_close_rate) × completion_rate; min(completed_jobs, capacity_jobs) if supplied; deliverable_jobs × job_value','warning':'Conditional increment above normal outcomes, not all open quote value, measured loss, collected cash, profit or guaranteed recovery. Validate cohort matching, baseline applicability and overlap outside this helper.'}
def calculate(p):
    if not isinstance(p,dict):raise ValueError('Input object required')
    if p.get('mode')=='screen':return screen(p)
    if p.get('mode')=='opportunity':return opportunity(p)
    raise ValueError('mode must be screen or opportunity')
def aggregate(results,*,disjoint_cohorts=False):
    if not results or disjoint_cohorts is not True:raise ValueError('Evidence-supported disjoint cohorts required')
    if any(r.get('output_kind')!='POTENTIAL OPPORTUNITY' for r in results):raise ValueError('Only opportunity results can be summed')
    if len({r['cohort'] for r in results})!=len(results):raise ValueError('Duplicate cohorts cannot be summed')
    if len({(r['period'],r['currency']) for r in results})!=1:raise ValueError('Period/currency must match')
    return {'output_kind':'POTENTIAL OPPORTUNITY','potential_revenue':exact(sum((Decimal(r['potential_revenue']) for r in results),Decimal(0))),'projection_confidence':max((r['projection_confidence'] for r in results),key={'HIGH':0,'MEDIUM':1,'LOW':2}.__getitem__),'warning':'Caller asserted disjointness; overlapping portfolio findings cannot be summed.'}
def main():
    if len(sys.argv)!=2:print('Usage: python3 estimate_math.py INPUT.json',file=sys.stderr);return 2
    try:
        with open(sys.argv[1]) as f:p=json.load(f,parse_float=Decimal,parse_int=Decimal)
        print(json.dumps(calculate(p),indent=2));return 0
    except (OSError,ValueError,TypeError,InvalidOperation) as e:print('Cannot calculate: '+str(e),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
