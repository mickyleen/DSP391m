## Trang 1

Robust Resource Bounds with Static Analysis and Bayesian
Inference
LONG PHAM, Carnegie Mellon University, USA
FERAS A. SAAD, Carnegie Mellon University, USA
JAN HOFFMANN, Carnegie Mellon University, USA
There are two approaches to automatically deriving symbolic worst-case resource bounds for programs: static
analysis of the source code and data-driven analysis of cost measurements obtained by running the program.
Static resource analysis is usually sound but incomplete. Data-driven analysis can always return a result, but
its lack of robustness often leads to unsound results. This paper presents the design, implementation, and
empirical evaluation of hybrid resource bound analyses that tightly integrate static analysis and data-driven
analysis. The static analysis part builds on automatic amortized resource analysis (AARA), a state-of-the-art
type-based resource analysis method that performs cost bound inference using linear optimization. The
data-driven part is rooted in novel Bayesian modeling and inference techniques that improve upon previous
data-driven analysis methods by reporting an entire probability distribution over likely resource cost bounds.
A key innovation is a new type inference system called Hybrid AARA that coherently integrates Bayesian
inference into conventional AARA, combining the strengths of both approaches. Hybrid AARA is proven to
be statistically sound under standard assumptions on the runtime cost data. An experimental evaluation on a
challenging set of benchmarks shows that Hybrid AARA (i) effectively mitigates the incompleteness of purely
static resource analysis; and (ii) is more accurate and robust than purely data-driven resource analysis.
CCS Concepts: • Theory of computation → Type theory; Program analysis; • Mathematics of comput￾ing → Probabilistic inference problems; Markov-chain Monte Carlo methods.
Additional Key Words and Phrases: resource analysis, worst-case costs, static analysis, data-driven analysis,
hybrid analysis, Bayesian inference
ACM Reference Format:
Long Pham, Feras A. Saad, and Jan Hoffmann. 2024. Robust Resource Bounds with Static Analysis and Bayesian
Inference. Proc. ACM Program. Lang. 8, PLDI, Article 150 (June 2024), 26 pages. https://doi.org/10.1145/3656380
1 INTRODUCTION
Static resource analysis. The prevailing goal of resource analysis—and the goal of this article—is to
derive a symbolic expression that bounds the worst-case execution cost of a program as a function
of the inputs. Building on pioneering resource analysis works such as Wegbreit’s metric system [88],
modern tools use various static analysis techniques: type systems [5, 21, 24, 26, 38, 40, 59, 86],
recurrence relations [2, 25, 35, 55, 56, 88], term rewriting [6, 7, 49, 72], ranking functions [12, 20, 31,
82], and abstract interpretation [3, 37, 91]. They can automatically and accurately analyze complex
functions such as operations on splay trees [61] and software product code [37]. Automatic resource
analysis is now used on a daily basis by developers in tools such as Meta’s static analyzer Infer [22].
Authors’ addresses: Long Pham, Carnegie Mellon University, Pittsburgh, USA, longp@andrew.cmu.edu; Feras A. Saad,
Carnegie Mellon University, Pittsburgh, USA, fsaad@cmu.edu; Jan Hoffmann, Carnegie Mellon University, Pittsburgh, USA,
jhoffmann@cmu.edu.
© 2024 Copyright held by the owner/author(s).
ACM 2475-1421/2024/6-ART150
https://doi.org/10.1145/3656380
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

### Hình ảnh trên trang

![Hình ảnh](images/page_0001_image_001.jpg)

![Hình ảnh](images/page_0001_image_002.jpg)

---

## Trang 2

150:2 Long Pham, Feras A. Saad, and Jan Hoffmann
However, since static resource analysis is undecidable for Turing-complete languages, even the
most sophisticated tools fail to infer cost bounds for some programs. In such cases, users must
resort to rewriting their code or using manual techniques for resource analysis [19, 59, 70, 74, 75].
Both of these workarounds require expertise in programming languages and resource analysis,
which is a fundamental barrier to leveraging these methods in a wider spectrum of applications.
Data-driven resource analysis. An alternative approach to static resource analysis is data-driven
resource analysis, which infers resource bounds from a set of cost measurements obtained by running
the program [23, 30, 33, 50, 77, 80, 90]. Data-driven resource analysis is not as well established as
static resource analysis. A main advantage of data-driven approaches is that a program can be
treated as a black box, greatly expanding the scope of programs that can be analyzed.
Data-driven resource analysis comes with its own set of challenges, particularly for deriving
worst-case bounds. First, the analysis is sensitive to the given dataset and data collection can be
difficult. For example, inputs generated uniformly at random are unlikely to trigger worst-case
behaviors in many programs. Second, commonly used statistical techniques for inferring a bound
from the cost dataset lack accuracy (i.e., how close the inference result is to a sound worst-case
cost bound) and robustness (i.e., the inference result has a positive probability of being a sound
worst-case cost bound even if the dataset does not contain worst-case inputs). The aforementioned
works use optimization, and as we demonstrate with experiments (Section 7), bounds derived in
this way are prone to being unsound. Prior works also do not quantify any notion of uncertainty in
the inferred bounds.
Bayesian resource analysis. The first contribution of this work is the design and implementation of
Bayesian resource analysis for worst-case bounds. In general, Bayesian resource analyses are more
customizable than optimization-based ones, as users can express domain knowledge in the form of
probabilistic models. Additionally, Bayesian resource analyses return whole posterior distributions
of inferred cost bounds, providing richer information about the uncertainty in inference results.
This article presents two new Bayesian resource analyses: BayesWC and BayesPC. In BayesWC, for
each input size present in the runtime cost data, we conduct Bayesian inference to infer likely values
of worst-case costs that are no less than the observed costs. By treating these two costs separately,
we account for the possibility that worst-case costs have not been observed in the runtime data.
The inferred worst-case costs from BayesWC produce optimization problems that can be solved to
obtain cost bounds. In BayesPC, on the other hand, we conduct Bayesian inference to directly infer
cost bounds, bypassing optimization altogether. Compared to BayesWC, BayesPC allows users to
construct more holistic probabilistic models for specifying how observed cost measurements are
probabilistically generated. In our experiments, cost bounds inferred by BayesWC and BayesPC
are shown to be more sound and robust than those inferred by an optimization-based data-driven
baseline. However, because they ignore the source code and exclusively rely on data-driven analysis,
BayesWC and BayesPC can still fail to infer sound cost bounds in several important benchmarks.
Hybrid resource analysis. The main contribution of this work is the design, implementa￾tion, and evaluation of a new hybrid resource analysis method that combines static and
data-driven resource analyses. To the best of our knowledge, this article is the first to develop
such a hybrid analysis. Hybrid resource analysis aims to mitigate the incompleteness of static
resource analysis and improve the accuracy and robustness of data-driven resource analysis. A
main research challenge is designing a principled interface between static and data-driven resource
analyses that enables a tight integration to combine the respective strengths of both approaches.
For the static part of the hybrid resource analysis, we rely on automatic amortized resource
analysis (AARA) [45, 47], a type-based state-of-the-art technique that is implemented for OCaml
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 3

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:3
programs in Resource-Aware ML (RaML) [41]. AARA supports advanced language features such as
recursive types [36], side effects [62], and higher-order functions [53]. Two distinguishing features
of AARA are the ability to handle non-monotone resources such as memory and the ability to
account for amortization effects. As a type-based technique, AARA is naturally compositional, and
cost bound inference can be reduced to off-the-shelf linear programming (LP) solving, even if the
derived bounds are nonlinear. We dub our hybrid resource analysis method Hybrid AARA.
For the data-driven part of Hybrid AARA, we present a new type inference system that combines
the two data-driven Bayesian resource analysis methods (BayesPC and BayesWC) with conventional
AARA. To invoke Hybrid AARA, a user annotates part of the code for data-driven analysis using
a syntactic form that has no runtime effect. Our integration of Bayesian resource analysis and
AARA rests on two key technical innovations. For Hybrid AARA with BayesWC, we combine the
optimization problems produced by the data-driven Bayesian inference with the linear constraints
derived using conventional AARA type inference to obtain and solve a joint linear program.
For Hybrid AARA with BayesPC, we integrate constraints from conventional AARA into the
probabilistic cost bound models of BayesPC. Bayesian inference within this model leverages recent
innovations from the sampling algorithm literature that allow Hamiltonian Monte Carlo (HMC)
sampling to be restricted to a convex polytope defined by AARA’s linear constraints [18, 69]. To
establish the soundness of Hybrid AARA, we first prove that its inferred bounds are sound with
respect to runtime cost data. Additionally, we prove the statistical soundness that the inferred
bounds converge to a sound bound if the analysis is repeated with a successively growing set of
runtime cost data that contains worst-case inputs with nonzero probability.
Applications. Hybrid AARA (and its special case of purely data-driven analysis) using Bayesian
inference returns a collection of cost bounds that approximate the posterior distribution. Even if
the proportion of sound cost bounds in the posterior distribution is less than 100%, Hybrid AARA
using Bayesian inference is useful for applications that can tolerate occasional underestimates of
the worst-case cost. One such application is scheduling of jobs in cloud computing, where the
cloud-service provider would like to have a reasonably accurate (but not necessarily sound at
all times) estimate of the resources required to run the job. The job’s cost use may respect the
tighter bounds in the posterior sample, but if it happens to run out of computational resources, then
the cloud-service provider can rerun the job with more resources. Other applications of Hybrid
AARA with Bayesian inference include auto-grading of students’ programming assignments and
annotating software libraries to help users of the library understand its performance characteristics.
Evaluation. In an experimental evaluation with a prototype built on RaML [41], we compare fully
data-driven analyses and Hybrid AARA on a curated set of benchmarks that pose challenges to
static, data-driven, and hybrid analyses. We find that Hybrid AARA outperforms fully data-driven
analyses both when considering soundness and tightness of the bounds.
Contributions. In summary, this article makes the following contributions.
• We present novel Bayesian data-driven resource analyses (BayesWC in Section 5.2; BayesPC
in Section 5.3) to infer posterior probability distributions over program cost bounds.
• We present Hybrid AARA: a novel type inference system that combines BayesWC and
BayesPC with conventional AARA (Sections 6.1 and 6.2).
• We formulate and prove two notions of soundness for Hybrid AARA (Theorems 6.1 and 6.2)
• We implement a prototype of Hybrid AARA by extending Resource-Aware ML (RaML) [41].
• We evaluate Hybrid AARA and fully data-driven resource analyses on a challenging bench￾mark set, showing examples of improvements in accuracy and robustness (Section 7).
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 4

150:4 Long Pham, Feras A. Saad, and Jan Hoffmann
let rec partition pivot xs =
match xs with
| [] → ([], [])
| hd :: tl →
let lower, upper = partition pivot tl in
if complex_compare hd pivot then
(hd :: lower, upper)
else (lower, hd :: upper)
let rec quicksort xs =
match xs with
| [] → []
| hd :: tl →
let lower, upper = Raml.stat (partition hd tl) in
let lower_sorted = quicksort lower in
let upper_sorted = quicksort upper in
append lower_sorted (hd :: upper_sorted)
Lst. 1. icksort in OCaml. The function complex_compare in line 6 is intractable to static resource analysis.
The annotation Raml.stat in line 5 indicates data-driven resource analysis on partition.
2 OVERVIEW
In this section, we review static and data-driven resource analyses, identify their shortcomings,
and outline our main contribution of hybrid resource analysis. We use the implementation of
quicksort in OCaml given in Listing 1 as a running example. Our goal is to automatically derive a
symbolic worst-case cost bound for the function quicksort. For simplicity, we use the resource
metric that records the time cost of executing the comparisons complex_compare hd pivot in the
function partition. We consider different versions of complex_compare. For example, if the cost of
evaluating complex_compare hd pivot is bounded by 1, then the worst-case cost of quicksort
xs is 푛(푛 − 1)/2, where 푛 is the length of the list xs.
Static resource analysis. The predominant method for automatically deriving symbolic worst-case
bounds is static resource analysis. This article builds on automatic amortized resource analysis
(AARA) [39–42] (Section 4), a compositional type-based static analysis technique.
Resource-Aware ML (RaML) is an implementation of AARA that derives polynomial bounds
for a subset of OCaml. The compositionality of AARA ensures that RaML can derive a bound
for quicksort if it can derive a bound for complex_compare. Assuming each comparison has
cost 1, RaML correctly infers the tight bound 푛(푛 − 1)/2 for quicksort in less than 0.1 seconds.
Similarly, assume that the argument of quicksort is a list of lists and that complex_compare is a
lexicographical comparison whose worst-case is 푘, where 푘 is the length of the first argument list.
Then RaML infers the tight bound 푚푛(푛 − 1)/2 for quicksort in less than 0.2 seconds, where 푚
is the maximum length of the inner lists. This analysis is nontrivial because of the nonstructural
recursion: to derive a cost bound, it is not enough to separately analyze the cost of the partition
function and the number of recursive steps. We must also analyze how the partition function
changes input sizes, relaying the size-change information to the next recursive call of quicksort.
Because resource analysis is undecidable, however, even the most sophisticated static resource
analyses are incomplete, and there remain programs that cannot be analyzed automatically. If the
comparison function complex_compare in partition is, for example, OCaml’s built-in polymor￾phic comparator, which examines the low-level memory representations of input values, RaML is
not able to derive a bound because the comparison code is not available to the analysis. Indeed, there
are many other comparison functions that RaML cannot analyze, even if the cost of the comparison
is bounded by a constant. AARA fails, for instance, if the control flow depends on mutable data or
complex loop conditions. A concrete example of a constant-time function that cannot be statically
analyzed is compare_dist, an implementation of complex_compare that compares two vectors by
computing their distance to a fixed vector that is stored in a reference cell. Such limitations are not
specific to RaML: every static resource analysis has unsupported language features or iteration
patterns that make the analysis feel brittle for non-experts users.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 5

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:5
(a) Data-Driven Resource Analysis
0 50 100 150 200
Input Size
100
101
102
103
104
Cost
Runtime Data
True Bound
Inferred Bound
Opt
(b) Data-Driven Resource Analysis
0 50 100 150 200
Input Size
100
101
102
103
104
Cost
BayesWC
(c) Hybrid Resource Analysis
0 50 100 150 200
Input Size
100
101
102
103
104
Cost
Fig. 1. Hybrid resource analysis on quicksort infers more accurate bounds than purely data-driven analyses.
Data-driven resource analysis. One way to overcome the incompleteness of static analysis is
data-driven analysis. Existing data-driven techniques first collect execution costs for different inputs
and then solve an optimization problem to fit a cost function on the data [23, 30, 33, 50, 77, 80, 90].
Although these optimization-based approaches are fast, they can infer unsound cost bounds and do
not quantify the uncertainty over the unknown cost bounds.
To showcase such an approach, suppose that quicksort uses the aforementioned comparator
compare_dist and that the cost varies between 0.5 and 1.0 for different inputs. Figure 1a shows
the inferred quadratic cost bound (blue line) of data-driven optimization-based resource analysis
adapted from [23, 33, 90], given a randomly generated dataset of measured costs of quicksort
(black dots). Any worst-case cost bound must lie above all the measured costs and minimize the
total 퐿1 distance between the curve and runtime data. This optimization problem can be framed as
a linear program (Opt; Section 5.1). Optimization fails to infer the correct worst-case cost bound
(red line), because randomly generated data sets rarely contain worst-case inputs.
To mitigate the shortcomings of such greedy optimizations, this paper introduces data-driven
Bayesian resource analyses (BayesWC and BayesPC; Sections 5.2 and 5.3). Bayesian resource
analysis enables users to express their domain knowledge in the form of models that specify
how observed runtime samples are probabilistically generated. It returns an entire probability
distribution over the corresponding cost bounds given observed samples. In particular, we condition
the probabilistic model on observed cost data and compute the posterior distribution of cost bounds
by running sampling-based probabilistic inference algorithms. For quicksort, Fig. 1b shows the
posterior distribution over cost bounds from Bayesian resource analysis. The blue line indicates
the median cost bound and the light-blue shade is the 10–90th percentile range. Most of the cost
bounds in the posterior distribution are closer to the true worst-case bound (red line) as compared to
optimization-based approach in Fig. 1a. In fact, 28/1000 bounds drawn from the posterior distribution
are sound. Although this fraction is small, it is already a substantial improvement over optimization.
Hybrid resource analysis. A central contribution of this work is the design, implementation, and
evaluation of Hybrid AARA (Section 6), which integrates our two novel data-driven methods for
Bayesian resource analysis (BayesWC and BayesPC) and a simple optimization-based data-driven
baseline (Opt) into conventional AARA. Hybrid AARA is modular and lets users combine data￾driven and static analyses in different parts of a program. Therefore, it covers a spectrum ranging
from fully data-driven to fully static analyses.
Consider again the example of quicksort where the comparator is compare_dist, which in￾tractable for static analysis and has a cost varying between 0.5 and 1.0. If we perform data-driven
analysis on the comparator and static analysis on the rest of the code, Hybrid BayesWC amounts
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 6

150:6 Long Pham, Feras A. Saad, and Jan Hoffmann
to (i) inferring the worst-case constant cost of the comparator by data-driven analysis; and (ii) in￾corporating the inferred cost into conventional AARA. All 1000/1000 cost bounds drawn from the
posterior distribution are sound (the analysis time in our Hybrid AARA prototype is 66.2 seconds).
In the previous example, the interface between the statistical analysis and the static analysis is
particularly simple since the cost of evaluating quicksort does not depend on the result of the
comparison function. Many examples fall into this category, for which Hybrid AARA enables the
analysis of code that is intractable for purely static methods while clearly outperforming purely
data-driven methods. However, our experiment focuses on a different category of benchmarks for
which the integration of data-driven methods is technically challenging and the benefits of a hybrid
analysis are less clear.
Challenges for hybrid resource analysis. Revisit the quicksort example, using the compare_dist
comparator. But this time let us assume that the user marks the call to partition for data-driven
analysis instead of the call to complex_compare. A data-driven analysis could be able to derive a
linear cost bound for partition, but how can use this information to derive a bound for quicksort
using AARA? We would need additional information on the size of the result of partition. However, it
is not clear what exact information we need. For example, it is insufficient for analyzing quicksort
to statistically bound the size of each component in the result of partition.
A main technical innovation of our work is the design of a principled interface between data￾driven and static analyses that can handle such challenging cases. BayesWC and Opt are integrated
into AARA by developing a type inference system that combines the underlying LP problems.
Integrating BayesPC into AARA poses a significant challenge because the former relies on sampling
algorithms to approximate posterior distributions of resource coefficients instead of LP problems
as in AARA. To overcome this challenge, we leverage an innovative sampling algorithm that allow
Hamiltonian Monte Carlo (HMC) sampling to be restricted to a convex polytope [18, 69].
Figure 1c shows the posterior distribution over bounds from Hybrid BayesWC on quicksort
with the data-driven analysis of partition. The 10–90th percentile range (blue shade) is situated
above the true worst-case bound (red line) for all input sizes between 0 and 200. In fact, 471/1000
samples drawn from the posterior distribution in Hybrid BayesWC are theoretically sound bounds
for all input sizes, in contrast to the 28/1000 bounds for purely data-driven analysis with BayesWC
(Fig. 1b) and 0/1000 bounds for data-driven resource analysis with Opt (Fig. 1a).
We have empirically evaluated hybrid resource analysis on challenging and realistic micro
benchmarks where data-driven analysis is applied to non-trivial code that stresses the interface
between data-driven and static analysis (Section 7). The benchmarks demonstrate that (i) Bayesian
resource analysis returns more accurate cost bounds than optimization-based analysis and (ii) hybrid
resource analysis returns more accurate cost bounds than fully data-driven analysis. Notable among
our benchmarks is the median-of-medians-based linear-time selection algorithm [11]. Conventional
AARA cannot statically analyze this program, as it is challenging to reason about how the median
of medians influences the partition function. Fully data-driven analysis does not infer a sound
cost bound, either, as the worst-case behavior of partition rarely occurs in all recursive calls. By
exploiting hybrid resource analysis, we successfully infer a sound worst-case cost bound that
neither fully data-driven nor fully static analyses can.
3 SYNTAX AND COST SEMANTICS
We set the stage for Hybrid AARA by introducing a functional programming language. While AARA
can handle higher-order functions, we focus on the first-order setting to simplify the presentation.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 7

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:7
휏 F unit | int | 휏1 + 휏2 | 휏1 × 휏2 | 퐿(휏 ) polynomial and list types
푒 F ⟨ ⟩ | 푛 | 푥 unit, integer, and variable; 푥 ∈ X, 푛 ∈ Z
| le · 푥 | right · 푥 | case 푥 {le · 푥1 ↩→ 푒1 | right · 푥2 ↩→ 푒2 } sum constructor and destructor
| ⟨푥1, 푥2 ⟩ | case 푥 { ⟨푥1, 푥2 ⟩ ↩→ 푒 } product constructor and destructor
| [ ] | 푥1 :: 푥2 | case 푥 { [ ] ↩→ 푒1 | (푥1 :: 푥2 ) ↩→ 푒2 } list constructor and destructor
| 푓 푥 function application; 푓 ∈ F
| let 푥 = 푒1 in 푒2 | share 푥 as 푥1, 푥2 in 푒 let-binding and variable sharing
| tick 푞 resource consumption;푞 ∈ Q
| statℓ 푒 statistical analysis;ℓ ∈ L
Lst. 2. Datatypes 휏 and expressions 푒 in a first-order AARA functional programming language.
3.1 Syntax
Datatypes 휏 and expressions 푒 are formed by the grammar shown in Listing 2, where X, F, and L
are countable sets of identifiers for variable names, function names, and label names, respectively.
A program P contains a finite set 퐹 ⊂ F of function identifiers and mutually-recursive definitions
푓 (푥) =푒 for every 푓 ∈ 퐹 . (3.1)
Function types have the form 휏1 → 휏2. The function body 푒 can reference all functions 푔 ∈ 퐹 .
As in AARA [39, 40, 42], we adopt the share-let normal1
form where (i) variables are affine (i.e.,
they are used at most once) and (ii) constructors and destructors are applied to variables, but not
general expressions. The first restriction ensures that the potential stored in variables is consumed
at most once. To use variable 푥 twice, we write share 푥 as 푥1, 푥2 in 푒, where fresh variables 푥1 and 푥2
have the same value as 푥. The second restriction simplifies proofs of AARA. To apply constructors
and destructors to non-variable expressions, we first bind variables to them by let-bindings.
The construct tick 푞 increments a cost counter by 푞 ∈ Q, which is possibly negative, and returns
the unit element ⟨ ⟩. To specify a particular resource metric, users (manually or automatically)
insert tick 푞 throughout their code. As the tick metric lets us consider arbitrary resource metrics, it
is a standard practice in the literature of static resource analysis [25, 42, 67, 75, 86].
If all 푞’s in tick 푞 are non-negative, such resource metrics (e.g., running time) are said to be
monotone. Conversely, if we have 푞 < 0, it means resources can be freed up, and such resource
metrics (e.g., memory) are non-monotone. This article focuses on monotone resource metrics.
The construct statℓ 푒 does not have a runtime effect, but is used in the hybrid resource analysis. It
indicates that expression 푒 should be analyzed using data-driven analysis instead of static analysis.
The label ℓ ∈ L is used to uniquely identify sites of data-driven analysis in source code.
Our prototype implementation is based on Resource-Aware ML (RaML) [41], which uses OCaml
extended with annotations Raml.tick and Raml.stat as the input language. By way of example,
Listing 1 displays an implementation of quicksort.
The annotation stat can be either manually inserted by the user or automatically inserted by
walking over the program’s source code bottom-up to identify functions (or more fine-grained code
fragments) that cannot be analyzed statically by conventional AARA. Concretely, we first look at
the leaves of the program call graph (i.e., functions which do not call other functions), check if we
can analyze them using conventional AARA, and then recurse up the call graph to identify other
problematic functions. We then insert the annotations at all the required points.
1The share-let normal form does not affect the expressive power of the language. The implementation of AARA for
OCaml [41, 42] only uses the share-let normal form internally—users are allowed to write any OCaml programs.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 8

150:8 Long Pham, Feras A. Saad, and Jan Hoffmann
3.2 Cost Semantics
Given a program P, the cost semantics of expression 푒 is given by the judgment
푉 ⊢P 푒 ⇓
푐
푣, (3.2)
where 푉 is an environment (i.e., a mapping from variables to values), 푣 is the value that 푒 evaluates
to, and 푐 ∈ Q≥0 denotes the cost of evaluating 푒. Values 푣 are defined by the following grammar:
푣 F ⟨ ⟩ | 푛 | le · 푣 | right · 푣 | ⟨푣1, 푣2⟩ | [ ] | 푣1 :: 푣2.
A well-formed value can be assigned a type 휏 and we write 푣 : 휏.
Under non-monotone resource metrics, we would have two notions of costs: peak costs and
net costs [39, 40, 42]. However, as this article focuses on monotone resource metrics, (3.2) only
contains a single cost 푐 ∈ Q≥0. Additionally, for simplicity, this article assumes that (i) 푞 in tick 푞 is
known with absolute certainty and (ii) costs are measured perfectly without measurement errors.
Measurement errors can be factored into probabilistic models of Bayesian resource analysis by
encoding them in the input program.
3.3 Data Collection
In fully data-driven analysis (Section 5), we collect a dataset of runtime cost measurements for
a program P = {푓 (푥) =푒} with a single function 푓 . Sweeping through a list of environments
푉푖 = {푥 : 푣푖 } (푖 = 1, . . . , 푁) that each includes bindings for argument 푥, we evaluate the cost
semantics 푉푖 ⊢P 푒 ⇓
푐푖 푣˜푖
. We then define the dataset as D = {(푉푖
,푣˜푖
, 푐푖)}
푁
푖=1
.
The data collection for hybrid resource analysis (Section 6) is more involved. It is formalized with
a judgment that extends the cost semantics (3.2). Letting 푁 > 0 be a positive integer, the expression
(푉푖 ⊢P 푒 ⇓
푐푖
푣푖)
푁
푖=1
| D (3.3)
is defined as follows. We again perform independent executions of the program sweeping through
environments (푉1, . . . ,푉푁 ). Let 퐿
′ ⊂ L denote the labels of all statℓ subexpressions in program 푒.
We collect in Dℓ all measurements (푉 , 푣, 푐) associated with expression statℓ 푒ℓ
, for each ℓ ∈ 퐿
′
. The
overall dataset is D = {(ℓ,푉 , 푣, 푐) | ℓ ∈ 퐿
′
, (푉 , 푣, 푐) ∈ Dℓ }.
4 BACKGROUND ON STATIC RESOURCE ANALYSIS
This work builds on automatic amortized resource analysis (AARA) [21, 39, 40, 42, 47, 48, 60], a
type-based resource analysis technique for functional programs. It aims to automatically infer
polynomial cost bounds. It adopts the potential method of amortized analysis [85], where data
structures are equipped with potential functions mapping concrete values to non-negative numbers.
4.1 Linear AARA
To illustrate how AARA works, consider the function partition in Listing 1. Our goal is to derive
a worst-case bound on the number of comparisons during an evaluation of partition, namely
푛, where 푛 is the input list length. In AARA, we type expression partition (p,x), where p is a
pivot and x is an input list, as follows:
{p : int, x : 퐿
1
(int)}; 0 ⊢ partition (p,x) : ⟨퐿
0
(int) × 퐿
0
(int), 0⟩.
The type 퐿
1
(int) assigns the potential function Φ(푣 : 퐿
1
(int)) = 1·|푣| to an input list푣, representing
the tight worst-case bound. The annotation 0 in the typing context indicates that 0 additional
constant potential is stored in the context.
AARA is naturally compositional because potential functions explicitly track size changes of
data structures. Assume we have two nested calls to partition as in the following function f.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 9

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:9
f(x) = let (x1,x2) = partition (8128,x) in partition (1,x1)
In the call partition (1,x1), we can use the previous type for partition. However, for the call
partition (8128,x), we use the typing judgment
{p : int, x : 퐿
2
(int)}; 0 ⊢ partition (p,x) : ⟨퐿
1
(int) × 퐿
1
(int), 0⟩.
It assigns type 퐿
1
(int) to the output lists. Let 푣, 푣1, 푣2 be values of variables 푥, 푥1, 푥2, respectively.
The intuition is that the input potential Φ(푣 : 퐿
2
(int)) = 2 · |푣| is used to cover both the cost (1 · |푣|)
and the potential of the result (1 · |푣1 | + 1 · |푣2 |). It relies on the fact |푣1 | + |푣2 | = |푣|. The remaining
potential Φ(푣1 : 퐿
1
(int)) = 1 · |푣1 | covers the cost of the second function call partition (1,x1).
In general, the type of partition (p,x) can be expressed with linear constraints:
{p : int, x : 퐿
푝1
(int)}; 푝0 ⊢ partition (p,x) : ⟨퐿
푞1
(int) × 퐿
푞2
(int), 푞0⟩
subject to 푝1 ≥ 1 + 푞
′
, 푞′ ≥ 푞1, 푞′ ≥ 푞2, 푝0 ≥ 푞0.
Similar constraints are emitted by the local type rules during the type inference. The constraints
are then solved with an off-the-shelf linear programming solver to derive a bound for the program.
4.2 Polynomial AARA
AARA can be extended to polynomial potential functions and therefore polynomial cost bounds
while retaining compositionality and type inference with linear constraint solving [39, 43]. Consider
quicksort from Listing 1. In terms of the number of comparisons, the worst-case cost of quicksort
is 푛(푛 − 1)/2, where 푛 is the input list length. This cost bound is expressed by the following typing
judgment in univariate polynomial AARA:
{x : 퐿
(0,1)
(int)}; 0 ⊢ quicksort x : ⟨퐿
(0,0)
(int), 0⟩. (4.1)
Here, the input type 퐿
(0,1)
(int) assigns the potential function Φ(푣 : 퐿
(0,1)
(int)) = 0 ·

|푣 |
1

+ 1 ·

|푣 |
2

,
and the constant 0 after 퐿
(0,1)
(int) indicates the constant zero potential stored in the input.
Univariate polynomial AARA extends linear AARA with univariate polynomial potential func￾tions. For instance, given two values 푣1 and 푣2, univariate AARA can express a potential function
|푣1 |
2 + |푣2 |
2
. Resource-annotated datatypes in univariate AARA are formed by the grammar
푎 F unit | int | ⟨푎1, 푞1⟩ + ⟨푎2, 푞2⟩ | 푎1 × 푎2 | 퐿
푞®
(푎).
Here, 푞1, 푞2 ∈ Q≥0 denote constant potential, and a tuple 푞® over Q≥0 records coefficients of
polynomial potential functions, except their constant (i.e., degree-zero) potential. To indicate
constant potential 푞 ∈ Q≥0 in addition to higher-degree coefficients, we write ⟨푎, 푞⟩.
The amount Φ of potential stored in value 푣 according to a resource-annotated datatype 푎 is
Φ(푣 : unit) = Φ(푣 : int) := 0 Φ(⟨푣1, 푣2⟩ : 푎1 × 푎2) := Φ(푣1 : 푎1) + Φ(푣2 : 푎2)
Φ(le · 푣 : ⟨푎1, 푞1⟩ + ⟨푎2, 푞2⟩) := 푞1 + Φ(푣 : 푎1) Φ( [ ] : 퐿
푞®
(푎)) := 0
Φ(right · 푣 : ⟨푎1, 푞1⟩ + ⟨푎2, 푞2⟩) := 푞2 + Φ(푣 : 푎2) Φ(푣1 :: 푣2 : 퐿
푞®
(푎)) := 푞1 + Φ(푣1 : 푎)
+ Φ(푣2 : 퐿
⊳( ®푞)
(푎)),
where 푞® = (푞1, . . . , 푞푑 ) and the shift operator ⊳ on tuples is ⊳(푞1, . . . , 푞푑 ) := (푞1+푞2, . . . , 푞푑−1+푞푑, 푞푑 ).
Equivalently, if 푞® = (푞1, . . . , 푞푑 ), then a size-푛 list [푣1, . . . , 푣푛] of type 퐿
푞®
(푎) has potential
Φ( [푣1, . . . , 푣푛] : 퐿
푞®
(푎)) =
Í푑
푖=1
푞푖

푛
푖

+
Í푛
푖=1 Φ(푣푖
: 푎). (4.2)
Given an evaluation context 푉 = {푥1 : 푣1, . . . , 푥푛 : 푣푛}, its potential according to a resource￾annotated typing context Γ = {푥1 : 푎1, . . . , 푥푛 : 푎푛} is Φ(푉 : Γ) :=
Í푛
푖=1 Φ(푣푖
: 푎푖). The notation of
potential function Φ is used for both value 푣 : 푎 and evaluation context 푉 : Γ.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 10

150:10 Long Pham, Feras A. Saad, and Jan Hoffmann
input size
cost
Observed Data
Linear Programming
(a) Opt
input size
cost
Observed Data
Linear Programming
Bayesian Survival
Analysis
(b) BayesWC
input size
cost
Observed Data
Linear Programming
Bayesian Polynomial
Regression
(c) BayesPC
Fig. 2. Three approaches to data-driven resource analysis. (a) Opt uses linear programming to fit a polynomial
curve that lies above the runtime data while minimizing the distance to the observed worst-case cost at each
input size. (b) BayesWC uses a two-step approach: first, Bayesian survival analysis is used to infer a posterior
distribution over the worst-case cost at each input size; second, linear programming is used to fit polynomial
curves with respect to samples from the inferred distribution of worst-case costs. (c) BayesPC uses Bayesian
polynomial regression to infer the coefficients of polynomial curves that lie above the observed runtime data.
A resource-annotated typing judgment of univariate AARA is
Γ; 푝 ⊢ 푒 : ⟨푎, 푞⟩, (4.3)
where Γ is a resource-annotated typing context (i.e., a mapping from variables to resource-annotated
types), 푝 ∈ Q≥0 is constant potential of the context, and 푎 is a resource-annotated type of the
output with constant potential 푞 ∈ Q≥0. The judgment (4.3) means, given an environment 푉 that
carries potential 푝 + Φ(푉 : Γ), if 푒 evaluates to value 푣, then 푣 carries 푞 + Φ(푣 : 푎) much potential.
The soundness of univariate AARA is formally stated in Theorem 4.1 [44].
Theorem 4.1 (Soundness of univariate AARA). Under a monotone resource metric, suppose
Γ; 푝 ⊢ 푒 : ⟨푎, 푞⟩. If we have 푉 ⊢P 푒 ⇓
푐
푣, then Φ(푉 : Γ) + 푝 − Φ(푣 : 푎) − 푞 ≥ 푐 holds.
In our prototype of hybrid resource analysis, we use multivariate polynomial AARA [40, 42]
that can express multivariate polynomial potential functions and hence is strictly more expressive
than univariate polynomial AARA. Multivariate AARA preserves compositionality and linear￾programming-based type inference from univariate AARA. However, for the ease of presentation,
we use the notation of univariate AARA throughout this article.
5 DATA-DRIVEN BAYESIAN RESOURCE ANALYSIS
This section presents two novel data-driven resource analysis methods called BayesWC and
BayesPC that use Bayesian inference to learn probability distributions over cost bounds of programs.
Recall from Section 3.3 that fully data-driven resource analysis begins with a program P =
{푓 (푥) =푒} that contains a single function 푓 and runtime dataset D = {(푉푖
,푣˜푖
, 푐푖)}
푁
푖=1
. To simplify
the presentation, we assume in this section that 푓 takes as input a length-푛 integer list, returns a
length 휉(푛)-integer list, and contains no free variables. Since 푉푖 ≡ {푥 : 푣푖 } holds for each 푖, . . . , 푁,
we denote the measurements more concisely as (푣푖
,푣˜푖
, 푐푖). Following Eq. (4.3), a cost bound of 푓 is
{푥 : 퐿
푝®
(int)}, 푝0 ⊢ 푓 푥 : ⟨퐿
푞®
(int), 푞0⟩. (5.1)
This typing judgment is sound if, for all lists 푣 : 퐿(int), the relation {푥 : 푣 } ⊢P 푓 푥 ⇓
푐
푣˜ holds, i.e.,
[Φ(푣 : 퐿
푝®
(int)) + 푝0] − [Φ(푣˜ : 퐿
푞®
(int)) + 푞0] ≡ 
Ψ(|푣|; 푝0, 푝®) − Ψ(|푣˜|;푞0, 푞®)

≥ 푐, (5.2)
where we have introduced the function Ψ(푛; 푝0, 푝®) :=
Í|푝®|
푖=1
푝푖

푛
푖

+ 푝0 (푛 ∈ N). Unlike conventional
AARA, which derives (5.1) by static analysis of 푒 and linear programming, in data-driven resource
analysis we will infer the parameters (푝0, 푝®) and (푞0, 푞®) using the dataset D.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 11

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:11
5.1 Optimization
Before presenting Bayesian inference, we consider a simple optimization-based baseline (adapted
from [23, 33, 90]) to ensure that (5.2) is satisfied with respect to the runtime data D, i.e.,
∀푖 = 1, . . . , 푁 . Ψ(|푣푖
|; 푝0, 푝®) ≥ 푐푖 + Ψ(|푣˜푖
|;푞0, 푞®). (5.3)
We seek the tightest bound among all 푝0, 푝, 푞 ® 0, 푞® that minimizes the nonnegative cost gaps between
the predicted and observed costs in the dataset D. Letting
푁D ≔ {|푣푖
|;푖 = 1, . . . , 푁} set of unique input sizes appearing in D (5.4)
푐ˆ
max
푛 ≔ max {푐푖
| 푖 = 1, . . . , 푁; |푣푖
| = 푛} max. observed cost for input size 푛 ∈ 푁D (5.5)
푐
max
푛 ≔ max {cost(푓 푣) | 푣 : 퐿(int), |푣| = 푛} true worst-case cost for input size 푛 ∈ 푁D, (5.6)
we define the following linear program:
minimize Í푁
푖=1

Ψ(|푣푖
|; 푝0, 푝®) − Ψ(|푣˜푖
|;푞0, 푞®)

− 푐ˆ
max
|푣푖
|
(Opt-LP)
subject to Ψ(|푣푖
|; 푝0, 푝®) ≥ Ψ(|푣˜푖
|;푞0, 푞®) + 푐ˆ
max
|푣푖
|
(푖 = 1, . . . , 푁); 푝0, 푝1, . . . , 푝|푝®|
, 푞0, 푞1, . . . , 푞| ®푞| ≥ 0.
An example of this approach, which we call Opt, is shown in Fig. 2a. While any solution 푝ˆ0,
ˆ
푝, ® 푟ˆ0,
ˆ푞®
to (Opt-LP) is guaranteed to satisfy (5.3), even a conservative estimate Ψ(푛; 푝ˆ0,
ˆ
푝®) of the worst-case
cost may lie below the true value 푐
max
푛
in Eq. (5.6) (which we assume is finite), as shown in Fig. 1a.
This shortcoming occurs because Opt uses the point estimate 푐ˆ
max
푛 given in Eq. (5.5) as a proxy for
푐
max
푛
, which is not robust in cases where the data D is such that 푐ˆ
max
푛 < 푐
max
푛
for some 푛 ∈ 푁D.
5.2 Bayesian Inference on Worst-Case Costs
Overview. Our first approach to addressing the aforementioned limitation of Opt is Bayesian
inference on worst-case costs (BayesWC). Whereas Opt uses the data D to form a point estimate
푐ˆ
max
푛 of the worst-case cost푐
max
푛
for each input size 푛 ∈ 푁D in the linear program, BayesWC instead
leverages D to learn an entire probability distribution 휇푛 that characterizes our uncertainty about
푐
max
푛
. We identify two requirements that the inferred worst-case cost distributions 휇푛 must satisfy:
휇푛 ( [푐ˆ
max
푛
, ∞)) = 1, ∀휖 > 0,푤 > 푐ˆ
max
푛
. 휇푛 ( [푤 − 휖,푤 + 휖]) > 0. (5.7)
The left expression guarantees soundness (5.3) with respect to D and the right expression ensures
robustness with respect to the true worst-case cost 푐
max
푛
. The latter property is not satisfied by Opt.
If we have access to probability distributions 휇푛 (푛 ∈ 푁D) over worst-case costs, we can use
them to robustly estimate bounds by generating |푁D | batches of 푀 > 0 i.i.d. samples
(푐
′
푛,1
, . . . 푐′
푛,푀 ) ∼ 휇푛 (푛 ∈ 푁D). (5.8)
Reorganizing these |푁D | × 푀 samples into 푀 lists c
′
푗 ≔ (푐
′
푛,푗 ;푛 ∈ 푁D) (푗 = 1, . . . , 푀) each of
length 푁D, we obtain posterior samples of coefficients 푝0, 푝, 푞 ® 0, 푞® by solving 푀 linear programs
parametrized the random samples c
′
푗
:
minimize Í푁
푖=1

Ψ(|푣푖
|; 푝0, 푝®) − Ψ(|푣˜푖
|;푞0, 푞®)

− 푐
′
|푣푖
|,푗 (BayesWC-LP)
subject to Ψ(|푣푖
|; 푝0, 푝®) ≥ Ψ(|푣˜푖
|;푞0, 푞®) + 푐
′
|푣푖
|,푗 (푖 = 1, . . . , 푁); 푝0, 푝1, . . . , 푝|푝®|
, 푞0, 푞1, . . . , 푞| ®푞| ≥ 0.
Figure 2b shows an example of BayesWC, where the blue dots above a given input size 푛 represents
the samples 푐
′
푛,푗 from the worst-case cost distribution 휇푛. The solutions of the corresponding linear
programs (BayesWC-LP) are shown in red. Whereas Opt delivers a single bound using from one
LP, BayesWC delivers a posterior samples of bounds using multiple randomly generated LPs.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 12

150:12 Long Pham, Feras A. Saad, and Jan Hoffmann
Sampling worst-case costs via Bayesian inference. A central design challenge in BayesWC is
obtaining the distributions 휇푛 over worst-case costs that satisfy Eq. (5.7). Our approach uses
Bayesian inference in a probabilistic generative model over observed costs of the target function 푓 .
In particular, let 퐶푛 be a random variable representing the cost of 푓 applied to a size-푛 input 푣
(the randomness is taken over the (unknown) distribution of 푣). Letting v ≔ (푣1, . . . , 푣푁 ) denote
the observed inputs in D and c ≔ (푐1, . . . , 푐푁 ) the corresponding costs, we infer the distribution of
퐶푛 (푛 ∈ 푁D) by designing a (yet-to-be-specified) Bayesian model that is indexed by v and defines a
probability distribution 휋v (휃, c) over latent parameters 휃 and observable costs c. Conditioned on
the realization of c in the dataset D, the posterior distribution of 휃 is given by the Bayes rule as
휋v (휃 |c) ≔
휋v (휃, c)
∫
휃
′ 휋v (휃
′
, c)d휃
′
∝ ℎ(휃)
Ö
푁
푖=1
푔(푐푖
; 휃, |푣푖
|) (5.9)
where the joint probability factorizes into prior distribution ℎ(휃) over parameters 휃 and a product
of likelihood terms 푔(푐푖
; 휃, |푣푖
|) for the conditionally independent observed costs 푐푖
. Here, 푔 denotes
a distribution over costs R>0 parameterized by an input size 푛 and latent parameter 휃.
Suppose that, given D, we are able to infer the posterior 휋v (휃 |c) as defined in Eq. (5.9). We
generate samples (푐
′
푛,1
, . . . , 푐′
푛,푀 ) in Eq. (5.8) from the worst-case cost distribution 휇푛 by sampling:
휃 푗 ∼ 휋v (휃 |c), 푐′
푛,푗 ∼ 푔e(·;푛, 휃 푗
, [푐ˆ
max
푛
, ∞)) (푗 = 1, . . . , 푀;푛 ∈ 푁D), (5.10)
where the distribution 푔eis defined as the restriction of 푔 to an interval 푈 ⊂ R, that is,
푔e(푥;푛, 휃,푈 ) ≔
푔(푥;푛, 휃)I[푥 ∈ 푈 ]
∫
푥
′∈푈
푔(푥
′
;푛, 휃)d푥
′
(푥 ∈ R). (5.11)
Proposition 5.1. If the likelihood 푔(푐; 휃, 푛) has full support over [0, ∞), then the inferred worst-case
distribution 휇푛 defined by Eqs. (5.10) and (5.11) satisfies the soundness and robustness properties (5.7).
Remark 5.2. The reader may be concerned that the distributions of the 푀 simulated worst-cost
bounds c
′ ≔ (푐
′
푛
, 푛 ∈ 푁D) in Eq. (5.10) are defined in terms of 푐ˆ
max
푛
, which are observation-specific
quantities. However, because the prior 휋v is a probability distribution indexed by a fixed vector
of input instances v that uniquely define the sizes 푁D, the random variable 푐
′
푛 has a well-defined
prior distribution, as demonstrated by the factorization and graphical representation:
휃 c c
′ 휋v (휃, c, c
′
) = ℎ(휃)
Î푁
푖=1
푔(푐푖
; 휃, |푣푖
|) Î
푛∈푁D
푔e(푐
′
푛
;푛, 휃, [ max
푖∈ [푁 ];|푣푖
|=푛
푐푖
, ∞)).
The conditional independence structure in the model is now obvious, and the 푀 replicates of c˜
drawn in Eq. (5.11) are valid posterior inferences conditioned on the observed costs c in D. «
Survival analysis for worst-case costs. To obtain the distribution 휋v (휃, c) (5.9) we design a domain￾general probability model grounded in survival analysis [4] for predicting “time-to-occurrence”
data beyond an observed horizon. We have three parameters 휃 = {훽0, 훽1, 휎} with i.i.d. normal
prior ℎ; a hyperparameter 훾0; a likelihood model 푔 over observable costs 푐 that is defined implicitly
through a variable transformation; and a noise distribution 푔noise:
훽0, 훽1, 휎
iid
∼ Normal(0,훾0), 휖푖 ∼ 푔noise (0, 1), 푦푖 = 훽0 + 훽1 |푣푖
| + |휎|휖푖
, 푐푖 = exp(푦푖). (5.12)
for each 푖 = 1, . . . , 푁 (i.i.d.). Possible choices for the noise distribution 푔noise include the standard
normal, logistic, or Gumbel distributions, which in turn imply that the likelihood model 푔 is a
log-normal, log-logistic, or Weibull distribution each with scale parameter exp(훽0 + 훽1 |푣푖
|) and
shape parameters |휎|, |휎|
−1
, and |휎|
−1
, respectively. Our reference implementation sets 푔noise to be
a Gumbel distribution, for its relatively heavier tails as compared to other choices.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 13

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:13
5.3 Bayesian Inference on Polynomial Coefficients
Overview. Whereas BayesWC performs Bayesian inference on worst-case costs and composes the
results with (BayesWC-LP) to deliver bounds, we develop another approach that bypasses LP solving
and directly performs inference over the unknown coefficients 푝0, 푝, 푞 ® 0, 푞® in the judgment (5.1).
In this approach, which we call BayesPC, our Bayesian model is again indexed by the input
instances v and defines a probability distribution 휋v (휃, 푝0, 푝, 푞 ® 0, 푞, ® c) over a set of auxiliary latent
parameters 휃, resource coefficients 푝0, 푝, 푞 ® 0, 푞®, and observable costs c. Conditioned on c, we sample
푝
′
0
, 푝®
′
, 푞′
0
, 푞®
′ ∼ 휋v (푝0, 푝, 푞 ® 0, 푞®|c), (5.13)
which define the posterior bound 휆푛. Ψ(푛; 푝
′
0
, 푝®
′
) − Ψ(휉(푛);푞
′
0
, 푞®
′
). Figure 2c illustrates this idea:
the blue curves represent posterior samples of cost bounds and the blue dots show samples 푐
′
푛
of inferred worst-case costs that estimate the true value 푐
max
푛
at each input size 푛 ∈ 푁D. As in
BayesWC, BayesPC delivers posterior samples of both worst-case costs and cost bounds, but it
rests on a different modeling and inference approach that bypasses linear programming entirely.
Bayesian polynomial regression for inferring coefficients. The generative model 휋v (휃, 푝0, 푝, 푞 ® 0, 푞, ® c)
in BayesPC must be carefully designed to ensure that the posterior distribution assigns probability
one to the set of coefficients (푝0, 푝, 푞 ® 0, 푞®) that satisfy Eq. (5.3), for any dataset D. As in Remark 5.2,
to obtain a valid Bayesian model, we must define a prior distribution independently of the observed
maximum costs 푐ˆ
max
푛
. We thus model the observable costs (푐1, . . . , 푐푁 ) as random variables where
each 푐푖 takes values in a bounded interval [0, 푐′
|푣푖
|
], 푖 = 1, . . . , 푁. For each 푛 ∈ 푁D, the endpoints 푐
′
푛
of these intervals are themselves random variables defined as polynomial regression outputs that
capture uncertainty in the true worst-case cost 푐
max
푛
. The generative model in BayesPC is given by:
(푝푗)
|푝®|
푗=0
, (푞푗)
| ®푞|
푗=0
iid
∼ Normal≥0 (0,훾0), 휃 ∼ ℎnoise (훾1) (5.14)
푐
′
푛 ≔ Ψ(푛; 푝0, 푝®) − Ψ(휉(푛);푞0, 푞®) (푛 ∈ 푁D) (5.15)
휖푖 ∼ 푔enoise (·; 휃, [0, 푐′
|푣푖
|
]), 푐푖 ≔ 푐
′
|푣푖
|
− 휖푖 (푖 = 1, . . . , 푁; i.i.d.), (5.16)
where 훾0,훾1 are hyperparameters. The term 푔enoise (·; 휃, [0, 푐′
푛
]) is the truncation of an underlying
noise distribution 푔noise (·; 휃) that has full support over [0, ∞) (c.f., Eq. (5.11)). Its parameter 휃 has
prior ℎnoise. We take 푔noise to be a Weibull distribution with scale and shape parameters 휃 ≔ (휃0, 휃1).
Remark 5.3. The main challenge to posterior inference in BayesPC is the fact that the poly￾nomial coefficients 푝0, 푝, 푞 ® 0, 푞® are constrained by 푔enoise to the linear regions 푐푖 ≤ Ψ(|푣푖
|; 푝0, 푝®) −
Ψ(휉(|푣푖
|);푞0, 푞®) for 푖 = 1, . . . , 푁 (in addition to further constraints discussed in Section 6.2). Coeffi￾cients outside this region have zero posterior probability density because they require 휖푖 < 0 for
some 푖, which has zero prior probability. Whereas traditional Markov chain Monte Carlo algorithms
struggle in this setting, we leverage “reflective” Hamiltonian Monte Carlo sampling [15, 18, 58, 69]
for posterior inference in BayesPC, where simulated trajectories reflect at the boundaries of the
convex polytopes. A high-quality implementation is available in the C++ library Volesti [17]. «
5.4 Generalizations
We briefly describe generalizations of BayesWC and BayesPC that relax the simplifying assumptions
made at the beginning of this section and are needed to describe hybrid resource analysis in Section 6.
General variable environments. Suppose we perform data-driven analysis on a function 푓 (푥) =푒
where the measurements (푉푖
,푣˜푖
, 푐푖) in D have general variable environments푉푖 = {푥1 : 푣1, 푥2 : 푣2, . . .}.
In this case, we define a projection function 휑(푉 , 푣) that maps an environment and value to integer
tuples in the set ∪
∞
푑=0
N
푑
. For example, if 푣1 : 퐿(int), 푣2 : 퐿(int), 푣˜ : 퐿(int) are three integer lists
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 14

150:14 Long Pham, Feras A. Saad, and Jan Hoffmann
푓 (푥 ) =
let
statℓ 푒
. . .
Program
Data
Collection Dℓ
runtime
data
BayesWC c
′ℓ
푗
inferred worst-case costs
푗 = 1, . . . , 푀
AARA+H:BayesWC 퐶푗
inferred LP constraints
푗 = 1, . . . , 푀
LP
Solver 퐵푗
inferred cost bounds
푗 = 1, . . . , 푀
(a) Hybrid BayesWC
푓 (푥 ) =
let
statℓ 푒
. . .
Program
Data
Collection Dℓ
runtime
data
BayesPC
AARA+H:Opt 퐶0
inferred LP constraints
(Γ
ℓ
푗
, 푝ℓ
0, 푗, 푎ℓ
푗
, 푞ℓ
0, 푗 )
inferred typing judgments
푗 = 1, . . . , 푀
⊕
combine
퐶푗
inferred LP constraints
푗 = 1, . . . , 푀
LP
Solver 퐵푗
inferred cost bounds
푗 = 1, . . . , 푀
(b) Hybrid BayesPC
Fig. 3. Two hybrid resource analysis techniques for composing static and data-driven resource analysis.
Subexpression 푒 in program 푓 has a cannot be analyzed using AARA: it is analyzed using Bayesian inference.
and 푉 = {푥1 : 푣1, 푥2 : 푣2}, we may define 휑(푉 , 푣) = (|푣1 |, |푣2 |, |푣1 | + |푣2 |, |푣˜|) ∈ N
4
. The unique input
sizes (5.4) are 푁D ≔ {휑(푉푖
,푣˜푖) | 푖 = 1, . . . , 푁}. The models 휋v in BayesWC and BayesPC are now
indexed by v ≔ ( (푉푖
,푣˜푖),푖 = 1, . . . , 푛). Remaining details generalize with minor modifications.
General type judgments. When generalizing the resource-annotated typing judgment (5.1) to the
form {푥1 : 푎1, 푥2 : 푎2, . . . , 푥푚 : 푎푚} ; 푝0 ⊢ 푒 : ⟨푎, 푞0⟩ in Eq. (4.3), each resource-annotated type 푎푖
is
associated with symbolic coefficients 푝®푖 (푖 = 1, . . . ,푚), and the output type 푎 with coefficients 푞®.
The constant potentials 푝0 and 푞0 are unchanged. The linear programs (Opt-LP) and (BayesWC-LP)
and the BayesPC generative model (5.14)–(5.16) are then defined over this expanded collection
of coefficients. Simulations in Eq. (5.13) produced from BayesPC, for example, may be written as
equivalently (푝
′
0
,

푝®
′
푖
	푚
푖=1
, 푞, 푞 ®
′
0
) ∼ 휋v (·|c) or (푝
′
0
, Γ
′
, 푎′
, 푞′
0
) ∼ 휋v (·|c). In the latter case, the sampled
typing environment Γ
′
is obtained by using the sampled coefficient 푝®
′
푖
in place of the symbolic
coefficient within each resource-annotated type 푎푖 (푖 = 1, . . . ,푚), and similarly for 푎
′
and 푞®
′
.
6 HYBRID RESOURCE ANALYSIS
Having described two novel methods for Bayesian data-driven resource analysis, we next present
hybrid resource analysis (Hybrid AARA), which integrates data-driven analysis for parts of the
program tagged by statℓ with static AARA analysis (Section 4) on remaining parts. Hybrid AARA
is based on a formal typing system that extends AARA with a new type judgment:
Γ; 푝0 ⊢D statℓ 푒 : ⟨푎, 푞0⟩. (6.1)
Eq. (6.1) extends (4.3) by including a dataset D of runtime measurements that are collected using
the procedure described in Section 3.3. We also describe novel type inference algorithms and key
technical challenges in the design of the interface between data-driven resource analysis using
Bayesian inference and conventional AARA using static inference and linear programming.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 15

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:15
6.1 Hybrid BayesWC and Opt
Typing rules. Opt and BayesWC are integrated into the AARA type system (described in Appen￾dix A) by adding the following rules for statℓ subexpressions:
H:Opt
푝0 + Φ(푉
ℓ
푖
: Γ) ≥ 푞0 + Φ(푣
ℓ
푖
: 푎) + 푐
ℓ
푖
(푖 = 1, . . . , |Dℓ
|)
Γ; 푝0 ⊢D statℓ 푒 : ⟨푎, 푞0⟩
H:BayesWC
푝0 + Φ(푉
ℓ
푖
: Γ) ≥ 푞0 + Φ(푣
ℓ
푖
: 푎) + 푐
′ℓ
휑 (푉 ,푣)
푐
′ℓ
푛 ∼ 휋
ℓ
v
ℓ (·|c
ℓ
) (푖 = 1, . . . , |Dℓ
|;푛 ∈ 푁Dℓ
)
Γ; 푝0 ⊢D statℓ 푒 : ⟨푎, 푞0⟩
. (6.2)
H:Opt states that the consequent holds whenever the input potential 푝0 + Φ(푉 : Γ) is large enough
to cover both cost 푐 and leftover potential 푞0 + Φ(푣 : 푎) for every measurement (푉 , 푣, 푐) ∈ Dℓ
. In
H:BayesWC, we use labels ℓ to disambiguate data-driven inferences related to different labeled
statℓ sites in the program. That is, we have Dℓ =

(푉
ℓ
푖
, 푣ℓ
푖
, 푐ℓ
푖
) | 푖 = 1, . . . , 푀ℓ
	
, v
ℓ ≔ ( (푉
ℓ
푖
, 푣ℓ
푖
),푖 =
1, . . . , 푀ℓ), and c
ℓ ≔ (푐
ℓ
푖
,푖 = 1, . . . , 푀ℓ). The corresponding probabilistic model (e.g., Eq. (5.12))
used within statℓ
is denoted 휋
ℓ
. H:BayesWC is similar to H:Opt, except that each observed cost 푐
within a measurement (푉 , 푣, 푐) is replaced with a posterior sample 푐
′ℓ
휑 (푉 ,푣)
from BayesWC (5.8) that
captures inferential uncertainty about the true worst-case cost 푐
max
휑 (푉 ,푣)
.
Type inference. Because the premises of H:Opt and H:BayesWC are linear constraints over
the resource coefficients in 푒, type inference operates similarly to conventional AARA. Figure 3a
shows the type inference workflow for BayesWC. Given the runtime data D we first perform data￾driven BayesWC inference to produce 푀 batches of posterior samples of c
′ℓ
푗 ≔ (푐
′ℓ
푛,푗, 푛 ∈ 푁Dℓ
) for
푗 = 1, . . . , 푀 and each label ℓ, which define 푀 versions of H:BayesWC for each statℓ subexpression.
Next, for each 푗 = 1, . . . , 푀 we perform a static pass, denoted AARA+H:BayesWC in Fig. 3a, that
constructs a template typing tree according to the conventional AARA type system for traditional
expressions and uses (the posterior sample of) H:BayesWC for statℓ subexpressions. This process
produces 푀 systems of linear constraints 퐶푗 (푗 = 1, . . . , 푀), where the linear constraints within
each 퐶푗 are derived from two provenances: those from the conventional AARA type system and
those from the H:BayesWC type rule. Each 퐶푗
is provided to an LP solver to provide a typing
judgment 퐽푗 for the root node’s typing context, which translates to an inferred cost bound.
Linear Programming Objective. When solving the overall linear program in AARA+H:BayesWC
or AARA+H:Opt, our solver first minimizes the sum of cost gaps form the data-driven components
(i.e., (Opt-LP) or (BayesWC-LP)) and then performs minimization of input coefficients at the root.
As with conventional AARA [42], it is possible to either minimize the sum of coefficients at the root
or minimize higher-degree coefficients with higher priorities. Our prototype of hybrid resource
analysis allows users to make either choice.
6.2 Hybrid BayesPC
Key challenge. Integrating Bayesian data-driven resource analysis with BayesPC into conven￾tional AARA is fundamentally more difficult as compared to integrating Opt and BayesWC. This
difficulty arises because resource coefficients in the typing judgment Γ; 푝0 ⊢D statℓ 푒 : ⟨푎, 푞0⟩
are sampled using Bayesian inference in BayesPC, while they are optimized using LP solvers in
both Opt and BayesWC. AARA poses a challenge because we do not know in advance how much
potential should be stored in ⟨푎, 푞0⟩. Unlike in fully data-driven resource analysis, in hybrid resource
analysis the output ofstatℓ 푒 may be used in a subsequent computation that also consumes potential.
Both Γ and 푝0 should store enough potential to pay for both its own cost and the cost of subsequent
computation. Naïvely sampling resource annotations (Γ, 푝0, 푎, 푞0) for the statℓ subexpressions using
BayesPC and providing them to a conventional AARA pass over the remaining program will
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 16

150:16 Long Pham, Feras A. Saad, and Jan Hoffmann Density
−1.0
−0.5
0.0
0.5
1.0
1.5
Feasible Region
π
ℓ
vℓ
(a) BayesPC
Density
−1.0
−0.5
0.0
0.5
1.0
1.5
Feasible
Region C0
AARA
π
ℓ
vℓ
|C0
(b) Hybrid BayesPC
Fig. 4. Posterior distributions over resource coefficients restricted to convex polytopes using BayesPC.
likely produce a system with no solution. Hence, we need an interface between sampling-based
probabilistic inference over some coefficients and linear programming over other coefficients.
Type inference. We address this challenge by adding linear constraints to the BayesPC probabilistic
models that encode feasible regions of linear programs computed by conventional AARA. This
approach guarantees that judgments from BayesPC cannot impose new constraints that cause the
linear programs to fail to have a solution.
Figure 3b shows our type inference approach. We start by performing a static analysis pass
through the program using the conventional AARA type system to obtain a set of linear constraints
퐶0, treating any statℓ using the rule H:Opt to ensure consistency with runtime data Dℓ
. Next, for
each subexpression statℓ encountered in the first pass, we apply a variant of BayesPC that combines
both the runtime data Dℓ and constraints 퐶0 from the first pass to infer a resource-annotated typing
judgment of the form Γ; 푝0 ⊢D statℓ 푒ℓ
: ⟨푎, 푞0⟩.
Let 휋
ℓ
v
ℓ
(휃, Γ, 푝0, 푞0, 푎, c) denote the BayesPC probabilistic model for statℓ
(e.g., Eqs. (5.14)–(5.16)).
The constraints 퐶0 are used to construct a modified probabilistic model 휋
ℓ
v
ℓ
|퐶0
(휀, 휃, Γ, 푝0, 푞0, 푎, c),
where 휀 is a collection of nuisance parameters that contains all the resource coefficients appearing
in the AARA constraints 퐶0. Letting ℎ(휀) denote an uninformative prior (e.g., uniform if 퐶0 is
bounded), the modified probabilistic model is restricted to the convex polytope defined by 퐶0:
휋
ℓ
v
ℓ
|퐶0
(휀, 휃, Γ, 푝0, 푞0, 푎, c) ∝ ℎ(휀)휋
ℓ
v
ℓ (휀, 휃, Γ, 푝0, 푞0, 푎, c)I[(휀, . . . ) ∈ 퐶0], (6.3)
where I[(휀, . . . ) ∈ 퐶0] is 1 if the resource coefficients in the arguments to 휋
ℓ
v
ℓ
|퐶0
satisfy constraints
퐶0 and 0 otherwise. Figure 4 shows an example: the original “Feasible Region” (grey, Fig. 4a) in
BayesPC induced by runtime data is further constrained by the constraints from the first AARA
pass (orange, Fig. 4b), with the distribution re-normalized appropriately.
Eq. (6.3) is then used to sample judgments
(Γ
ℓ
푗
, 푝ℓ
0,푗, 푎ℓ
푗
, 푞ℓ
0,푗) ∼ 휋
ℓ
v
ℓ
|퐶0
(Γ, 푝0, 푞0, 푎|c
ℓ
) (푗 = 1, . . . , 푀;ℓ ∈ 퐿
′
), (6.4)
which are shown as the output of BayesPC in Fig. 3a. Each sampled typing judgment in Eq. (6.4)
corresponds to a concrete realization of symbolic LP variables in 퐶0 created by the corresponding
H:Opt rule at label ℓ during the first pass. We can then obtain 푀 new constraints
퐶푗 ≔ 퐶0 ⊕

(Γ
ℓ
푗
, 푝ℓ
0,푗, 푎ℓ
푗
, 푞ℓ
0,푗) | ℓ ∈ 퐿
′
	
(푗 = 1, . . . , 푀) (6.5)
by syntactically replacing the symbolic LP variables in 퐶0 with concrete variables at all labels ℓ ∈ 퐿
′
.
Each 퐶푗
is then fed to an LP solver to obtain 푀 posterior samples (퐵1, . . . , 퐵푀 ) of cost bounds.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 17

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:17
6.3 Soundness
We formulate and prove two soundness theorems for Hybrid AARA.
Theorem 6.1 establishes that inferred cost bounds from Hybrid AARA are sound with respect to
all 푁 measurements in the runtime data (collected using the procedure described in Section 3.3)
Theorem 6.1. Given a program P, expression 푒 and D be the runtime data such that (푉푖 ⊢P 푒 ⇓
푐푖
푣푖)
푁
푖=1
| D. The following property holds with probability one: If Γ; 푝0 ⊢D 푒 : ⟨푎, 푞0⟩ holds in the type
system of hybrid resource analysis, then Φ(푉푖
: Γ) + 푝0 − Φ(푣푖
: 푎) − 푞0 ≥ 푐푖 for any 푖 = 1, . . . , 푁.
Proof. The proof proceeds by nested induction on (푉푖 ⊢ 푒 ⇓푐푖
푣푖)
푁
푖=1
| D (outer induction)
and Γ; 푝0 ⊢D 푒 : ⟨푎, 푞0⟩ (inner induction), following the same structure as the soundness proof
of conventional AARA [39, 40]. The only necessary modification is proving the base case where
푒 ≡ statℓ 푒
′
for some expression 푒
′
, for the new inference rules H:Opt, H:BayesWC, and H:BayesPC.
We argue that for each typing rule, the resource-annotated judgment Γ; 푃 ⊢D statℓ 푒
′
: ⟨푎, 푞0⟩
is sound with respect to any measurement (푉 , 푣, 푐) ∈ Dℓ
, meaning that the typing rule ensures
Φ(푉 : Γ) + 푝0 − Φ(푣 : 푎) − 푞0 ≥ 푐 holds with probability one. For H:OPT, the property follows
immediately from the premise of the typing rule. For H:BayesWC, Proposition 5.1 establishes a
condition that guarantees, for any runtime sample (푉 , 푣, 푐) ∈ Dℓ
, the probabilistic model 휋v used in
BayesWC has zero probability of simulating a cost푐
′ℓ
휑 (푉 ,푣)
< 푐. Our choice of the likelihood function
푔 in Eq. (5.12) satisfies this requirement. Using this fact, the premise of H:BayesWC implies
Φ(푉 : Γ) + 푝0 − Φ(푣 : 푎) − 푞0 ≥ 푐
′ℓ
휑 (푉 ,푣)
≥ 푐ˆ
max,ℓ
휑 (푉 ,푣)
≥ 푐 = 1 almost surely, (6.6)
and the conclusion follows. For H:BayesPC, Remark 5.3 establishes that the 휋
ℓ
v
assigns zero posterior
probability density to any (Γ, 푝0, 푎, 푞0) that satisfies Φ(푉 : Γ) + 푝0 − Φ(푣 : 푎) − 푞0 < 푐 for some
runtime sample (푉 , 푣, 푐) ∈ Dℓ
. As constraining 휋
ℓ
v
to the convex polytope 퐶0 in Eq. (6.3), cannot
possibly increase its support, the conclusion follows for H:BayesPC. □
The next result establishes the probability (over the randomness of the collected runtime data)
that inferred cost bounds from Hybrid AARA are sound up to a given input-size limit converges to
one as the dataset size 푁 tends to infinity.
Theorem 6.2. Let D be runtime data such that (푉푖 ⊢P 푒 ⇓
푐푖 푣푖)
푁
푖=1
| D, where (푉푖)
푁
푖=1
are 푁
i.i.d. samples from an (unknown) input distribution and 푒 is an expression in program P. Assume there
exists an integer 푚 and finite set V푚 of well-typed environments such that for all 푉 ∈ V푚: 휑(푉 ) < 푚
and 푉 has nonzero probability of appearing in D. Then for any typing judgment Γ; 푝0 ⊢D 푒 : ⟨푎, 푞0⟩
inferred from Hybrid AARA, the probability that it satisfies Φ(푉 : Γ) + 푝0 − Φ(푣 : 푎) − 푞0 ≥ 푐 for all
푉 such that 푉 ⊢P 푒 ⇓
푐
푣 and 휑(푉 ) ≤ 푚 converges to one as 푁 → ∞.
Proof. For each 푛 = 1, . . . ,푚, there exists a worst-case environment
푉
max
푛 ≔ arg max
푉 ∈V푚
{푐 | 휙 (푉 ) = 푛,푉 ⊢P 푒 ⇓
푐
푣˜} (6.7)
with a maximal execution cost. Let 푝
max
푛 > 0 be the probability 푉
max
푛
is selected. Let 푊푛,푁 be
the event that 푉
max
푛
is sampled within 푁 i.i.d. draws. The probability that all worst-case inputs
푉
max
1
, . . . ,푉 max
푚 occur in runtime dataset D of size 푁 is
P
Ñ푚
푛=0푊푛,푁 
= 1 − P
Ð푚
푛=0푊 푛,푁 
≥ 1 −
Í푚
푛=1 P(푊 푛,푁 ) = 1 −
Í푚
푛=1
(1 − 푝
max
푛
)
푁 (6.8)
where 푊 푛,푁 denotes the complement of event 푊푛,푁 . The inequality follows from the union bound.
The last expression converges to one as 푁 → ∞ because 푝
max
푛 > 0 for each 푛. The conclusion
follows from Theorem 6.1, which establishes that resource-annotated typing judgements from
Hybrid AARA are sound with respect to the environments used to generate runtime data D. □
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 18

150:18 Long Pham, Feras A. Saad, and Jan Hoffmann
7 EVALUATION
Implementation. We implemented a prototype of Hybrid AARA [76] that integrates data-driven
(optimization-based and Bayesian) resource analysis into Resource-Aware ML (RaML) [42] and
evaluated it on challenging benchmarks that purely static analysis cannot solve. Each analysis run
using the prototype requires: (i) an OCaml program annotated with Raml.tick and Raml.stat; (ii)
a list of inputs for runtime cost data generation; and (iii) a configuration file, which includes e.g., a
polynomial degree, a data-driven analysis technique, a probabilistic model, and hyperparameters.
Appendix B describes an empirical Bayesian procedure to automatically determine hyperparameters.
Benchmarks. We built a benchmark suite of 10 functional programs (source code in Appendix C).
• MapAppend: Given two lists, 푥 and 푦, for each element of 푥, run some (statically unanalyzable)
function 푓 and append its output to the cumulative result (whose initial value is 푦).
• Concat: Given a nested list, recursively append inner lists to the cumulative result.
• InsertionSort2: Sequentially run insertion sort twice on a list. We focus on the cost of
comparisons in the second insertion sort.
• QuickSort: Run deterministic quicksort on lists with their heads as pivots for partition.
• QuickSelect: Given an integer 푖 and a list, run deterministic quickselect and return the 푖
th
smallest element in the list. Like Quicksort, it uses the heads of lists as pivots.
• MedianOfMedians: Given an integer 푖 and a list, recursively compute the 푖
th smallest element
in the list by first computing the median of medians then using it to partition the list.
• ZAlgorithm: Given a list 푥, return a list 푦 such that 푦[푖] stores the maximum integer ℓ such
that 푥 [0, . . . , ℓ − 1] = 푥 [푖, . . . ,푖 + ℓ − 1].
• BubbleSort: Run bubble sort where pairs of adjacent reverse-ordered elements are repeatedly
swapped until no such pairs exist (i.e., saturation).
• Round: Given a natural number 푥 (represented as a list), compute a natural number 푦 such
that 푦 is the largest power of two below 푥. Once 푦 is computed, we traverse 푦.
• EvenOddTail: Given a natural number 푥 (represented as a list), first traverse the list and if 푥
is even, we divide it by two; otherwise, we subtract one from it.
Conventional AARA cannot return a tight cost bound for any of these 10 programs. Specifically,
it cannot analyze 7/10 programs at all as they contain statically unanalyzable code fragments. For
BubbleSort, AARA cannot even reason about its termination due to bubble sort being saturation￾based. For MedianOfMedians, AARA cannot reason about the mathematical properties of medians.
For Round, to prove its linear complexity, AARA would need an infinitely tall resource-annotated
typing tree. The four benchmarks MapAppend, Concat, QuickSort, and QuickSelect fail because
they contain some complex function that conventional AARA cannot analyze (e.g., OCaml’s built-in
polymorphic comparator). For the remaining 3/10 programs, to infer some polynomial cost bound,
conventional AARA requires a wrong polynomial degree that is too high.
Proportions of sound cost bounds. Table 1 shows the proportion of inferred cost bounds that
are sound as well as analysis runtimes for all 10 benchmarks using data-driven analysis (Opt,
BayesWC, BayesPC) and their hybrid counterparts, where applicable. Optimization-based resource
analyses (data-driven and hybrid Opt) always return a single inferred cost bound, while Bayesian
resource analyses return collections of samples of cost bounds drawn from the posterior probability
distribution. In all benchmarks, for both data-driven and hybrid analyses, BayesWC produces
strictly higher proportions of sound cost bounds than Opt. This finding demonstrates that cost
bounds inferred by BayesWC are more robust than those inferred by Opt in 10/10 cases (data￾driven) and 7/7 cases (hybrid); that is, BayesWC has a strictly positive probability of inferring a
sound bound even though the runtime cost dataset does not contain worst-case inputs. In contrast,
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 19

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:19
Table 1. Percentage of inferred cost bounds that are sound and analysis runtime for 10 benchmark programs.
Benchmark Conventional Analysis Fraction of Sound Inferred Bounds Analysis Runtime
Program AARA Method Data-Driven Hybrid Data-Driven Hybrid
MapAppend Cannot Analyze Opt 0% 0% 0.01 s 0.01 s
BayesWC 68.5% 100% 1.87 s 12.44 s
BayesPC 75.5% 100% 51.83 s 360.80 s
Concat Cannot Analyze Opt 0% 0% 0.00 s 0.01 s
BayesWC 67.3% 96.7% 2.54 s 14.73 s
BayesPC 96% 100% 113.53 s 125.28 s
InsertionSort2 Wrong Degree Opt 0% 0% 0.01 s 0.02 s
BayesWC 57.6% 100% 1.53 s 5.46 s
BayesPC 21% 57.5% 10.68 s 220.66 s
QuickSort Cannot Analyze Opt 0% 0% 0.01 s 0.11 s
BayesWC 4% 96% 2.20 s 144.88 s
BayesPC 0% 100% 13.72 s 274.51 s
QuickSelect Cannot Analyze Opt 0% 0% 0.02 s 0.19 s
BayesWC 0.2% 98.2% 1.83 s 222.47 s
BayesPC 0% 100% 12.39 s 277.20 s
MedianOfMedians Cannot Analyze Opt 0% 0% 0.17 s 0.21 s
BayesWC 11.5% 71.3% 2.36 s 93.89 s
BayesPC 0% 100% 70.39 s 896.98 s
ZAlgorithm Wrong Degree Opt 0% 0% 0.09 s 0.13 s
BayesWC 13.7% 95.9% 1.96 s 72.21 s
BayesPC 28% 100% 11.11 s 509.29 s
BubbleSort Cannot Analyze Opt 0% Cannot Analyze 0.01 s ∅
BayesWC 40.1% Cannot Analyze 2.69 s ∅
BayesPC 31.5% Cannot Analyze 11.70 s ∅
Round Cannot Analyze Opt 0% Cannot Analyze 0.01 s ∅
BayesWC 58.3% Cannot Analyze 1.91 s ∅
BayesPC 81% Cannot Analyze 12.87 s ∅
EvenOddTail Wrong Degree Opt 0% Wrong Degree 0.01 s ∅
BayesWC 65.1% Wrong Degree 1.98 s ∅
BayesPC 70% Wrong Degree 11.79 s ∅
10 100 1000
Input Size
-1
0
1
2
4
8
16
32
64
128
256
512
1024
2048
Relative Gap in Inferred Cost Bound
QuickSort
10 100 1000
Input Size
-1
0
1
2
4
8
16
32
64
128
256
QuickSelect
10 100 1000
Input Size
-1
0
1
2
4
MedianOfMedians
10 100 1000
Input Size
-1
0
1
2
4
8
Unsound
Region
Sound
Region
Round
10 100 1000
Input Size
-1
0
1
2
4
8
EvenOddTail
OPT Data-Driven BayesWC Data-Driven BayesPC Data-Driven OPT Hybrid BayesWC Hybrid BayesPC Hybrid
Fig. 5. Estimation gaps of inferred cost bounds with respect to ground-truth worst-case costs on 5 benchmarks.
in these benchmarks, Opt never returns a sound bound. Likewise, BayesPC returns more robust
bounds than Opt in 7/10 (data-driven) and 7/7 cases (hybrid). These improvements highlight the
benefits of probabilistic inference as compared to optimization.
Between fully data-driven Bayesian analysis and Hybrid AARA using BayesWC and BayesPC,
the latter delivers a substantially larger fraction of sound cost bounds in all seven benchmarks.
These results illustrate the benefits of integrating data-driven analysis with static type inference on
the remaining parts of the program not tagged with stat expressions.
The right two columns of Table 1 show the analysis runtime. Opt uses an LP solver that is much
faster than sampling algorithms: it returns answers in less than one second, whereas Bayesian
resource analysis can take minutes. Between BayesWC and BayesPC, the former is faster in terms
of analysis time per iteration. The main reason is that BayesWC uses HMC sampling without
constraints, which is much simpler than reflective HMC sampling over convex polytopes (Fig. 4)
needed for inference in BayesPC.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 20

150:20 Long Pham, Feras A. Saad, and Jan Hoffmann
QuickSort (D) QuickSelect (D) MedianOfMedians (D) Round (D)
QuickSort (H) QuickSelect (H) MedianOfMedians (H) EvenOddTail (D)
Fig. 6. Plots of inferred bounds for various benchmarks and resource analysis methods shown in Fig. 5
(D=Data Driven; H=Hybrid). Each benchmark has three plots (le-to-right): Opt, BayesWC, and BayesPC.
Opt
0
10
20
30
40 Input Size 1
0
10
20
30
40
Input Size 2
0
20
40
60
BayesWC
0
10
20
30
40 Input Size 1
0
10
20
30
40
Input Size 2
0
20
40
60
BayesPC
0
10
20
30
40 Input Size 1
0
10
20
30
40
Input Size 2
0
20
40
60
(a) Data-Driven Resource Analysis
Opt
0
10
20
30
40 Input Size 1
0
10
20
30
40
Input Size 2
0
20
40
60
BayesWC
0
10
20
30
40 Input Size 1
0
10
20
30
40
Input Size 2
0
20
40
60
BayesPC
0
10
20
30
40 Input Size 1
0
10
20
30
40
Input Size 2
0
20
40
60
(b) Hybrid Resource Analysis
Fig. 7. Plots of inferred multivariate cost bounds for MapAppend using data-driven resource analysis and
Hybrid AARA. Red planes show ground-truth tight worst-case bound and blue planes show inferred bounds.
Distributions of estimation gaps. Figure 5 shows relative estimation gaps of inferred cost bounds
with respect to the ground truth worst case bound in five benchmarks (full results in Appendix C).
In each benchmark, we fix three input sizes (10, 100, and 1000). For each size, we show the 5th
,
50th, and 95th percentiles of relative estimation gaps. Because Opt infers a single bound, it has the
same estimation gap for all percentiles. Relative estimation gaps below 0 (resp. above 0) indicate an
underestimate (resp. overestimate) of the true bound. A cost bound is sound if its estimation gap is
at least 0. Figure 5 exhibits similar results as in Table 1. The QuickSort and QuickSelect panels
in Fig. 5 show an interesting finding. At input size 10, the bounds from Data-Driven BayesWC and
BayesPC are tighter than those from their Hybrid counterparts, but some of the former bounds are
unsound. As the input size increases, the estimation gaps from Hybrid AARA shrink but remain in
the “Sound Region,” whereas those from data-driven Bayesian analysis become unsound.
Posterior distributions of cost bounds. Figure 6 shows posterior distributions of cost bounds of five
benchmarks. Red curves are the true bounds and black dots show the runtime cost data. Blue curves
are median cost bounds, and light-blue shades around them show the 10–90th percentile ranges. In
both data-driven and hybrid analyses, Bayesian resource analysis delivers a sizeable fraction of
correct bounds. Certain datasets such as MedianOfMedians in Fig. 6 are particularly challenging for
purely data-driven analysis, however. Between data-driven and hybrid analyses, the cost bounds
from the latter are always more accurate (i.e., closer to sound worst-case cost bounds). Fig. 7 shows
inferred cost bounds for MapAppend, which are multivariate. The median bounds for the Bayesian
methods always lie about the ground-truth plane, whereas the single bounds for Data-Driven Opt
and Hybrid Opt are both incorrect.
Summary. Our evaluation has several key takeaways. First, in the 7/10 programs that conventional
AARA cannot solve (first 7 rows of Table 1), Hybrid AARA successfully returns accurate and robust
bounds using at least one of Hybrid BayesWC or Hybrid BayesPC. In the 3/10 programs that
Hybrid AARA cannot solve (last 3 rows of Table 1), purely data-driven analysis using BayesWC or
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 21

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:21
BayesPC gives good proportions of sound bounds. Second, Bayesian resource analysis delivers a
substantially higher percentage of sound cost bounds as compared to optimization-based analysis
in both the purely data-driven and hybrid case. Between BayesWC and BayesPC, the former is
more conservative: it gives a larger fraction of sound bounds in the purely data-driven case, but its
cost gaps are higher. Third, for Hybrid AARA, incorporating static analysis (when possible) gives a
higher proportion of sound bounds than purely data-driven analysis with a similar runtime.
We have no clear winner between Hybrid BayesWC and Hybrid BayesPC: the latter is slower
but more accurate than the former in 5/7 cases. Additionally, BayesPC enables richer probabilistic
models than BayesWC since the probabilistic model of BayesPC models not only worst-case costs
but also resource coefficients. In practice, depending on the application, one can take the looser or
tighter result of the two methods.
8 RELATED WORK
Static resource analysis. Existing static resource techniques are based on type systems [5, 21,
24, 26, 38, 59, 86], recurrence relations [2, 25, 35, 55, 56, 88], term rewriting [6, 7, 49, 72], ranking
functions [12, 20, 31, 82], and abstract interpretation [3, 37, 91]. Our works builds on automatic
amortized resource analysis (AARA) [36, 39, 40, 42, 45, 48, 54, 57, 61] a type-based resource￾analysis technique to analyze functional programs by automating the potential method of amortized
analysis [83–85]. AARA also has been used to analyze imperative code [13], parallel programs [46],
probabilistic programs [8, 73, 87], and session-typed concurrent programs [27, 28]. We are not
aware of prior works that combine static resource analysis with data-driven resource analysis.
Experimental algorithmics. Inference of algorithmic complexity from experiment data has been
extensively studied in the field of experimental algorithmics [29, 52, 65, 66, 71, 81]. These works
focus on using experimental data for improving pen-and-paper analyses of asymptotic complexity of
algorithms. Instead, this work focuses on using data-driven approaches for deriving non-asymptotic
bounds for programs and combining data-driven analysis with static resource analysis.
Data-driven resource analysis. There exist tools for analyzing the complexity of programs from
runtime cost samples [23, 30, 33, 50, 77, 80, 90]. Most of these works deliver average-case bounds
instead of worst-case bounds. Dynaplex [51] first infers a recurrence relation of a recursive program
from its execution traces by optimization and then solves the recurrence relation by the master
theorem. Our work on data-driven Bayesian resource analysis differs from existing works in this
field in several ways. First, we develop novel data-driven resource analyses based on Bayesian
inference (Section 5), which give us posterior distributions over unknown bounds that are more
robust than point estimates from optimization-based inference (e.g., Demontiê et al. [30] use
polynomial interpolation and Goldsmith et al. [33] use least-square power regression). Second, we
integrate data-driven Bayesian resource analysis into AARA to obtain Hybrid AARA (Section 6),
which to our knowledge is the first such combination of static and data-driven analysis.
Worst-case execution time analysis. Data-driven techniques have been studied in the worst-case
execution time (WCET) analysis of real-time embedded systems. This area focuses on deriving
concrete (i.e., non-symbolic) cost bounds of programs running on real-world hardware. Typically,
the maximum number of loop iterations in programs is assumed to be a constant independent
of input sizes. Numerous works study the use of extreme-value theory in measurement-based,
probabilistic WCET analysis [1, 16, 32, 34, 63, 64, 68, 78]. These methods all leverage frequentist
(non-Bayesian) inference. The hybrid of static and measurement-based WCET analyses has been
studied [9, 10, 89]. Unlike WCET analysis, our work focuses on symbolic cost bounds of programs
parametric in input sizes.
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 22

150:22 Long Pham, Feras A. Saad, and Jan Hoffmann
9 CONCLUSION
This article has introduced Hybrid AARA, which to the best of our knowledge is the first resource
analysis method that combines data-driven and static resource analysis. We have presented two
novel data-driven Bayesian resource analysis methods (BayesWC and BayesPC) for inferring
principled posterior distributions over cost bounds. The data-driven Bayesian resource analyses
introduced in this work deliver more accurate and robust bounds as compared to previous methods
that use greedy optimization, which only gives a single point estimate. Our main contribution—
Hybrid AARA—integrates our Bayesian data-driven resource analyses into conventional AARA
using a novel type inference system. Two notions of soundness for Hybrid AARA are identified and
proven. We implemented a prototype of Hybrid AARA by extending Resource-Aware ML (RaML)
and evaluated it on a set of 10 challenging benchmarks that conventional AARA cannot solve. The
results on this benchmark set indicate that Hybrid AARA achieves several of its design goals. Our
system demonstrates the benefits of integrating Bayesian inference with traditional type inference
for improving the coverage of static analysis on the one hand and the accuracy and robustness of
data-driven analysis on the other hand.
ACKNOWLEDGMENTS
The authors wish to thank the anonymous referees for their valuable comments and helpful
suggestions. We also would like to thank Richard Peng and Daniel Sleator at Carnegie Mellon
University for their helpful suggestions for the benchmark suite of Hybrid AARA. This material
is based upon work supported by the National Science Foundation under Grant Nos. 2311983,
2007784, and 1845514. Any opinions, findings, and conclusions or recommendations expressed
in this material are those of the authors and do not necessarily reflect the views of the National
Science Foundation.
REFERENCES
[1] Jaume Abella, Maria Padilla, Joan Del Castillo, and Francisco J. Cazorla. 2017. Measurement-Based Worst-Case
Execution Time Estimation Using the Coefficient of Variation. ACM Transactions on Design Automation of Electronic
Systems 22, 4, Article 72 (June 2017), 29 pages. https://doi.org/10.1145/3065924
[2] Elvira Albert, Puri Arenas, Samir Genaim, German Puebla, and Damiano Zanardini. 2007. Cost Analysis of Java
Bytecode. In Programming Languages and Systems (Lecture Notes in Computer Science, Vol. 4421). Springer, Berlin,
157–172. https://doi.org/10.1007/978-3-540-71316-6_12
[3] Elvira Albert, Puri Arenas, Samir Genaim, German Puebla, and Damiano Zanardini. 2008. COSTA: Design and
Implementation of a Cost and Termination Analyzer for Java Bytecode. In Formal Methods for Components and Objects
(Lecture Notes in Computer Science, Vol. 5382). Springer, Berlin, 113–132. https://doi.org/10.1007/978-3-540-92188-2_5
[4] Per K. Andersen and Michael Vaeth. 2015. Survival Analysis. In Wiley StatsRef: Statistics Reference Online. John Wiley
& Sons, Ltd, Hoboken, NJ, USA. https://doi.org/10.1002/9781118445112.stat02177.pub2
[5] Martin Avanzini and Ugo Dal Lago. 2017. Automating Sized-Type Inference for Complexity Analysis. Proc. ACM
Program. Lang. 1, ICFP, Article 43 (Aug. 2017), 29 pages. https://doi.org/10.1145/3110287
[6] Martin Avanzini, Ugo Dal Lago, and Georg Moser. 2015. Analysing the Complexity of Functional Programs: Higher￾order Meets First-Order. In Proc. 20th ACM SIGPLAN International Conference on Functional Programming. ACM, New
York, NY, USA, 152–164. https://doi.org/10.1145/2784731.2784753
[7] Martin Avanzini and Georg Moser. 2016. A Combination Framework for Complexity. Information and Computation
248 (2016), 22–55. https://doi.org/10.1016/j.ic.2015.12.007
[8] Martin Avanzini, Georg Moser, and Michael Schaper. 2020. A Modular Cost Analysis for Probabilistic Programs. Proc.
ACM Program. Lang. 4, OOPSLA (Nov. 2020), 1–30. https://doi.org/10.1145/3428240
[9] Guillem Bernat, Antoine Colin, and Stefan Petters. 2003. pWCET: A Tool for Probabilistic Worst-Case Execution Time
Analysis of Real-Time Systems. Technical Report YCS-2003-353. University of York.
[10] Adam Betts, Nicholas Merriam, and Guillem Bernat. 2010. Hybrid Measurement-Based WCET Analysis at the Source
Level Using Object-Level Traces. In 10th International Workshop on Worst-Case Execution Time Analysis (OpenAccess
Series in Informatics (OASIcs), Vol. 15). Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik, Dagstuhl, Germany, 54–63.
https://doi.org/10.4230/OASIcs.WCET.2010.54
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 23

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:23
[11] Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest, and Robert E. Tarjan. 1973. Time Bounds for Selection.
J. Comput. System Sci. 7, 4 (Aug. 1973), 448–461. https://doi.org/10.1016/S0022-0000(73)80033-9
[12] Marc Brockschmidt, Fabian Emmes, Stephan Falke, Carsten Fuhs, and Jürgen Giesl. 2014. Alternating Runtime and
Size Complexity Analysis of Integer Programs. In Proc. 20th International Conference on Tools and Algorithms for the
Construction and Analysis of Systems (TACAS 2014) (Lecture Notes in Computer Science, Vol. 8413). Springer, Berlin,
140–155. https://doi.org/10.1007/978-3-642-54862-8_10
[13] Quentin Carbonneaux, Jan Hoffmann, and Zhong Shao. 2015. Compositional Certified Resource Bounds. In Proc. 36th
ACM SIGPLAN Conference on Programming Language Design and Implementation. ACM, New York, NY, USA, 467–478.
https://doi.org/10.1145/2737924.2737955
[14] George Casella. 1985. An Introduction to Empirical Bayes Data Analysis. The American Statistician 39, 2 (1985), 83–87.
https://doi.org/10.1080/00031305.1985.10479400
[15] Frederic Cazals, Augustin Chevallier, and Sylvain Pion. 2022. Improved Polytope Volume Calculations Based on
Hamiltonian Monte Carlo with Boundary Reflections and Sweet Arithmetics. Journal of Computational Geometry 13, 1
(April 2022), 52–88. https://doi.org/10.20382/jocg.v13i1a3
[16] Francisco J. Cazorla, Tullio Vardanega, Eduardo Quiñones, and Jaume Abella. 2013. Upper-Bounding Program
Execution Time with Extreme Value Theory. In 13th International Workshop on Worst-Case Execution Time Analysis
(Open Access Series in Informatics, Vol. 30). Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, Wadern, 64–76. https:
//doi.org/10.4230/OASIcs.WCET.2013.64
[17] Apostolos Chalkis and Vissarion Fisikopoulos. 2021. Volesti: Volume Approximation and Sampling for Convex
Polytopes in R. The R Journal 13, 2 (2021), 642–660. https://doi.org/10.32614/RJ-2021-077
[18] Apostolos Chalkis, Vissarion Fisikopoulos, Marios Papachristou, and Elias Tsigaridas. 2023. Truncated Log-concave
Sampling for Convex Bodies with Reflective Hamiltonian Monte Carlo. ACM Trans. Math. Software 49, 2, Article 16
(June 2023), 25 pages. https://doi.org/10.1145/3589505
[19] Arthur Charguéraud and François Pottier. 2019. Verifying the Correctness and Amortized Complexity of a Union-Find
Implementation in Separation Logic with Time Credits. Journal of Automated Reasoning 62, 3 (March 2019), 331–365.
https://doi.org/10.1007/s10817-017-9431-7
[20] Krishnendu Chatterjee, Hongfei Fu, and Amir Kafshdar Goharshady. 2019. Non-Polynomial Worst-Case Analysis of
Recursive Programs. ACM Transactions on Programming Languages and Systems 41, 4, Article 20 (Oct. 2019), 52 pages.
https://doi.org/10.1145/3339984
[21] Ezgi Çiçek, Gilles Barthe, Marco Gaboardi, Deepak Garg, and Jan Hoffmann. 2017. Relational Cost Analysis. In
Proc. 44th ACM SIGPLAN Symposium on Principles of Programming Languages. ACM, New York, NY, USA, 316–329.
https://doi.org/10.1145/3009837.3009858
[22] Ezgi Çiçek, Mehdi Bouaziz, Sungkeun Cho, and Dino Distefano. 2021. Static Resource Analysis at Scale (Extended
Abstract). In Proc. 27th International Static Analysis Symposium (Lecture Notes in Computer Science, Vol. 12389). Springer,
Cham, 3–6. https://doi.org/10.1007/978-3-030-65474-0_1
[23] Emilio Coppa, Camil Demetrescu, and Irene Finocchi. 2012. Input-Sensitive Profiling. In Proc. 33rd ACM SIGPLAN
Conference on Programming Language Design and Implementation. ACM, New York, NY, USA, 89–98. https://doi.org/
10.1145/2254064.2254076
[24] Karl Crary and Stephnie Weirich. 2000. Resource Bound Certification. In Proc. 27th ACM SIGPLAN-SIGACT Symposium
on Principles of Programming Languages. ACM, New York, NY, USA, 184–198. https://doi.org/10.1145/325694.325716
[25] Joseph W. Cutler, Daniel R. Licata, and Norman Danner. 2020. Denotational Recurrence Extraction for Amortized
Analysis. Proc. ACM Program. Lang. 4, ICFP, Article 97 (Aug. 2020), 29 pages. https://doi.org/10.1145/3408979
[26] Nils Anders Danielsson. 2008. Lightweight Semiformal Time Complexity Analysis for Purely Functional Data Structures.
In Proc. 35th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages. ACM, New York, NY,
USA, 133–144. https://doi.org/10.1145/1328438.1328457
[27] Ankush Das, Stephanie Balzer, Jan Hoffmann, Frank Pfenning, and Ishani Santurkar. 2019. Resource-Aware Session
Types for Digital Contracts. arXiv:1902.06056 [cs]
[28] Ankush Das, Jan Hoffmann, and Frank Pfenning. 2018. Work Analysis with Resource-Aware Session Types. In
Proc. 33rd Annual ACM/IEEE Symposium on Logic in Computer Science. ACM, New York, NY, USA, 305–314. https:
//doi.org/10.1145/3209108.3209146
[29] Camil Demetrescu, Irene Finocchi, and Giuseppe F. Italiano. 2003. Algorithm Engineering, Algorithmics Column. Bull.
EATCS 79 (2003), 48–63.
[30] Francisco Demontiê, Junio Cezar, Mariza Bigonha, Frederico Campos, and Fernando Magno Quintão Pereira. 2015.
Automatic Inference of Loop Complexity Through Polynomial Interpolation. In Proc. 19th Brazilian Symposium on
Programming Languages (Lecture Notes in Computer Science, Vol. 9325), Alberto Pardo and S. Doaitse Swierstra (Eds.).
Springer, Cham, 1–15. https://doi.org/10.1007/978-3-319-24012-1_1
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 24

150:24 Long Pham, Feras A. Saad, and Jan Hoffmann
[31] Jürgen Giesl, Nils Lommen, Marcel Hark, and Fabian Meyer. 2022. Improving Automatic Complexity Analysis of Integer
Programs. In The Logic of Software. A Tasting Menu of Formal Methods: Essays Dedicated to Reiner Hähnle on the Occasion
of His 60th Birthday, Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, and Einar Broch Johnsen (Eds.). Lecture
Notes in Computer Science, Vol. 13360. Springer, Cham, 193–228. https://doi.org/10.1007/978-3-031-08166-8_10
[32] Samuel Jiménez Gil, Iain Bate, George Lima, Luca Santinelli, Adriana Gogonel, and Liliana Cucu-Grosjean. 2017. Open
Challenges for Probabilistic Measurement-Based Worst-Case Execution Time. IEEE Embedded Systems Letters 9, 3
(2017), 69–72.
[33] Simon F. Goldsmith, Alex S. Aiken, and Daniel S. Wilkerson. 2007. Measuring Empirical Computational Complexity.
In Proc. the 6th Joint Meeting of the European Software Engineering Conference and the ACM SIGSOFT Symposium on
The Foundations of Software Engineering. ACM, New York, NY, USA, 395–404. https://doi.org/10.1145/1287624.1287681
[34] David Griffin and Alan Burns. 2010. Realism in Statistical Analysis of Worst Case Execution Times. In 10th Interna￾tional Workshop on Worst-Case Execution Time Analysis (OpenAccess Series in Informatics (OASIcs), Vol. 15). Schloss
Dagstuhl–Leibniz-Zentrum fuer Informatik, Wadern, 44–53. https://doi.org/10.4230/OASIcs.WCET.2010.44
[35] Bernd Grobauer. 2001. Cost Recurrences for DML Programs. In Proc. 6th ACM SIGPLAN International Conference on
Functional Programming. ACM, New York, NY, USA, 253–264. https://doi.org/10.1145/507635.507666
[36] Jessie Grosen, David M. Kahn, and Jan Hoffmann. 2023. Automatic Amortized Resource Analysis with Regular
Recursive Types. In Proc. 38th Annual ACM/IEEE Symposium on Logic in Computer Science. IEEE, New York, NY, USA,
1–14. https://doi.org/10.1109/LICS56636.2023.10175720
[37] Sumit Gulwani, Krishna K. Mehra, and Trishul Chilimbi. 2009. SPEED: Precise and Efficient Static Estimation of Program
Computational Complexity. In Proc. 36th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
Languages. ACM, New York, NY, USA, 127–139. https://doi.org/10.1145/1480881.1480898
[38] Martin A. T. Handley, Niki Vazou, and Graham Hutton. 2019. Liquidate Your Assets: Reasoning about Resource Usage
in Liquid Haskell. Proc. ACM Program. Lang. 4, POPL, Article 24 (Dec. 2019), 27 pages. https://doi.org/10.1145/3371092
[39] Jan Hoffmann. 2011. Types with Potential: Polynomial Resource Bounds via Automatic Amortized Analysis. Ph. D.
Dissertation. Ludwig-Maximilians-Universität München. https://edoc.ub.uni-muenchen.de/13955/
[40] Jan Hoffmann, Klaus Aehlig, and Martin Hofmann. 2011. Multivariate Amortized Resource Analysis. In Proc. 38th
Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages. ACM, New York, NY, USA,
357–370. https://doi.org/10.1145/1926385.1926427
[41] Jan Hoffmann, Klaus Aehlig, and Martin Hofmann. 2012. Resource Aware ML. In Proc. 24 International Conference on
Computer Aided Verification (Lecture Notes in Computer Science, Vol. 7358), P. Madhusudan and Sanjit A. Seshia (Eds.).
Springer, Berlin, 781–786. https://doi.org/10.1007/978-3-642-31424-7_64
[42] Jan Hoffmann, Ankush Das, and Shu-Chun Weng. 2017. Towards Automatic Resource Bound Analysis for OCaml. In
Proc. 44th ACM SIGPLAN Symposium on Principles of Programming Languages. ACM, New York, NY, USA, 359–373.
https://doi.org/10.1145/3009837.3009842
[43] Jan Hoffmann and Martin Hofmann. 2010. Amortized Resource Analysis with Polymorphic Recursion and Partial
Big-Step Operational Semantics. In Proc. 8th Asian Symposium on Programming Languages and Systems (Lecture Notes
in Computer Science, Vol. 6461), Kazunori Ueda (Ed.). Springer, Berlin, 172–187. https://doi.org/10.1007/978-3-642-
17164-2_13
[44] Jan Hoffmann and Martin Hofmann. 2010. Amortized Resource Analysis with Polynomial Potential. In Proc. 19th
European Symposium on Programming Languages and Systems (Lecture Notes in Computer Science, Vol. 6012), Andrew D.
Gordon (Ed.). Springer, Berlin, 287–306. https://doi.org/10.1007/978-3-642-11957-6_16
[45] Jan Hoffmann and Steffen Jost. 2022. Two Decades of Automatic Amortized Resource Analysis. Mathematical Structures
in Computer Science 32, 6 (June 2022), 729–759. https://doi.org/10.1017/S0960129521000487
[46] Jan Hoffmann and Zhong Shao. 2015. Automatic Static Cost Analysis for Parallel Programs. In Proc. 24th European
Symposium on Programming Languages and Systems (Lecture Notes in Computer Science, Vol. 9032), Jan Vitek (Ed.).
Springer, Berlin, 132–157. https://doi.org/10.1007/978-3-662-46669-8_6
[47] Martin Hofmann and Steffen Jost. 2003. Static Prediction of Heap Space Usage for First-Order Functional Programs. In
Proc. 30th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages. ACM, New York, NY, USA,
185–197. https://doi.org/10.1145/604131.604148
[48] Martin Hofmann, Lorenz Leutgeb, David Obwaller, Georg Moser, and Florian Zuleger. 2022. Type-Based Analysis
of Logarithmic Amortised Complexity. Mathematical Structures in Computer Science 32, 6 (June 2022), 794–826.
https://doi.org/10.1017/S0960129521000232
[49] Martin Hofmann and Georg Moser. 2014. Amortised Resource Analysis and Typed Polynomial Interpretations. In
Rewriting and Typed Lambda Calculi (Lecture Notes in Computer Science, Vol. 8560). Springer, Heidelberg, 272–286.
https://doi.org/10.1007/978-3-319-08918-8_19
[50] Ling Huang, Jinzhu Jia, Bin Yu, Byung-Gon Chun, Petros Maniatis, and Mayur Naik. 2010. Predicting Execution Time
of Computer Programs Using Sparse Polynomial Regression. In Advances in Neural Information Processing Systems,
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 25

Robust Resource Bounds with Static Analysis and Bayesian Inference 150:25
Vol. 23. Curran Associates Inc., Red Hook, NY, USA, 883–891.
[51] Didier Ishimwe, KimHao Nguyen, and ThanhVu Nguyen. 2021. Dynaplex: Analyzing Program Complexity Using
Dynamically Inferred Recurrence Relations. Proc. ACM Program. Lang. 5, OOPSLA, Article 138 (Oct. 2021), 23 pages.
https://doi.org/10.1145/3485515
[52] David S. Johnson. 1999. A Theoretician’s Guide to the Experimental Analysis of Algorithms. In Data Structures, Near
Neighbor Searches, and Methodology: Fifth and Sixth DIMACS Implementation Challenges (DIMACS Series in Discrete
Mathematics and Theoretical Computer Science, Vol. 59), Michael H. Goldwasser, David S. Johnson, and Catherine C.
McGeoch (Eds.). DIMACS/AMS, Piscataway, NJ, USA, 215–250. https://doi.org/10.1090/dimacs/059/11
[53] Steffen Jost, Kevin Hammond, Hans-Wolfgang Loidl, and Martin Hofmann. 2010. Static Determination of Quantitative
Resource Usage for Higher-Order Programs. Proc. 37th Annual ACM SIGPLAN-SIGACT Symposium on Principles of
Programming Languages 45, 1 (Jan. 2010), 223–236. https://doi.org/10.1145/1706299.1706327
[54] David M. Kahn and Jan Hoffmann. 2020. Exponential Automatic Amortized Resource Analysis. In Proc. 23rd International
Conference on Foundations of Software Science and Computation Structures (Lecture Notes in Computer Science, Vol. 12077),
Jean Goubault-Larrecq and Barbara König (Eds.). Springer, Cham, 359–380. https://doi.org/10.1007/978-3-030-45231-
5_19
[55] G. A. Kavvos, Edward Morehouse, Daniel R. Licata, and Norman Danner. 2019. Recurrence Extraction for Functional
Programs through Call-by-Push-Value. Proc. ACM Program. Lang. 4, POPL, Article 15 (Dec. 2019), 31 pages. https:
//doi.org/10.1145/3371083
[56] Zachary Kincaid, John Cyphert, Jason Breck, and Thomas Reps. 2017. Non-Linear Reasoning for Invariant Synthesis.
Proc. ACM Program. Lang. 2, POPL, Article 54 (Dec. 2017), 33 pages. https://doi.org/10.1145/3158142
[57] Tristan Knoth, Di Wang, Adam Reynolds, Jan Hoffmann, and Nadia Polikarpova. 2020. Liquid Resource Types. Proc.
ACM Program. Lang. 4, ICFP, Article 106 (Aug. 2020), 29 pages. https://doi.org/10.1145/3408988
[58] Yunbum Kook, YinTat Lee, Ruoqi Shen, and Santosh Vempala. 2022. Sampling with Riemannian Hamiltonian Monte
Carlo in a Constrained Space. In Advances in Neural Information Processing Systems, Vol. 35. Curran Associates Inc.,
Red Hook, NY, USA, 13 pages.
[59] Ugo Dal Lago and Marco Gaboardi. 2011. Linear Dependent Types and Relative Completeness. In Proc. 26th IEEE
Symposium on Logic in Computer Science. IEEE, New York, NY, USA, 133–142. https://doi.org/10.1109/LICS.2011.22
[60] Lorenz Leutgeb, Georg Moser, and Florian Zuleger. 2021. ATLAS: Automated Amortised Complexity Analysis of
Self-adjusting Data Structures. In Proc. 33rd International Conference on Computer Aided Verification (Lecture Notes in
Computer Science, Vol. 12760). Springer-Verlag, Berlin, 99–122. https://doi.org/10.1007/978-3-030-81688-9_5
[61] Lorenz Leutgeb, Georg Moser, and Florian Zuleger. 2022. Automated Expected Amortised Cost Analysis of Probabilistic
Data Structures. In Proc. 34th International Conference on Computer Aided Verification (Lecture Notes in Computer Science,
Vol. 13372), Sharon Shoham and Yakir Vizel (Eds.). Springer, Cham, 70–91. https://doi.org/10.1007/978-3-031-13188-2_4
[62] Benjamin Lichtman and Jan Hoffmann. 2017. Arrays and References in Resource Aware ML. In Proc. 2nd International
Conference on Formal Structures for Computation and Deduction (Leibniz International Proceedings in Informatics,
Vol. 84), Dale Miller (Ed.). Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik, Dagstuhl, Germany, 20 pages. https:
//doi.org/10.4230/LIPIcs.FSCD.2017.26
[63] George Lima, Dario Dias, and Edna Barros. 2016. Extreme Value Theory for Estimating Task Execution Time
Bounds: A Careful Look. In Proc. 28th Euromicro Conference on Real-Time Systems. IEEE, New York, NY, USA, 200–211.
https://doi.org/10.1109/ECRTS.2016.20
[64] Yue Lu, Thomas Nolte, Iain Bate, and Liliana Cucu-Grosjean. 2011. A New Way About Using Statistical Analysis of
Worst-Case Execution Times. ACM SIGBED Review 8, 3 (2011), 11–14. https://doi.org/10.1145/2038617.2038619
[65] Catherine McGeoch. 1987. Experimental Analysis of Algorithms. Ph. D. Dissertation. Carnegie Mellon University.
[66] Catherine McGeoch, Peter Sanders, Rudolf Fleischer, Paul R. Cohen, and Doina Precup. 2002. Using Finite Experiments
to Study Asymptotic Performance. In Experimental Algorithmics: From Algorithm Design to Robust and Efficient Software,
Rudolf Fleischer, Bernard Moret, and Erik Meineche Schmidt (Eds.). Springer, Berlin, 93–126. https://doi.org/10.1007/3-
540-36383-1_5
[67] Glen Mével, Jacques-Henri Jourdan, and François Pottier. 2019. Time Credits and Time Receipts in Iris. In Proc. 28th
European Symposium on Programming (Lecture Notes in Computer Science, Vol. 11423), Luís Caires (Ed.). Springer, Cham,
3–29. https://doi.org/10.1007/978-3-030-17184-1_1
[68] Suzana Milutinovic, Enrico Mezzetti, Jaume Abella, Tullio Vardanega, and Francisco J. Cazorla. 2017. On Uses of
Extreme Value Theory Fit for Industrial-Quality WCET Analysis. In Proc. 12th IEEE International Symposium on
Industrial Embedded Systems. IEEE, New York, NY, USA, 1–6. https://doi.org/10.1109/SIES.2017.7993402
[69] Hadi Mohasel Afshar and Justin Domke. 2015. Reflection, Refraction, and Hamiltonian Monte Carlo. In Advances in
Neural Information Processing Systems, Vol. 28. MIT Press, Cambridge, MA, USA, 3007–3015.
[70] Alexandre Moine, Arthur Charguéraud, and François Pottier. 2023. A High-Level Separation Logic for Heap Space under
Garbage Collection. Proc. ACM Program. Lang. 7, POPL, Article 25 (Jan. 2023), 30 pages. https://doi.org/10.1145/3571218
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.

---

## Trang 26

150:26 Long Pham, Feras A. Saad, and Jan Hoffmann
[71] Bernard M. E. Moret. 1999. Towards a Discipline of Experimental Algorithmics. In Data Structures, Near Neighbor
Searches, and Methodology: Fifth and Sixth DIMACS Implementation Challenges (DIMACS Series in Discrete Mathematics
and Theoretical Computer Science, Vol. 59), Michael H. Goldwasser, David S. Johnson, and Catherine C. McGeoch (Eds.).
DIMACS/AMS, Piscataway, NJ, USA, 197–213. https://doi.org/10.1090/dimacs/059/10
[72] Georg Moser and Manuel Schneckenreither. 2020. Automated Amortised Resource Analysis for Term Rewrite Systems.
Science of Computer Programming 185, Article 102306 (Jan. 2020), 18 pages. https://doi.org/10.1016/j.scico.2019.102306
[73] Van Chan Ngo, Quentin Carbonneaux, and Jan Hoffmann. 2018. Bounded Expectations: Resource Analysis for
Probabilistic Programs. In Proc. 39th ACM SIGPLAN Conference on Programming Language Design and Implementation.
ACM, New York, NY, USA, 496–512. https://doi.org/10.1145/3192366.3192394
[74] Tobias Nipkow and Hauke Brinkop. 2019. Amortized Complexity Verified. Journal of Automated Reasoning 62, 3
(March 2019), 367–391. https://doi.org/10.1007/s10817-018-9459-3
[75] Yue Niu, Jonathan Sterling, Harrison Grodin, and Robert Harper. 2022. A Cost-Aware Logical Framework. Proc. ACM
Program. Lang. 6, POPL (Jan. 2022), 1–31. https://doi.org/10.1145/3498670
[76] Long Pham, Feras Saad, and Jan Hoffmann. 2024. Hybrid Resource-Aware ML. https://doi.org/10.5281/zenodo.10937074
[77] Boqin Qin, Tengfei Tu, Ziheng Liu, Tingting Yu, and Linhai Song. 2022. Algorithmic Profiling for Real-World Complexity
Problems. IEEE Trans. Softw. Eng. 48, 7 (July 2022), 2680–2694. https://doi.org/10.1109/TSE.2021.3067652
[78] Federico Reghenzani, Luca Santinelli, and William Fornaciari. 2020. Dealing with Uncertainty in pWCET Estimations.
ACM Transactions on Embedded Computing Systems 19, 5, Article 33 (Sept. 2020), 23 pages. https://doi.org/10.1145/
3396234
[79] Stefano Rizzelli, Judith Rousseau, and Sonia Petrone. 2024. Empirical Bayes in Bayesian Learning: Understanding a
Common Practice. arXiv:2402.19036 [math]
[80] Daniele Rogora, Antonio Carzaniga, Amer Diwan, Matthias Hauswirth, and Robert Soulé. 2020. Analyzing System
Performance with Probabilistic Performance Annotations. In Proc. 15th European Conference on Computer Systems.
ACM, New York, NY, USA, 1–14. https://doi.org/10.1145/3342195.3387554
[81] Peter Sanders and Rudolf Fleischer. 2001. Asymptotic Complexity from Experiments? A Case Study for Randomized
Algorithms. In International Workshop on Algorithm Engineering (Lecture Notes in Computer Science, Vol. 1982), Stefan
Näher and Dorothea Wagner (Eds.). Springer, Berlin, 135–146. https://doi.org/10.1007/3-540-44691-5_12
[82] Moritz Sinn, Florian Zuleger, and Helmut Veith. 2014. A Simple and Scalable Static Analysis for Bound Analysis
and Amortized Complexity Analysis. In Proc. 26th International Conference on Computer Aided Verification (Lecture
Notes in Computer Science, Vol. 8559), Armin Biere and Roderick Bloem (Eds.). Springer, Cham, 745–761. https:
//doi.org/10.1007/978-3-319-08867-9_50
[83] Daniel D. Sleator and Robert E. Tarjan. 1983. Self-Adjusting Binary Trees. In Proc. 15th Annual ACM Symposium on
Theory of Computing. ACM, New York, NY, USA, 235–245. https://doi.org/10.1145/800061.808752
[84] Daniel D. Sleator and Robert E. Tarjan. 1985. Amortized Efficiency of List Update and Paging Rules. Commun. ACM 28,
2 (Feb. 1985), 202–208. https://doi.org/10.1145/2786.2793
[85] Robert E. Tarjan. 1985. Amortized Computational Complexity. SIAM J. Matrix Anal. Appl. 6, 2 (April 1985), 306–13.
https://doi.org/10.1137/0606031
[86] Pedro B. Vasconcelos. 2008. Space Cost Analysis Using Sized Types. Ph. D. Dissertation. University of St. Andrews.
[87] Di Wang, David M. Kahn, and Jan Hoffmann. 2020. Raising Expectations: Automating Expected Cost Analysis with
Types. Proc. ACM Program. Lang. 4, ICFP (Aug. 2020), 31 pages. https://doi.org/10.1145/3408992
[88] Ben Wegbreit. 1975. Mechanical Program Analysis. Commun. ACM 18, 9 (Sept. 1975), 528–539. https://doi.org/10.
1145/361002.361016
[89] Reinhard Wilhelm et al. 2008. The Worst-Case Execution-Time Problem—Overview of Methods and Survey of Tools.
ACM Transactions on Embedded Computing Systems 7, 3, Article 36 (May 2008), 53 pages. https://doi.org/10.1145/
1347375.1347389
[90] Dmitrijs Zaparanuks and Matthias Hauswirth. 2012. Algorithmic Profiling. In Proc. 33rd ACM SIGPLAN Conference
on Programming Language Design and Implementation. ACM, New York, NY, USA, 67–76. https://doi.org/10.1145/
2254064.2254074
[91] Florian Zuleger, Sumit Gulwani, Moritz Sinn, and Helmut Veith. 2011. Bound Analysis of Imperative Programs with
the Size-Change Abstraction. In Proc. 18th International Static Analysis Symposium (Lecture Notes in Computer Science,
Vol. 6887), Eran Yahav (Ed.). Springer, Berlin, 280–297. https://doi.org/10.1007/978-3-642-23702-7_22
Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 150. Publication date: June 2024.
