# Exact acceptance calculations under two different sampling laws

The [ICLR 2025 final paper by Hu et al.](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf), Eq. (6), defines successive sampling without replacement: each draw removes its token and renormalizes the remaining draft probabilities. Section 4.2.2 instead computes the probability that every draft lies in H as e_n(q_H)/e_n(q). That ratio describes iid draws conditioned on the whole batch being distinct. The laws generally differ even after discarding order.

This substitution affects a claimed exact calculation, not merely notation. The finite examples and analytic family below satisfy the stated positivity and draft-count assumptions. Exact rational computation checks the finite examples; the asymptotic conclusion follows from a proof.

## An arbitrarily large error in the exact optimum

Take n common tokens with raw draft weight w>1 each and one rare token with weight 1. Draw n of the V=n+1 tokens. Define

s = product over j=1,…,n of jw/(jw+1),
r = w/(w+n),
p(rare)=1−r, and p(each common)=r/n.

All probabilities are positive. The event that every draft is common has probability s under successive sampling and r under the formula's product-weighted law.

A valid verifier outputs the rare token whenever it is drafted. When all drafts are common, it outputs a uniform common token with probability r/s and otherwise outputs the rare token as a rejection. Its output marginal is exactly p. Induction proves s≥r, so the kernel probabilities are valid.

Its acceptance equals **1−s+r**. This is also an upper bound: the all-common draft event has mass s, but the target allocates only r mass to common tokens, forcing at least s−r rejection mass. Thus the verifier is optimal.

The published calculation returns **1**. All common tokens precede the rare token in the q/p prefix ordering. Prefixes shorter than n have zero degree-n coefficient; the all-common prefix has substituted Q=r=P; the empty and complete prefixes also give objective 1.

For n=w=7, the normalized distributions are q(rare)=1/50, q(each common)=7/50, p(rare)=1/2, and p(each common)=1/14. Here

s=5764801/8230200,
true optimum=6580499/8230200≈79.9555%,
calculated optimum=100%.

The gap is **20.0445 percentage points**. With only three drafts and four tokens, w=5 gives true optimum 161/176≈91.4773% versus calculated 100%.

For any n,w, 1−s≤H_n/w, where H_n is the nth harmonic number. Choose n=m² and w=m. Then

0≤true optimum≤H_(m²)/m+1/(m+1)≤(1+2 log m)/m+1/(m+1)→0.

The formula remains 1, so its additive error approaches 100 percentage points. This is a worst-case mathematical statement. It makes no claim about feasible runtime at growing draft counts or prevalence in model logits.

The complete proof and explicit kernels are in [family/PROOF.md](family/PROOF.md). An independently derived proof and subset-state implementation are in [family-independent/REVIEW.md](family-independent/REVIEW.md).

## The opposite error also occurs

For three drafts with q=(1/2,1/6,1/6,1/6) and p=(19/20,1/60,1/60,1/60), successive sampling omits token zero with probability 1/20. Output zero if drafted, otherwise the first draft. This gives exact marginal p and always accepts.

The published calculation returns 19/20. The paper's own recursive-rejection rule gives 191/200. Thus the calculation can also fall below a feasible acceptance rate: it is not universally a valid upper bound for the stated law. See [FOUR-TOKEN-REPORT.md](FOUR-TOKEN-REPORT.md).

## What this establishes

This refutes the claimed exact without-replacement computation under Eq. (6). Replacing the stated sampler with the product-weighted law repairs these formulas and positive controls, but changes the protocol. The general transport characterization, q-convexity itself, with-replacement results, Greedy method and empirical tables have not been refuted.

Independent implementation checks and adversarial source review pass within a Codex-assisted workflow. Specific novelty, external human review and empirical impact remain unverified. The proof does not require paid compute. This research packet was prepared on 18 October 2026.
