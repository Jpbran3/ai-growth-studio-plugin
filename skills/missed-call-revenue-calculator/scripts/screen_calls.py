"""Screen a reconciled sequential unanswered-call pool; no data defaults."""
import json,sys
from decimal import Decimal,InvalidOperation
from calculate import metric,exact,weakest,STATUSES
NAMES=('missed_attempts','repeat_attempts','nonprospect_unique','already_recovered_unique')
def screen(payload):
    required={'period','cohort','definitions_confirmed','screening_basis','inputs'}
    if not isinstance(payload,dict) or set(payload)!=required:raise ValueError('Exactly period, cohort, definitions_confirmed, screening_basis and inputs required')
    for k in ('period','cohort','screening_basis'):
        if not isinstance(payload[k],str) or not payload[k].strip():raise ValueError(f'{k}: nonempty definition/basis required')
    if payload['definitions_confirmed'] is not True:raise ValueError('Reconcile sequential disjoint exclusions before screening')
    inputs=payload['inputs']
    if not isinstance(inputs,dict) or set(inputs)!=set(NAMES):raise ValueError('All four screening metrics required; unknown exclusions do not default to zero')
    v={k:metric(inputs[k],k) for k in NAMES}
    unique=v['missed_attempts']-v['repeat_attempts']
    suitable=unique-v['nonprospect_unique']
    eligible=suitable-v['already_recovered_unique']
    if min(unique,suitable,eligible)<0:raise ValueError('Inconsistent waterfall: an exclusion exceeds its available pool')
    status=weakest(inputs.values())
    return {'period':payload['period'],'cohort':payload['cohort'],'inputs':{k:{**inputs[k],'value':exact(v[k])} for k in NAMES},'formula':'missed_attempts - repeat_attempts - nonprospect_unique - already_recovered_unique','unique_callers':exact(unique),'suitable_new_prospects':exact(suitable),'eligible_leads':{'value':exact(eligible),'status':status,'basis':payload['screening_basis']+'; derived from labeled sequential screening inputs'},'screening_confidence':STATUSES[status],'warning':'Counts are not sold jobs or revenue. Definitions confirmed by caller; this helper cannot verify truth or real-world overlap.'}
def main():
    if len(sys.argv)!=2:print('Usage: python3 screen_calls.py INPUT.json',file=sys.stderr);return 2
    try:
        with open(sys.argv[1]) as f:p=json.load(f,parse_int=Decimal,parse_float=Decimal)
        print(json.dumps(screen(p),indent=2));return 0
    except (ValueError,TypeError,OSError,InvalidOperation) as e:print('Cannot screen: '+str(e),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
