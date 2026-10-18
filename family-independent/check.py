#!/usr/bin/env python3
"""Independent exact subset-state enumeration for n=7, w=7; no sibling imports."""
from fractions import Fraction as F
from itertools import combinations
from math import prod
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def as_text(x):
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def elementary(weights, mask, degree):
    coeff = [F(1)] + [F(0)]*degree
    for i, weight in enumerate(weights):
        if mask & (1 << i):
            for k in range(degree, 0, -1):
                coeff[k] += weight*coeff[k-1]
    return coeff[degree]


def main():
    start = time.process_time()
    n, w = 7, 7
    # Token zero is rare; tokens 1..n are common.
    weights = [1] + [w]*n
    q = [F(x, sum(weights)) for x in weights]
    r = F(w, w+n)
    p = [1-r] + [r/n]*n
    full = (1 << (n+1))-1
    common = full ^ 1
    # Exact aggregation over chosen-token sets. Transition denominators depend
    # only on the chosen set, so this sums every ordered history without
    # assuming a product-weighted unordered law.
    law = {0: F(1)}
    state_counts = [1]
    for _ in range(n):
        next_law = {}
        for mask, mass in law.items():
            remaining_weight = sum(weight for i, weight in enumerate(weights)
                                   if not mask & (1 << i))
            for i, weight in enumerate(weights):
                if not mask & (1 << i):
                    dest = mask | (1 << i)
                    next_law[dest] = next_law.get(dest, F(0)) + mass*F(weight,remaining_weight)
        law = next_law
        assert sum(law.values()) == 1
        state_counts.append(len(law))
    s_closed = prod(F(j*w,j*w+1) for j in range(1,n+1))
    s = law[common]
    assert s == s_closed and s >= r
    alpha = 1-s+r
    # The kernel is explicitly allowed to output the absent rare token on
    # rejection. Its accepted outputs always belong to the draft set.
    marginal = [F(0)]*(n+1)
    accepted = F(0)
    kernels = {}
    for mask, mass in law.items():
        if mask & 1:
            kernel = [F(1)] + [F(0)]*n
        else:
            kernel = [1-r/s] + [r/(n*s)]*n
        assert sum(kernel) == 1 and min(kernel) >= 0
        for i, output_mass in enumerate(kernel):
            marginal[i] += mass*output_mass
            if mask & (1 << i):
                accepted += mass*output_mass
        kernels[str(mask)] = list(map(as_text,kernel))
    assert marginal == p and accepted == alpha
    # Independently evaluate the printed coefficient ratio for every H.
    denom = elementary(q,full,n)
    printed_q = {mask:elementary(q,mask,n)/denom for mask in range(full+1)}
    actual_q = {mask:sum((mass for draft,mass in law.items() if draft & mask == draft),F(0))
                for mask in range(full+1)}
    pset = {mask:sum((p[i] for i in range(n+1) if mask & (1 << i)),F(0))
            for mask in range(full+1)}
    true_cut_min = min(1+pset[mask]-actual_q[mask] for mask in range(full+1))
    printed_cut_min = min(1+pset[mask]-printed_q[mask] for mask in range(full+1))
    order = sorted(range(n+1), key=lambda i:q[i]/p[i], reverse=True)
    prefix, prefix_values = 0, [F(1)]
    for i in order:
        prefix |= 1 << i
        prefix_values.append(1+pset[prefix]-printed_q[prefix])
    assert true_cut_min == alpha and 1+pset[common]-actual_q[common] == alpha
    assert printed_cut_min == min(prefix_values) == 1
    assert printed_q[common] == r
    # Positive control: exact product weights over all n-subsets.
    product_law = {}
    for subset in combinations(range(n+1),n):
        mask = sum(1 << i for i in subset)
        product_law[mask] = prod(q[i] for i in subset)/denom
    assert sum(product_law.values()) == 1
    control_marginal = [F(0)]*(n+1)
    for mask,mass in product_law.items():
        if mask & 1:
            control_marginal[0] += mass
        else:
            for i in range(1,n+1): control_marginal[i] += mass/n
    assert control_marginal == p
    result = {
        'status':'PASS_EXACT_V8_CASE', 'n':n,'w':w,'q':list(map(as_text,q)),
        'p':list(map(as_text,p)), 'subset_state_counts_by_depth':state_counts,
        'subsets_checked':full+1,'successive_draft_set_law':{str(k):as_text(v) for k,v in law.items()},
        'rare_absence_successive_s':as_text(s),'rare_absence_product_r':as_text(r),
        'true_optimum':as_text(alpha),'true_optimum_decimal':float(alpha),
        'printed_full_cut_minimum':as_text(printed_cut_min),
        'printed_prefix_minimum':as_text(min(prefix_values)),
        'additive_overestimate':as_text(1-alpha),'percentage_point_overestimate':float(100*(1-alpha)),
        'kernel_rows':kernels,'verified_target_marginal':list(map(as_text,marginal)),
        'product_law_positive_control_acceptance':'1',
        'declared_source_pdf_sha256':'9df97ac3c93f77bde2f805382b3b523b26e4175c15880302d021c897e9edba7b',
        'cpu_seconds':time.process_time()-start,
        'scope':'Finite exact check; asymptotic proof is in REVIEW.md. No model experiment or q-convexity counterexample.'}
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','rare_absence_successive_s','rare_absence_product_r','true_optimum','percentage_point_overestimate','cpu_seconds']},indent=2))


if __name__ == '__main__':
    main()
