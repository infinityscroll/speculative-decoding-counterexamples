# Independent adversarial review: the counterexample survives

**Confirmed:** the final paper's efficient acceptance calculation can return 95% for its stated draft law when a valid verifier accepts 100%. This is a false exact-bound claim for the successive-without-replacement case, not a refutation of the whole paper. The independently implemented RRS baseline also exceeds the alleged bound at 95.5%.

I independently downloaded the [final ICLR 2025 paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf) and checked printed pages 4, 6, 14, 17. The [current arXiv history](https://arxiv.org/abs/2502.18779) lists only v1; its equations agree with the final proceedings on the audited passages. The final PDF's SHA256 is `9df97ac3c93f77bde2f805382b3b523b26e4175c15880302d021c897e9edba7b`.

## What is actually contradicted

Eq. (6) defines successive weighted draws, each excluding previous tokens and renormalizing the remaining original q. Section 4.2.2 substitutes an elementary-symmetric-polynomial ratio for the probability that every draft belongs to H. That ratio instead describes iid draws conditioned on the entire batch being distinct. Section 4.2.1 then uses the substituted probabilities to report an exact optimal acceptance rate. Appendix C's proof of Theorem 4 also uses the incorrect identity.

For q=(1/2,1/6,1/6,1/6), p=(19/20,1/60,1/60,1/60), and three drafts, all assumptions needed for this witness hold: distributions are normalized, all probabilities are positive, and the draft count is smaller than the vocabulary. Under Eq. (6), the probability token 0 is absent is

(1/2)(2/5)(1/4)=1/20.

Output token 0 whenever present; otherwise output the first draft. This deterministic rule always returns a draft. Symmetry of the three minor tokens gives output marginal p exactly. Hence acceptance is 1, and 1 is necessarily optimal.

For H={1,2,3}, the paper substitutes Q(H)=1/10 while P(H)=1/20. The q/p order places these three tokens first, so the prescribed prefix scan returns 1+1/20−1/10=19/20. The discrepancy is exact. It does not depend on floating-point error, estimation, order-tie selection, or inference timing.

## Strongest defenses

The most favorable interpretation is that the intended sampler was iid with whole-batch rejection on any duplicate. Under that **different law**, the formula is correct, and an independently checked coupling attains 19/20. But this changes Eq. (6) and its relationship to the sequential RRS baseline in Eq. (27). It cannot preserve both statements as written.

Treating tuples as unordered does not help: the event that every draft belongs to H is order-invariant and still has the two different probabilities. Resampling only a duplicate slot produces the successive law, not the whole-batch-conditioned law. Reinterpreting q as transformed weights would require an absent parameter transformation and equivalence proof.

Nor is the verifier inadmissible: the paper's transport formulation permits an arbitrary conditional output kernel after observing all drafts, subject to the two marginals. The rule above satisfies that definition. There is no requirement that p be close to q or that acceptance use only the first draft. An unpublished corrected implementation could affect the interpretation of experiments, but it cannot make the printed universal calculation true.

## Independent checks and scope

`independent_replay.py` builds the successive law recursively, independently generates all 64 iid batches before conditioning on distinctness, evaluates all 16 subsets, and checks row normalization, target marginals and acceptance for three kernels. It imports no parent or sibling certificate. It obtains:

| Quantity | Exact value |
|---|---:|
| True successive-law optimum |1|
| Published calculation |19/20|
| Eq. (27) RRS acceptance under successive draws |191/200|
| Optimum under the alternative product-weighted law |19/20|

Run:

```sh
python3 independent_replay.py
```

The general optimal-transport/subset identity survives. Theorem 4's proof step is invalid, but **q-convexity itself has not been disproved**. With-replacement results, the separate Greedy protocol, empirical tables, and real-model speedups are not refuted here. No efficient replacement algorithm or new inference enhancement is claimed.

The result supports a carefully scoped private correction candidate. Novelty priority and absence of prior reports remain unestablished; no public outreach or paid computation occurred.
