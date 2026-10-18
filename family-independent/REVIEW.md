# Independent adversarial review of the near-unit-error family

**PASS, with conditions.** For integer n≥1 and real w≥1, the constructed successive-sampling optimum is exactly 1−s+r, while the printed coefficient-ratio/prefix calculation returns 1. The discrepancy is positive for n≥2,w>1. Along n=m²,w=m, it approaches one. All probabilities stay strictly positive at every finite instance.

This is a worst-case counterexample to an exact mathematical calculation, not a measured model effect, an inference improvement, or a refutation of the paper's general transport formulation. It is a posthoc extension of the earlier counterexample. Priority and external human scientific review remain unverified.

## Independent derivation

Let C contain n common tokens, each with raw draft weight w, and let R have raw weight 1. There are V=n+1 tokens and n distinct successive draws. Normalize by nw+1. Define

\[
s=\prod_{j=1}^{n}\frac{jw}{jw+1},\quad
r=\frac{w}{w+n},\quad
p(R)=1-r,\quad p(i)=\frac r n\;(i\in C).
\]

**Successive draft law.** To omit R, every draw must be common. When j common tokens remain, that conditional probability is jw/(jw+1). Thus Pr(all drafts in C)=s.

**Product-weighted draft law.** The all-common n-set has raw weight wⁿ. The n other n-sets each have weight wⁿ⁻¹. Normalizing gives Pr(all drafts in C)=r. This is the law encoded by the elementary-symmetric coefficient ratio, and generally differs from the successive law.

**Feasibility condition.** At n=1, s₁=w/(w+1). If sₙ₋₁≥w/(w+n−1), then

\[
s_n\ge\frac{w}{w+n-1}\frac{nw}{nw+1}\ge\frac{w}{w+n},
\]

because the final comparison, after multiplying positive denominators, is

\[
nw(w+n)-(w+n-1)(nw+1)=(n-1)(w-1)\ge0.
\]

Hence s≥r. Equality holds for n=1 or w=1; strict inequality holds for n≥2,w>1. The gate r/s is therefore a valid probability.

**Upper bound without any disputed theorem.** On E={all drafts in C}, accepted output must be common. Yet the entire output marginal permits only p(C)=r common mass. Since Pr(E)=s, at least s−r probability mass must be rejected on E. Every verifier therefore has acceptance at most 1−s+r.

**Achieving kernel.** If R is drafted, output R. Otherwise output a uniform common draft with probability r/s, and output the absent R with probability 1−r/s. The common output marginal is r/n for each token; R's marginal is (1−s)+(s−r)=1−r. Accepted mass is (1−s)+r. This proves the exact optimum, including a matching explicit feasible kernel.

Under the product-weighted law, output R when present and otherwise a uniform common draft. That always accepts and has the same target marginal. Thus 1 is the correct answer for the alternative sampler.

**Printed prefix computation.** A common token has q/p=n(w+n)/(nw+1), while R has q/p=(w+n)/(n(nw+1)). Their ratio is n². All common tokens precede R for n>1. A prefix of size below n has degree-n coefficient zero, giving objective 1+P(prefix)≥1. At C, both P(C) and the substituted Q(C) equal r, giving 1. At the complete set the objective is also 1. The printed prefix minimum is exactly 1, regardless of ties among the common tokens. The n=1 case also returns 1.

## Asymptotic claim

The elementary inequality 1−∏(1−a_j)≤Σa_j for 0≤a_j≤1 gives

\[
1-s\le\sum_{j=1}^n\frac1{jw+1}\le\frac{H_n}{w},
\quad
0\le A_{\rm seq}=1-s+r\le\frac{H_n}{w}+\frac{w}{w+n}.
\]

For integers m≥2, choose n=m² and w=m. Then

\[
A_{\rm seq}\le\frac{H_{m^2}}m+\frac1{m+1}
\le\frac{1+2\log m}{m}+\frac1{m+1}\longrightarrow0.
\]

Here **H_{m²} is the harmonic number indexed by m²**, not the square of H_m. The printed answer remains 1. Consequently, for every ε>0, a finite strictly positive rational instance exists whose additive overestimate exceeds 1−ε. This means a gap approaching **100 percentage points**; it does not attain a 100-point gap at a finite instance.

## Exact V=8 check

For n=w=7:

\[
q(R)=1/50,\;q(i)=7/50,\quad
p(R)=1/2,\;p(i)=1/14.
\]

| Quantity | Exact value |
|---|---:|
| s, successive rare-absence probability | 5764801/8230200 |
| r, product-weighted rare-absence probability | 1/2 |
| Actual optimum | 6580499/8230200 |
| Printed prefix minimum | 1 |
| Additive overestimate | 1649701/8230200 |

The actual optimum is approximately 0.799555174844, and the overestimate is 20.0444825156 percentage points.

`check.py` independently propagates exact rational probability through chosen-token **subset states** using successive conditional denominators. It does not use the proposer's ordered-tuple enumeration or import any sibling implementation. It checks the explicit kernel's row sums, target marginal and acceptance, all 256 subset objectives, the printed coefficient recurrence and prefix scan, and an exact product-law positive control. Runtime was approximately 0.0112 CPU seconds. No optimizer or model was run.

The independent derivation and checker were completed before inspecting the proposer's `PROOF.md` and without reading its `certificate.py`. Root's expected V=8 numerical answer was received before execution and was treated as a comparison target, not as verification. I subsequently read `PROOF.md`; it agrees with the independent argument. The proposer's additional V=4 enumeration was not replayed in this review.

## Source assumptions and strongest defenses

The cached [final ICLR 2025 paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf), printed pp.4–6 and17, was read for the relevant definitions. Eq.(6) specifies successive renormalization. Eq.(7) allows a joint output/draft distribution with the two specified marginals and rewards output membership in the draft tuple. Section4.2.1 sorts descending q/p; Section4.2.2 substitutes the coefficient ratio. The source requires positive target coordinates for the sorting theorem, which this family supplies. No closeness assumption between p and q or fixed small bound on n appears in these audited statements.

- **Different intended sampler:** the formula is correct under whole-batch conditioning on distinct iid draws. The positive control confirms this. That interpretation changes Eq.(6); it does not save the exact calculation under the stated successive law.
- **V=n+1 or large n is impractical:** valid as a limit on empirical relevance. It does not exclude these instances from the universal finite-distribution claim. The asymptotic discrepancy explicitly allows n and V to grow; it is not a fixed-vocabulary or fixed-draft-count limit.
- **p is far from q:** also a practical limitation, not an unmet mathematical assumption. Every coordinate is positive; there is no zero-support or undefined-renormalization pathology.
- **The rejection kernel outputs an absent token:** permitted by the transport objective. Such mass is counted as rejection, and the target marginal is exact. No acceptance is counted for an absent output.
- **The prefix theorem may still hold for the true successive Q:** this witness does not settle that general question. Indeed, the all-common prefix attains the true optimum here when its actual probability s is used. The contradiction is the wrong substituted probability, not evidence that the general subset identity fails.
- **A loose upper bound of 1 is still valid:** yes, but the audited claim is an exact optimal-value computation. The family shows that its overestimate can be arbitrarily loose. It does not claim that 1 ceases to be an upper bound.
- **Experiments could use another law:** unresolved. No code execution, original model outputs, empirical acceptance curves, or runtime measurements are audited here.

## Verdict and reproducibility

**PASS_THEORETICAL_FAMILY_AND_EXACT_V8_INSTANCE.** The proof establishes arbitrary worst-case additive error for the stated exact calculation, under the documented sampler and acceptance definition. It does not refute q-convexity itself, with-replacement results, the separate Greedy method, or the empirical tables.

Run `python3 -B check.py` in this directory with Python3.8+ and the existing cached source PDF at `../speculative-bound-root/source-final.pdf`. The checker verifies the PDF hash and writes only this directory's `RESULT.json`. PDF SHA256: `9df97ac3c93f77bde2f805382b3b523b26e4175c15880302d021c897e9edba7b`.

This review is part of the same Codex-assisted workflow, not external human peer review. No prior frozen packet was changed, and no public communication or paid computation occurred.
