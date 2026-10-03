"""Score actual host observations, preserving unobservable/missing routing."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def score(path):
    expected={r['id']:r for r in map(json.loads,(ROOT/'tests/golden-prompts.jsonl').read_text().splitlines())}
    observations={}
    for line in Path(path).read_text().splitlines():
        if not line.strip():continue
        row=json.loads(line);key=row['id']
        if key not in expected or key in observations:raise ValueError(f'Unknown or duplicate ID: {key}')
        if row.get('activated') is not None and type(row['activated']) is not bool:raise ValueError('activated must be boolean or null')
        if type(row.get('activated')) is bool and not str(row.get('evidence','')).strip():raise ValueError('Observed routing needs host evidence')
        observations[key]=row
    counts={'true_positive':0,'false_negative':0,'true_negative':0,'false_positive':0}
    unobservable=[]
    for key,row in observations.items():
        if row.get('activated') is None:unobservable.append(key);continue
        wanted=expected[key]['expected_activation'];actual=row['activated']
        counts['true_positive' if wanted and actual else 'false_negative' if wanted else 'false_positive' if actual else 'true_negative']+=1
    missing=sorted(set(expected)-set(observations));observed=sum(counts.values())
    return {'counts':counts,'observed':observed,'missing':missing,'unobservable':sorted(unobservable),'coverage':f'{observed}/70','release_criterion_met':observed==70 and counts['false_negative']==0 and counts['false_positive']==0,'scope':'Only supplied actual routing observations; no assumed passes.'}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('observations');args=parser.parse_args();print(json.dumps(score(args.observations),indent=2))
