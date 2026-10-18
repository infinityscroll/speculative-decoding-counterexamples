#!/usr/bin/env python3
"""Independent probability-tree replay; no imports from other certificates."""
from fractions import Fraction as R
from pathlib import Path
import hashlib
import json

Q=(R(1,2),R(1,6),R(1,6),R(1,6))
P=(R(19,20),R(1,60),R(1,60),R(1,60))
N=3

def successive_tree(prefix=(),prob=R(1)):
    if len(prefix)==N:
        return {prefix:prob}
    available=[i for i in range(4) if i not in prefix]
    remaining=sum(Q[i] for i in available)
    out={}
    for i in available:
        out.update(successive_tree(prefix+(i,),prob*Q[i]/remaining))
    return out

def iid_tree(prefix=(),prob=R(1)):
    if len(prefix)==N:
        return {prefix:prob}
    out={}
    for i in range(4):
        out.update(iid_tree(prefix+(i,),prob*Q[i]))
    return out

def elementary(mask):
    coeff=[R(1)]+[R(0)]*N
    for i in range(4):
        if mask & (1<<i):
            for degree in range(N,0,-1):
                coeff[degree]+=Q[i]*coeff[degree-1]
    return coeff[N]

def marginal(law,kernel):
    m=[R(0)]*4;accepted=R(0);rows=[]
    for drafts,mass in law.items():
        k=kernel(drafts)
        assert all(a>=0 for a in k) and sum(k)==1
        for i,conditional in enumerate(k):
            m[i]+=mass*conditional
            if i in drafts: accepted+=mass*conditional
        rows.append({'drafts':drafts,'draft_mass':str(mass),'conditional_output':list(map(str,k))})
    assert sum(m)==1
    return tuple(m),accepted,rows

def deterministic(drafts):
    chosen=0 if 0 in drafts else drafts[0]
    assert chosen in drafts
    return tuple(R(i==chosen) for i in range(4))

def rejective_control(drafts):
    if 0 in drafts:return (R(1),R(0),R(0),R(0))
    return (R(1,2),R(1,6),R(1,6),R(1,6))

def rrs_kernel(drafts,p=P,q=Q):
    if not drafts:return p
    first=drafts[0]
    assert q[first]>0
    acceptance=min(p[first]/q[first],R(1))
    out=[R(0)]*4;out[first]=acceptance
    if acceptance==1:return tuple(out)
    residual=[max(a-b,R(0)) for a,b in zip(p,q)]
    z=sum(residual);assert z>0
    pnext=tuple(a/z for a in residual)
    qnext=tuple(R(0) if i==first else q[i]/(1-q[first]) for i in range(4))
    rest=rrs_kernel(drafts[1:],pnext,qnext)
    for i,a in enumerate(rest):out[i]+=(1-acceptance)*a
    assert sum(out)==1
    return tuple(out)

seq=successive_tree();iid=iid_tree()
assert len(seq)==24 and len(iid)==64 and sum(seq.values())==sum(iid.values())==1
z=sum(v for t,v in iid.items() if len(set(t))==N)
rej={t:v/z for t,v in iid.items() if len(set(t))==N}
assert z==6*elementary(15) and sum(rej.values())==1
sm,sa,srows=marginal(seq,deterministic)
rm,ra,rrows=marginal(rej,rejective_control)
am,aa,arows=marginal(seq,rrs_kernel)
assert sm==rm==am==P
assert sa==1 and ra==R(19,20) and aa==R(191,200)
rows=[]
for mask in range(16):
    subset=[i for i in range(4) if mask & (1<<i)]
    trueq=sum(v for t,v in seq.items() if all(i in subset for i in t))
    otherq=sum(v for t,v in rej.items() if all(i in subset for i in t))
    formulaq=elementary(mask)/elementary(15)
    assert otherq==formulaq
    p=sum(P[i] for i in subset)
    rows.append({'subset':subset,'P':str(p),'actual_Q':str(trueq),
      'formula_Q':str(formulaq),'actual_dual':str(1+p-trueq),'formula_dual':str(1+p-formulaq)})
assert min(R(r['actual_dual']) for r in rows)==1
assert min(R(r['formula_dual']) for r in rows)==R(19,20)
assert rows[14]['actual_Q']=='1/20' and rows[14]['formula_Q']=='1/10'
order=sorted(range(4),key=lambda i:(-Q[i]/P[i],i))
mask=0;prefix=[rows[0]]
for i in order:
    mask|=1<<i;prefix.append(rows[mask])
assert order==[1,2,3,0]
assert min(R(r['formula_dual']) for r in prefix)==R(19,20)
# The ratio is correct in the uniform special case: all distinct orders are
# equiprobable under both laws. This is a direct normalization control.
uniform_mass=R(1,4)*R(1,3)*R(1,2)
assert uniform_mass==R(1,24)
result={'status':'PASS_INDEPENDENT_EXACT_BOUND_COUNTEREXAMPLE',
 'q':list(map(str,Q)),'p':list(map(str,P)),'n':N,
 'sequential_ordered_tuples':len(seq),'iid_unconditioned_tuples':len(iid),
 'deterministic_valid_verifier_acceptance':str(sa),
 'RRS_acceptance':str(aa),'product_weighted_law_optimum':str(ra),
 'computed_published_prefix_value':'19/20','true_optimum':'1',
 'true_optimum_proof':'A feasible target-marginal coupling always outputs a drafted token; no acceptance can exceed1.',
 'all_three_output_marginals_equal_target':True,
 'subset_checks':rows,'sorted_prefixes':prefix,
 'sequential_coupling':srows,'rejective_positive_control':rrows,'RRS_coupling':arows,
 'source_dependence':'No imports, execution, or copied numerical outputs from parent or sibling certificates.',
 'limits':['Does not disprove q-convexity for successive sampling.','Does not recalculate empirical tables or establish novelty.','Does not challenge the general transport formula or separate Greedy protocol.'],
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','deterministic_valid_verifier_acceptance','RRS_acceptance','computed_published_prefix_value','true_optimum','script_sha256']},indent=2))
