"""Independent exact check of the reported without-replacement example."""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import prod
import json
from pathlib import Path

q = [F(1,2),F(1,6),F(1,6),F(1,6)]
p = [F(19,20),F(1,60),F(1,60),F(1,60)]
n = 3
joint = {}
out = [F(0)]*len(q)
records = []
for draft in permutations(range(len(q)),n):
    mass=F(1);remaining=F(1)
    for token in draft:
        mass*=q[token]/remaining
        remaining-=q[token]
    joint[draft]=mass
    selected=0 if 0 in draft else draft[0]
    assert selected in draft
    out[selected]+=mass
    records.append({'draft':draft,'mass':str(mass),'selected':selected})
assert sum(joint.values())==1
assert out==p
normalizer=sum(prod(q[i] for i in t) for t in combinations(range(len(q)),n))
rows=[]
for bits in range(1<<len(q)):
    h={i for i in range(len(q)) if bits&(1<<i)}
    actual=sum(m for t,m in joint.items() if set(t)<=h)
    other=sum(prod(q[i] for i in t) for t in combinations(sorted(h),n))/normalizer
    ph=sum(p[i] for i in h)
    rows.append({'H':sorted(h),'sequential_Q':str(actual),'elementary_symmetric_Q':str(other),
                 'sequential_dual_value':str(1+ph-actual),'formula_dual_value':str(1+ph-other)})
actual_bound=min(F(r['sequential_dual_value']) for r in rows)
formula_bound=min(F(r['formula_dual_value']) for r in rows)
assert actual_bound==1 and formula_bound==F(19,20)
result={'status':'PASS_EXACT_RATIONAL_WITNESS','q':list(map(str,q)),'p':list(map(str,p)),
        'drafts':n,'ordered_tuples':len(joint),'verifier':'Output token0 when present; otherwise output the first draft.',
        'verified_output_marginal':list(map(str,out)),'verified_acceptance':'1',
        'true_subset_dual_optimum':str(actual_bound),'elementary_symmetric_formula_optimum':str(formula_bound),
        'absolute_gap':str(actual_bound-formula_bound),'tuples':records,'subsets':rows,
        'scope':'Only the sampling-law/formula mismatch is checked. q-convexity, prior-art novelty and original empirical results are not established by this script.'}
Path(__file__).with_name('REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['tuples','subsets']},indent=2))
