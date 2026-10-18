# A claimed speculative-decoding optimum is below an achievable acceptance rate

An exact four-token counterexample contradicts the efficient without-replacement acceptance calculation in Hu et al., *Towards Optimal Multi-draft Speculative Decoding* (ICLR 2025). The paper's calculation returns **95%**, while a valid verifier achieves **100%** under the paper's stated draft law. Its recursive-rejection baseline also achieves **95.5%**, exceeding the calculated optimum.

This is a counterexample to a universal mathematical computation, using a small distribution that satisfies its assumptions. It is not a measured language-model speedup or a corrected experimental table.

## The mismatch

The [final paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf) defines successive draws in Eq. (6), printed page 4: after each draw, remove that token and renormalize the remaining probabilities. In Section 4.2.2, printed page 6, it computes the event that all drafts lie in a set H using

`Q(H) = e_n(q_H) / e_n(q)`,

where `e_n` is the elementary symmetric polynomial of degree n. That ratio instead describes independent draws conditioned on the *entire batch* being distinct. Changing from ordered tuples to unordered subsets does not equate these two probabilities.

The same substitution appears in the proof of Theorem 4 on printed page 17. This invalidates that proof step under Eq. (6); it does **not** by itself disprove q-convexity. The independent source check used the final PDF, SHA256 `9df97ac3c93f77bde2f805382b3b523b26e4175c15880302d021c897e9edba7b`.

## An exact counterexample

Use three drafts and four tokens, with strictly positive probabilities:

```
draft q  = (1/2,   1/6,  1/6,  1/6)
target p = (19/20, 1/60, 1/60, 1/60)
```

Under successive sampling, the probability that token 0 never appears is

`(1/2) × (2/5) × (1/4) = 1/20`.

Output token 0 whenever it appears; otherwise output the first draft. This always outputs a drafted token. The output probability of token 0 is 19/20. Symmetry gives probability 1/60 for each other token. The output marginal therefore equals p exactly, and acceptance is 100%.

For `H={1,2,3}`, the paper's formula gives

`Q(H) = (1/216)/(10/216) = 1/10`,

although the actual probability is 1/20. Its sorted-prefix calculation includes H because the three low tokens have q/p ratio 10, greater than token 0's ratio 10/19. It returns

`1 + P(H) − Q(H) = 1 + 1/20 − 1/10 = 19/20`.

The remaining prefixes give larger values. Thus the published procedure reports a 95% optimum despite an explicit 100% feasible verifier.

## The paper's baseline also exceeds the calculated optimum

The recursive rejection rule in Appendix A.1, Eq. (27), printed page 14, uses successive renormalization. An independent exact replay on the same p and q gives output marginal p and acceptance **191/200 = 95.5%**. This is already **1/200 = 0.5 percentage point** above the formula's 95%.

This additional check avoids depending only on our specially chosen verifier. It remains a finite mathematical example, not a claim that the paper's reported empirical baseline exceeds its reported empirical curve.

## Reproduction and scope

`verify.py` enumerates all 24 ordered draft tuples and all 16 subsets using standard-library rational arithmetic. It verifies the feasible coupling, output marginal, and both subset minima. `verify_rrs.py` separately replays the recursive rejection rule and verifies its output marginal. A second agent wrote separate rational implementations; an adversarial source review is recorded separately. These are separate checks within a Codex-assisted workflow, not external human validation.

The elementary-symmetric formula is correct for the product-weighted, distinct-batch law. A separate positive-control coupling attains 95% under that law. Repairing the paper by adopting that sampler changes Eq. (6) and the relevant baseline comparison.

The following remain intact or unestablished:

- The general optimal-transport/subset-selection identity, the with-replacement results, and the separate Greedy sampler are not refuted.
- Q-convexity for successive sampling has not been disproved. A bounded exact scan found no violation; that is not a proof.
- No released per-context logits or executed implementation were located in the bounded search. We have not corrected the experimental tables or measured runtime consequences.
- The distinction between the two sampling laws is standard probability. Specific priority for this paper correction remains unverified. Targeted searches found no explicit correction, and current arXiv lists only v1; OpenReview discussion was inaccessible behind a verification challenge.
- The later *Global Resolution* paper invokes the without-replacement formula in an extension discussion. Its demonstrated iid method is outside this finding's scope.

This result was developed and checked with Codex assistance. No model inference or paid compute was required. Public release and author review are pending.
