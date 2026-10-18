# Fixed three drafts, arbitrary vocabulary, and close distributions

**PASS: the near-full-vocabulary condition is not necessary.** For every finite vocabulary size V≥5 there are strictly positive rational target and draft distributions with three successive drafts for which the printed prefix/coefficient calculation overestimates the true optimum by **at least 7.40068673549 percentage points**. A second corollary permits arbitrarily small total variation between p and q, with a positive but shrinking error.

These are analytical extensions, not model experiments, prevalence estimates, speedups, or corrections to empirical tables. The original frozen packets are unchanged. The source interpretation is the already reviewed Eq.(6) successive sampler and Section4.2 coefficient-ratio calculation in [Hu et al., ICLR2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/0907335ecf28faf15be54485dbcbe70e-Paper-Conference.pdf). No new source or novelty search was performed.

## 1. Base family with three drafts

Use three common tokens C and a token R, with raw draft weights w,w,w,1 for rational w>1. Define

\[
q_0(i)=\frac{w}{3w+1}\ (i\in C),\quad q_0(R)=\frac1{3w+1},
\quad r=\frac{w}{w+3},\quad
p_0(i)=\frac r3,\quad p_0(R)=1-r.
\]

As derived independently in the prior extension review, the probability that three successive drafts all lie in C is

\[
s=\prod_{j=1}^3\frac{jw}{jw+1}.
\]

The actual optimum is 1−s+r; the printed computation returns 1. In the alternative product-weighted law, an all-common draft set has probability r. Outputting R when present and otherwise a uniform common draft realizes p₀ with acceptance1. This positive control also proves, for every subset H of the core vocabulary,

\[
P_0(H)\ge Q_{\rm product,0}(H),
\]

because an always-accepted output must be in H whenever all drafts lie in H.

## 2. Embedding into any V=4+L, L≥1

Choose rational 0<ε<1, multiply every original p₀ and q₀ coordinate by 1−ε, and add L new tokens with identical target and draft probabilities ε/L. All coordinates are strictly positive and both distributions normalize exactly. Keep the draft count equal to three. Write t=ε/(1−ε).

The event that all three successive drafts are original common tokens has probability

\[
s_\varepsilon=\prod_{j=1}^3\frac{jw}{jw+1+(3w+1)t}.
\]

This formula depends only on the total added mass, not on L. Its target common mass is (1−ε)r. The general event-capacity argument therefore gives

\[
\boxed{A_{\rm actual}\le 1+(1-\varepsilon)r-s_\varepsilon.}
\]

This is an upper bound, not a claim that this cut remains exactly optimal after embedding.

### A lower bound for the printed calculation

Let e₂ and e₃ be elementary symmetric polynomials of the original four normalized draft coordinates. Direct expansion gives

\[
e_2=\frac{3w(w+1)}{(3w+1)^2},\qquad
e_3=\frac{w^2(w+3)}{(3w+1)^3}.
\]

For the added coordinates, their first elementary sum is ε, their second is at most ε²/2, and their third at most ε³/6. The normalization for the enlarged product-weighted triple law is

\[
Z=(1-\varepsilon)^3e_3+
\varepsilon(1-\varepsilon)^2e_2+
(1-\varepsilon)e_2(\text{added})+e_3(\text{added}).
\]

Conditional on drawing no added token under this law, the original product-weighted law is recovered exactly. Its probability δ of drawing at least one added token satisfies

\[
\delta\le D_{\rm product}(t)
:=\frac{e_2}{e_3}t+\frac1{2e_3}t^2+\frac1{6e_3}t^3.
\]

This is a bound, uniform in L; it need not equal δ. The enlarged product law and the original law embedded with zero added-token mass have total variation δ. The corresponding target distributions have total variation ε. Consequently, for **every** subset H of the enlarged vocabulary,

\[
P_\varepsilon(H)-Q_{\rm product,\varepsilon}(H)
\ge -\varepsilon-\delta
\ge-\varepsilon-D_{\rm product}(t).
\]

The printed coefficient ratio equals this product-law event probability. Therefore its value on every prefix, regardless of ties, is at least 1−ε−D_product(t). No disputed q-convexity statement is needed. Combining bounds proves

\[
\boxed{A_{\rm printed}-A_{\rm actual}
\ge s_\varepsilon-(1-\varepsilon)r-\varepsilon-D_{\rm product}(t).}
\]

## 3. Explicit uniform numerical theorem

Take w=5 and ε=1/1000 for every L≥1. Then

\[
q_\varepsilon(i)=\frac{999}{1000}\frac5{16},\quad
q_\varepsilon(R)=\frac{999}{1000}\frac1{16},
\]
\[
p_\varepsilon(i)=\frac{999}{1000}\frac5{24},\quad
p_\varepsilon(R)=\frac{999}{1000}\frac38,
\quad p_\varepsilon(\text{each added})=q_\varepsilon(\text{each added})=\frac1{1000L}.
\]

Here e₂=45/128, e₃=25/512 and t=1/999, so

\[
D_{\rm product}(t)=\frac{36}{5}t+\frac{256}{25}t^2+\frac{256}{75}t^3
=\frac{539688028}{74775224925}.
\]

Exact rational arithmetic gives:

| Quantity | Certified value |
|---|---:|
| All-original-common successive probability sε | 2991008997/4232963200 |
| Lower bound for printed value | 2966430466883/2991008997000 ≈0.991782528858 |
| Upper bound for actual optimum | 3884910601/4232963200 ≈0.917775661504 |
| Lower bound for overestimate | 4684942207714402543/63304155075849552000 ≈0.0740068673549 |

Thus a discrepancy exceeding seven percentage points is retained for every finite V≥5 with n=3. There is no near-full-vocabulary requirement. These bounds are not presented as exact enlarged-vocabulary optimal values.

## 4. Arbitrarily close p and q, still fixed n=3

For the unembedded four-token family, only R gains target mass relative to q₀. Hence

\[
\operatorname{TV}(p_0,q_0)
=\frac3{w+3}-\frac1{3w+1}
=\frac{8w}{(w+3)(3w+1)}<\frac8{3w}\longrightarrow0.
\]

The exact original error factors as

\[
g(w)=s-r
=\frac{w(w-1)(7w+1)}{(w+3)(w+1)(2w+1)(3w+1)}>0.
\]

Thus exactness already fails for arbitrarily close p,q at fixed three drafts. The gap tends to zero: this does not give a fixed-size error in an arbitrarily small neighborhood of p=q.

This corollary can also be embedded uniformly into any larger finite V. Define positive rational constants

\[
a=e_2/e_3,\ b=1/(2e_3),\ c=1/(6e_3),\
d=(3w+1)\sum_{j=1}^3\frac1{jw+1},\quad K=1+2(a+b+c+d).
\]

The elementary telescoping bound for products in [0,1] yields s−sε≤dt. For 0<ε≤1/4, t≤2ε and t²,t³≤t. Substitution into the boxed error bound gives

\[
A_{\rm printed}-A_{\rm actual}
\ge g(w)-(1-r)\varepsilon-(a+d)t-bt^2-ct^3
\ge g(w)-K\varepsilon.
\]

Choose

\[
\varepsilon=\min\{1/4,\ g(w)/(2K)\}>0.
\]

Then the enlarged-vocabulary error is at least g(w)/2>0 for every L≥1. Because added coordinates agree in p and q,

\[
\operatorname{TV}(p_\varepsilon,q_\varepsilon)
=(1-\varepsilon)\operatorname{TV}(p_0,q_0).
\]

**Combined theorem:** for every finite V≥4 and every η>0, there are strictly positive rational p,q with TV(p,q)<η and n=3<V for which the printed calculation strictly overestimates the actual successive-sampling optimum. Choose an integer w>max{1,8/(3η)} and use the construction above (the original family when V=4). The retained error can shrink with η.

## 5. Limits and strongest defenses

- The explicit ≥7.4006-point example assigns only 0.1% total probability to added tokens. It resolves a formal support-size objection, not an objection about concentration on a small effective vocabulary or realism of the distributions.
- Its TV distance is (999/1000)(5/16)=0.3121875. The close-distribution corollary is separate and does not retain that numerical gap.
- Total-variation closeness is not coordinatewise likelihood-ratio closeness. In the close family, the rare token's p/q ratio tends to9 while its probability tends to0. No uniformly multiplicative-close counterexample is established here.
- The paper might have intended the alternative product law; under that law its coefficient calculation has a different interpretation. This construction concerns the explicitly stated successive law.
- Nothing here shows frequency in model logits, an altered experimental ranking, a runtime gain, or failure of the general transport identity. Specific novelty and external human validation are unverified.

`check_constants.py` reproduces only the displayed rational constants and algebraic checks. It does not enumerate large vocabularies, run a solver, or execute a model. The general theorem is the analytical proof above. This is a Codex-assisted work product, not external peer review.
