"""Exact optimal acceptance value for two successive distinct drafts."""
from fractions import Fraction as F

def two_draft_optimal_acceptance(p, q, *, return_trace=False):
    """Positive rational probabilities. Returns the optimum, optionally a trace.

    O(V log V) comparisons and O(V) arithmetic operations, not a bit-cost bound.
    This computes the optimal value; it does not construct a verification kernel.
    The default uses constant scan state beyond the sorted inputs. Optional trace
    stores one order plus constant-sized scalar state per prefix, not prefix copies.
    """
    p, q = tuple(map(F, p)), tuple(map(F, q))
    if len(p) != len(q) or len(p) < 2:
        raise ValueError("Equal vocabulary sizes at least two are required")
    if any(x <= 0 for x in p + q) or sum(p) != 1 or sum(q) != 1:
        raise ValueError("Strictly positive probability vectors are required")
    order = tuple(sorted(range(len(p)), key=lambda i: (-q[i]/p[i], i)))
    a = b = c = F(0)
    best = F(1)
    states = [{"prefix_length": 0, "q_mass": a, "q_odds_sum": b, "p_mass": c,
               "Q": F(0), "objective": best}] if return_trace else None
    for count, i in enumerate(order, 1):
        a += q[i]
        b += q[i]/(1-q[i])
        c += p[i]
        Q = a-(1-a)*b
        objective = 1+c-Q
        best = min(best, objective)
        if return_trace:
            states.append({"prefix_length":count, "q_mass":a, "q_odds_sum":b,
                           "p_mass":c, "Q":Q, "objective":objective})
    return (best, {"order":order,"states":states}) if return_trace else best
