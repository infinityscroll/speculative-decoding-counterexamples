"""Exact independent RRS recursion under the paper's sequential draft law."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json

p0=[F(19,20),F(1,60),F(1,60),F(1,60)]
q0=[F(1,2),F(1,6),F(1,6),F(1,6)]
output=[F(0)]*4
acceptance=F(0)
all_mass=F(0)
trace=[]
for draft in permutations(range(4),3):
    draft_prob=F(1)
    rem=F(1)
    for token in draft:
        draft_prob*=q0[token]/rem
        rem-=q0[token]
    all_mass+=draft_prob
    p,q=p0[:],q0[:]
    survival=F(1)
    local=[F(0)]*4
    for token in draft:
        a=min(F(1),p[token]/q[token])
        output[token]+=draft_prob*survival*a
        local[token]+=survival*a
        acceptance+=draft_prob*survival*a
        survival*=1-a
        if survival==0: break
        residual=[max(F(0),x-y) for x,y in zip(p,q)]
        z=sum(residual)
        assert z>0
        p=[x/z for x in residual]
        mass_removed=q[token]
        q=[F(0) if i==token else x/(1-mass_removed) for i,x in enumerate(q)]
    if survival:
        for i in range(4):
            output[i]+=draft_prob*survival*p[i]
            local[i]+=survival*p[i]
    assert sum(local)==1
    trace.append({'draft':draft,'draft_prob':str(draft_prob),'acceptance_given_draft':str(1-survival),'output_given_draft':list(map(str,local))})
assert all_mass==1
assert output==p0
assert acceptance==F(191,200)
r={'status':'PASS_EXACT_RRS_MARGINAL_AND_ACCEPTANCE','target':list(map(str,p0)),
   'draft':list(map(str,q0)),'output_marginal':list(map(str,output)),
   'RRS_acceptance':str(acceptance),'paper_formula_optimum':'19/20',
   'exceeds_formula_by':str(acceptance-F(19,20)),
   'trace':trace,'scope':'Published recursive rejection rule on this admissible finite distribution; no original-model experiment or empirical table corrected.'}
Path(__file__).with_name('RRS-REPLAY.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='trace'},indent=2))
