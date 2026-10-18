# A speculative-decoding optimum calculation can be arbitrarily inaccurate

An exact counterexample family contradicts the without-replacement optimum calculation in Hu et al., *Towards Optimal Multi-draft Speculative Decoding* (ICLR 2025). The published formula returns 100% while the actual optimum can approach zero under the paper's stated sampling law. An eight-token instance gives 100% versus 79.9555%.

These are our evaluations of the published formula on constructed distributions, not the paper's experimental measurements.

| Exact case | Formula | True optimum |
|---|---:|---:|
| Four tokens, three drafts, original witness | 95% | 100% |
| Four tokens, three drafts, family witness | 100% | 161/176 ≈ 91.4773% |
| Eight tokens, seven drafts, family witness | 100% | 6580499/8230200 ≈ 79.9555% |
| Family n=m², V=n+1, m→∞ | 100% | tends to 0% |

The original witness also makes the paper's recursive-rejection rule achieve 95.5%, above the calculated 95% optimum. The original underestimate invalidates upper-bound validity; the family overestimates invalidate claimed exactness. A 100% estimate remains a valid loose upper bound.

Read [REPORT.md](REPORT.md), the [family proof](family/PROOF.md), the [independent review](family-independent/REVIEW.md), and the [original witness](FOUR-TOKEN-REPORT.md).

## Constructive repair and broader support

The [addendum](addendum/README.txt) supplies a valid exponential-clock proof of q-convexity for the successive sampler. This preserves sorted-prefix minimization, while leaving the published probability evaluator incorrect. For two drafts, a corrected [exact acceptance-value oracle](addendum/repair/repair.py) takes O(V log V) comparisons and O(V) arithmetic operations; it does not construct an optimal verification kernel or claim a runtime speedup. [Proof](addendum/repair/PROOF.md) · [Separate review](addendum/repair-review/REVIEW.md).

A [second proof](addendum/relevance/PROOF.md) extends the discrepancy to **three drafts and every finite vocabulary size V≥5**, with an overestimate of at least **7.4006 percentage points**. The enlarged-vocabulary values are bounds, and the fixed-gap example concentrates 99.9% of its probability on four tokens. A separate corollary permits arbitrarily small total variation between p and q with shrinking positive error. Neither result establishes prevalence in trained models. [Independent bound check](addendum/relevance-review/REVIEW.txt).

## Reproduce

Python 3.8 or newer, standard library only:

```sh
python3 -B verify_all.py
```

The command verifies file integrity and executes separately written rational-arithmetic implementations in an isolated temporary directory. It checks the original witness and RRS rule, both finite family witnesses, every relevant subset cut, explicit output marginals, and positive controls for the alternative product-weighted sampling law. It also replays the repaired two-draft oracle, separate structural-proof controls, and exact large-vocabulary bounds. It does not infer the infinite-family theorem from finite enumeration: that claim has an analytic proof and a separate proof review.

No model inference, API, solver, network or paid compute is needed. Source PDFs are linked and hashed, not redistributed or re-extracted by the verifier. [PACKAGING-NOTES.json](PACKAGING-NOTES.json) records the portability-only changes to frozen source scripts.

## Scope and status

The paper specifies successive renormalized sampling but calculates probabilities for iid draws conditioned on the entire batch being distinct. The latter law makes the disputed formula correct, but changes the stated protocol.

The general transport identity, q-convexity itself, with-replacement results and separate Greedy sampler are not refuted. No experimental table has been corrected and no runtime speedup is claimed. Large-draft asymptotics need not be practical; no frequency of these distributions in trained models has been measured.

A bounded primary-source check found no prior correction, which does not establish priority. A later ICLR 2026 paper invokes the affected calculation in an extension discussion; its main iid algorithm is outside this result. See [NOVELTY-AND-DOWNSTREAM.md](NOVELTY-AND-DOWNSTREAM.md).

Specific novelty and external human scientific validation remain unverified. The derivation, code and separate checks were developed with Codex assistance; separate agent checks are not external human peer review.
