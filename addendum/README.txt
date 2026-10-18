FOLLOW-UP TO THE ORIGINAL SPECULATIVE-DECODING COUNTEREXAMPLES

Published base: https://github.com/infinityscroll/speculative-decoding-counterexamples
Original published commit: c06d7db55383075481da2de8a25b7b58d781ec00

1. Constructive repair
An exponential-clock merging proof establishes the actual successive sampler's q-convexity and sorted-prefix reduction. For two drafts, Q(H)=a-(1-a)b with a=sum_Hq and b=sum_Hq/(1-q) gives an exact O(V log V) acceptance-value oracle. It does not construct an optimal verification kernel or supply a fast general-n evaluator. Proof and final runtime passed separate review.

2. Relevance extension
For every finite vocabulary size V>=5, strictly positive rational distributions with just three drafts retain an overestimate of at least7.40068673549percentagepoints. These are bounds on enlarged-vocabulary optima. A separate corollary shows failure for arbitrarily TV-close distributions, with shrinking error. The fixed7.40-point construction still concentrates99.9%mass on four tokens. No model prevalence or inference speedup claim is made.

The new derivations use standard probability facts. Specific priority and external human validation remain unverified. These are Codex-assisted results, separately checked within that workflow. This addendum was prepared after the original release. The original counterexample source and results are unchanged.

Reproduce with Python3.8+ and standard library only: python3 -B verify_all.py. The verifier checks the manifest, executes the frozen checkers in an isolated temporary directory, and compares every output field except elapsed CPU time. The analytic theorems still require reading their proofs; finite cases do not establish them. No source code changes were needed for portability. The original frozen files remain unchanged.
