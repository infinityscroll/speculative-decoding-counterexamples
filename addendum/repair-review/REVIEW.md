# Independent proof review

**PASS: the exponential-race argument proves q-convexity for successive sampling with positive rates and every feasible draft count.** It repairs Theorem 4's justification without repairing the elementary-symmetric probability substitution. I derived the event argument in `INDEPENDENT-DERIVATION.md` before opening the proposer proof. No proposer code is imported by my exact checks.

The decisive inclusions are sound. On A, x arrives in the original first n and y does not, so deleting y leaves those arrivals unchanged and the merged identity is x. On B, reinserting the later pair clock only adds an allowed token and can remove at most the last currently selected token. It cannot remove the earlier pair clock. Thus B implies E. Winner identity is independent **jointly** of the merged time and all other clocks, since the competing-exponential density factors and the pair is independent of the other clocks. Consequently Pr(A)≤q_x Pr(E)/(q_x+q_y), giving exactly the desired inequality after rearrangement.

## Edges and assumptions

- For n=V, the left marginal is zero, and the inequality is immediate. This separate case is essential because a reduced V−1-clock race cannot supply n arrivals. The proposer handles it explicitly.
- n=V−1 is valid: the reduced race has exactly n clocks. The inclusion proof still works. n=1 gives equality.
- Positive exponential clocks have no ties almost surely; the proof need not define behavior on the null tie set.
- For zero rates, the law requires n≤|supp(q)|. Restrict the quotient inequality to positive-rate tokens, or state its cross-multiplied form. A literal expression dividing by q_x=0 is undefined. Cross-multiplied zero-rate cases have zero relevant marginals and hold directly. The proposer claims strict positivity, so this is a scope qualification rather than a blocker.

## Consequences checked

The maximum-cardinality minimizer proof of the sorted-prefix reduction is valid: if a selected lower-ratio token has an excluded higher-or-equal-ratio token, q-convexity forces adding the latter to preserve the minimum, contradicting maximal cardinality. This also handles ties; an appropriate minimizer includes an entire boundary tie group. Empty and complete prefixes are included.

For two drafts, direct first-draw conditioning gives Q(H)=Σ_i∈H q_i(a−q_i)/(1−q_i). Using q_i²/(1−q_i)=q_i/(1−q_i)−q_i yields Q(H)=a−(1−a)b. With V≥2 and strict positivity, each q_i<1, so these denominators are well-defined. A streaming prefix scan after sorting is an exact acceptance-value oracle with O(V log V) comparisons and O(V) arithmetic operations. Those are not bit-complexity bounds or an optimal conditional verification sampler.

## Independent finite controls

`check_independently.py` uses only standard-library rational arithmetic. Its fixed controls passed 1,848 cross-multiplied q-convex inequalities over 503 ordered-draft instances (including n=V and zero-rate support edges), 3,456 samplewise inclusion checks over all 4-token clock orders, and 56 complete-subset checks of the two-draft formula and prefix optimum. The explicit (3/7,3/7,1/7) example returns 67/70. Runtime was about 0.014 CPU seconds. These finite checks supplement the proof; they do not establish the theorem by enumeration.

## Remaining scope

This repair leaves the wrong-law numerical counterexamples intact. It shows that the true Q can be minimized over sorted prefixes, but gives no fast general-n evaluator for true Q. No empirical speedup, reanalysis of author experiments, or publication priority is established. The exponential-race facts are standard.

An initial implementation retained a copy of every full prefix, causing quadratic trace storage/copying despite only linear rational scan updates. The proposer fixed this before final freeze: the default now streams the optimum, and the optional trace retains one order plus fixed-field scalar records. Four independent runtime controls and six invalid-input checks pass. All declared payload hashes match before and after this replay. Details are in `FINAL-RUNTIME-REVIEW.json`. All original counterexample packets remain untouched.
