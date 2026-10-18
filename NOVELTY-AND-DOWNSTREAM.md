# Bounded correction-status check — 18 October 2026

**No prior correction was found in this ten-request primary-source screen. Novelty and priority remain unestablished.** The meaningful new finding is that the official ICLR 2026 final of *Global Resolution* still relies on the affected Hu calculation; checking its November 2025 arXiv version alone would have been insufficient.

## Current source boundary

Hu et al.'s [official ICLR 2025 final](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf) defines successive renormalized sampling without replacement in Eq.6 (p.4), but substitutes the elementary-symmetric ratio in §4.2.2 (p.6). Our earlier independent exact replay establishes a false numerical optimum under that stated law: 19/20 computed, versus feasible and optimal 1; its Eq.27 RRS baseline attains 191/200. This gate did not rerun or modify those verifiers. The checked Hu arXiv record listed only v1; that fact does not rule out a separate erratum or code change.

The elementary-symmetric expression is valid for product-weighted subsets, equivalently an iid batch conditioned on all tokens being distinct. Adopting that interpretation changes Eq.6's probability law. The distinction between these sampling laws is established mathematics; our potential contribution is identifying its specific use in this published exact-bound claim, not discovering the distinction.

## Later final paper: reliance persists

The [official final record](https://proceedings.iclr.cc/paper_files/paper/2026/hash/83995c2acef585ae0f0d647154cfdd85-Abstract-Conference.html) identifies Rahul Thomas and Arka Pal's paper as *Global Resolution: Optimal Multi-Draft Speculative Sampling via Convex Optimization*, ICLR 2026, published 20 April 2026. Its [final PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/83995c2acef585ae0f0d647154cfdd85-Paper-Conference.pdf) is distinct from the arXiv title ending in *Convex Minimization*.

Appendix S, pp.33–34, Table 5 marks both computation of H* and outer residuals as immediate extensions to sampling without replacement. The discussion explicitly relies on Hu Theorem 4 and §4.2.2 for the first step and the same algorithm for the second. Its conclusion says: “sampling without replacement seems almost immediately tractable for global resolution.” No correction or distinction between successive and product-weighted sampling appears in this discussion.

This shows a concrete downstream reliance, **not a second refutation of the full Global Resolution paper**. Its principal algorithm and results explicitly use iid drafts (§6, pp.5–6). Appendix S describes an extension rather than a completed tested without-replacement algorithm. The cited justification needs revisiting under Hu's stated successive law; the extension might still be repaired by another argument. The counterexample does not disprove q-convexity itself or the general optimal-transport/subset identity.

## Coverage and limits

Six targeted search queries and four direct primary-source retrievals exhausted the ten-request limit. Searches covered the exact Hu title/arXiv identifier with code/correction terms, the sampling-law terms, and the later Global Resolution paper. Several results were weak or irrelevant. The author-maintained Hu repository was not located, so neither its current implementation nor its issue tracker was inspected. OpenReview discussion remained unverified; no verification was bypassed. No complete citation census was performed.

Accordingly, the defensible description is: **a confirmed error in the published exact without-replacement bound, with no prior correction located in a limited primary-source screen**. “First discovery,” “previously unknown,” empirical speedup corrections, and claims about real-model prevalence are unsupported. No new mathematical computation, model inference, paid resource, or outreach occurred.

`SOURCE-LEDGER.json` records all requests and source locations; `RESULT.json` records the machine-readable verdict. The official 2026 PDF SHA256 is `30e8f157250f2575541a6e590d842d22e5a648beb26552c5f552528600368b79`.
