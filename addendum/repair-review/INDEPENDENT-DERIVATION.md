# Independent derivation before inspecting the proposer proof

Let Ω be finite, let every rate q_i>0, and choose 1≤n≤|Ω|. Draw independent clocks T_i~Exp(q_i); let S_n be the indices of the n earliest clocks. Exponential memorylessness gives the successive renormalized sampling law: the first winner has probability q_i/sum(q), and after its time, the residual clocks of all other tokens are independent exponentials with their original rates. Induction gives the entire ordered law. Equal times have probability zero.

For H⊆Ω and distinct x,y outside H, write Q(H)=Pr(S_n⊆H), A={S_n⊆H∪{x},x∈S_n}, and E={S_n⊆H∪{x,y},S_n∩{x,y}≠∅}. Thus a=Pr(A)=Q(H+x)−Q(H), e=Pr(E)=Q(H+x+y)−Q(H), and the second marginal in the proposed q-convex inequality is e−a.

Assume first n≤|Ω|−1. Replace the pair by one clock T=min(T_x,T_y), labelled m, and retain the other clocks unchanged. Let I be the identity of the smaller original clock. Direct densities give Pr(T∈dt,I=x)=q_x exp(−(q_x+q_y)t)dt. Hence I is independent of T, with Pr(I=x)=q_x/(q_x+q_y). The pair of original clocks is independent of every other clock, so I is jointly independent of the entire reduced race (T and all retained clocks).

Let B be the event that the first n indices in this reduced race all belong to H∪{m} and include m. The following are samplewise inclusions outside the null tie event:

1. A⊆B∩{I=x}. In A, x is selected and y is not, so T_x<T_y. Removing y, which occurs after the nth selected original clock, leaves the first n unchanged apart from renaming x as m. Thus B holds and I=x.
2. B⊆E. Restore the losing clock at its original time, which is later than T. Adding this one clock either leaves the first n unchanged or replaces their last member by the losing member of the pair. Every resulting first-n token lies in H∪{x,y}. The earlier pair member remains selected: it had reduced rank≤n, and the newly inserted clock is later than it. Consequently at least one pair member is selected. This proves E.

Since B only depends on the reduced race, Pr(B∩{I=x})=Pr(B)q_x/(q_x+q_y). Therefore a≤q_x e/(q_x+q_y), so q_y a≤q_x(e−a), equivalently

[Q(H+x)−Q(H)]/q_x ≤ [Q(H+x+y)−Q(H+x)]/q_y.

For n=|Ω|, H+x contains at most |Ω|−1 tokens, so a=0. The right marginal is nonnegative. No reduced race with n draws is needed. For n=1, the inequality is equality, since both normalized marginals equal 1/sum(q). Cases where H is too small are covered automatically by events of probability zero.

Zero rates: require n≤|supp(q)| for the actual successive law to be defined; omit all zero-rate clocks or assign time +∞. For x,y of positive rate apply the same proof within the support, discarding zero-rate elements of H. If either rate is zero, the corresponding selection marginal is zero and the cross-multiplied inequality still holds. The displayed quotient expression is undefined at a zero denominator: it must be stated on positive-rate tokens, or replaced by the cross-multiplied extension. If n exceeds the number of positive rates, successive renormalization eventually has denominator zero and there is no claimed probability law.

This establishes q-convexity for the stated successive law on its positive-support domain, without any elementary-symmetric probability formula. It does not validate that formula, its dynamic program, or numerical values based on it. The sorted-prefix theorem can use this repaired q-convexity premise, but still needs correct all-in-H probabilities to yield the true optimum; this proof supplies no efficient evaluator for those probabilities.
