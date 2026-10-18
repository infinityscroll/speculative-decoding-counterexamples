# A family with arbitrarily large acceptance-bound error

**Posthoc extension of the frozen four-token counterexample.** This packet concerns the published exact without-replacement acceptance calculation. It is not a decoding speedup, a model experiment, or an empirical table correction. No claim of novelty is made for the standard distinction between successive and product-weighted sampling.

## Definition and source scope

Fix an integer n≥2 and a rational w>1. The vocabulary has n common tokens C={1,…,n} and one rare token R, so V=n+1 and n<V. Set

q(i)=w/(nw+1) for i∈C, and q(R)=1/(nw+1).

Sample n distinct drafts successively, each time renormalizing q over the remaining tokens. This is the law in Hu et al., *Towards Optimal Multi-draft Speculative Decoding*, [ICLR 2025 final paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf), Eq. (6), printed p. 4.

Define

s = ∏(j=1,…,n) jw/(jw+1),       r = w/(w+n),

and the target

p(i)=r/n for i∈C, and p(R)=1−r.

Every p and q coordinate is strictly positive. The final paper's Section 4.2.2, printed p. 6, uses the elementary-symmetric-polynomial ratio for the all-in-H probability. Appendix C.2, printed p. 17, uses the same ratio. The original frozen source packet documents that these passages also remain in the sole current arXiv v1.

## The two all-common probabilities

Let E be the event that the n drafts contain only common tokens. Under successive sampling, once j common tokens and R remain, the next draw is common with probability jw/(jw+1). Hence Pr_seq(E)=s.

Under the different product-weighted fixed-size law (iid drafts conditioned on being distinct), the all-common set has weight w^n. Each of the n possible sets containing R has weight w^(n−1). Therefore

Pr_product(E) = w^n / (w^n + n w^(n−1)) = r.

These probabilities are order-invariant; forgetting the draft order cannot make the laws coincide.

## Feasibility of the coupling: s≥r

Write s_n(w)=∏(j=1,…,n) jw/(jw+1). At n=1, s_1(w)=w/(w+1). If s_(n−1)(w)≥w/(w+n−1), then

s_n(w) ≥ [w/(w+n−1)] [nw/(nw+1)] ≥ w/(w+n),

where the second inequality follows from

nw(w+n) − (w+n−1)(nw+1) = (n−1)(w−1) ≥ 0.

Thus s≥r; for n≥2 and w>1 the inequality is strict. In particular 0<r/s<1, so the verifier below uses valid probabilities.

## Exact successive-sampling optimum

Use the following conditional verifier:

1. If R is among the drafts, output R.
2. Otherwise, with probability r/s output a uniformly selected common draft; with probability 1−r/s output R as a rejection/resampling result.

The total output mass assigned to common tokens is s(r/s)=r, equally divided among n tokens. The output mass of R is (1−s)+s(1−r/s)=1−r. The output marginal is therefore exactly p.

This verifier accepts precisely on the event R is drafted, plus the common-output portion of E. Its acceptance is

**A_seq(n,w) = 1−s+r.**

It is optimal without invoking a numerical solver or any disputed theorem. E has probability s, while the entire target distribution assigns only r mass to common tokens. At least s−r mass of E must therefore output R outside the draft set. Every valid coupling rejects at least s−r, giving acceptance at most 1−s+r. The constructed verifier attains that bound.

For the product-weighted law, output R when present and otherwise choose a uniform common draft. Since Pr_product(E)=r, this yields p and always accepts. Its exact optimum is 1. This is the positive control for the alternate sampling-law interpretation.

## What the published computation returns

For a common token the q/p ratio is n(w+n)/(nw+1); for R it is (w+n)/(n(nw+1)). Their ratio is n². Thus the paper's descending q/p order puts all common tokens before R, with arbitrary order among commons.

For every prefix of size k<n, the degree-n elementary symmetric polynomial is zero, so its reported objective is 1+P(prefix)≥1. At the n-common prefix, P(C)=r and the substituted Q(C)=r, giving objective 1. The empty and complete prefixes also give 1. Therefore its sorted-prefix algorithm returns

**A_reported(n,w) = 1.**

The exact overestimate is **s−r**, not an approximation or floating-point effect. Reinterpreting the formula under product-weighted batch conditioning makes it correct, but changes Eq. (6)'s sampling law.

## The error can approach one

For any a_j∈[0,1], the elementary product inequality gives 1−∏(1−a_j)≤Σ a_j. Applying a_j=1/(jw+1) yields

1−s ≤ Σ(j=1,…,n) 1/(jw+1) ≤ H_n/w,

where H_n=Σ(j=1,…,n)1/j. Consequently

A_seq(n,w) ≤ H_n/w + w/(w+n).

Choose n=m² and w=m for integers m≥2. Then

0≤A_seq(m²,m) ≤ H_(m²)/m + 1/(m+1)
                 ≤ (1+2 log m)/m + 1/(m+1) → 0.

The reported value stays 1. Hence for every ε>0, sufficiently large m gives a strictly positive rational p,q with n<V for which the reported optimum is 1 while the actual optimum is below ε. The discrepancy approaches 100 percentage points. This is an asymptotic mathematical construction, not a statement that large draft counts are operationally practical or that this distribution occurs in a trained model.

## Small exact witnesses and verification

The fixed local certificate evaluates only (n,w)=(3,5) and (7,7), independently aggregating every ordered distinct draft tuple using the successive conditional probabilities. It then checks both coupling marginals and all subset objectives by exact rational arithmetic.

The first witness keeps the paper's default n=3 and has V=4:

q(common)=5/16, q(R)=1/16;
p(common)=5/24, p(R)=3/8.

Here s=125/176, r=5/8, and A_seq=161/176≈91.4773%, while the reported value is 100%. Its exact gap is 15/176≈8.5227 percentage points. The rejection probability on E is only 3/25; there are no zero-probability coordinates.

The second witness has V=8, n=7, w=7:

q(common)=7/50, q(R)=1/50;
p(common)=1/14, p(R)=1/2.

RESULT.json records its exact product s, optimum, gap, all subset values, and the explicit coupling masses. No optimizer or model is run. This eight-token instance was selected after deriving the family; it is posthoc diagnostic evidence, not a preregistered empirical evaluation.

## Decision and limits

GO for independent mathematical review of a substantially stronger formal counterexample. NO_GO as an implemented inference enhancement or empirical performance claim. No original author code or experimental outputs were obtained here. This extension does not refute the general transport formulation, q-convexity itself, with-replacement calculations, or the separate Greedy sampler. It establishes that the stated efficient without-replacement calculation can be arbitrarily wrong under its own specified successive law. The original certificate and manifest are untouched.
