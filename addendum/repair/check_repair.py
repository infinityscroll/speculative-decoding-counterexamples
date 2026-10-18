#!/usr/bin/env python3
"""Fixed exact checks against direct ordered-pair/subset enumeration."""
from fractions import Fraction as F
from itertools import permutations, combinations
from pathlib import Path
import hashlib
import json
import time
from repair import two_draft_optimal_acceptance

HERE = Path(__file__).resolve().parent
started = time.process_time()

def normalized(weights):
    total = sum(weights)
    return tuple(F(x, total) for x in weights)

inputs = [
    ((F(3,10),F(3,10),F(2,5)), (F(3,7),F(3,7),F(1,7))),
    (normalized((19,1,1,1)), normalized((5,3,2,1))),
    (normalized((1,3,5,7,9)), normalized((9,7,5,3,1))),
    (normalized(tuple(range(1,9))), normalized(tuple(range(8,0,-1)))),
]
cases = []
for p,q in inputs:
    V = len(p)
    law = {(i,j):q[i]*q[j]/(1-q[i]) for i,j in permutations(range(V),2)}
    assert sum(law.values()) == 1
    optimum = two_draft_optimal_acceptance(p,q)
    traced_optimum, trace = two_draft_optimal_acceptance(p,q,return_trace=True)
    assert optimum == traced_optimum
    prefixes = trace["states"]
    assert len(prefixes) == V+1 and len(trace["order"]) == V
    assert all("prefix" not in state for state in prefixes)
    subset_rows = []
    for size in range(V+1):
        for H in combinations(range(V),size):
            S = set(H)
            direct_Q = sum((mass for (i,j),mass in law.items() if i in S and j in S),F(0))
            a = sum((q[i] for i in H),F(0))
            b = sum((q[i]/(1-q[i]) for i in H),F(0))
            assert direct_Q == a-(1-a)*b
            P = sum((p[i] for i in H),F(0))
            subset_rows.append({"H":H,"direct_Q":direct_Q,"objective":1+P-direct_Q})
    assert optimum == min(row["objective"] for row in subset_rows)
    for state in prefixes:
        prefix = set(trace["order"][:state["prefix_length"]])
        row = next(row for row in subset_rows if set(row["H"]) == prefix)
        assert state["Q"] == row["direct_Q"]
    cases.append({"V":V,"p":p,"q":q,"ordered_pairs":len(law),"subsets":len(subset_rows),
                  "corrected_optimum":optimum,"prefix_trace":trace,"subset_rows":subset_rows})
assert cases[0]["corrected_optimum"] == F(67,70)

def encode(x):
    if isinstance(x,F): return {"exact":str(x),"decimal":float(x)}
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encode(v) for v in x]
    return x

result = {"status":"PASS_EXACT_TWO_DRAFT_REPAIR_CHECKS","cases":cases,
          "total_ordered_pairs":sum(x["ordered_pairs"] for x in cases),
          "total_subsets":sum(x["subsets"] for x in cases),
          "cpu_seconds":time.process_time()-started,
          "scope":"Implementation check; general q-convexity and prefix proofs are in PROOF.md",
          "repair_sha256":hashlib.sha256((HERE/"repair.py").read_bytes()).hexdigest(),
          "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/"RESULT.json").write_text(json.dumps(encode(result),indent=2)+"\n")
print(json.dumps(encode({k:result[k] for k in ("status","total_ordered_pairs","total_subsets","cpu_seconds","repair_sha256","checker_sha256")}),indent=2))
