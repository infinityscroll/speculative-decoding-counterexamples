# A valid q-convexity proof for successive sampling

**Concrete repair:** The q-convexity statement is valid for the actual successive without-replacement law. An exponential-race argument proves it without the incorrect elementary-symmetric-polynomial identity. Consequently the sorted-prefix minimization remains valid when supplied the true set probability. For two drafts that probability has a simple cumulative formula, giving a corrected acceptance oracle with O(V log V) arithmetic operations.

This is a repair of the theoretical acceptance calculation, not a new verification sampler or a measured inference speedup. The proof uses standard exponential-race facts; publication novelty and prior application have not been established. All prior source and counterexample packets remain unchanged.

## Setting

Let Σ be a finite vocabulary, with strictly positive weights q_i summing to one. Draw n≤|Σ| distinct tokens successively, choosing at each draw proportionally to the remaining q weights. Let D be the resulting unordered set, and define

Q(H)=Pr(D⊆H),             Q(x|H)=Q(H∪{x})−Q(H).

For x,y∉H, x≠y, the required q-convexity inequality is

**Q(x|H)/q_x ≤ Q(y|H∪{x})/q_y.**

The target statement is Theorem 4 in Hu et al., *Towards Optimal Multi-draft Speculative Decoding*, [ICLR 2025 final paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf). Eq. (6), printed p. 4, defines the successive law; Definition 2 and Theorem 4 are on printed pp. 5–6. The previous packet disproves the generating-function identity used in its proof, not this theorem statement.

## Standard exponential-race representation

Take independent clocks T_i~Exp(q_i). Their first n arrivals have precisely the successive-sampling distribution: the first identity has probability q_i/Σ_j q_j, and the memoryless property gives the same rule over remaining clocks after each arrival. Ties have probability zero.

For two selected identities x,y, put T=min(T_x,T_y), and let I identify the first of these two clocks. Then

Pr(I=x)=q_x/(q_x+q_y),

and I is independent of T and of all other clocks. Indeed, the joint density of {I=x,T=t} is q_x exp(−(q_x+q_y)t), which factors into q_x/(q_x+q_y) times the density of Exp(q_x+q_y).

## Merging proof

Assume first that n≤|Σ|−1. Work on this common clock probability space and define:

- A: the first n original arrivals lie in H∪{x} and include x.
- E: the first n original arrivals lie in H∪{x,y} and include at least one of x,y.
- B: delete the later of T_x,T_y and replace the earlier one by a single merged identity z at time T. In this reduced race, the first n arrivals lie in H∪{z} and include z.

The reduced race still has at least n clocks. Two samplewise inclusions are sufficient.

First, **A⊆B∩{I=x}**. On A, x is among the original first n clocks and y is not. Therefore T_x<T_y. Removing the later clock y does not change those first n arrivals, and renaming x as z gives B.

Second, **B⊆E**. Restore the deleted later clock. It either comes after the reduced first n arrivals or displaces one of them. It cannot displace the earlier merged clock, so at least one of x,y remains in the first n; all selected identities still lie in H∪{x,y}. Thus E holds.

B depends only on T and the clocks of identities outside {x,y}. It is therefore independent of I. Hence

Pr(A) ≤ Pr(B∩{I=x})
      = [q_x/(q_x+q_y)] Pr(B)
      ≤ [q_x/(q_x+q_y)] Pr(E).

Now Pr(A)=Q(H∪{x})−Q(H) and Pr(E)=Q(H∪{x,y})−Q(H). Let a=Pr(A) and b=Q(H∪{x,y})−Q(H∪{x}). The preceding inequality is a≤q_x(a+b)/(q_x+q_y), so q_y a≤q_x b. Dividing by q_x q_y proves the required q-convexity.

When n=|Σ|, Q(H∪{x})=Q(H)=0 because y is excluded; the desired inequality is immediate. Thus all feasible draft counts are covered.

## Consequence: the sorted-prefix reduction survives

Let the target p have positive coordinates, define P(H)=Σ_{i∈H}p_i, and f(H)=P(H)−Q(H). The general transport identity gives optimum acceptance 1+min_H f(H). The following argument only concerns minimization of f and uses the repaired q-convexity.

Choose an f-minimizer S of maximum cardinality. Suppose x∈S but y∉S has q_y/p_y≥q_x/p_x. Put A=S\{x}. Optimality gives f(x|A)≤0, hence Q(x|A)/q_x≥p_x/q_x. Repaired q-convexity gives

Q(y|S)/q_y ≥ Q(x|A)/q_x ≥ p_x/q_x ≥ p_y/q_y.

Therefore f(y|S)≤0. Adding y cannot lower the global minimum, so it preserves the minimum and contradicts maximal cardinality. Thus such x,y cannot exist, and some minimizer is a prefix of any ordering by descending q_i/p_i (including ties consistently). The empty and complete prefixes must also be evaluated.

This proves that only V+1 sets need be considered for every draft count. It does **not** supply an inexpensive general-n evaluation of the true Q for those sets. The false elementary-symmetric formula remains false.

## A complete two-draft probability repair

For n=2, direct conditioning on the first draw gives

Q(H) = Σ_{i∈H} q_i [a−q_i]/[1−q_i],

where a=Σ_{i∈H}q_i. Put b=Σ_{i∈H}q_i/(1−q_i). Since q_i²/(1−q_i)=q_i/(1−q_i)−q_i, this becomes

**Q(H)=a−(1−a)b.**

After sorting by q_i/p_i, maintain a, b, and c=P(H) along prefixes. Each new token updates all three with a constant number of operations. Evaluate

**1+c−a+(1−a)b**

at the empty prefix and after every insertion; its minimum is the true two-draft optimal acceptance. Sorting costs O(V log V) comparisons, and the scan costs O(V) arithmetic operations with O(1) additional scan state. These are arithmetic-operation bounds, not bit-complexity or floating-point stability claims. The implementation here uses exact rational arithmetic.

The formula is an acceptance-value oracle. Constructing a corresponding optimal conditional verifier is a separate task and is not provided by the scan.

## Exact check and concrete correction

For q=(3/7,3/7,1/7), p=(3/10,3/10,2/5), and two drafts, the common-token prefix has a=6/7 and b=3/2. The correct Q is 9/14, giving exact optimum 1+3/5−9/14=67/70. The product-weighted formula instead uses Q=3/5 and returns 1.

The local verifier checks four fixed positive rational p,q pairs, with V=3,4,5,8. It computes the successive law directly from all ordered distinct pairs, verifies the cumulative Q identity for every subset, and compares the repaired prefix result against complete subset enumeration. This finite check supports the implementation; the general result is established by the proof above.

## Verdict and limits

**GO: a complete useful repair of q-convexity and of the two-draft acceptance oracle.** No inference, weights, paid compute, source mutation, or outreach is involved. No new algorithmic novelty, general-n fast probability evaluator, finite-precision production correctness, or empirical speedup is claimed. The repaired theorem does not erase the previously certified wrong-law counterexamples to the published Q formula.
