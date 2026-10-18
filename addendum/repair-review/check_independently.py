#!/usr/bin/env python3
"""Small exact controls for an independent proof review. No proposer imports."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib, json, time

def all_in_probabilities(weights,n):
    V=len(weights); total=sum(weights); mass=[F(0)]*(1<<V)
    support=[i for i,w in enumerate(weights) if w>0]
    assert 1<=n<=len(support)
    count=0
    for order in permutations(support,n):
        probability=F(1); remaining=total; mask=0
        for i in order:
            probability *= F(weights[i],remaining)
            remaining-=weights[i];mask|=1<<i
        mass[mask]+=probability;count+=1
    assert sum(mass)==1
    Q=mass[:]
    for i in range(V):
        for H in range(1<<V):
            if H>>i&1: Q[H]+=Q[H^(1<<i)]
    return Q,count

def main():
    start=time.process_time();checks=0;ordered=0;cases=[]
    vectors=[(1,),(1,2),(1,2,4),(1,2,3,7),(1,1,1,5),(1,2,3,4,6),(0,1,2,3),(0,0,1,2,4)]
    for w in vectors:
        V=len(w)
        for n in range(1,sum(x>0 for x in w)+1):
            Q,count=all_in_probabilities(w,n);ordered+=count
            minimum=None; strict=0;local=0
            for H in range(1<<V):
                outside=[i for i in range(V) if not H>>i&1]
                for x,y in permutations(outside,2):
                    a=Q[H|(1<<x)]-Q[H]
                    b=Q[H|(1<<x)|(1<<y)]-Q[H|(1<<x)]
                    slack=w[x]*b-w[y]*a
                    assert slack>=0,(w,n,H,x,y,slack)
                    if n==1:assert slack==0
                    minimum=slack if minimum is None else min(minimum,slack)
                    strict+=slack>0;checks+=1;local+=1
            cases.append({'weights':w,'n':n,'ordered_drafts':count,'inequalities':local,'strict':strict,'minimum_cross_slack':str(minimum)})
    # Samplewise inclusions depend only on order. Exhaust all V=4 clock orders.
    inclusion_checks=0
    for order in permutations(range(4)):
        for n in range(1,4):
            D=set(order[:n])
            for Hmask in range(16):
                H={i for i in range(4) if Hmask>>i&1}
                for x,y in permutations(set(range(4))-H,2):
                    winner=x if order.index(x)<order.index(y) else y
                    loser=y if winner==x else x
                    reduced=[i for i in order if i!=loser]
                    R=set(reduced[:n])
                    A=D<=H|{x} and x in D
                    B=R<=H|{winner} and winner in R
                    E=D<=H|{x,y} and bool(D&{x,y})
                    assert not A or (B and winner==x)
                    assert not B or E
                    inclusion_checks+=1
    # Independent n=2 prefix oracle checks; correct Q remains the enumerated law.
    pair_checks=[]
    for w in [(3,3,1),(1,2,3,7),(1,2,3,4,6)]:
        V=len(w);q=[F(x,sum(w)) for x in w]
        p=[F(i+1,V*(V+1)//2) for i in range(V)]
        if w==(3,3,1):p=[F(3,10),F(3,10),F(2,5)]
        Q,_=all_in_probabilities(w,2)
        f=[]
        for H in range(1<<V):
            a=sum((q[i] for i in range(V) if H>>i&1),F(0))
            b=sum((q[i]/(1-q[i]) for i in range(V) if H>>i&1),F(0))
            assert Q[H]==a-(1-a)*b
            f.append(1+sum((p[i] for i in range(V) if H>>i&1),F(0))-Q[H])
        order=sorted(range(V),key=lambda i:(-q[i]/p[i],i));H=0;prefix=[f[H]]
        for i in order:H|=1<<i;prefix.append(f[H])
        assert min(prefix)==min(f)
        if w==(3,3,1):assert min(f)==F(67,70)
        pair_checks.append({'weights':w,'all_subsets':1<<V,'true_optimum':str(min(f))})
    result={'status':'PASS_FINITE_CONTROLS_NOT_A_PROOF_BY_ENUMERATION','independent_of_proposer_imports':True,'ordered_draft_instances':ordered,'cross_multiplied_qconvex_checks':checks,'samplewise_inclusion_checks':inclusion_checks,'cases':cases,'two_draft_controls':pair_checks,'cpu_seconds':time.process_time()-start}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
