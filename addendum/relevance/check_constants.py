#!/usr/bin/env python3
"""Finite rational constants for the analytical embedding; no sweeps or models."""
from fractions import Fraction as F
from math import prod
from pathlib import Path
import json
import time

start = time.process_time()
w, eps = F(5), F(1,1000)
t = eps/(1-eps)
r = w/(w+3)
e2 = 3*w*(w+1)/(3*w+1)**2
e3 = w*w*(w+3)/(3*w+1)**3
assert (e2,e3)==(F(45,128),F(25,512))
s_eps = prod(j*w/(j*w+1+(3*w+1)*t) for j in range(1,4))
delta_bound = (e2/e3)*t + t*t/(2*e3) + t*t*t/(6*e3)
printed_lower = 1-eps-delta_bound
actual_upper = 1+(1-eps)*r-s_eps
gap_lower = printed_lower-actual_upper
assert gap_lower > F(7,100)
tv = (1-eps)*8*w/((w+3)*(3*w+1))
# Exact base factorization at this fixed witness. The general identity and
# arbitrary-vocabulary bounds are proved analytically in PROOF.md.
s = prod(j*w/(j*w+1) for j in range(1,4))
g = w*(w-1)*(7*w+1)/((w+3)*(w+1)*(2*w+1)*(3*w+1))
assert s-r == g == F(15,176)
result = {'status':'PASS_FIXED_RATIONAL_CONSTANTS',
          'uniform_vocabulary_scope':'All finite V>=5, n=3, extra tokens each p=q=1/[1000(V-4)]',
          'w':str(w),'epsilon':str(eps),
          'exact':{k:str(v) for k,v in [('s_epsilon',s_eps),('product_law_TV_upper',delta_bound),
                   ('printed_value_lower',printed_lower),('actual_optimum_upper',actual_upper),
                   ('overestimate_lower',gap_lower),('target_draft_TV',tv)]},
          'decimal':{'printed_value_lower':float(printed_lower),'actual_optimum_upper':float(actual_upper),
                     'overestimate_lower_percentage_points':float(100*gap_lower),'target_draft_TV':float(tv)},
          'meaning':'Bounds on enlarged-vocabulary values, not exact optima. Arbitrary-vocabulary and close-distribution theorems are analytical.',
          'scientific_compute':'No sweep, optimizer, model inference, or large-vocabulary enumeration.',
          'cpu_seconds':time.process_time()-start}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
