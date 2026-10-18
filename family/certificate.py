#!/usr/bin/env python3
"""Two fixed exact witnesses; no solver, search, inference, or original imports."""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
started = time.process_time()

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def product(values):
    out = F(1)
    for value in values:
        out *= value
    return out

def check(n, w):
    assert n >= 2 and w > 1
    rare, V = n, n + 1
    tokens = tuple(range(V))
    weights = (w,) * n + (1,)
    weight_sum = sum(weights)
    q = tuple(F(x, weight_sum) for x in weights)
    r = F(w, w+n)
    s = product(F(j*w, j*w+1) for j in range(1,n+1))
    p = (r/n,) * n + (1-r,)
    assert all(x > 0 for x in p+q) and sum(p) == sum(q) == 1
    assert 0 < r < s < 1

    # Independently enumerate the successive law, without using its closed-form s.
    sequential = defaultdict(F)
    ordered_count = 0
    for t in permutations(tokens, n):
        probability = F(1)
        available = weight_sum
        for token in t:
            probability *= F(weights[token], available)
            available -= weights[token]
        sequential[tuple(sorted(t))] += probability
        ordered_count += 1
    assert sum(sequential.values()) == 1
    commons = tuple(range(n))
    assert sequential[commons] == s

    set_weights = {S: product(weights[i] for i in S) for S in combinations(tokens,n)}
    normalizer = sum(set_weights.values())
    rejective = {S: value / normalizer for S, value in set_weights.items()}
    assert sum(rejective.values()) == 1 and rejective[commons] == r

    def coupling(law, mode):
        marginal = [F(0)] * V
        acceptance = F(0)
        rows = []
        for S in sorted(law):
            conditional = [F(0)] * V
            if rare in S:
                conditional[rare] = F(1)
            else:
                keep = r/s if mode == "successive" else F(1)
                conditional[rare] = 1-keep
                for token in S:
                    conditional[token] = keep/n
            assert sum(conditional) == 1 and all(x >= 0 for x in conditional)
            joint = [law[S]*x for x in conditional]
            for token in tokens:
                marginal[token] += joint[token]
                if token in S:
                    acceptance += joint[token]
            rows.append({"draft_set":S,"draft_mass":law[S],"kernel":conditional,"joint":joint})
        assert tuple(marginal) == p
        return {"output_marginal":marginal,"acceptance":acceptance,"rows":rows}

    seq_witness = coupling(sequential,"successive")
    rej_witness = coupling(rejective,"rejective")
    assert seq_witness["acceptance"] == 1-s+r
    assert rej_witness["acceptance"] == 1

    subsets = []
    for k in range(V+1):
        for H in combinations(tokens,k):
            Hset = set(H)
            P = sum((p[i] for i in H),F(0))
            Qseq = sum((mass for S,mass in sequential.items() if set(S)<=Hset),F(0))
            Qrej = sum((mass for S,mass in rejective.items() if set(S)<=Hset),F(0))
            en = sum((product(weights[i] for i in S) for S in combinations(H,n)),F(0))
            assert Qrej == en/normalizer
            subsets.append({"H":H,"P":P,"Q_successive":Qseq,"Q_product_formula":Qrej,
                            "actual_objective":1+P-Qseq,"formula_objective":1+P-Qrej})
    actual_min = min(row["actual_objective"] for row in subsets)
    formula_min = min(row["formula_objective"] for row in subsets)
    order = tuple(sorted(tokens,key=lambda i:(-q[i]/p[i],i)))
    assert order == tokens
    prefix_set = {tuple(order[:k]) for k in range(V+1)}
    prefix_min = min(row["formula_objective"] for row in subsets if row["H"] in prefix_set)
    assert actual_min == 1-s+r and formula_min == prefix_min == 1
    return {"n":n,"w":w,"V":V,"p":p,"q":q,"s":s,"r":r,"gap":s-r,
            "actual_optimum":actual_min,"reported_prefix_value":prefix_min,
            "all_subsets_product_minimum":formula_min,"ordered_drafts_enumerated":ordered_count,
            "subsets_enumerated":len(subsets),"successive_coupling":seq_witness,
            "rejective_positive_control":rej_witness,"all_subset_values":subsets}

def encode(x):
    if isinstance(x,F): return {"exact":str(x),"decimal":float(x)}
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encode(v) for v in x]
    return x

cases = [check(3,5),check(7,7)]
assert cases[0]["actual_optimum"] == F(161,176)
assert cases[0]["gap"] == F(15,176)
assert cases[1]["gap"] > F(1,5)
result = {"status":"PASS_TWO_EXACT_FIXED_WITNESSES","posthoc":True,"cases":cases,
          "cpu_seconds":time.process_time()-started,
          "script_sha256":hash_file(Path(__file__)),
          "asymptotic_proof":"PROOF.md; not inferred from finite cases",
          "limits":["No model inference or empirical speedup claim","No author-code or experiment-table correction","Finite verifier does not establish novelty"]}
(HERE/"RESULT.json").write_text(json.dumps(encode(result),indent=2)+"\n")
brief={"status":result["status"],"cpu_seconds":result["cpu_seconds"],"script_sha256":result["script_sha256"],
       "cases":[{k:case[k] for k in ("n","w","V","s","r","gap","actual_optimum","reported_prefix_value","ordered_drafts_enumerated")} for case in cases]}
print(json.dumps(encode(brief),indent=2))
