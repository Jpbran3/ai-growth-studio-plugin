"""Labeled opportunity arithmetic; standard library, no network or persistence."""
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
STATUSES = {'KNOWN': 'HIGH', 'ESTIMATED': 'MEDIUM', 'ASSUMED': 'LOW'}
RANK = {'KNOWN': 0, 'ESTIMATED': 1, 'ASSUMED': 2}
REQUIRED = ('eligible_leads', 'recovery_rate', 'booking_rate', 'completion_rate', 'sale_rate', 'job_value')
ALLOWED = set(REQUIRED) | {'capacity_jobs', 'inbound_calls', 'missed_rate'}

def metric(item, name):
    if not isinstance(item, dict) or set(item) != {'value', 'status', 'basis'}:
        raise ValueError(f'{name}: exactly value, status, basis required')
    if item['status'] not in STATUSES:
        raise ValueError(f'{name}: KNOWN, ESTIMATED or ASSUMED status required')
    if not isinstance(item['basis'], str) or not item['basis'].strip():
        raise ValueError(f'{name}: nonempty source/assumption basis required')
    raw = item['value']
    if raw is None or isinstance(raw, bool) or not isinstance(raw, (int, float, str, Decimal)):
        raise ValueError(f'{name}: numeric value required; unknown is not zero')
    try: value = Decimal(str(raw))
    except InvalidOperation as exc: raise ValueError(f'{name}: invalid number') from exc
    if not value.is_finite() or value < 0:
        raise ValueError(f'{name}: finite nonnegative value required')
    if name.endswith('_rate') and value > 1:
        raise ValueError(f'{name}: fraction must be between 0 and 1')
    return value

def exact(value): return format(value.normalize(), 'f')
def weakest(items): return max((m['status'] for m in items), key=RANK.__getitem__)

def calculate(payload):
    if not isinstance(payload, dict) or set(payload) != {'period', 'cohort', 'currency', 'inputs'}:
        raise ValueError('Exactly period, cohort, currency and inputs required')
    for field in ('period', 'cohort', 'currency'):
        if not isinstance(payload[field], str) or not payload[field].strip():
            raise ValueError(f'{field}: nonempty definition required')
    inputs = payload['inputs']
    if not isinstance(inputs, dict) or set(inputs) - ALLOWED or set(REQUIRED) - set(inputs):
        raise ValueError('Missing required inputs or unsupported input names')
    if ('inbound_calls' in inputs) != ('missed_rate' in inputs):
        raise ValueError('inbound_calls and missed_rate must be supplied together')
    values = {name: metric(item, name) for name, item in inputs.items()}
    jobs = values['eligible_leads']
    for name in ('recovery_rate', 'booking_rate', 'completion_rate', 'sale_rate'): jobs *= values[name]
    has_capacity = 'capacity_jobs' in values
    deliverable = min(jobs, values['capacity_jobs']) if has_capacity else jobs
    revenue = deliverable * values['job_value']
    material = [inputs[name] for name in REQUIRED]
    if has_capacity: material.append(inputs['capacity_jobs'])
    status = weakest(material)
    output = {
        'period': payload['period'], 'cohort': payload['cohort'], 'currency': payload['currency'],
        'output_kind': 'POTENTIAL OPPORTUNITY',
        'inputs': {n: {**inputs[n], 'value': exact(values[n])} for n in inputs},
        'formula': 'eligible_leads × recovery_rate × booking_rate × completion_rate × sale_rate; min(jobs, capacity_jobs) when capacity supplied; adjusted_jobs × job_value',
        'potential_jobs_before_capacity': exact(jobs), 'potential_jobs': exact(deliverable), 'potential_revenue': exact(revenue),
        'display_revenue_whole_units': exact(revenue.quantize(Decimal('1'), rounding=ROUND_HALF_UP)),
        'capacity_status': 'CAPPED' if has_capacity and jobs > deliverable else 'WITHIN SUPPLIED CAPACITY' if has_capacity else 'UNCONSTRAINED — CAPACITY UNKNOWN',
        'projection_confidence': STATUSES[status] if has_capacity else 'LOW',
        'confidence_reason': f'Weakest material input: {status}.' if has_capacity else f'Capacity is unknown; weakest other material input: {status}.',
        'warning': 'Conditional incremental opportunity, not measured lost revenue, profit or guaranteed recovery. Check cohort eligibility, overlap and causality outside this calculator.'}
    if 'inbound_calls' in values:
        call_status = weakest([inputs['inbound_calls'], inputs['missed_rate']])
        output['unanswered_call_attempts'] = {'value': exact(values['inbound_calls'] * values['missed_rate']), 'status': call_status, 'confidence': STATUSES[call_status], 'formula': 'inbound_calls × missed_rate', 'warning': 'Attempts are not unique eligible lost leads.'}
    return output

def aggregate(results, *, disjoint_cohorts=False):
    if not results or disjoint_cohorts is not True:
        raise ValueError('Aggregation requires results and evidence-supported disjoint cohorts')
    if len({r['cohort'] for r in results}) != len(results): raise ValueError('Duplicate cohorts cannot be aggregated')
    if len({(r['period'], r['currency']) for r in results}) != 1: raise ValueError('Period and currency must match')
    return {'output_kind': 'POTENTIAL OPPORTUNITY', 'potential_revenue': exact(sum((Decimal(r['potential_revenue']) for r in results), Decimal(0))), 'period': results[0]['period'], 'currency': results[0]['currency'], 'projection_confidence': max((r['projection_confidence'] for r in results), key={'HIGH':0,'MEDIUM':1,'LOW':2}.__getitem__), 'cohorts': [r['cohort'] for r in results], 'basis': 'Caller asserted evidence-supported disjoint cohorts; calculator cannot verify real-world overlap.'}

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 calculate.py INPUT.json', file=sys.stderr); return 2
    try:
        with open(sys.argv[1]) as file: payload = json.load(file, parse_float=Decimal, parse_int=Decimal)
        print(json.dumps(calculate(payload), indent=2)); return 0
    except (OSError, ValueError, InvalidOperation, TypeError, OverflowError) as exc:
        print(f'Cannot calculate: {exc}', file=sys.stderr); return 2
if __name__ == '__main__': raise SystemExit(main())
