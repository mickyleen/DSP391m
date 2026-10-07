## Trang 1

Fully Abstract Module Compilation
Karl Crary
Carnegie Mellon University
Abstract
We give a translation suitable for compilation of mod￾ern module calculi supporting sealing, generativity, translu￾cent signatures, applicative functors, higher-order func￾tors and/or first-class modules. Ours is the first module￾compilation translation with a dynamic correctness theo￾rem. The theorem states that the translation produces tar￾get terms that are contextually equivalent to the source, in
an appropriate sense. A corollary of the theorem is that the
translation is fully abstract. Consequently, the translation
preserves all abstraction present in the source. In passing,
we also show that modules are a definitional extension of the
underlying core language. All of our proofs are formalized
in Coq.
1 Introduction
ML-style module calculi [10] provide powerful abstraction
tools for various programming-in-the-large settings. Struc￾tures collect related type and term components, as well as
other structures, together in a single expression. More than
just a namespace management mechanism, modules can be
made opaque, so that clients can use them only through
their specified interfaces. Functors map modules to other
modules, which allows the programmer to give an implemen￾tation of an abstract data type that depends parametrically
on an unknown implementation of another.
In an untyped setting, compiling modules is not too dif￾ficult. One can simply erase the types and compile modu￾lar code as ordinary code, rendering modules as tuples or
records, and functors and functions. Nevertheless, there
are compelling reasons to prefer type-preserving compila￾tion. Chief among them is the assistance that type struc￾ture offers in achieving compiler correctness. Simply as a
matter of engineering, experience shows that it is very dif￾ficult to implement (accidentally) a type-preserving global
transformation1
that is incorrect and yet type correct.
Types can take on an even more significant role in com￾piler verification. The best correctness result for a compiler
phase is contextual equivalence, which says that the source
and translated terms are indistinguishable by any legal ob￾servation (in an appropriate sense). This is the most robust
form of translation correctness because it applies regardless
of how the translated code is used, be it translated further
1We refer here to such transformations as CPS or closure conver￾sion, in contrast to local transformations such as arithmetic optimiza￾tion, where types help much less.
(vertical composition), linked with other code (horizontal
composition), or used in other way. Types are essential to
contextual equivalence: without type structure to circum￾scribe how the code may be used, too many observations are
possible, making non-trivial contextual equivalence nearly
impossible.
In this paper we give the first compilation strategy for
ML-style modules that (1) supports the full array of abstrac￾tion mechanisms offered by the Standard ML module system
(i.e., structures, sealing, generative functors, and translu￾cent signatures) [23] as well as some other important features
(applicative functors, higher-order functors, and first-class
modules), and (2) admits a contextual equivalence result
between modules and their translation.
As a corollary of contextual equivalence, the module
translation is fully abstract: Modules are equivalent exactly
when their translations are equivalent. The left-to-right por￾tion of this is also called abstraction preservation. It says
that no legal target code can break any abstractions present
in the source code.
This is particularly valuable today, as functional lan￾guages are increasingly becoming part of heterogeneous
(multi-language) development environments. Full abstrac￾tion means that a programmer can be confident that his or
her abstractions will be respected even by code linked in
from another language, provided types are preserved and
enforced [25].
Moreover, our compilation strategy admits separate com￾pilation, meaning that units can be linked entirely in the
target language, without reference to the source code that
generated them. In practice, this means that every module
expression—including functors—is independently translated
to a target-language expression.
The first mathematical examination of the compilation
of modules was undertaken by Harper, et al. [12]. Their in￾terest was not in compilation per se, but in the equational
theory of higher-order modules. Specifically, they wished to
show that code that employs functors respects a compile￾time/run-time phase distinction, meaning that code can al￾ways be type-checked without executing any code.
That the phase distinction is respected is not obvious a
priori. A module contains both type and term components,
and a functor is a function that maps modules to modules,
so at first glance it appears as though the type components
of the result can depend on the term components of the ar￾gument. If so, it would be necessary to execute the argument
terms in order to determine the result types.
This does not happen because the module language is

---

## Trang 2

structured in such a way that types can never depend on
terms. Harper, et al. show that module expressions can
be separated into two parts: a static (or “compile-time”)
phase and a dynamic (or “run-time”) phase. Dynamic-phase
expressions can depend on static-phase expressions, but not
vice versa. This relies crucially on modules being second￾class.
Harper, et al. go on to show that the static-phase equa￾tional theory is unaffected by the deletion of all dynamic￾phase equations. But for our purposes, we are interested in
their phase-separation algorithm itself. In their algorithm,
every module M is split into two pieces [c, e], in which c is
a type constructor representing M’s static portion, and e is
a term representing its dynamic portion. Both pieces can
be rendered without reference to the module language, so
modules are compiled away.
Harper, et al.’s module language supported some impor￾tant features, but it omitted other ones, most notably seal￾ing and generativity. The only form of abstraction available
was lambda abstraction, which meant that their language
supported only client-side abstraction, not provider-side ab￾straction, which is more robust [2].
Subsequently, Shao [32] employed a similar algorithm in
a compiler for Standard ML. Unlike Harper, et al., Shao’s
source language supports sealing and generativity. However,
the translation deals with them simply by removing them,
so it does not preserve abstraction. (This was consistent
with his purpose of facilitating cross-module inlining.)
Next, Shan [31] and Rossberg, et al. [27] proposed a dif￾ferent approach for compiling modules with sealing and gen￾erativity, in which sealing was treated as introducing an ex￾istential type. This provides a very natural treatment of
abstraction [24].
Neither Shan nor Rossberg, et al. included any dynamic
correctness result, much less full abstraction. In fact, neither
one gave an evaluation semantics for the source language.2
We resolve the question here in the negative; their trans￾lation is probably not fully abstract. More precisely, their
translation is not fully abstract if the target’s dynamic se￾mantics provides any strict mechanism (e.g., call-by-value
or seq) capable of observing the termination of a function
expression. However, the problem is easily corrected by a
change to the target’s static semantics.
This paper’s main contribution is the first module￾compilation algorithm with a dynamic correctness proof.
The algorithm is given as a phase-separation translation:
as in Harper, et al.’s original translation, we split each pure
module into a type constructor and a term. The correct￾ness result is as strong as possible: we show that modules
are translated to contextually equivalent terms, and we con￾clude, as a corollary, that the translation is fully abstract.
The most obvious obstacle to the contextual equivalence
result is that the source expression and its translation belong
to different types, different syntactic classes, and indeed dif￾ferent languages. The difference in languages is easily dealt
with: our target language is a strict subset of our source
language, obtained by omitting all module-oriented forms.
2This was understandable in both cases. Shan was working from a
pre-existing type theory [6] that did not commit to a specific dynamic
semantics. Rossberg, et al. were defining a module system by giving
an elaboration of ML modules into a module-free core language, so
the source language necessarily had no independent semantics at all.
(Nevertheless, the question remains whether the elaboration realizes
the programmer’s expectations.)
Thus, we can compare a source expression and its trans￾lation simply by taking the translation as another source
expression.
To mediate the difference in types and syntactic classes,
we show that we can define a pair of functions Snd and Join
that convert back-and-forth between modules and terms of
appropriate types. The result then states that if a module M
is phase-separated into static portion c and dynamic portion
e, then Join[c, e] is contextually equivalent to M. Since Snd
and Join are inverses, one may equivalently say that SndM
is contextually equivalent to e.
If Join merely traversed e to reverse the phase-separation
translation, this result would be trivial. It does not. The
important fact about Snd and Join is they are defined within
the grammar of the language. They are not able to traverse
the syntax of an expression, and thus they can only interact
with an expression through the interface given by its type.
Their purpose is to coerce between interfaces.
One observation that we can draw from this result is
that modules are a definitional extension of the core lan￾guage. Put less formally, the module language can be viewed
as merely a very convenient syntax for writing modular
programs. A practical consequence of this observation is
that some useful module features (notably first-class mod￾ules [29]) need not be included as distinct features to be
compiled, because they are already definitional extensions
of the language.
Our development proceeds as follows: First, we summa￾rize our module calculus and state some preliminary results
regarding it (Section 2). Our module calculus is nearly iden￾tical to Crary [2], except we add a value restriction for poly￾morphic functions. Second, we give the phase separation al￾gorithm (Section 3). Third, we define contextual equivalence
(Section 4). This is adapted from Crary, with small changes
to deal with the value restriction. We also state some useful
lemmas about contextual equivalence, corollaries of the de￾velopment of logical equivalence in Crary. Finally we prove
our correctness results (Section 5): We define Snd and Join,
show that they are inverses, show that modules translate to
contextually equivalent terms (modulo Join), and conclude
full abstraction as a corollary.
All of our proofs are formalized in Coq, and may be found
at:
www.cs.cmu.edu/~crary/papers/2018/famc-formal.tgz
2 The Module Calculus
Our module calculus is nearly identical to Crary [2], which
is adapted from that of Dreyer [5], which in turn builds on
a long line of prior work on module calculi [21, 12, 22, 9,
17, 18, 15, 34, 28, 33, 6]. The sole change from Crary is
the addition of a value restriction to polymorphic functions.
(As we will show, the value restriction is necessary for our
translation to be fully abstract.) The module calculus itself
is not a research contribution of this paper; our purpose
here is just to lay the foundation for our phase-separation
algorithm.
The module calculus is intended to account for the fun￾damental elements of a module system that are vital for
data abstraction [2]. However, it does not account for all of
the convenience features of modern module systems: Fields
of modules are identified by position, not by name. Co￾ercion of a module to a specified signature (i.e., by drop￾2

---

## Trang 3

k ::= 1 unit kind
| T types
| S(c) singleton kind
| Πα:k.k dependent functions
| Σα:k.k dependent pairs
c, ::= α
τ | ? unit constructor
| λα:k.c | c c lambda, application
| hc, ci pair
| π1c | π2c projection
| unit unit type
| τ1 → τ2 functions
| τ1 × τ2 products
| ∀α:k.τ universals
| ∃α:k.τ existentials
e ::= x
| ? unit term
| λx:τ.e | e e lambda, application
| he, ei pair
| π1e | π2e projection
| Λα:k.e polymorphic fun.
| e[c] polymorphic app.
| pack [c, e] as ∃α:k.τ existential package
| unpack [α, x] = e in e unpack
| fixτ e recursion
| let x = e in e term binding
| let α/m = M in e module binding
| Ext M extraction
M ::= m
| ? unit module
| L c M atomic module
| h| e |i atomic module
| λ
gnα/m:σ.M generative functor
| M M generative app.
| λ
apα/m:σ.M applicative functor
| M · M applicative app.
| hM, Mi pair
| π1M | π2M projection
| unpack [α, x] = e in (M : σ) unpack
| let x = e in M term binding
| let α/m = M in (M : σ) module binding
| M :> σ sealing
σ ::= 1 unit signature
| L k M atomic signature
| h| τ |i atomic signature
| Π
gnα:σ.σ generative functors
| Π
apα:σ.σ applicative functors
| Σα:σ.σ pairs
Γ ::=  empty context
| Γ, α:k constr. hypothesis
| Γ, x:τ term hypothesis
| Γ, α/m:σ module hypothesis
Figure 1: Syntax
ping fields, reordering fields, or monomorphizing polymor￾phic functions) is not done automatically; to do so creates
complications that are orthogonal to the abstraction con￾cerns we focus on here. Like nearly all module calculi (but
not Harper and Mitchell [11]), sharing specifications are not
primitive, but are taken as syntactic sugar over translucent
signatures. The open declaration, which is useful in practice
but makes little sense in a type theory with a proper notion
of binding, is not supported. First-class modules (supported
in some dialects of ML [29]) are not explicitly supported
(but see Section 6). We also do not support recursive mod￾ules [3, 30, 5] (supported in some dialects of ML [30, 19]);
the abstraction implications of recursive modules are not yet
well examined. All of these features can be implemented by
elaboration [15, 6, 5], but those elaborated aspects of the
language fall outside the results we prove here.
Most significantly, we follow earlier work [15, 6, 27] by
using elaboration to address the avoidance problem [6], in
which the structure of a program mandates that type vari￾ables leave scope, but there is no best way for a mod￾ule’s type to avoid those variables. This arises most im￾portantly in sealed arguments to functors. No satisfactory
type-theoretic treatment of the avoidance problem has yet
been found. The elaboration involves retaining in “hidden”
modules the type variables that are supposed to leave scope.
Unfortunately, the hidden-ness of those modules is not en￾forceable after elaboration, which may lead to tangible com￾promises in data abstraction. To avoid this, the programmer
must manually ascribe signatures whenever type variables
leave scope. This preserves abstraction, but is inconvenient.
Syntax A key design goal of the module calculus is to re￾spect the phase distinction [12], which means that the mean￾ing of static phrases, and specifically their equivalence, can
be determined without referring to dynamic phrases. The
static syntactic classes are kinds (k), type constructors (c),
and signatures (σ). The dynamic syntactic classes are terms
(e) and modules (M). Signatures serve as the types of mod￾ules, and kinds serve (as usual) as the types of type con￾structors. The full syntax is given in Figure 1. (Figures 1,
2, and 4 are borrowed from Crary [2].)
Static phrases The constructor and kind expressions are
the singleton kind calculus of Stone and Harper [35], with
some minor extensions. Actual types belong to the kind
T. (We often use the metavariable τ instead of c for actual
types.) The unit constructor ? belongs to the kind 1.
If τ is a type, we may form the singleton kind S(τ ), which
contains precisely τ (and other types equivalent to it). This
is used to model type definitions and sharing specifications
in signatures. Thus, if τ : S(τ
0
), we can conclude that τ and
τ
0
are equivalent types. As a consequence, equivalence is
context sensitive: α and τ are equivalent under the assump￾tion α : S(τ ), but not under α : T. As a further consequence,
equivalence depends on the kind at which constructors are
compared: λα:T.α and λα:T.τ are equivalent at S(τ ) → T
but not at T → T. Although the singleton kind primitive is
restricted to types, one can use it to define singletons at any
kind.
Since singletons allow kinds to depend on constructors,
it is useful to support dependent kinds. The dependent form
of function kinds is written Πα:k.k0
and the dependent form
of products is written Σα:k.k0
. When α does not appear free
in k
0
, these are written using k → k
0
and k × k
0
respectively,
3

---

## Trang 4

as usual.
Dynamic phrases The syntax for terms is largely standard.
The recursion form fixτ e has the type τ , provided e has the
type (unit→τ )→τ , and we evaluate fixτ e to e(λ :unit.fixτ e).3
The module language contains static and dynamic
atomic modules, generative and applicative functors, and
pairs. An atomic module models a single field of a module:
a static atom (L c M) contains a single constructor, and a dy￾namic atom (h| e |i) contains a single term. For example, the
ML module:
struct
type t = bool
val x = true
end
could be elaborated hL boolM,h|true |ii. (Observe that, as
noted above, the field names disappear when a module is
elaborated.)
Abstraction is introduced using the form M :> σ, which
seals M so that its components can be accessed only through
the interface given by σ. In particular, if a signature gives
the kind of a type field as T, that type is unknown and
therefore abstract. Proper enforcement of type abstraction
requires that sealing be viewed as a computational effect [6],
and that types cannot be extracted from impure modules.
Thus, to use the types from a sealed module, one must bind
that module to a variable; variables are always pure.
We syntactically distinguish between generative and ap￾plicative functors. A generative functor can have sealing in
its body, and calling it induces an effect. In contrast, an
applicative functor cannot, and does not.
For technical reasons related to the avoidance problem [5,
section 4.2.6], a module that either let-binds a module or un￾packs an existential type must include an explicit signature
annotation, and such modules are deemed to induce an ef￾fect.
Static portions, twinned variables, and phase separation
To extract a term from a dynamic atom, one uses the form
Ext M. However, to extract a type constructor from a static
atom, we employ a judgement rather than a syntactic form.
The judgement Fst(M)  c says that c is the static portion
of M.
4
In particular, Fst(L c M)  c.
The reason for this design, invented by Dreyer [5], is it
removes any syntactic dependency of static phrases (such as
types) on terms or modules. By disentangling the singleton
kind calculus from all dynamic phrases, we are able to use
Stone and Harper’s singleton-kind metatheory [35] off the
shelf.
For static extraction to work compositionally, we must be
able to compute the static portion of any pure module, not
only static atom literals. (Impure modules do not have static
portions.) The rules for doing so are given in Figure 2. Two
subtle points arise: First, by its nature, a generative functor
returns nothing that is statically predictable. Therefore the
static component of a generative functor is trivial. Second,
3Observe that the argument to e is a value, so this evaluation
behaves acceptably in a call-by-value setting. That would not be the
case with the evaluation to e(fixτ e) that would be implied by a more
conventional typing.
4The name Fst is motivated by the connection to phase separation,
which explicit renders modules as a pair of a static and dynamic
component.
Fst(σ) : kind
Fst(1) def = 1
Fst(L k M)
def = k
Fst(h| τ |i)
def = 1
Fst(Πgnα:σ1.σ2)
def = 1
Fst(Πapα:σ1.σ2)
def = Πα: Fst(σ1). Fst(σ2)
Fst(Σα:σ1.σ2)
def = Σα: Fst(σ1). Fst(σ2)
Γ ` Fst(M)  c
α/m ∈ Dom(Γ)
Γ ` Fst(m)  α Γ ` Fst(?)  ? Γ ` Fst(L c M)  c
Γ ` Fst(h| e |i)  ? Γ ` Fst(λ
gnα/m:σ.M)  ?
Γ, α/m:σ ` Fst(M)  c
Γ ` Fst(λ
apα/m:σ.M)  λα: Fst(σ).c
Γ ` Fst(M1)  c1 Γ ` Fst(M2)  c2
Γ ` Fst(M1 · M2)  c1c2
Γ ` Fst(hM1, M2i)  hc1, c2i
Γ ` Fst(M)  c
Γ ` Fst(πiM)  πic
Γ ` Fst(M)  c
Γ ` Fst(let x = e in M)  c
Figure 2: Static portions
for any module variable m, we must be able to compute m’s
static portion, but of course that cannot be known, so we
must have a type-constructor variable prepared to stand in
for m’s static portion. This leads to the concept of twinned
variables [16]: every module variable m is twinned with a
constructor variable α, written α/m, where α is the static
portion of m.
5 However, when α is not used, we will often
leave it out.
Twinned variables are recorded in the context and static
portions depend on them, so the static portion judgement
is written in its most general form as Γ ` M  c. However,
when Γ is empty or can be determined from context, we
often write Fst(M)  c, or even just Fst(M) for the unique
c such that Fst(M)  c.
Our static-portion rules are very similar in spirit to the
non-standard equational rules of Harper, et al. [12]. As in
this work, Harper et al. gave rules for determining the static
portions of modules as part of their static semantics, and
also—separately—gave an algorithm for compiling modules
into static and dynamic components. The main difference
(apart from the extra features we support here), is that their
“non-standard” rules determined not only a static portion,
but also a dynamic portion, even though only the static
portion ended up being relevant to typing judgements.
Signatures Signatures forms include signatures for atomic
modules, generative and application functors, and pairs.
5An alternative [12, 5] is to use a naming convention to associate
module and constructor variables, but this complicates binding and
substitution. Sorting out those complications carefully leaves you
with something very close to twinned variables.
4

---

## Trang 5

S(c : k) : kind
S(c : 1) def = 1
S(c : T)
def = S(c)
S(c : S(c
0
)) def = S(c)
S(c : Πα:k1.k2)
def = Πα:k1.S(c α : k2)
S(c : Σα:k1.k2)
def = S(π1c : k1) × S(π2c : [π1c/α]k2)
S(c : σ) : signature
S(c : 1) def = 1
S(c : L k M)
def = L S(c : k)M
S(c : h| τ |i)
def = h| τ |i
S(c : Πgnα:σ1.σ2)
def = Πgnα:σ1.σ2
S(c : Πapα:σ1.σ2)
def = Πapα:σ1.S(c α : σ2)
S(c : Σα:σ1.σ2)
def = S(π1c : σ1) × S(π2c : [π1c/α]σ2)
Figure 3: Higher-order singletons
The signatures for functors and for pairs are dependent, so
one might expect to write them with a twinned left-hand￾side, like Σα/m:σ1.σ2. However, since a module can never
appear within a signature (signatures being static phrases),
the m variable will never be used, so we don’t bother to
write it. (As usual, when α does not appear free in σ2, we
write Σα:σ1.σ2 as σ1 × σ2.)
In a twinned binding α/m:σ, or in the binding α:σ within
a dependent signature, α stands for the static portion of
some module belonging to σ. Thus, α will have kind Fst(σ),
which stands for the static portion of σ. The definition of
Fst appears in Figure 2. Whenever m : σ and Fst(m)  c,
we have c : Fst(σ).
Higher-order singletons The primitive singleton kind S(c)
is well-formed only when c is a type. However, singletons at
higher kinds (written S(c : k)) are definable using dependent
kinds. For example, S(c : k1→k2) = Πα:k1.S(c α : k2), since
a constructor is equivalent to c in kind k1→k2 precisely when
it takes an argument of kind k1 and does with it whatever
c does with it.
We can use the same technique to define singleton sig￾natures. Suppose c : Fst(σ). Then the singleton signature
S(c : σ) contains all pure modules in σ whose static compo￾nent is equivalent to c. For instance S(c : L k M) = L S(c : k)M.
The definitions of higher-order singletons are given in Fig￾ure 3. Note that when the static component of σ is trivial
(i.e., when Fst(σ) = 1), S(c : σ) = σ, since all static compo￾nents are equivalent at kind 1.
Semantics The static semantics is given by several judge￾ments summarized in Figure 4. The rules are exactly those
from Crary [2], with the sole exception that the typing rule
for polymorphic functions is replaced by the one given be￾low, which includes a value restriction.
The top-level judgement is the typing judgement for
modules, written Γ `κ M : σ, where the purity class κ
is either P, indicating that the module is pure (unsealed),
or I, indicating that it is impure (sealed). A “forget” rule
allows pure modules to be viewed as impure.
` Γ ok context formation
Γ ` k : kind kind formation
Γ ` k ≡ k
0
kind equivalence
Γ ` k ≤ k
0
subkind
Γ ` c : k constructor formation
Γ ` c ≡ c
0
: k constructor equivalence
Γ ` σ : sig signature formation
Γ ` σ ≡ σ
0
: sig signature equivalence
Γ ` σ ≤ σ
0
subsignature
Γ ` e : τ term formation
Γ `κ M : σ module formation
Γ ` Fst(M)  c static portion
Figure 4: Static semantic judgements
The dynamic semantics is given by a standard, call-by￾value, structured operational semantics, written Γ ` e 7→ e
0
and Γ ` M 7→ M0
. (It is convenient to be able to evaluate
open terms, but in the typical case in which Γ is empty, we
will omit the turnstile.) The value forms are:
v ::= x | ? | λx:τ.e | hv, vi | Λα:k.e
| pack [c, v] as ∃α:k.τ
V ::= m | ? | L c M | h| v |i | hV, V i
| λ
gnα/m:σ.M | λ
apα/m:σ.M
We write e↓ or M↓ to mean that e or M evaluates to a value.
Two rules illustrate issues that arise in the dynamic se￾mantics. The evaluation rule for sealed modules immedi￾ately removes the seal:
Γ ` (M :> σ) 7→ M
In essence, this step is the computational effect that the type
system tracks. Rules that substitute for module variables,
such as the beta rules for functors, also must substitute for
the twinned constructor variable, which is obtained using
the Fst judgement:
Γ ` Fst(V2)  c2
Γ ` (λ
gnα/m:σ.M1)V2 7→ [c2, V2/α, m]M1
This rule works because well-formed module values are al￾ways pure, so their static portion can always be obtained.
The value restriction In the typing rule for polymorphic
functions, we require that the body be a static value:
Γ ` k : kind Γ, α:k ` sv : τ
Γ ` Λα:k.sv : ∀α:k.τ
where a static value (sv) is like an ordinary value (v) except
variables are excluded:
sv ::= ? | λx:τ.e | hsv, svi | Λα:k.sv
| pack [c, sv] as ∃α:k.τ
We distinguish between static and ordinary values and use
the former because we wish for well-formedness to be pre￾served by the substitution of any appropriately typed term—
even a non-value—for a variable, and that is not the case
5

---

## Trang 6

with ordinary values. This is necessary to have a useful
contextual-equivalence functionality lemma.
The inclusion of the value restriction has no significant
effect on the development of logical equivalence given in
Crary [2], but it is essential for the phase separation trans￾lation to be fully abstract.
Metatheory We can now state some metatheoretic results
from Crary [2]:
Lemma 2.1
• If Γ `P M : σ then Γ ` Fst(M) : Fst(σ).
• If ` Γ ok and Γ ` c : k then Γ ` c : S(c : k) and
Γ, α:S(c : k) ` α ≡ c : k.
• If ` Γok and Γ `P M : σ then Γ `P M : S(Fst(M) : σ).
• If Γ `I V : σ then Γ `P V : σ.
Theorem 2.2 (Type preservation) If ` Γ ok then:
• If Γ ` e : τ and Γ ` e 7→ e
0
then Γ ` e
0
: τ .
• If Γ `κ M : σ and Γ ` M 7→ M0
then Γ `κ M0
: σ.
• If Γ `P M : σ and Γ ` M 7→ M0
then Γ ` Fst(M) ≡
Fst(M0
) : Fst(σ).
Theorem 2.3 (Progress) If ` e : τ then either e is a
value or takes a step. If `κ M : σ then either M is a value
or takes a step.
Theorem 2.4 (Determinism)
• If Γ ` e 7→ e1 and Γ ` e 7→ e2 then e1 = e2.
• If Γ ` M 7→ M1 and Γ ` M 7→ M2 then M1 = M2.
• If Γ ` Fst(M)  c1 and Γ ` Fst(M)  c2 then c1 = c2.
3 Phase Separation
The target language for our translation is the subset of the
source language obtained by deleting all the module-oriented
forms. Note that the syntactic classes of kinds and con￾structors contain no module-oriented forms, and are thus
unchanged. (This is an advantage of Dreyer’s device [5]
wherein Fst is a judgement, rather than a syntactic form.)
Using a fragment of the source as the target dramati￾cally simplifies several aspects of the development: (1) We
need not develop the metatheory of the target language; the
source’s metatheory applies directly. (2) The type trans￾lation is the identity. (3) Full abstraction is a direct con￾sequence of the dynamic correctness theorem, since every
target observation is a source observation, and every source
observation can be translated to a target observation.
We express phase separation as a type-directed transla￾tion [13] using three judgements, one each for terms, pure
modules, and impure modules. The term translation judge￾ment is Γ ` e : τ e¯, meaning that Γ ` e : τ and ¯e is a
translation of e. Since the type translation is the identity, ¯e
will have the same type as e.
Different translation derivations can ostensibly result in
different translations, but we can show that the translation
is coherent [1], meaning that all of a term’s translations are
equivalent. Coherence is another simple corollary of dy￾namic correctness.
The term translation does very little, since most term
forms do not pertain to modules. Its rules are given in Ap￾pendix A. The main judgements are the phase-separation
judgements for modules. For pure modules, the judgement
is written:
Γ `P M : σ [c, e]
Here, M is separated into its static portion c and its dy￾namic portion e. Recall that the module calculus has its
own internal concept of static components (Fst(M)). These
notions agree: if also Γ ` Fst(M)  c
0
then c = c
0
.
The types of c and e are governed by the phase separation
judgement for signatures:
σ [α:k. τ ]
Here σ is separated into its static portion k and its dynamic
portion τ (in which τ can refer to α, which stands for the
actual static component). Thus, in the above, c belongs to
kind k, and e belongs to type [c/α]τ .
The best way to understand the translation is through
the phase-separation rules for signatures. A static atom is
all static, so L k M [ : k. unit]. Conversely, a dynamic atom
is all dynamic, so h| τ |i [ :1. τ ]. A trivial module is trivial
is trivial in both components, so 1 [ :1. unit].
In an applicative functor, the static portion maps the
static portion of the argument to the static portion of the
result, while the dynamic portion maps both portions of the
argument to the dynamic portion of the result:
σ1 [α1:k1. τ1] σ2 [α2:k2. τ2]
Π
apα:σ1.σ2 [β : Πα:k1.k2. ∀α:k1. [α/α1]τ1 → [βα/α2]τ2]
In a pair, the static (dynamic) portion is the pair of the
static (dynamic) portions of the constituents:
σ1 [α1:k1. τ1] σ2 [α2:k2. τ2]
Σα:σ1.σ2 [β : Σα:k1.k2. [π1β/α1]τ1 × [π1β, π2β/α, α2]τ2]
These rules are essentially the rules from Harper, et
al. [12] (adapted for dependent kinds), but they did not
account for generative functors. For generative functors, we
adapt the translation of Shan [31] and Rossberg, et al. [27].
The tricky point is how to phase-separate impure (i.e.,
sealed) modules. Our translation wishes to separate mod￾ules into their static and dynamic components, but sealed
modules are not supposed to have a static component, since
their abstract type components are notionally determined
at run-time.6 Any translation that makes them available
statically will not preserve abstraction.
But once a sealed module has executed, its result value
will be pure (recall part 4 of Lemma 2.1), and therefore it
will have static and dynamic components. Thus, the ap￾propriate translation of an impure module is a term that
dynamically computes the static and dynamic portions of
that eventual value. Thus we write:
Γ `I M : σ e
where e belongs to ∃α:k.τ (assuming σ [α:k. τ ]).
Now we can give the rule for a generative functor, which
returns an impure module. Its static portion is trivial, while
6
Indeed, when first-class modules are added, they are actually de￾termined at run-time.
6

---

## Trang 7

σ [α:k. τ ]
1 [ :1. unit] L k M [ : k. unit] h| τ |i [ :1. τ ]
σ1 [α1:k1. τ1] σ2 [α2:k2. τ2]
Π
gnα:σ1.σ2 [ :1. ∀α:k1. [α/α1]τ1 → ∃α2:k2.τ2]
σ1 [α1:k1. τ1] σ2 [α2:k2. τ2]
Π
apα:σ1.σ2 [β : Πα:k1.k2. ∀α:k1. [α/α1]τ1 → [βα/α2]τ2]
σ1 [α1:k1. τ1] σ2 [α2:k2. τ2]
Σα:σ1.σ2 [β : Σα:k1.k2. [π1β/α1]τ1 × [π1β, π2β/α, α2]τ2]
Figure 5: The signature translation
its dynamic portion maps both portions of the argument to
an existential package containing the static and dynamic
portions of the module value that the functor eventually
returns:
σ1 [α1:k1. τ1] σ2 [α2:k2. τ2]
Π
gnα:σ1.σ2 [ :1. ∀α:k1. [α/α1]τ1 → ∃α2:k2.τ2]
For convenience, the signature translation rules are col￾lected in Figure 5. The module translation is given in Fig￾ures 6, and 7. Most of its rules are dictated by the signa￾ture phase-separation rules given above. We touch on a few
points that are interesting or subtle:
The translation’s calling convention is given by the con￾text translation Γ, which is formalized in Figure 8. Con￾structor and term bindings are translated directly, as one
would expect. In a module binding α/m, we introduce two
variables—a constructor variable α and a term variable ˆm—
to represent the module’s static and dynamic portions. Here
we assume that there are infinitely many term variables, so
for every module variable m we can associate a term variable
mˆ that is not otherwise used.
With the calling convention established, we can consider
the translation rules for functors. For applicative functors,
the rule states:
Γ ` σ1 : sig σ1 [α:k1. τ1] Γ, α/m:σ1 `P M : σ2 [c, e]
Γ `P λ
apα/m:σ1.M : Πapα:σ1.σ2 [λα:k1.c, Λα:k1.λmˆ :τ1.e]
The functor’s static portion λα:k1.c takes the static por￾tion of the functor argument (α:k1) to the static portion
of the body (c). In accordance with the phase distinction,
there is no dependence on the dynamic portion of the argu￾ment. The functor’s dynamic portion takes the static and
dynamic portions of the argument (α:k1 and ˆm:τ1)—thereby
following the calling convention for α/m:σ1—to the dynamic
portion of the body (e).
The applicative functor application rule states (in the
pure case):
Γ `P M1 : Πapα:σ1.σ2 [c1, e1] Γ `P M2 : σ1 [c2, e2]
Γ `P M1 · M2 : [c2/α]σ2 [c1c2, e1 [c2] e2]
Γ `P M : σ [c, e]
(α/m : σ) ∈ Γ
Γ `P m : S(α : σ) [α, mˆ ]
Γ ` ? : 1 [?, ?]
Γ ` c : k
Γ ` L c M : L k M [c, ?]
Γ ` e : τ e¯
Γ ` h| e |i : h| τ |i [?, e¯]
Γ ` σ1 : sig σ1 [α:k1. τ1] Γ, α/m:σ1 `I M : σ2 e
Γ `P λ
gnα/m:σ1.M : Πgnα:σ1.σ2 [?, Λα:k1.λmˆ :τ1.e]
Γ ` σ1 : sig σ1 [α:k1. τ1] Γ, α/m:σ1 `P M : σ2 [c, e]
Γ `P λ
apα/m:σ1.M : Πapα:σ1.σ2 [λα:k1.c, Λα:k1.λmˆ :τ1.e]
Γ `P M1 : Πapα:σ1.σ2 [c1, e1] Γ `P M2 : σ1 [c2, e2]
Γ `P M1 · M2 : [c2/α]σ2 [c1c2, e1 [c2] e2]
Γ `P M1 : σ1 [c1, e1] Γ `P M2 : σ2 [c2, e2]
Γ `P hM1, M2i : σ1 × σ2 [hc1, c2i,he1, e2i]
Γ `P M : Σα:σ1.σ2 [c, e]
Γ `P π1M : σ1 [π1c, π1e]
Γ `P M : Σα:σ1.σ2 [c, e]
Γ `P π2M : [π1c/α]σ2 [π2c, π2e]
Γ `P e : τ e1 Γ, x:τ `P M : σ [c, e2]
Γ `P let x = e in M : σ [c, let x = e1 in e2]
Γ `P M : σ1 [c, e] Γ ` σ1 ≤ σ2 f
Γ `P M : σ2 [c, f [c] e]
Figure 6: The pure module translation
7

---

## Trang 8

Γ `I M : σ e
Γ `I M1 : Πgnα:σ1.σ2 e1 Γ `P M2 : σ1 [c2, e2]
Γ `I M1M2 : [c2/α]σ2 unpack [ , f] = e1 in f [c2] e2
Γ `I M1 : Πapα:σ1.σ2 e1
Γ `P M2 : σ1 [c2, e2] σ2 [β:k2. τ2]
Γ `I M1 · M2 : [c2/α]σ2 unpack [γ, f] = e1
in pack [γ c2, f [c2] e2]
as[c2/α](∃β:k2.τ2)
Γ ` M1 : σ1 e1 Γ ` M2 : σ2 e2
σ1 [α1:k1. τ1] σ2 [α2:k2. τ2]
Γ ` hM1, M2i : σ1 × σ2 unpack [α1, x1] = e1
in unpack [α2, x2] = e2
in pack [hα1, α2i,hx1, x2i]
as ∃β:(k1 × k2). [π1β/α1]τ1
× [π2β/α2]τ2
Γ ` e : ∃α:k.τ e1 Γ, α:k, x:τ `I M : σ e2 Γ ` σ : sig
Γ `I unpack [α, x] = e in (M : σ) : σ unpack [α, x] = e1 in e2
Γ ` e : τ e1 Γ, x:τ `I M : σ e2
Γ ` let x = e in M : σ let x = e1 in e2
Γ ` M1 : σ1 e1 Γ, α/m:σ1 ` M2 : σ2 e2 Γ ` σ2 : sig
Γ ` let α/m = M1 in (M2 : σ2) : σ2 unpack [α, mˆ ] = e1 in e2
Γ `I M : σ e
Γ `I (M :> σ) : σ e
Γ `P M : σ [c, e] σ [α:k. τ ]
Γ `I M : σ pack [c, e] as ∃α:k.τ
Γ `I M : σ1 e Γ ` σ1 ≤ σ2 f σ2 [α:k2. τ2]
Γ `I M : σ2 unpack [α, x] = e in pack [α, f[α]x] as ∃α:k2.τ2
Figure 7: The impure module translation

def = 
Γ, α:k
def = Γ, α:k
Γ, x:τ
def = Γ, x:τ
Γ, α/m:σ
def = Γ, α:k, mˆ :τ where σ [α:k. τ ]
Figure 8: The context translation
This simply applies the functor’s static portion to the
argument’s, and applies the functor’s dynamic portion to
the argument’s static and dynamic portion. The impure
case does the same thing, but first unpacks the functor from
an existential package, and afterwards repacks the result.
Observe that, unless one were to do something obviously
foolish, both of these rules are completely determined by the
signature translation. The same is true for the translation
of generative functors:
Γ ` σ1 : sig σ1 [α:k1. τ1] Γ, α/m:σ1 `I M : σ2 e
Γ `P λ
gnα/m:σ1.M : Πgnα:σ1.σ2 [?, Λα:k1.λmˆ :τ1.e]
The static portion of a generative functor is trivial. The
dynamic portion takes in the static and dynamic portions
of the argument (again α:k1 and ˆm : τ1)—again following
the calling convention—and then computes an existential
package (e) containing the static and dynamic portions of
the result.
The generative functor application rule:
Γ `I M1 : Πgnα:σ1.σ2 e1 Γ `P M2 : σ1 [c2, e2]
Γ `I M1M2 : [c2/α]σ2 unpack [ , f] = e1 in f [c2] e2
after extracting the functor’s dynamic portion from a trivial
existential package simply applies it to the argument’s static
and dynamic portion.
Again, these rules are determined by the signature trans￾lation. The same is true of the rules governing atomic mod￾ules and pairs. The translation of let binding is determined
simply by the calling convention:
Γ ` M1 : σ1 e1 Γ, α/m:σ1 ` M2 : σ2 e2 Γ ` σ2 : sig
Γ ` let α/m = M1 in (M2 : σ2) : σ2 unpack [α, mˆ ] = e1 in e2
Since M1 is impure, its translation is an existential pack￾age that must be unpacked to follow the calling convention.
Once this is done, the right-hand-side is just passed through.
Since σ2 does not mention α, the type of e2 also will not
mention α.
The translation rule corresponding to the “forgetting”
rule takes the statically determined static and dynamic com￾ponents and rolls them into an existential package:
Γ `P M : σ [c, e] σ [α:k. τ ]
Γ `I M : σ pack [c, e] as ∃α:k.τ
Interestingly, this leaves nothing for the sealing rule to do:
Γ `I M : σ e
Γ `I (M :> σ) : σ e
All the sealing rule does is require that M be translated
impurely. This induces the forgetting rule to do the work of
sealing M up as an existential package.
Retyping principles Two technically tricky points pertain
to the module calculus’s retyping principles. The first such
principle is the subsumption rule:
Γ `κ M : σ1 Γ ` σ1 ≤ σ2
Γ `κ M : σ2
If σ1 ≤ σ2 and σi [α:ki. τi], we can show that k1 ≤ k2.
If we had subtyping (and the full F≤ subtyping rule [4]) we
8

---

## Trang 9

could also show that τ1 ≤ τ2. But we do not have subtyping,
and it is not the case that τ1 ≡ τ2, since k
0 ≤ k does not
imply ∀α:k.τ ≡ ∀α:k
0
.τ . Consequently, the subsumption
rule must apply a τ1 → τ2 coercion to the dynamic portion:
Γ `P M : σ1 [c, e] Γ ` σ1 ≤ σ2 f
Γ `P M : σ2 [c, f [c] e]
Γ `I M : σ1 e Γ ` σ1 ≤ σ2 f σ2 [α:k2. τ2]
Γ `I M : σ2 unpack [α, x] = e in pack [α, f[α]x] as ∃α:k2.τ2
The coercion is computed by a judgement Γ ` σ1 ≤ σ2 f.
It is essentially a large eta-expansion; it unrolls a term rep￾resenting the dynamic portion of a module belonging to σ1,
and then re-rolls it at the type corresponding to σ2. De￾tails appear in Appendix A. In a practical implementation,
this coercion can very frequently be inlined. Moreover, for
fragments without higher-order functors (such as Standard
ML), the coercion is always the identity.
The second retyping principle is the calculus’s exten￾sional typing rules, such as this rule for module pairs:
Γ `P π1M : σ1 Γ `P π2M : σ2
Γ `P M : σ1 × σ2
The extensional typing rules say that a module belongs
to a signature if uses of M produce appropriate results. For
instance, M belongs to σ1 × σ2 if its left projection belongs
to σ1 and its right to σ2. These rules are never needed
when M is an introduction form, but they allow one to as￾cribe stronger signatures to paths (i.e., series of elimina￾tions starting from a variable) than the elimination rules
permit [9]. For example, they allow one to give a path a
translucent signature that refers to itself, a procedure whim￾sically called “selfification.” Extensional typing is necessary
for higher-order singleton kinds and signatures to work prop￾erly (recall parts 2 and 3 of Lemma 2.1).
However, the extensional typing rules cause a problem
for the translation. Suppose M translated to [c, e] before
using extensionality. The translation rule corresponding to
the above rule would produce [hπ1c, π2ci,hπ1e, π2ei]. A sim￾ilar thing would happen with the extensional typing rule for
functors.
Unfortunately, this eta-expansion is not only inefficient,
it is incorrect. In an eager operational semantics such as
ours, e and hπ1e, π2ei have observably different behavior
whenever e has effects.
The solution to this problem is to exploit the fact that
the extensional typing rules are needed only for paths. Our
translation omits the extensional typing rules, and replaces
them with a single “selfifying” translation rule for variables:
(α/m : σ) ∈ Γ
Γ `P m : S(α : σ) [α, mˆ ]
Note the typing rule for variables gives m the signature
σ, but the translation here gives it S(α : σ). Because of
this discrepancy, the translation rules are not in perfect cor￾respondence with the typing rules, but we can nevertheless
show that all well-typed expressions translate and vice versa:
Theorem 3.1 If ` Γ ok then:
• Γ ` σ1 ≤ σ2 iff Γ ` σ1 ≤ σ2 f (for some f).
• Γ `P M : σ iff Γ `P M : σ [c, e] (for some c, e).
• Γ `I M : σ iff Γ `I M : σ e (for some e).
• Γ ` e : τ iff Γ ` e : τ e¯ (for some e¯).
We will need more machinery before we can show the
translation’s full correctness, but at this point we can show
its static correctness:
Lemma 3.2 (Static correctness) If ` Γ ok then:
• If Γ ` σ : sig and σ [α:k. τ ] then Γ ` k : kind and
Γ, α:k ` τ : T.
• If Γ ` σ1 ≤ σ2 f and σi [α:ki. τi] then Γ ` f :
∀α:k1. τ1 → τ2.
• If Γ `P M : σ [c, e] and σ [α:k. τ ] then Γ ` c : k
and Γ ` e : [c/α]τ .
• If Γ `I M : σ e and σ [α:k. τ ] then Γ ` e : ∃α:k.τ .
• If Γ ` e : τ e¯ then Γ ` e¯ : τ .
4 Contextual Equivalence
We follow Crary [2] by defining contextual equivalence as
the coarsest congruence that is consistent with execution,7
and our definitions in this section are adapted from there.
However, in contrast to Crary, our indexed relations include
a relation on static values. This comes into play in the
compatibility rule for polymorphic functions because of the
value restriction. Fortunately, this affects the development
almost not at all, and ultimately we will prove that the value
relation can be ignored (Lemma 4.5).
Definition 4.1 An indexed dynamic relation R is a triple
of relations: relations (Rt and Rv) on terms and static val￾ues indexed by a context and type; and a relation (Rm) on
modules indexed by a context, signature, and purity class;
such that if ` Γ ok then:
• if Γ ` e Rt e
0
: τ then Γ ` e, e0
: τ , and
if Γ ` e Rv e
0
: τ then Γ ` e, e0
: τ and e, e
0
are static
values, and
• if Γ `κ M Rm M0
: σ then Γ `κ M, M0
: σ, and
• if Γ `P M Rm M0
: σ then Γ ` Fst(M) ≡ Fst(M0
) :
Fst(σ).
Definition 4.2 Suppose R is an indexed dynamic relation.
• R is compatible if it respects the rules in Appendix B.
(Informally, R is compatible if R-related expressions
can be built from R-related subexpressions.)
• R is substitutive if it respects substitution (of val￾ues where appropriate) and weakening for construc￾tor, term, and module hypotheses. (For example, if
Γ, α/m:σ, Γ
0 ` e Rt e
0
: τ and Γ `P V : σ then
Γ, [c/α]Γ0 ` [Fst(V ), V /α, m]e Rt [Fst(V ), V /α, m]e
0
:
[c/α]τ .)
7A more common definition would say that two expressions are
contextually equivalent if they produce the same behavior when used
to fill a hole in a program. Such a definition would be equivalent to
ours, but in the setting of the module calculus, it is too unwieldy to
use [2].
9

---

## Trang 10

• R is a congruence if it is compatible, substitutive, re￾flexive, transitive, and symmetric.
• R is consistent if it preserves module termination.
(That is, if `I M Rm M0
: σ and M halts then M0
halts.)
Although we define consistency in terms of module ter￾mination, it is easy to show that a consistent, compatible
relation also preserves term termination.
Definition 4.3 Contextually equivalence (written Γ ` e ≈
e
0
: τ and Γ ` e ≈v e
0
: τ and Γ `κ M ≈ M0
: σ) is defined
as the union of all consistent congruences.8
4.1 Properties of Contextual Equivalence
In proving dynamic correctness of phase separation, we will
use several properties of contextual equivalence. One-and￾a-half of these can be proven directly (the first and the
left-to-right direction of the second). But contextual equiv￾alence, which effectively quantifies over all observing con￾texts that might use the comparees, is awkward to work
with. For the rest of the properties, we require a tool to
obtain leverage on contextual equivalence. The tool is logi￾cal equivalence, which defines the equivalence of comparees
intrinsically, rather than extrinsically through their use in
surrounding code.
Crary [2] defines logical equivalence for the module calcu￾lus and shows that it coincides with contextual equivalence.
We use that development off-the-shelf, except that we need
a notion of logical equivalence for values. We define it as
simply the restriction of logical equivalence to static values.
The desired properties are all corollaries of the coinci￾dence of logical and contextual equivalence. Conveniently,
we can state them all without reference to logical equiva￾lence, so we do so in the interest of brevity. Proofs are given
in the companion Coq formalization.
First, contextual equivalence is adequate for the opera￾tional semantics:
Lemma 4.4 (Adequacy) If Γ ` e : τ and Γ ` e 7→ e
0
then
Γ ` e ≈ e
0
: τ , and similarly for modules.
Proof Sketch
The compatible, reflexive, and transitive closure of eval￾uation is a consistent congruence, and therefore is con￾tained in contextual equivalence.
Second, contextual equivalence for values is precisely the
restriction of ordinary contextual equivalence to static val￾ues. Thus, henceforth we can ignore contextual equivalence
for values.
Lemma 4.5 (Value equivalence) Γ ` sv ≈v sv0
: τ if
and only if Γ ` sv ≈ sv0
: τ .
Proof Sketch
Immediate from the definition of logical equivalence and
its coincidence with contextual equivalence. Alterna￾tively, for the left-to-right direction, observe that sv ≈
(Λ :1.sv)[?] ≈ (Λ :1.sv0
)[?] ≈ sv0
.
8
In the Coq formalization, contextual equivalence is given a dif￾ferent definition (the symmetrization of contextual approximation)
which is then proved equivalent to this one.
Third, we can show two expressions are contextually
equivalent by considering their closed instances:
Lemma 4.6 (Closed instances)
• If Γ ` e, e0
: τ and for any substitution γ such that `
γ : Γ we have ` γ(e) ≈ γ(e
0
) : γ(τ ), then Γ ` e ≈ e
0
: τ .
• If Γ `I M, M0
: σ and for any substitution γ such that
` γ : Γ we have `I γ(M) ≈ γ(M0
) : γ(σ), then Γ `I
M ≈ M0
: σ.
• If Γ `P M, M0
: σ and Γ ` Fst(M) ≡ Fst(M0
) : Fst(σ)
and for any substitution γ such that ` γ : Γ we have
`P γ(M) ≈ γ(M0
) : γ(σ), then Γ `I M ≈ M0
: σ.
Fourth, when two closed expressions have the same ter￾mination behavior, we can assume they terminate when
showing they are contextually equivalent:
Lemma 4.7 (Conditional equivalence)
• If ` e, e0
: τ and e↓⇔ e
0
↓, then if e↓ implies ` e ≈ e
0
:
τ , then ` e ≈ e
0
: τ .
• If `I M, M0
: τ and M↓⇔ M0
↓, then if M↓ implies
`I M ≈ M0
: σ, then `I M ≈ M0
: σ.
• If `P M, M0
: τ and ` Fst(M) ≡ Fst(M0
) : Fst(σ) and
M↓⇔ M0
↓, then if M↓ implies `P M ≈ M0
: σ, then
`P M ≈ M0
: σ.
Fifth, for closed terms and closed, pure modules, we have
a variety of extensionality properties:
Lemma 4.8 (Extensionality) Suppose ` e, e0
: τ and
e↓⇔ e
0
↓, then ` e ≈ e
0
: τ provided:
• τ = unit, or
• τ = τ1 →τ2 and for every ` v : τ1 we have ` e v ≈ e
0
v :
τ2, or
• τ = ∀α:k.τ 0
and for every ` c : k we have ` e[c] ≈
e
0
[c] : [c/α]τ
0
, or
• τ = τ1 ×τ2 and ` π1e ≈ π1e
0
: τ1 and ` π2e ≈ π2e
0
: τ2.
Suppose `P M, M0
: σ and M↓⇔ M0
↓, then `P M ≈ M0
: σ
provided:
• σ = 1, or
• σ = L k M and ` Fst(M) ≡ Fst(M0
) : k, or
• σ = h| τ |i and ` Ext M ≈ Ext M0
: τ , or
• σ = Πgnα:σ1.σ2 and for every `P V : σ1 we have `I
MV ≈ M0V : [Fst(V )/α]σ2, or
• σ = Πapα:σ1.σ2 and ` Fst(M) ≡ Fst(M0
) :
Fst(Πapα:σ1.σ2) and for every `P V : σ1 we have
`P M · V ≈ M0
· V : [Fst(V )/α]σ2, or
• σ = Σα:σ1.σ2 and `P π1M ≈ π1M0
: σ1 and `P π2M ≈
π2M0
: [π1 Fst(M)/α]σ2.
10

---

## Trang 11

Snd1M
def = let = M in ?
SndL k MM
def = let = M in ?
Sndh| τ |iM
def = Ext M
SndΠgnα:σ1.σ2M
def = let m = M
in Λα:k1.λx:τ1.
let β/n = m(Joinσ1
[α, x])
in pack [β, Sndσ2 n] as ∃β:k2.τ2
(where σ1 [α:k1. τ1]
and σ2 [β:k2. τ2])
SndΠapα:σ1.σ2M
def = let m = M
in Λα:k1.λx:τ1.
Sndσ2
(m · (Joinσ1
[α, x]))
(where σ1 [α:k1. τ1])
SndΣα:σ1.σ2M
def = let γ/m = M
in hSndσ1
(π1m), Snd[π1γ/α]σ2
(π2m)i
Join1[c, e]
def = let = e in ?
JoinL k M[c, e]
def = let = e in L c M
Joinh| τ |i[c, e]
def = h| e |i
JoinΠgnα:σ1.σ2
[c, e]
def = let x = e
in λ
gnα/m:σ1.
unpack [β, y] = x[α](Sndσ1m)
in (Joinσ2
[β, y] : σ2)
JoinΠapα:σ1.σ2
[c, e]
def = let x = e
in λ
apα/m:σ1.
Joinσ2
[c α, x[α](Sndσ1m)]
JoinΣα:σ1.σ2
[c, e]
def = let x = e
in hJoinσ1
[π1c, π1x],
Join[π1c/α]σ2
[π2c, π2x]i
Figure 9: Dynamic Phase Separation
5 Correctness
Our main aim is to show that every module is contextu￾ally equivalent to its translation, in an appropriate sense.
But what is the appropriate sense? Since a module and its
translation belong to different types, and indeed different
syntactic classes, we require some way to relate them.
We do this using Sndσ and Joinσ, two (families of)
functions that convert back-and-forth between modules and
terms. Given a module, Snd computes its dynamic compo￾nent, and given a module’s static and dynamic component,
Join recovers the original module.
The important fact about Sndσ and Joinσ is that they
are expressed within the language. They do not traverse
the syntax of their arguments the way the translation does.
Rather, they operate through the interface given by their ar￾guments’ signature/kind/type. We refer to Snd as dynamic
phase separation since it does phase separation at run time
instead of compile time.
The definitions of Snd and Join are given in Figure 9. The
fact that they are definable within the language is interesting
in its own right. It shows that modules are a definitional
extension of the core language. In other words, modules
confer no fundamental expressive power absent in the core.
On the other hand, the fact that the definitions are rather
baroque shows that modules are nevertheless a useful feature
for a language to support.
Lemma 5.1 Suppose ` Γ ok and Γ ` σ : sig and σ 
[α:k. τ ]. Then:
• If Γ `P M : σ then Γ ` SndσM : [Fst(M)/α]τ .
• If Γ ` c : k and Γ ` e : [c/α]τ then Γ `P Joinσ[c, e] : σ
and Γ ` c ≡ Fst(Joinσ[c, e]) : k.
The main lemmas state that Snd and Join are inverses:
Lemma 5.2 (Join of Snd) If Γ `P M : σ then Γ `P M ≈
Joinσ[Fst(M), Sndσ(M)] : σ.
Proof Sketch
The proof is by induction on the gross structure of σ
(that is, considering all atoms (L k M or h| τ |i) to be iden￾tical for the purposes of the induction order).
We give one case, by way of example. Suppose σ =
Π
apα:σ1.σ2. By the closed instances lemma, we may
assume without loss of generality that Γ is empty.
(Note that σ’s instances have the same gross struc￾ture as σ.) It is not hard to show that M↓⇔
Joinσ[Fst(M), Sndσ(M)]↓. Therefore, by the conditional
equivalence lemma, we may assume without loss of gen￾erality that M is some value V . Let σ1 [α:k1. τ1].
Then:
Joinσ[Fst(V ), Sndσ(V )]
= let f = let m = V
in Λα:k1.λx:τ1.
Sndσ2
(m · Joinσ1
[α, x])
in λ
apα/m:σ1.
Joinσ2
[Fst(V ) α, f[α](Sndσ1m)]
≈ let f = Λα:k1.λx:τ1.
Sndσ2
(V · Joinσ1
[α, x])
in λ
apα/m:σ1.
Joinσ2
[Fst(V ) α, f[α](Sndσ1m)]
≈ λ
apα/m:σ1.
Joinσ2
[Fst(V ) α,
(Λα:k1.λx:τ1.
Sndσ2
(V · Joinσ1
[α, x]))
[α] (Sndσ1m)]
≈ λ
apα/m:σ1.
Joinσ2
[Fst(V ) α,
Sndσ2
(V · Joinσ1
[α, Sndσ1m]))
= λ
apα/m:σ1.
Joinσ2
[Fst(V · m),
Sndσ2
(V · Joinσ1
[Fst(m), Sndσ1m]))
≈ λ
apα/m:σ1. Joinσ2
[Fst(V · m), Sndσ2
(V · m)]
≈ λ
apα/m:σ1. V · m
≈ V
The last step is by eta equivalence (which follows from
extensionality, since V halts), and the previous two steps
use the induction hypothesis.
Lemma 5.3 (Snd of Join) If Γ ` σ : sig and σ [α:k. τ ]
and Γ ` c : k and Γ ` e : [c/α]τ then Γ ` e ≈
Sndσ(Joinσ[c, e]) : [c/α]τ .
Proof Sketch
By induction on the gross structure of σ. (But see Sec￾tion 5.3.)
11

---

## Trang 12

Next, we establish the correctness of the subsignature
coercion judgement. It is equivalent to the function that
converts a term to a module at the subsignature, and back
to a term at the supersignature:
Lemma 5.4 If Γ ` σ1 ≤ σ2 f and σi [α:ki. τi] then
Γ ` f ≈ Λα:k1.λx:τ1.Sndσ2
(Joinσ1
[α, x]) : ∀α:k1. τ1 → τ2.
Proof Sketch
By induction on the derivation.
Recall that the variable translation case selfified its sig￾nature. To deal with this, we require one more lemma:
Lemma 5.5 Suppose Γ ` σ : sig and σ [α:k. τ ] and
Γ ` c : k and Γ ` e : [c/α]τ . Then Γ `P Joinσ[c, e] ≈
JoinS(c:σ)[c, e] : σ.
Proof Sketch
We can show that if Γ `P M, M0
: σ and Γ ` Fst(M) ≡
Fst(M0
) : Fst(σ) and if M and M0 differ only in type
annotations, then Γ `P M ≈ M0
: σ.
Let S(c : σ) [α:k
0
. τ 0
]. Then k
0 = S(c : k) and we can
show that Γ, α:k
0 ` τ ≡ τ
0
: T, so Γ ` e : [c/α]τ
0
. The
first two conditions hold using Lemma 5.1 and S(c : σ) ≤
σ. The third is by inspection.
To mediate the difference between the original context
Γ and its translation Γ, we define the substitution SndΓ to
map ˆm to Sndσm for every α/m:σ ∈ Γ. Note that Sndσ does
not touch constructor variables, so we need not apply it to
any kinds, constructors, or signatures.
Lemma 5.6 If ` Γ ok then Γ ` SndΓ : Γ.
With this, we can finally establish our main theorem:
Theorem 5.7 (Dynamic correctness)
• If Γ `P M : σ [c, e] then Γ ` M ≈ Joinσ[c, SndΓ(e)] :
σ.
• If Γ `I M : σ e then Γ `I M ≈ unpack [α, x] =
SndΓ(e)in (Joinσ[α, x] : σ) : σ.
• If Γ ` e : τ e¯ then Γ ` e ≈ SndΓ(¯e) : τ .
Proof Sketch
The proof is by induction on the translation derivation.
We give a few cases by way of example.
Case:
(α/m : σ) ∈ Γ
Γ `P m : S(α : σ) [α, mˆ ]
Then JoinS(α:σ)[α, SndΓ( ˆm)] = JoinS(α:σ)[Fst(m),
Sndσ(m)] ≈ Joinσ[Fst(m), Sndσ(m)] ≈ m, the second
and third steps using Lemmas 5.5 and 5.2.
Case:
Γ ` σ1 : sig Γ, α/m:σ1 `P M : σ2 [c, e] σ1 [α:k1.τ1]
Γ `P λ
apα/m:σ1.M : Πapα:σ1.σ2 [λα:k1.c, Λα:k1.λmˆ :τ1.e]
Then:
JoinΠapα:σ1.σ2
[λα:k1.c, SndΓ(Λα:k1.λmˆ :τ1.e)]
= JoinΠapα:σ1.σ2
[λα:k1.c, Λα:k1.λmˆ :τ1.SndΓ(e)]
≈ λ
apα/m:σ1.Joinσ2
[(λα:k1.c)α,
(Λα:k1.λmˆ :τ1.SndΓ(e))[α](Sndσ1m)]
≈ λ
apα/m:σ1.Joinσ2
[c, [Sndσ1m/mˆ ]SndΓ(e)]
= λ
apα/m:σ1.Joinσ2
[c, SndΓ,α/m:σ1
(e)]
≈ λ
apα/m:σ1.M
Case:
Γ `P M : σ [c, e] σ [α:k. τ ]
Γ `I M : σ pack [c, e] as ∃α:k.τ
Then (unpack [β, x] = SndΓ(pack [c, e] as ∃α:k.τ )in
Joinσ[β, x]) = (unpack [β, x] = pack [c, SndΓ(e)] as ∃α:k.τ
in Joinσ[β, x]) ≈ Joinσ[c, SndΓ(e)] ≈ M.
Case:
Γ `P M : σ1 [c, e] Γ ` σ1 ≤ σ2 f
Γ `P M : σ2 [c, f [c] e]
Then Joinσ2
[c, SndΓ(f [c] e)] = Joinσ2
[c, f [c] (SndΓ(e))] ≈
Joinσ2
[c, Sndσ2
(Joinσ1
[c,
SndΓ(e)])] ≈ Joinσ1
[c, SndΓ(e)] ≈ M. The first step is
because f is closed with respect to term variables; the
second and third are by Lemmas 5.4 and 5.2.
Observe that for closed terms, the theorem degenerates
to if ` e : τ e¯ then ` e ≈ e¯ : τ .
5.1 Abstraction Preservation
It remains to collect some corollaries. We can prove a con￾verse of dynamic correctness:
Corollary 5.8 Let Joinσ be the substitution that maps m
to Joinσ[α, mˆ ] for every α/m:σ ∈ Γ. (So Γ ` JoinΓ : Γ
whenever ` Γ ok.) Suppose ` Γ ok. Then:
• If Γ `P M : σ [c, e] and σ [α:k. τ ] then Γ ` e ≈
Sndσ(JoinΓ(M)) : [c/α]τ .
• If Γ `I M : σ e and σ [α:k. τ ] then Γ `
e ≈ let α/m = JoinΓ(M) in pack [α, Sndσm] as ∃α:k.τ :
∃α:k.τ .
• If Γ ` e : τ e¯ then Γ ` e¯ ≈ JoinΓ(e) : τ .
Proof Sketch
Consider the first clause. Using compatibility, we
can show that contextual equivalence respects func￾tionality, so JoinΓ(SndΓ(e)) ≈ e by Lemma 5.3. By
dynamic correctness, M ≈ Joinσ[c, SndΓ(e)]. By
substitutivity, JoinΓ(M) ≈ JoinΓ(Joinσ[c, SndΓ(e)]) =
Joinσ[c, JoinΓ(SndΓ(e))] ≈ Joinσ[c, e]. Then, again by
Lemma 5.3, Sndσ(JoinΓ(M)) ≈ Sndσ(Joinσ[c, e]) ≈ e.
The second clause is similar but messier. The third
clause is similar but simpler.
Abstraction preservation follows directly from this. If one
neglects (for the moment) the difference between the source
and target language, this is the hard direction of full ab￾straction:
Corollary 5.9 (Abstraction preservation) Suppose `
Γ ok. Then:
• If Γ `P M1 ≈ M2 : σ and σ [α:k. τ ] and Γ `P Mi :
σ [ci, ei] then Γ ` e1 ≈ e2 : [c1/α]τ .
• If Γ `I M1 ≈ M2 : σ and σ [α:k. τ ] and Γ `I Mi :
σ ei then Γ ` e1 ≈ e2 : ∃α:k.τ .
• If Γ ` e1 ≈ e2 : τ and Γ ` ei : τ e¯i then Γ ` e¯1 ≈
e¯2 : τ .
12

---

## Trang 13

Proof Sketch
We give the first clause; the others are similar. Suppose
Γ `P M1 ≈ M2 : σ. By substitutivity of contextual
equivalence, Γ ` JoinΓ(M1) ≈ JoinΓ(M2) : σ. There￾fore e1 ≈ Sndσ(JoinΓ(M1)) ≈ Sndσ(JoinΓ(M2)) ≈ e2 by
Corollary 5.8 and compatibility.
The coherence of the translation is an immediate conse￾quence of this, using reflexivity for the antecedent:
Corollary 5.10 (Coherence) Suppose ` Γ ok. Then:
• If Γ `P M : σ and σ [α:k. τ ] and Γ `P M : σ 
[ci, ei] (for i = 1, 2) then Γ ` e1 ≈ e2 : [c1/α]τ .
• If Γ `I M : σ and σ [α:k. τ ] and Γ `I M : σ ei
(for i = 1, 2) then Γ ` e1 ≈ e2 : ∃α:k.τ .
• If Γ ` e : τ and Γ ` e : τ e¯i (for i = 1, 2) then
Γ ` e¯1 ≈ e¯2 : τ .
5.2 Full Abstraction
Full abstraction states that expressions are source￾equivalent (i.e., equivalent in the source language) exactly
when their translations are target-equivalent. Abstraction
preservation gives us most of this: It says that that transla￾tions of source-equivalent expressions are source-equivalent.
Since the target language is a subset of the source, every ob￾serving context in the target is also one in the source, and
consequently source-equivalence implies target-equivalence.
Thus, abstraction preservation gives us half of full abstrac￾tion.
It remains to show that expressions are source-equivalent
when their translations are target-equivalent. Dynamic cor￾rectness says that source expressions are source-equivalent
to their translations, so the result follows by transi￾tivity, provided target-equivalent expressions are source￾equivalent:
Lemma 5.11 Let Γ `tgt e ≈ e
0
: τ be contextual equivalence
for the target, defined analogously to Section 4, but using
only the features of the target language. Then Γ `tgt e ≈ e
0
:
τ implies Γ ` e ≈ e
0
: τ .
Proof Sketch
As developed in Crary [2], contextual equivalence coin￾cides with logical equivalence, which is biorthogonally
closed [26]. Dynamic correctness tells us that every
closed source term has an equivalent target term. Thus,
in biorthogonal closure we may assume without loss of
generality that the continuations are target terms. It
follows that biorthogonally closed sets are closed under
target-equivalence.
Corollary 5.12 (Full abstraction) Suppose ` Γ ok.
Then:
• If σ [α:k. τ ] and Γ `P Mi : σ [ci, ei] then Γ `P
M1 ≈ M2 : σ exactly when both Γ ` c1 ≡ c2 : k and
Γ `tgt e1 ≈ e2 : [c1/α]τ .
• If σ [α:k. τ ] and Γ `I Mi : σ ei then Γ `I M1 ≈
M2 : σ exactly when Γ `tgt e1 ≈ e2 : ∃α:k.τ .
• If Γ ` ei : τ e
0
i
then Γ ` e1 ≈ e2 : τ exactly when
Γ `tgt e
0
1 ≈ e
0
2 : τ .
5.3 The Role of the Value Restriction
Observe that Join ◦ Snd and Snd ◦ Join have the effect of
eta-expanding their arguments (after evaluating them to
values). For example, suppose F is an applicative func￾tor value. As we saw in the proof sketch of Lemma 5.2,
Join[Fst(F), Snd(F)] is equivalent, after some simplification,
to λm. F · m. The latter is equivalent to F because F is a
value.
On the other hand, suppose f is a value, and suppose c
and f have an appropriate kind/type to be the static and dy￾namic components of an applicative functor. Note that f’s
type must have the form ∀α:k. τ→τ
0
. Then Snd(Join[c, f]) is
equivalent, after some simplification, to Λα.λx.f[α]x. This
is equivalent to f, but only because of the value restriction.
Since f is a value, it is certainly equivalent to Λα.f[α], but
f[α] is not a value, so without a value restriction, it would
not in general be equivalent to λx.f[α]x. The value restric￾tion ensures that f[α] will halt, which is good enough to
conclude f[α] ≈ λx.f[α]x. Thus Lemma 5.3 relies crucially
on the value restriction.
We can work backward from this observation to obtain
a counterexample of full abstraction if the value restriction
were omitted. Suppose m is a variable with an applicative￾functor signature. Since m is a value, m ≈ λ
apα/n. m·n. But
m translates to dynamic component ˆm, whereas λ
apα/n. m ·
n translates to dynamic component Λα.λn. ˆ mˆ [α]ˆn. These
translations can be distinguished by the observing context
let mˆ = Λα.⊥ in let = [ ] c in ? (where c is any constructor
of appropriate kind).
This issue with full abstraction does not rely on applica￾tive functors. A similar example can be constructed using a
generative functor.
(Both Shan [31] and Rossberg, et al. [27] produce a gen￾erally similar translation to ours, but neither of their target
languages has a value restriction on polymorphic functions.9
Consequently neither of them preserves abstraction, so long
as their target language is capable of expressing the eager
let used in the observing context above.)
Note that this issue does not rule out having a second
form of polymorphic function without a value restriction,
were one desired. The important thing is that the target
language have a form of function able to take in both a
constructor and a value at once, without any intervening
effects.
One could even have a value restriction in the target and
not the source, although having different source and tar￾get languages would complicate the development. We also
conjecture that the translation would be fully abstract even
without a value restriction if it were to translate variables
to their full eta-long form. But such a translation is un￾desirable for efficiency reasons, so we have not explored it
carefully.
6 Definitional Extensions
The alignment of abstraction with effects in our module
calculus suggests a natural treatment of first-class mod￾ules [29, 5] as a definitional extension. Suppose we have
a new term form mdσ(M), which stands for an encapsu￾lated module and has type md(σ). And suppose such an
9Note that it is the target language at issue here, not any value
restriction that might exist in the source language. Both Shan and
Rossberg et al. target ordinary Fω (extended with extra types), which
has no value restriction.
13

---

## Trang 14

encapsulated module can be made back into a module using
tmσ(e).
Although this formulation offers less expressive power
than systems that allow the propagation of type informa￾tion through first-class code [9], it supports most important
applications of first-class modules such as run-time selection
of implementations of abstract data types.
The critical point in the static semantics of first-class
modules is that the tm form must be impure. Since the
module depends on arbitrary code, it is impossible to deter￾mine its type components statically:
Γ `I M : σ
Γ ` mdσ(M) : md(σ)
Γ ` e : md(σ)
Γ `I tmσ(e) : σ
Two questions present themselves regarding these first￾class modules: Does the language still respect the phase
distinction, and does the extension leave intact the lan￾guage’s existing abstraction properties? At first glance, nei￾ther seems certain. The phase distinction depends on the
fact that types cannot depend on terms, but first-class mod￾ules appear, at least superficially, to provide a way for that
to happen. And, first-class modules provide a wealth of
new observing contexts that might be used to distinguish
between previously indistinguishable modules.
But the machinery developed here allows us easily to an￾swer both questions in the affirmative. We show that we can
faithfully define first-class modules as a definitional exten￾sion in the original language. This shows that the extension
respects the phase distinction, since the original did. It also
shows that the extension preserves abstraction, because any
observing context in the extended language can be turned
into an equivalent observing context in the original language.
Consequently, any modules that are indistinguishable in the
original language remain so with the extension.
Suppose σ [α:k. τ ]. We define:
md(σ)
def = ∃α:k.τ
mdσ(M)
def = let α/m = M in pack [α, Sndσm] as ∃α:k.τ
tmσ(e)
def = unpack [α, x] = e in (Joinσ[α, x] : σ)
We can easily show that tmσ(mdσ(N)) ≈ N, thereby
simulating the extension’s operational semantics.
Another useful extension is an operation purifyS(c:σ)
(M)
that takes an impure but transparent module and makes it
pure [33, 5]. This expresses the fact that in a module whose
exported type components are fully specified, any typing ef￾fects are benign. This is useful for using generative functors
within the implementation of an applicative functor.
Γ ` c : Fst(σ) Γ `I M : S(c : σ)
Γ `P purifyS(c:σ)
(M) : S(c : σ)
We show that purify is a definitional extension by defining
purifyS(c:σ)
(M) as:
JoinS(c:σ)[c, let m = M in SndS(c:σ)m]
This trick has two parts: First, by converting M to a
term, we disappear any typing effects it might have. Then,
since M is transparent, its static component (c) is known
without referring to M, so we are able to convert back to a
pure module using Join.
When M is a value (and hence pure), we can easily show
that purifyS(c:σ)
(M) ≈ M, thereby simulating the exten￾sion’s operational semantics.
Although these definitions are satisfactory from a theo￾retical standpoint, in practice it may be preferable to trans￾late the extensions directly:
Γ `I M : σ e
Γ ` mdσ(M) : md(σ) e
Γ ` e : md(σ) e¯
Γ `I tmσ(e) : σ e¯
Observe that first-class modules are actually trivial when
viewed through the lens of phase separation. On the other
hand, the type translation is no longer the identity (md(σ)
becomes ∃α:k.τ ), which adds a bit of overhead to the com￾piler.
Γ ` c : Fst(σ) Γ `I M : S(c : σ) e
Γ `P purifyS(c:σ)
(M) : S(c : σ) [c, unpack [α, x] = e in x]
This translation works because in the unpack, α has the
kind S(c : Fst(σ)), so α ≡ c : Fst(σ), so x’s type can be
expressed without reference to α.
7 Formalization
All the results in this paper are formalized in Coq (version
8.4). We implemented binding using deBruijn indices and
explicit substitutions. To make reasoning about relations
cleaner, we used the axioms of functional and propositional
extensionality.
The full development is 89k lines. (These counts include
comments and whitespace.) Of those, 70k are preliminaries
or the development of logical equivalence, which are bor￾rowed from Crary [2], with some modest editing, mostly to
deal with the value restriction. The all-new material—the
translation and its correctness proof—account for 19k lines.
We remarked above that the addition of value restriction
had almost no effect on the development of logical equiva￾lence. As a coarse measure of that, updating the logical￾equivalence Coq proofs to account for the value restriction
took less than one day.
The numerous typing premises involved in showing con￾textual equivalences rapidly become unmanageable. To
manage this, we defined reductive contextual equivalence.
We say that Γ ` e ⇒ e
0
if for any τ , Γ ` e : τ implies
Γ ` e ≈ e
0
: τ (and similarly for modules). One example
of how this simplifies proofs is we can say that Γ ` e 7→ e
0
implies Γ ` e ⇒ e
0
, eliminating the typing premise from
Lemma 4.4.
8 Additional Discussion of Related Work
As discussed above, the closest work to ours is Shan [31]
and Rossberg, et al. [27]. The most significant difference
from ours is they do not establish dynamic correctness, but
there is a stylistic difference as well. Although they are not
fundamentally different from the pattern of the Harper, et
al. [12], their translations do not explicitly separate modules
into type and term components. Instead, they realize the
phase distinction by separating all the opaque type compo￾nents into a prefix on which the module depends. (Shao [33]
calls this prefix the module’s flexroot.) In ordinary modules,
the prefix is existentially quantified, and in functors it is
lambda abstracted. In essence, the module is automatically
14

---

## Trang 15

rewritten to replace sharing-by-fibration with sharing-by￾parameterization [14]. An advantage of their presentation
is it allows one to dispense with any machinery to control
the propagation of type information (such as the singleton
kinds we use here).
These two differences may be connected. Our proof tech￾nique relies crucially on separating modules into type con￾structors and terms. It is not clear how to define something
like Snd and Join without doing so.
Shan also addresses weak sealing [6], which we do not.
He does so by generating a two-stage program. The first
stage resolves static effects (in the sense of Dreyer, et al. [6])
that arise from weak sealing, resulting in a program without
weak sealing. The second stage then executes that program,
resolving the remaining (dynamic) effects as it goes. Ross￾berg, et al. do something similar. This approach is very
plausible, but we do not follow it here, because the equa￾tional theory of weak sealing is still not well understood.
Specifically, we do not yet know how to reconcile logical
equivalence with weak sealing, so we cannot even begin to
prove full abstraction.
Elsman, et al. [7, 8] suggest a radically different approach
called static interpretation. It resolves all module-level com￾putation (e.g., functor application) at compile time. This
sacrifices separate compilation (functors cannot be compiled
separately from their arguments), but it makes it easy to op￾timize across module boundaries. In essence, static interpre￾tation weakens the phase distinction by assigning module￾level computation to the compile-time phase rather than
the run-time phase. Their languages do not include sealing,
but do include generative datatypes, which offer a means of
abstraction. As with other prior work, they do not show
dynamic correctness.
9 Conclusion
Our correctness and full abstraction results show that the
phase-separation algorithm is canonical, from a theoretical
standpoint anyway. Any other algorithm that is dynami￾cally correct (in our sense) is necessarily equivalent to ours.
Nevertheless, there is room for improvement in the lan￾guage itself. Our module calculus supports only a frag￾ment of the features needed for Standard ML [16]. Many
of the missing features are easily supported, but some—
particularly those involving references, exceptions, or other
forms of effects—are more difficult. Another important fea￾ture for languages that emphasize applicative functors (such
as OCaml [20]) is weak sealing [6]. Still another direction
is more powerful module features such as recursive mod￾ules [3, 30, 5].
In each of these cases, we anticipate that the general
proof strategy employed here should work. However, a pre￾condition for progress in any of these domains is a working
account of logical equivalence. These are important avenues
for future work.
A The Term and Subsignature Translations
Γ ` e : τ e¯
Γ(x) = τ
Γ ` x : τ x Γ ` ? : unit ?
Γ ` τ1 : T Γ, x:τ1 ` e : τ2 e¯
Γ ` λx:τ1.e : τ1 → τ2 λx:τ1.e¯
Γ ` e1 : τ → τ
0 e¯1 Γ ` e2 : τ e¯2
Γ ` e1e2 : τ
0 e¯1e¯2
Γ ` e1 : τ1 e¯1 Γ ` e2 : τ2 e¯2
Γ ` he1, e2i : τ1 × τ2 he¯1, e¯2i
Γ ` e : τ1 × τ2 e¯
Γ ` π1e : τ1 π1e¯
Γ ` e : τ1 × τ2 e¯
Γ ` π2e : τ2 π2e¯
Γ ` k : kind Γ, α:k ` sv : τ e¯
Γ ` Λα:k.sv : ∀α:k.τ Λα:k.e¯
Γ ` e : ∀α:k.τ e¯ Γ ` c : k
Γ ` e[c] : [c/α]τ e¯[c]
Γ ` c : k Γ ` e : [c/α]τ e¯ Γ, α:k ` τ : T
Γ ` pack [c, e] as ∃α:k.τ : ∃α:k.τ pack [c, e¯] as ∃α:k.τ
Γ ` e1 : ∃α:k.τ e¯1 Γ, α:k, x:τ ` e2 : τ
0 e¯2 Γ ` τ
0
: T
Γ ` unpack [α, x] = e1 in e2 : τ
0 unpack [α, x] = ¯e1 in e¯2
Γ ` e : (unit → τ ) → τ e¯
Γ ` fixτ e : τ fixτ e¯
Γ ` e1 : τ1 e¯1 Γ, x:τ1 ` e2 : τ2 e¯2
Γ ` let x = e1 in e2 : τ2 let x = ¯e1 in e¯2
Γ `I M : σ e1 Γ, α/m:σ ` e : τ e2 Γ ` τ : T
Γ ` let α/m = M in e : τ unpack [α, mˆ ] = e1 in e2
Γ `I M : h| τ |i e
Γ ` Ext M : τ unpack [ , x] = e in x
Γ ` e : τ e¯ Γ ` τ ≡ τ
0
: T
Γ ` e : τ
0 e¯
Γ ` σ ≤ σ
0 f
Γ ` σ ≡ σ
0
: sig σ [α:k. τ ]
Γ ` σ ≤ σ
0 Λα:k.λx:τ.x
Γ ` σ ≤ σ
0 f Γ ` σ
0 ≤ σ
00 f
0 σ [α:k. τ ]
Γ ` σ ≤ σ
00 Λα:k.λx:τ. f0
[α] (f [α] x)
Γ ` k ≤ k
0
Γ ` L k M ≤ L k
0
M Λα:k.λx:unit.x
15

---

## Trang 16

Γ ` σ
0
1 ≤ σ1 f1 Γ, α: Fst(σ
0
1) ` σ2 ≤ σ
0
2 f2
Γ, α: Fst(σ1) ` σ2 : sig
σ1 [α:k1.τ1] σ
0
1 [α:k
0
1.τ 0
1]
σ2 [β:k2.τ2] σ
0
2 [β:k
0
2.τ 0
2]
Γ ` Π
gnα:σ1.σ2 ≤ Π
gnα:σ
0
1.σ0
2
 Λ :1.λf:(∀α:k1.τ1 → ∃β:k2.τ2).
Λα:k
0
1.λx:τ
0
1.
unpack [β, y] = f [α] (f1 [α] x)
in pack [β, f2 [β] y] as ∃β:k
0
2.τ 0
2
Γ ` σ
0
1 ≤ σ1 f1 Γ, α: Fst(σ
0
1) ` σ2 ≤ σ
0
2 f2
Γ, α: Fst(σ1) ` σ2 : sig
σ1 [α:k1.τ1] σ
0
1 [α:k
0
1.τ 0
1] σ2 [β:k2.τ2]
Γ ` Π
apα:σ1.σ2 ≤ Π
apα:σ
0
1.σ0
2
 Λγ:(Πα:k1.k2).λf:(∀α:k1.τ1 → [γα/β]τ2).
Λα:k
0
1.λx:τ
0
1.
f2 [γα] (f [α] (f1 [α]x))
Γ ` σ1 ≤ σ
0
1 f1 Γ, α: Fst(σ1) ` σ2 ≤ σ
0
2 f2
Γ, α: Fst(σ
0
1) ` σ
0
2 : sig
σ1 [α:k1. τ1] σ2 [β:k2. τ2]
Γ ` Σα:σ1.σ2 ≤ Σα:σ
0
1.σ0
2
 Λγ:(Σα:k1.k2).λx:([π1γ/α]τ1 × [π1γ, π2γ/α, β]τ2).
hf1 [π1γ] (π1x),([π1γ/α]f2) [π2γ] (π2x)i
B Compatibility
Γ ` τ1 : T Γ, x:τ1 ` e Rt e
0
: τ2
Γ ` λx:τ1.e Rt λx:τ1.e0
: τ1 → τ2
Γ ` e1 Rt e
0
1 : τ → τ
0 Γ ` e2 Rt e
0
2 : τ
Γ ` e1e2 Rt e
0
1e
0
2 : τ
0
Γ ` e1 Rt e
0
1 : τ1 Γ ` e2 Rt e
0
2 : τ2
Γ ` he1, e2i Rt he
0
1, e0
2i : τ1 × τ2
Γ ` e Rt e
0
: τ1 × τ2
Γ ` π1e Rt π1e
0
: τ1
Γ ` e Rt e
0
: τ1 × τ2
Γ ` π2e Rt π2e
0
: τ2
Γ ` k : kind Γ, α:k; Γ ` e Rv e
0
: τ
Γ ` Λα:k.e Rt Λα:k.e0
: ∀α:k.τ
Γ ` e Rt e
0
: ∀α:k.τ Γ ` c : k
Γ ` e[c] Rt e
0
[c] : [c/α]τ
Γ ` c : k Γ ` e Rt e
0
: [c/α]τ Γ, α:k ` τ : T
Γ ` pack [c, e] as ∃α:k.τ Rt pack [c, e0
] as ∃α:k.τ : ∃α:k.τ
Γ ` e1 Rt e
0
1 : ∃α:k.τ Γ, α:k, x:τ ` e2 Rt e
0
2 : τ
0 Γ ` τ
0
: T
Γ ` unpack [α, x] = e1 in e2 Rt unpack [α, x] = e
0
1 in e
0
2 : τ
0
Γ ` τ : T Γ ` e Rt e
0
: (unit → τ ) → τ
Γ ` fixτ e Rt fixτ e
0
: τ
Γ ` e1 Rt e
0
1 : τ1 Γ, x:τ1 ` e2 Rt e
0
2 : τ2
Γ ` let x = e1 in e2 Rt let x = e
0
1 in e
0
2 : τ2
Γ ` M Rm M0
: σ Γ, α/m:σ ` e Rt e
0
: τ Γ ` τ : T
Γ ` let α/m = M in e Rt let α/m = M0
in e
0
: τ
Γ ` M Rm M0
: h| τ |i
Γ ` Ext M Rt Ext M0
: τ
Γ ` e Rt e
0
: τ Γ ` τ ≡ τ
0
: T
Γ ` e Rt e
0
: τ
0
Γ ` τ1 : T Γ, x:τ1 ` e Rt e
0
: τ2
Γ ` λx:τ1.e Rv λx:τ1.e0
: τ1 → τ2
Γ ` e1 Rv e
0
1 : τ1 Γ ` e2 Rv e
0
2 : τ2
Γ ` he1, e2i Rv he
0
1, e0
2i : τ1 × τ2
Γ ` k : kind Γ, α:k; Γ ` e Rv e
0
: τ
Γ ` Λα:k.e Rv Λα:k.e0
: ∀α:k.τ
Γ ` c : k Γ ` e Rv e
0
: [c/α]τ Γ, α:k ` τ : T
Γ ` pack [c, e] as ∃α:k.τ Rv pack [c, e0
] as ∃α:k.τ : ∃α:k.τ
Γ ` e Rv e
0
: τ Γ ` τ ≡ τ
0
: T
Γ ` e Rv e
0
: τ
0
Γ ` c : k
ΓP ` L c M Rm L c M : L k M
Γ ` e Rt e
0
: τ
Γ `P h| e |i Rm h| e
0
|i : h| τ |i
Γ ` σ1 : sig Γ, α/m:σ1 `I M Rm M0
: σ2
Γ `P λ
gnα/m:σ1.M Rm λ
gnα/m:σ1.M0
: Πgnα:σ1.σ2
Γ `I M1 Rm M0
1 : Πgnα:σ.σ0
Γ `P M2 Rm M0
2 : σ Γ ` Fst(M2)  c2
Γ `I M1M2 Rm M0
1M0
2 : [c2/α]σ
0
Γ ` σ1 : sig Γ, α/m:σ1 `P M Rm M0
: σ2
Γ `P λ
apα/m:σ1.M Rm λ
apα/m:σ1.M0
: Πapα:σ1.σ2
Γ `κ M1 Rm M0
1 : Πapα:σ.σ0
Γ `P M2 Rm M0
2 : σ Γ ` Fst(M2)  c2
Γ `κ M1 · M2 Rm M0
1 · M0
2 : [c2/α]σ
0
Γ `κ M1 Rm M0
1 : σ1 Γ `κ M2 Rm M0
2 : σ2
Γ `κ hM1, M2i Rm hM0
1, M0
2i : σ1 × σ2
Γ `P M Rm M0
: Σα:σ1.σ2
Γ `P π1M Rm π1M0
: σ1
Γ `P M Rm M0
: Σα:σ1.σ2 Γ ` Fst(M)  c
Γ `P π2M Rm π2M0
: [π1c/α]σ2
Γ ` e Rt e
0
: ∃α:k.τ
Γ, α:k, x:τ `I M Rm M0
: σ Γ ` σ : sig
Γ `I unpack [α, x] = e in (M : σ)
Rm unpack [α, x] = e
0
in (M0
: σ) : σ
Γ ` e Rt e
0
: τ Γ, x:τ `κ M Rm M0
: σ
Γ `κ let x = e in M Rm let x = e
0
in M0
: σ
Γ `I M1 Rm M0
1 : σ
Γ, α/m:σ `I M2 Rm M0
2 : σ
0 Γ ` σ
0
: sig
Γ `I let α/m = M1 in (M2 : σ
0
)
Rm let α/m = M0
1 in (M0
2 : σ
0
) : σ
0
Γ `I M Rm M0
: σ
Γ `I (M :> σ) Rm (M0
:> σ) : σ
Γ `P M Rm M0
: σ
Γ `I M Rm M0
: σ
Γ `κ M Rm M0
: σ Γ ` σ ≤ σ
0
Γ `κ M Rm M0
: σ
0
16

---

## Trang 17

References
[1] Val Breazu-Tannen, Thierry Coquand, Carl A. Gunter,
and Andre Scedrov. Inheritance as implicit coercion.
Information and Computation, 93:172–221, 1991.
[2] Karl Crary. Modules, abstraction, and parametric poly￾morphism. In Forty-Fourth ACM Symposium on Prin￾ciples of Programming Languages, Paris, France, Jan￾uary 2017.
[3] Karl Crary, Robert Harper, and Sidd Puri. What
is a recursive module? In 1999 SIGPLAN Confer￾ence on Programming Language Design and Implemen￾tation, pages 50–63, Atlanta, May 1999.
[4] Pierre-Louis Curien and Giorgio Ghelli. Coherence of
subsumption, minimum typing and type-checking in
F≤. Mathematical Structures in Computer Science,
2(1):55–91, 1992.
[5] Derek Dreyer. Understanding and Evolving the ML
Module System. PhD thesis, Carnegie Mellon Univer￾sity, School of Computer Science, Pittsburgh, Pennsyl￾vania, May 2005.
[6] Derek Dreyer, Karl Crary, and Robert Harper. A type
system for higher-order modules. In Thirtieth ACM
Symposium on Principles of Programming Languages,
pages 236–249, New Orleans, Louisiana, January 2003.
[7] Martin Elsman. Static interpretation of modules.
In 1999 ACM International Conference on Functional
Programming, pages 208–219, Paris, France, 1999.
[8] Martin Elsman, Troels Henriksen, Danil Annenkov,
and Cosmin E. Oancea. Static interpretation of higher￾order modules in Futhark: Functional GPU program￾ming in the large. In 2018 ACM International Confer￾ence on Functional Programming, 2018.
[9] Robert Harper and Mark Lillibridge. A type-theoretic
approach to higher-order modules with sharing. In
Twenty-First ACM Symposium on Principles of Pro￾gramming Languages, pages 123–137, Portland, Ore￾gon, January 1994.
[10] Robert Harper, David MacQueen, and Robin Milner.
Standard ML. Technical Report ECS-LFCS-86-2, De￾partment of Computer Science, University of Edin￾burgh, March 1986.
[11] Robert Harper and John C. Mitchell. On the type
structure of Standard ML. ACM Transactions on
Programming Languages and Systems, 15(2):211–252,
April 1993.
[12] Robert Harper, John C. Mitchell, and Eugenio Moggi.
Higher-order modules and the phase distinction. In Sev￾enteenth ACM Symposium on Principles of Program￾ming Languages, pages 341–354, San Francisco, Jan￾uary 1990.
[13] Robert Harper and Greg Morrisett. Compiling poly￾morphism using intensional type analysis. In Twenty￾Second ACM Symposium on Principles of Program￾ming Languages, pages 130–141, San Francisco, Jan￾uary 1995.
[14] Robert Harper and Benjamin C. Pierce. Design consid￾erations for ML-Style module systems. In Benjamin C.
Pierce, editor, Advanced Topics in Types and Program￾ming Languages. The MIT Press, 2005.
[15] Robert Harper and Chris Stone. A type-theoretic in￾terpretation of Standard ML. In Proof, Language and
Interaction: Essays in Honour of Robin Milner. The
MIT Press, 2000. Extended version published as CMU
technical report CMU-CS-97-147.
[16] Daniel K. Lee, Karl Crary, and Robert Harper. Towards
a mechanized metatheory of Standard ML. In Thirty￾Fourth ACM Symposium on Principles of Programming
Languages, Nice, France, January 2007.
[17] Xavier Leroy. Manifest types, modules and separate
compilation. In Twenty-First ACM Symposium on
Principles of Programming Languages, pages 109–122,
Portland, Oregon, January 1994.
[18] Xavier Leroy. Applicative functors and fully trans￾parent higher-order modules. In Twenty-Second ACM
Symposium on Principles of Programming Languages,
San Francisco, January 1995.
[19] Xavier Leroy. A proposal for recursive modules in
Objective Caml. Available at http://caml.inria.
fr/pub/papers/xleroy-recursive_modules-03.pdf,
2003.
[20] Xavier Leroy, Damien Doligez, Jacques Garrigue, Di￾dier R´emy, and J´erˆome Vouillon. The OCaml system,
release 4.03, Documentation and user’s manual. Insti￾tut National de Recherche en Informatique et Automa￾tique (INRIA), 2016.
[21] David MacQueen. Using dependent types to express
modular structure. In Thirteenth ACM Symposium on
Principles of Programming Languages, pages 277–286,
St. Petersburg Beach, Florida, January 1986.
[22] David B. MacQueen and Mads Tofte. A semantics for
higher-order functors. In Fifth European Symposium
on Programming, volume 788 of Lecture Notes in Com￾puter Science, pages 409–423. Springer, 1994.
[23] Robin Milner, Mads Tofte, and Robert Harper. The
Definition of Standard ML. The MIT Press, Cam￾bridge, Massachusetts, 1990.
[24] John C. Mitchell and Gordon D. Plotkin. Abstract
types have existential type. ACM Transactions on Pro￾gramming Languages and Systems, 10(3):470–502, July
1988.
[25] Marco Patrignani, Amal Ahmed, and Dave Clarke. For￾mal approaches to secure compilation. ACM Comput￾ing Surveys, 2019. To appear.
[26] Andrew Pitts. Typed operational reasoning. In Ben￾jamin C. Pierce, editor, Advanced Topics in Types and
Programming Languages, chapter 7, pages 245–289.
The MIT Press, 2005.
[27] Andreas Rossberg, Claudio Russo, and Derek Dreyer.
F-ing modules. Journal of Functional Programming,
24(5), September 2014.
17

---

## Trang 18

[28] Claudio V. Russo. Types for Modules. PhD thesis,
Edinburgh University, March 1998.
[29] Claudio V. Russo. First-class structures for Standard
ML. Nordic Journal of Computing, 7(4), 2000.
[30] Claudio V. Russo. Recursive structures for Standard
ML. In 2001 ACM International Conference on Func￾tional Programming, 2001.
[31] Chung-chieh Shan. Higher-order modules in System Fω
and Haskell. Available at homes.soic.indiana.edu/
ccshan/xlate/xlate.pdf, May 2006.
[32] Zhong Shao. Typed cross-module compilation. In 1998
ACM International Conference on Functional Program￾ming, pages 141–152, Baltimore, Maryland, September
1998.
[33] Zhong Shao. Transparent modules with fully syntac￾tic signatures. In 1999 ACM International Confer￾ence on Functional Programming, pages 220–232, Paris,
September 1999.
[34] Christopher A. Stone and Robert Harper. Deciding
type equivalence in a language with singleton kinds. In
Twenty-Seventh ACM Symposium on Principles of Pro￾gramming Languages, Boston, January 2000. Extended
version published as CMU technical report CMU-CS￾99-155.
[35] Christopher A. Stone and Robert Harper. Extensional
equivalence and singleton types. ACM Transactions on
Computational Logic, 7(4), October 2006. An earlier
version appeared in the 2000 Symposium on Principles
of Programming Languages.
(Typographical errors corrected, April 2020.)
18
