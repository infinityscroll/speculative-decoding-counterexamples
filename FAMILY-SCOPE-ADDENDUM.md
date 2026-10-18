# Release-scope addendum: positive family with V=n+1

**PASS_SOURCE_SCOPE.** No stated assumption in the cached official ICLR 2025 final excludes n=V−1 or the family's strictly positive p,q. This is a source/claim review only; it does not rerun or substitute for the separate independent family proof review.

Source: Hu et al., [*Towards Optimal Multi-draft Speculative Decoding*, final paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf), SHA256 `9df97ac3c93f77bde2f805382b3b523b26e4175c15880302d021c897e9edba7b`.

| Source location | Assumption / claim | Family scope |
|---|---|---|
| §2.1, pp.2–3 | Analysis fixes one context and considers a single generation step. | A fixed finite pair p,q is admissible; no trained-model realization is a theorem hypothesis. |
| §2.3, p.4, Eq.6 | Successive sampling renormalizes q after excluding already sampled tokens. | n draws from V=n+1 positive coordinates leave positive residual mass at every draw. |
| §2.3, p.4, Eq.7 | Arbitrary normalized target p and joint draft law; verification optimizes over couplings with these marginals. | No closeness, shared-ranking, minimum target/draft overlap, or n/V restriction is stated. Randomized conditional verification is allowed. |
| §4.2, p.6, Theorem 6 | Positivity p(x)>0 is required for the q/p ordering argument. | p(common)=w/[n(w+n)] and p(rare)=n/(w+n) are positive for n≥2,w>1. q is also strictly positive. |
| §4.2.1–4.2.2, p.6 | Sorted-prefix computation is stated as equality to the optimum α*, with the elementary-symmetric ratio for Q(H). | This is an exact-optimum claim, not an approximation with an error allowance. |
| Appendix C.2, p.17 | Theorem 4's proof uses the same polynomial-coefficient identity. | No extra n≪V or target/draft similarity assumption repairs the probability substitution. This review does not assert that q-convexity itself is false. |
| §6, pp.7–8 | Real-model experiments and a default of three drafts are described. | Experimental settings do not restrict the theorem. The separate n=3 family instance also matches that draft count; neither instance establishes empirical prevalence. |

The supplied extension reports n=w=7 (V=8): the formula returns 1, while the true successive-law optimum is 6580499/8230200≈0.799555. Its asymptotic n=m²,w=m construction has reported value 1 and true optimum tending to zero. These are exact-family results supplied by the mathematical lane, not new computation in this scope review. They obey the published input domain; the asymptotic draft count is not a claim of practical inference feasibility.

## Crucial wording distinction

For the new family, a reported 100% is still a **valid loose upper bound**. The contradiction is to the claim that the formula computes the exact optimum. Do not say that this overestimation example alone invalidates an upper-bound guarantee. The separately verified four-token example returning 95% when a 100% acceptance coupling is feasible establishes failure of upper-bound validity under the stated law.

A source-faithful release can say the published exact without-replacement computation can be arbitrarily inaccurate under its stated successive sampling law. It cannot infer that the whole paper, iid calculations, the separate Greedy method, measured speedups, or empirical tables are false. No priority claim is supported by the bounded novelty screen. A public release remains outside this task's authorization.
