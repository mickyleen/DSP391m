# Fully Abstract Module Compilation

Karl Crary

Carnegie Mellon University

#### Abstract

We give a translation suitable for compilation of modern module calculi supporting sealing, generativity, translucent signatures, applicative functors, higher-order functors and/or first-class modules. Ours is the first modulecompilation translation with a dynamic correctness theorem. The theorem states that the translation produces target terms that are contextually equivalent to the source, in an appropriate sense. A corollary of the theorem is that the translation is fully abstract. Consequently, the translation preserves all abstraction present in the source. In passing, we also show that modules are a definitional extension of the underlying core language. All of our proofs are formalized in Coq.

#### 1 Introduction

ML-style module calculi [10] provide powerful abstraction tools for various programming-in-the-large settings. Structures collect related type and term components, as well as other structures, together in a single expression. More than just a namespace management mechanism, modules can be made opaque, so that clients can use them only through their specified interfaces. Functors map modules to other modules, which allows the programmer to give an implementation of an abstract data type that depends parametrically on an unknown implementation of another.

In an untyped setting, compiling modules is not too difficult. One can simply erase the types and compile modular code as ordinary code, rendering modules as tuples or records, and functors and functions. Nevertheless, there are compelling reasons to prefer type-preserving compilation. Chief among them is the assistance that type structure offers in achieving compiler correctness. Simply as a matter of engineering, experience shows that it is very difficult to implement (accidentally) a type-preserving global transformation<sup>1</sup> that is incorrect and yet type correct.

Types can take on an even more significant role in compiler verification. The best correctness result for a compiler phase is contextual equivalence, which says that the source and translated terms are indistinguishable by any legal observation (in an appropriate sense). This is the most robust form of translation correctness because it applies regardless of how the translated code is used, be it translated further (vertical composition), linked with other code (horizontal composition), or used in other way. Types are essential to contextual equivalence: without type structure to circumscribe how the code may be used, too many observations are possible, making non-trivial contextual equivalence nearly impossible.

In this paper we give the first compilation strategy for ML-style modules that (1) supports the full array of abstraction mechanisms offered by the Standard ML module system (i.e., structures, sealing, generative functors, and translucent signatures) [23] as well as some other important features (applicative functors, higher-order functors, and first-class modules), and (2) admits a contextual equivalence result between modules and their translation.

As a corollary of contextual equivalence, the module translation is fully abstract: Modules are equivalent exactly when their translations are equivalent. The left-to-right portion of this is also called abstraction preservation. It says that no legal target code can break any abstractions present in the source code.

This is particularly valuable today, as functional languages are increasingly becoming part of heterogeneous (multi-language) development environments. Full abstraction means that a programmer can be confident that his or her abstractions will be respected even by code linked in from another language, provided types are preserved and enforced [25].

Moreover, our compilation strategy admits separate compilation, meaning that units can be linked entirely in the target language, without reference to the source code that generated them. In practice, this means that every module expression—including functors—is independently translated to a target-language expression.

The first mathematical examination of the compilation of modules was undertaken by Harper, et al. [12]. Their interest was not in compilation per se, but in the equational theory of higher-order modules. Specifically, they wished to show that code that employs functors respects a compiletime/run-time phase distinction, meaning that code can always be type-checked without executing any code.

That the phase distinction is respected is not obvious a priori. A module contains both type and term components, and a functor is a function that maps modules to modules, so at first glance it appears as though the type components of the result can depend on the term components of the argument. If so, it would be necessary to execute the argument terms in order to determine the result types.

This does not happen because the module language is

<sup>1</sup>We refer here to such transformations as CPS or closure conversion, in contrast to local transformations such as arithmetic optimization, where types help much less.

structured in such a way that types can never depend on terms. Harper, et al. show that module expressions can be separated into two parts: a static (or "compile-time") phase and a dynamic (or "run-time") phase. Dynamic-phase expressions can depend on static-phase expressions, but not vice versa. This relies crucially on modules being secondclass.

Harper, et al. go on to show that the static-phase equational theory is unaffected by the deletion of all dynamicphase equations. But for our purposes, we are interested in their phase-separation algorithm itself. In their algorithm, every module M is split into two pieces [c, e], in which c is a type constructor representing M's static portion, and e is a term representing its dynamic portion. Both pieces can be rendered without reference to the module language, so modules are compiled away.

Harper, et al.'s module language supported some important features, but it omitted other ones, most notably sealing and generativity. The only form of abstraction available was lambda abstraction, which meant that their language supported only client-side abstraction, not provider-side abstraction, which is more robust [2].

Subsequently, Shao [32] employed a similar algorithm in a compiler for Standard ML. Unlike Harper, et al., Shao's source language supports sealing and generativity. However, the translation deals with them simply by removing them, so it does not preserve abstraction. (This was consistent with his purpose of facilitating cross-module inlining.)

Next, Shan [31] and Rossberg, et al. [27] proposed a different approach for compiling modules with sealing and generativity, in which sealing was treated as introducing an existential type. This provides a very natural treatment of abstraction [24].

Neither Shan nor Rossberg, et al. included any dynamic correctness result, much less full abstraction. In fact, neither one gave an evaluation semantics for the source language.<sup>2</sup> We resolve the question here in the negative; their translation is probably not fully abstract. More precisely, their translation is not fully abstract if the target's dynamic semantics provides any strict mechanism (e.g., call-by-value or seq) capable of observing the termination of a function expression. However, the problem is easily corrected by a change to the target's static semantics.

This paper's main contribution is the first modulecompilation algorithm with a dynamic correctness proof. The algorithm is given as a phase-separation translation: as in Harper, et al.'s original translation, we split each pure module into a type constructor and a term. The correctness result is as strong as possible: we show that modules are translated to contextually equivalent terms, and we conclude, as a corollary, that the translation is fully abstract.

The most obvious obstacle to the contextual equivalence result is that the source expression and its translation belong to different types, different syntactic classes, and indeed different languages. The difference in languages is easily dealt with: our target language is a strict subset of our source language, obtained by omitting all module-oriented forms. Thus, we can compare a source expression and its translation simply by taking the translation as another source expression.

To mediate the difference in types and syntactic classes, we show that we can define a pair of functions Snd and Join that convert back-and-forth between modules and terms of appropriate types. The result then states that if a module M is phase-separated into static portion c and dynamic portion e, then Join[c, e] is contextually equivalent to M. Since Snd and Join are inverses, one may equivalently say that SndM is contextually equivalent to e.

If Join merely traversed e to reverse the phase-separation translation, this result would be trivial. It does not. The important fact about Snd and Join is they are defined within the grammar of the language. They are not able to traverse the syntax of an expression, and thus they can only interact with an expression through the interface given by its type. Their purpose is to coerce between interfaces.

One observation that we can draw from this result is that modules are a definitional extension of the core language. Put less formally, the module language can be viewed as merely a very convenient syntax for writing modular programs. A practical consequence of this observation is that some useful module features (notably first-class modules [29]) need not be included as distinct features to be compiled, because they are already definitional extensions of the language.

Our development proceeds as follows: First, we summarize our module calculus and state some preliminary results regarding it (Section 2). Our module calculus is nearly identical to Crary [2], except we add a value restriction for polymorphic functions. Second, we give the phase separation algorithm (Section 3). Third, we define contextual equivalence (Section 4). This is adapted from Crary, with small changes to deal with the value restriction. We also state some useful lemmas about contextual equivalence, corollaries of the development of logical equivalence in Crary. Finally we prove our correctness results (Section 5): We define Snd and Join, show that they are inverses, show that modules translate to contextually equivalent terms (modulo Join), and conclude full abstraction as a corollary.

All of our proofs are formalized in Coq, and may be found at:

### www.cs.cmu.edu/~crary/papers/2018/famc-formal.tgz

# 2 The Module Calculus

Our module calculus is nearly identical to Crary [2], which is adapted from that of Dreyer [5], which in turn builds on a long line of prior work on module calculi [21, 12, 22, 9, 17, 18, 15, 34, 28, 33, 6]. The sole change from Crary is the addition of a value restriction to polymorphic functions. (As we will show, the value restriction is necessary for our translation to be fully abstract.) The module calculus itself is not a research contribution of this paper; our purpose here is just to lay the foundation for our phase-separation algorithm.

The module calculus is intended to account for the fundamental elements of a module system that are vital for data abstraction [2]. However, it does not account for all of the convenience features of modern module systems: Fields of modules are identified by position, not by name. Coercion of a module to a specified signature (i.e., by drop-

<sup>2</sup>This was understandable in both cases. Shan was working from a pre-existing type theory [6] that did not commit to a specific dynamic semantics. Rossberg, et al. were defining a module system by giving an elaboration of ML modules into a module-free core language, so the source language necessarily had no independent semantics at all. (Nevertheless, the question remains whether the elaboration realizes the programmer's expectations.)

|k ::= | 1 |  |  | unit | kind |
|-------- | -------- | ----- | ----------------------- | --------------------- | ------------- |
| | T |  |  | types |  |
| | S | ( c | ) | singleton | kind |
| | Π | α | : k.k | dependent | functions |
| | Σ | α | : k.k | dependent | pairs |
|c, ::= | α |  |  |  |  |
|τ | ? |  |  | unit | constructor |
| | λα |  | : k.c c c | lambda, | application |
| | h | c, | c i | pair |  |
| | π | 1 | c π 2 c | projection |  |
| | unit |  |  | unit | type |
| | τ | 1 | → τ 2 | functions |  |
| | τ | 1 | × τ 2 | products |  |
| | ∀ | α | : k.τ | universals |  |
| | ∃ | α | : k.τ | existentials |  |
|e ::= | x |  |  |  |  |
| | ? |  |  | unit | term |
| | λx |  | : τ.e e e | lambda, | application |
| | h | e, | e i | pair |  |
| | π | 1 | e π 2 e | projection |  |
| | Λ | α | : k.e | polymorphic | fun. |
| | e | [ c | ] | polymorphic | app. |
| | pack |  | [ c, e ] as ∃ α : k.τ | existential | package |
| | unpack |  | [ α, x ] = e | in e unpack |  |
| | fix |  | τ e | recursion |  |
| | let |  | x = e in e | term | binding |
| | let |  | α/m = M in e | module | binding |
| | Ext |  | M | extraction |  |
|M ::= | m |  |  |  |  |
| | ? |  |  | unit | module |
| | L | c | M | atomic | module |
| | h | e | i | atomic | module |
| | λ |  |  |  |  |
| |  | gn | α/m : σ.M | generative | functor |
| | M |  | M | generative | app. |
| | λ |  |  |  |  |
| |  | ap | α/m : σ.M | applicative | functor |
| | M |  | M | applicative | app. |
| | h | M, | M i | pair |  |
| | π | 1 | M π 2 M | projection |  |
| | unpack |  | [ α, x ] = e | in ( M : σ ) unpack |  |
| | let |  | x = e in M | term | binding |
| | let |  | α/m = M in ( | M : σ ) module | binding |
| | M |  | : > σ | sealing |  |
|σ ::= | 1 |  |  | unit | signature |
| | L | k | M | atomic | signature |
| | h | τ | i | atomic | signature |
| | Π |  |  |  |  |
| |  | gn | α : σ.σ | generative | functors |
| | Π |  |  |  |  |
| |  | ap | α : σ.σ | applicative | functors |
| | Σ | α | : σ.σ | pairs |  |
|Γ ::= |  |  |  | empty | context |
| | Γ | , | α : k | constr. | hypothesis |
| | Γ | , | x : τ | term | hypothesis |
| | Γ | , | α/m : σ | module | hypothesis |

Figure 1: Syntax

ping fields, reordering fields, or monomorphizing polymorphic functions) is not done automatically; to do so creates complications that are orthogonal to the abstraction concerns we focus on here. Like nearly all module calculi (but not Harper and Mitchell [11]), sharing specifications are not primitive, but are taken as syntactic sugar over translucent signatures. The open declaration, which is useful in practice but makes little sense in a type theory with a proper notion of binding, is not supported. First-class modules (supported in some dialects of ML [29]) are not explicitly supported (but see Section 6). We also do not support recursive modules [3, 30, 5] (supported in some dialects of ML [30, 19]); the abstraction implications of recursive modules are not yet well examined. All of these features can be implemented by elaboration [15, 6, 5], but those elaborated aspects of the language fall outside the results we prove here.

Most significantly, we follow earlier work [15, 6, 27] by using elaboration to address the avoidance problem [6], in which the structure of a program mandates that type variables leave scope, but there is no best way for a module's type to avoid those variables. This arises most importantly in sealed arguments to functors. No satisfactory type-theoretic treatment of the avoidance problem has yet been found. The elaboration involves retaining in "hidden" modules the type variables that are supposed to leave scope. Unfortunately, the hidden-ness of those modules is not enforceable after elaboration, which may lead to tangible compromises in data abstraction. To avoid this, the programmer must manually ascribe signatures whenever type variables leave scope. This preserves abstraction, but is inconvenient.

Syntax A key design goal of the module calculus is to respect the phase distinction [12], which means that the meaning of static phrases, and specifically their equivalence, can be determined without referring to dynamic phrases. The static syntactic classes are kinds (k), type constructors (c), and signatures (σ). The dynamic syntactic classes are terms (e) and modules (M). Signatures serve as the types of modules, and kinds serve (as usual) as the types of type constructors. The full syntax is given in Figure 1. (Figures 1, 2, and 4 are borrowed from Crary [2].)

Static phrases The constructor and kind expressions are the singleton kind calculus of Stone and Harper [35], with some minor extensions. Actual types belong to the kind T. (We often use the metavariable τ instead of c for actual types.) The unit constructor? belongs to the kind 1.

If τ is a type, we may form the singleton kind S(τ), which contains precisely τ (and other types equivalent to it). This is used to model type definitions and sharing specifications in signatures. Thus, if τ: S(τ 0), we can conclude that τ and τ 0 are equivalent types. As a consequence, equivalence is context sensitive: α and τ are equivalent under the assumption α: S(τ), but not under α: T. As a further consequence, equivalence depends on the kind at which constructors are compared: λα:T.α and λα:T.τ are equivalent at S(τ) → T but not at T → T. Although the singleton kind primitive is restricted to types, one can use it to define singletons at any kind.

Since singletons allow kinds to depend on constructors, it is useful to support dependent kinds. The dependent form of function kinds is written Πα:k.k<sup>0</sup> and the dependent form of products is written Σα:k.k<sup>0</sup>. When α does not appear free in k 0, these are written using k → k 0 and k × k 0 respectively, as usual.

Dynamic phrases The syntax for terms is largely standard. The recursion form fix<sup>τ</sup> e has the type τ, provided e has the type (unit→τ)→τ, and we evaluate fix<sup>τ</sup> e to e(λ:unit.fix<sup>τ</sup> e).<sup>3</sup> The module language contains static and dynamic atomic modules, generative and applicative functors, and pairs. An atomic module models a single field of a module: a static atom (L <sup>c</sup> M) contains a single constructor, and a dynamic atom (h| e |i) contains a single term. For example, the ML module:

struct type t = bool val x = true end

could be elaborated <sup>h</sup>L boolM,h|true |ii. (Observe that, as noted above, the field names disappear when a module is elaborated.)

Abstraction is introduced using the form M:> σ, which seals M so that its components can be accessed only through the interface given by σ. In particular, if a signature gives the kind of a type field as T, that type is unknown and therefore abstract. Proper enforcement of type abstraction requires that sealing be viewed as a computational effect [6], and that types cannot be extracted from impure modules. Thus, to use the types from a sealed module, one must bind that module to a variable; variables are always pure.

We syntactically distinguish between generative and applicative functors. A generative functor can have sealing in its body, and calling it induces an effect. In contrast, an applicative functor cannot, and does not.

For technical reasons related to the avoidance problem [5, section 4.2.6], a module that either let-binds a module or unpacks an existential type must include an explicit signature annotation, and such modules are deemed to induce an effect.

Static portions, twinned variables, and phase separation To extract a term from a dynamic atom, one uses the form Ext M. However, to extract a type constructor from a static atom, we employ a judgement rather than a syntactic form. The judgement Fst(M) c says that c is the static portion of M. 4

In particular, Fst(L <sup>c</sup> M) <sup>c</sup>. The reason for this design, invented by Dreyer [5], is it removes any syntactic dependency of static phrases (such as types) on terms or modules. By disentangling the singleton kind calculus from all dynamic phrases, we are able to use Stone and Harper's singleton-kind metatheory [35] off the shelf.

For static extraction to work compositionally, we must be able to compute the static portion of any pure module, not only static atom literals. (Impure modules do not have static portions.) The rules for doing so are given in Figure 2. Two subtle points arise: First, by its nature, a generative functor returns nothing that is statically predictable. Therefore the static component of a generative functor is trivial. Second, Fst(σ): kind Fst(1) def = 1

Fst(L <sup>k</sup> M)

def = k

Fst(h| τ |i)

def = 1

Fst(Πgnα:σ1.σ2)

def = 1

Fst(Πapα:σ1.σ2)

def = Πα: Fst(σ1). Fst(σ2)

Fst(Σα:σ1.σ2)

def = Σα: Fst(σ1). Fst(σ2)

Γ ` Fst(M) c

α/m ∈ Dom(Γ)

<sup>Γ</sup> Fst(m) <sup>α</sup> <sup>Γ</sup> Fst(?)? <sup>Γ</sup> ` Fst(L <sup>c</sup> M) <sup>c</sup>

Γ Fst(h| e |i)? Γ Fst(λ

gnα/m:σ.M)?

Γ, α/m:σ ` Fst(M) c

Γ ` Fst(λ

apα/m:σ.M) λα: Fst(σ).c

Γ Fst(M1) c<sup>1</sup> Γ Fst(M2) c<sup>2</sup> Γ Fst(M<sup>1</sup> · M2) c1c<sup>2</sup> Γ Fst(hM1, M2i) hc1, c2i

Γ Fst(M) c Γ Fst(πiM) πic

Γ Fst(M) c Γ Fst(let x = e in M) c

Figure 2: Static portions

for any module variable m, we must be able to compute m's static portion, but of course that cannot be known, so we must have a type-constructor variable prepared to stand in for m's static portion. This leads to the concept of twinned variables [16]: every module variable m is twinned with a constructor variable α, written α/m, where α is the static portion of m. <sup>5</sup> However, when α is not used, we will often leave it out.

Twinned variables are recorded in the context and static portions depend on them, so the static portion judgement is written in its most general form as Γ ` M c. However, when Γ is empty or can be determined from context, we often write Fst(M) c, or even just Fst(M) for the unique c such that Fst(M) c.

Our static-portion rules are very similar in spirit to the non-standard equational rules of Harper, et al. [12]. As in this work, Harper et al. gave rules for determining the static portions of modules as part of their static semantics, and also—separately—gave an algorithm for compiling modules into static and dynamic components. The main difference (apart from the extra features we support here), is that their "non-standard" rules determined not only a static portion, but also a dynamic portion, even though only the static portion ended up being relevant to typing judgements.

Signatures Signatures forms include signatures for atomic modules, generative and application functors, and pairs.

<sup>3</sup>Observe that the argument to e is a value, so this evaluation behaves acceptably in a call-by-value setting. That would not be the case with the evaluation to e(fix<sup>τ</sup> e) that would be implied by a more conventional typing.

<sup>4</sup>The name Fst is motivated by the connection to phase separation, which explicit renders modules as a pair of a static and dynamic component.

<sup>5</sup>An alternative [12, 5] is to use a naming convention to associate module and constructor variables, but this complicates binding and substitution. Sorting out those complications carefully leaves you with something very close to twinned variables.

S(c: k): kind S(<sup>c</sup>: 1) def = 1

S(c: T)

def <sup>=</sup> S(c)

S(c: S(c 0

)) def <sup>=</sup> S(c)

S(c: Πα:k1.k2)

def = Πα:k1.S(c α: <sup>k</sup>2)

S(c: Σα:k1.k2)

def <sup>=</sup> S(π1<sup>c</sup>: <sup>k</sup>1) × S(π2<sup>c</sup>: [π1c/α]k2)

S(c: σ): signature S(<sup>c</sup>: 1) def = 1

<sup>S</sup>(<sup>c</sup>: L <sup>k</sup> M)

def <sup>=</sup> L <sup>S</sup>(<sup>c</sup>: <sup>k</sup>)M

S(c: h| τ |i)

def <sup>=</sup> h| <sup>τ</sup> |i

S(c: Πgnα:σ1.σ2)

def = Πgnα:σ1.σ<sup>2</sup>

S(c: Πapα:σ1.σ2)

def = Πapα:σ1.S(c α: <sup>σ</sup>2)

S(c: Σα:σ1.σ2)

def <sup>=</sup> S(π1<sup>c</sup>: <sup>σ</sup>1) × S(π2<sup>c</sup>: [π1c/α]σ2)

Figure 3: Higher-order singletons

The signatures for functors and for pairs are dependent, so one might expect to write them with a twinned left-handside, like Σα/m:σ1.σ2. However, since a module can never appear within a signature (signatures being static phrases), the m variable will never be used, so we don't bother to write it. (As usual, when α does not appear free in σ2, we write Σα:σ1.σ<sup>2</sup> as σ<sup>1</sup> × σ2.)

In a twinned binding α/m:σ, or in the binding α:σ within a dependent signature, α stands for the static portion of some module belonging to σ. Thus, α will have kind Fst(σ), which stands for the static portion of σ. The definition of Fst appears in Figure 2. Whenever m: σ and Fst(m) c, we have c: Fst(σ).

Higher-order singletons The primitive singleton kind S(c) is well-formed only when c is a type. However, singletons at higher kinds (written S(c: k)) are definable using dependent kinds. For example, S(c: k1→k2) = Πα:k1.S(c α: k2), since a constructor is equivalent to c in kind k1→k<sup>2</sup> precisely when it takes an argument of kind k<sup>1</sup> and does with it whatever c does with it.

We can use the same technique to define singleton signatures. Suppose c: Fst(σ). Then the singleton signature S(c: σ) contains all pure modules in σ whose static component is equivalent to <sup>c</sup>. For instance <sup>S</sup>(<sup>c</sup>: L <sup>k</sup> M) = L <sup>S</sup>(<sup>c</sup>: <sup>k</sup>)M. The definitions of higher-order singletons are given in Figure 3. Note that when the static component of σ is trivial (i.e., when Fst(σ) = 1), S(c: σ) = σ, since all static components are equivalent at kind 1.

Semantics The static semantics is given by several judgements summarized in Figure 4. The rules are exactly those from Crary [2], with the sole exception that the typing rule for polymorphic functions is replaced by the one given below, which includes a value restriction.

The top-level judgement is the typing judgement for modules, written Γ `<sup>κ</sup> M: σ, where the purity class κ is either P, indicating that the module is pure (unsealed), or I, indicating that it is impure (sealed). A "forget" rule allows pure modules to be viewed as impure.

|` | Γ | ok | context formation |
|--- | ----- | ----- | ----------------------------- |
|Γ | ` k | : | kind kind formation |
|Γ | ` k | ≡ | k |
| |  |  | kind equivalence |
|Γ | ` k | ≤ | k |
|Γ | ` c | : | k constructor formation |
|Γ | ` c | ≡ | c |
| |  |  | : k constructor equivalence |
|Γ | ` σ | : | sig signature formation |
|Γ | ` σ | ≡ | σ |
| |  |  | : sig signature equivalence |
|Γ | ` σ | ≤ | σ |
|Γ | ` e | : | τ term formation |
|Γ | ` κ | M | : σ module formation |
|Γ | ` | Fst | ( M ) c static portion |

Figure 4: Static semantic judgements

The dynamic semantics is given by a standard, call-byvalue, structured operational semantics, written Γ e 7→ e 0 and Γ M 7→ M<sup>0</sup>. (It is convenient to be able to evaluate open terms, but in the typical case in which Γ is empty, we will omit the turnstile.) The value forms are:

v::= x |? | λx:τ.e | hv, vi | Λα:k.e | pack [c, v] as ∃α:k.τ <sup>V</sup>::= <sup>m</sup> <sup>|</sup>? <sup>|</sup> L <sup>c</sup> M | h| <sup>v</sup> |i | hV, V <sup>i</sup> | λ gnα/m:σ.M | λ apα/m:σ.M

We write e↓ or M↓ to mean that e or M evaluates to a value.

Two rules illustrate issues that arise in the dynamic semantics. The evaluation rule for sealed modules immediately removes the seal:

Γ ` (M:> σ) 7→ M

In essence, this step is the computational effect that the type system tracks. Rules that substitute for module variables, such as the beta rules for functors, also must substitute for the twinned constructor variable, which is obtained using the Fst judgement:

Γ Fst(V2) c<sup>2</sup> Γ (λ gnα/m:σ.M1)V<sup>2</sup> 7→ [c2, V2/α, m]M<sup>1</sup>

This rule works because well-formed module values are always pure, so their static portion can always be obtained.

The value restriction In the typing rule for polymorphic functions, we require that the body be a static value:

Γ k: kind Γ, α:k sv: τ Γ ` Λα:k.sv: ∀α:k.τ

where a static value (sv) is like an ordinary value (v) except variables are excluded:

sv::=? | λx:τ.e | hsv, svi | Λα:k.sv | pack [c, sv] as ∃α:k.τ

We distinguish between static and ordinary values and use the former because we wish for well-formedness to be preserved by the substitution of any appropriately typed term even a non-value—for a variable, and that is not the case with ordinary values. This is necessary to have a useful contextual-equivalence functionality lemma.

The inclusion of the value restriction has no significant effect on the development of logical equivalence given in Crary [2], but it is essential for the phase separation translation to be fully abstract.

Metatheory We can now state some metatheoretic results from Crary [2]:

#### Lemma 2.1

- If Γ <sup>P</sup> M: σ then Γ Fst(M): Fst(σ).
- If Γ ok and Γ c: k then Γ c: S(c: k) and Γ, α:S(c: k) α ≡ c: k.
- If Γok and Γ <sup>P</sup> M: σ then Γ `<sup>P</sup> M: S(Fst(M): σ).
- If Γ <sup>I</sup> V: σ then Γ <sup>P</sup> V: σ.

Theorem 2.2 (Type preservation) If ` Γ ok then:

- If Γ e: τ and Γ e 7→ e 0 then Γ ` e 0: τ.
- If Γ <sup>κ</sup> M: σ and Γ M 7→ M<sup>0</sup> then Γ `<sup>κ</sup> M<sup>0</sup>: σ.
- If Γ <sup>P</sup> M: σ and Γ M 7→ M<sup>0</sup> then Γ ` Fst(M) ≡ Fst(M<sup>0</sup>): Fst(σ).

Theorem 2.3 (Progress) If e: τ then either e is a value or takes a step. If <sup>κ</sup> M: σ then either M is a value or takes a step.

# Theorem 2.4 (Determinism)

- If Γ e 7→ e<sup>1</sup> and Γ e 7→ e<sup>2</sup> then e<sup>1</sup> = e2.
- If Γ M 7→ M<sup>1</sup> and Γ M 7→ M<sup>2</sup> then M<sup>1</sup> = M2.
- If Γ Fst(M) c<sup>1</sup> and Γ Fst(M) c<sup>2</sup> then c<sup>1</sup> = c2.

#### 3 Phase Separation

The target language for our translation is the subset of the source language obtained by deleting all the module-oriented forms. Note that the syntactic classes of kinds and constructors contain no module-oriented forms, and are thus unchanged. (This is an advantage of Dreyer's device [5] wherein Fst is a judgement, rather than a syntactic form.)

Using a fragment of the source as the target dramatically simplifies several aspects of the development: (1) We need not develop the metatheory of the target language; the source's metatheory applies directly. (2) The type translation is the identity. (3) Full abstraction is a direct consequence of the dynamic correctness theorem, since every target observation is a source observation, and every source observation can be translated to a target observation.

We express phase separation as a type-directed translation [13] using three judgements, one each for terms, pure modules, and impure modules. The term translation judgement is Γ e: τ e¯, meaning that Γ e: τ and ¯e is a translation of e. Since the type translation is the identity, ¯e will have the same type as e.

Different translation derivations can ostensibly result in different translations, but we can show that the translation is coherent [1], meaning that all of a term's translations are equivalent. Coherence is another simple corollary of dynamic correctness.

The term translation does very little, since most term forms do not pertain to modules. Its rules are given in Appendix A. The main judgements are the phase-separation judgements for modules. For pure modules, the judgement is written:

Γ `<sup>P</sup> M: σ [c, e]

Here, M is separated into its static portion c and its dynamic portion e. Recall that the module calculus has its own internal concept of static components (Fst(M)). These notions agree: if also Γ ` Fst(M) c 0 then c = c 0.

The types of c and e are governed by the phase separation judgement for signatures:

σ [α:k. τ ]

Here σ is separated into its static portion k and its dynamic portion τ (in which τ can refer to α, which stands for the actual static component). Thus, in the above, c belongs to kind k, and e belongs to type [c/α]τ.

The best way to understand the translation is through the phase-separation rules for signatures. A static atom is all static, so L <sup>k</sup> M [: k. unit]. Conversely, a dynamic atom is all dynamic, so h| τ |i [:1. τ ]. A trivial module is trivial is trivial in both components, so 1 [:1. unit].

In an applicative functor, the static portion maps the static portion of the argument to the static portion of the result, while the dynamic portion maps both portions of the argument to the dynamic portion of the result:

σ<sup>1</sup> [α1:k1. τ1] σ<sup>2</sup> [α2:k2. τ2] Π apα:σ1.σ<sup>2</sup> [β: Πα:k1.k2. ∀α:k1. [α/α1]τ<sup>1</sup> → [βα/α2]τ2]

In a pair, the static (dynamic) portion is the pair of the static (dynamic) portions of the constituents:

σ<sup>1</sup> [α1:k1. τ1] σ<sup>2</sup> [α2:k2. τ2] Σα:σ1.σ<sup>2</sup> [β: Σα:k1.k2. [π1β/α1]τ<sup>1</sup> × [π1β, π2β/α, α2]τ2]

These rules are essentially the rules from Harper, et al. [12] (adapted for dependent kinds), but they did not account for generative functors. For generative functors, we adapt the translation of Shan [31] and Rossberg, et al. [27].

The tricky point is how to phase-separate impure (i.e., sealed) modules. Our translation wishes to separate modules into their static and dynamic components, but sealed modules are not supposed to have a static component, since their abstract type components are notionally determined at run-time.<sup>6</sup> Any translation that makes them available statically will not preserve abstraction.

But once a sealed module has executed, its result value will be pure (recall part 4 of Lemma 2.1), and therefore it will have static and dynamic components. Thus, the appropriate translation of an impure module is a term that dynamically computes the static and dynamic portions of that eventual value. Thus we write:

Γ `<sup>I</sup> M: σ e

where e belongs to ∃α:k.τ (assuming σ [α:k. τ ]).

Now we can give the rule for a generative functor, which returns an impure module. Its static portion is trivial, while

Indeed, when first-class modules are added, they are actually determined at run-time.

σ [α:k. τ ]

<sup>1</sup> [:1. unit] L <sup>k</sup> M [: k. unit] h| <sup>τ</sup> |i [:1. τ ]

σ<sup>1</sup> [α1:k1. τ1] σ<sup>2</sup> [α2:k2. τ2] Π gnα:σ1.σ<sup>2</sup> [:1. ∀α:k1. [α/α1]τ<sup>1</sup> → ∃α2:k2.τ2]

Figure 5: The signature translation

its dynamic portion maps both portions of the argument to an existential package containing the static and dynamic portions of the module value that the functor eventually returns:

σ<sup>1</sup> [α1:k1. τ1] σ<sup>2</sup> [α2:k2. τ2] Π gnα:σ1.σ<sup>2</sup> [:1. ∀α:k1. [α/α1]τ<sup>1</sup> → ∃α2:k2.τ2]

For convenience, the signature translation rules are collected in Figure 5. The module translation is given in Figures 6, and 7. Most of its rules are dictated by the signature phase-separation rules given above. We touch on a few points that are interesting or subtle:

The translation's calling convention is given by the context translation Γ, which is formalized in Figure 8. Constructor and term bindings are translated directly, as one would expect. In a module binding α/m, we introduce two variables—a constructor variable α and a term variable ˆm to represent the module's static and dynamic portions. Here we assume that there are infinitely many term variables, so for every module variable m we can associate a term variable mˆ that is not otherwise used.

With the calling convention established, we can consider the translation rules for functors. For applicative functors, the rule states:

Γ σ<sup>1</sup>: sig σ<sup>1</sup> [α:k1. τ1] Γ, α/m:σ<sup>1</sup> <sup>P</sup> M: σ<sup>2</sup> [c, e] Γ `<sup>P</sup> λ apα/m:σ1.M: Πapα:σ1.σ<sup>2</sup> [λα:k1.c, Λα:k1.λmˆ:τ1.e]

The functor's static portion λα:k1.c takes the static portion of the functor argument (α:k1) to the static portion of the body (c). In accordance with the phase distinction, there is no dependence on the dynamic portion of the argument. The functor's dynamic portion takes the static and dynamic portions of the argument (α:k<sup>1</sup> and ˆm:τ1)—thereby following the calling convention for α/m:σ1—to the dynamic portion of the body (e).

The applicative functor application rule states (in the pure case):

Γ <sup>P</sup> M<sup>1</sup>: Πapα:σ1.σ<sup>2</sup> [c1, e1] Γ <sup>P</sup> M<sup>2</sup>: σ<sup>1</sup> [c2, e2] Γ `<sup>P</sup> M<sup>1</sup> · M<sup>2</sup>: [c2/α]σ<sup>2</sup> [c1c2, e<sup>1</sup> [c2] e2]

Γ `<sup>P</sup> M: σ [c, e]

Γ `?: 1 [?,?]

Γ c: k <sup>Γ</sup> L <sup>c</sup> M: L <sup>k</sup> M [c,?] Γ e: τ e¯ Γ h| e |i: h| τ |i [?, e¯]

Γ σ<sup>1</sup>: sig σ<sup>1</sup> [α:k1. τ1] Γ, α/m:σ<sup>1</sup> <sup>I</sup> M: σ<sup>2</sup> e Γ `<sup>P</sup> λ gnα/m:σ1.M: Πgnα:σ1.σ<sup>2</sup> [?, Λα:k1.λmˆ:τ1.e]

Γ <sup>P</sup> M<sup>1</sup>: σ<sup>1</sup> [c1, e1] Γ <sup>P</sup> M<sup>2</sup>: σ<sup>2</sup> [c2, e2] Γ `<sup>P</sup> hM1, M2i: σ<sup>1</sup> × σ<sup>2</sup> [hc1, c2i,he1, e2i]

Γ <sup>P</sup> M: Σα:σ1.σ<sup>2</sup> [c, e] Γ <sup>P</sup> π1M: σ<sup>1</sup> [π1c, π1e]

Γ <sup>P</sup> M: Σα:σ1.σ<sup>2</sup> [c, e] Γ <sup>P</sup> π2M: [π1c/α]σ<sup>2</sup> [π2c, π2e]

Γ <sup>P</sup> e: τ e<sup>1</sup> Γ, x:τ <sup>P</sup> M: σ [c, e2] Γ `<sup>P</sup> let x = e in M: σ [c, let x = e<sup>1</sup> in e2]

Figure 6: The pure module translation

# Γ `<sup>I</sup> M : σ e

Γ <sup>I</sup> M<sup>1</sup>: Πgnα:σ1.σ<sup>2</sup> e<sup>1</sup> Γ <sup>P</sup> M<sup>2</sup>: σ<sup>1</sup> [c2, e2] Γ `<sup>I</sup> M1M<sup>2</sup>: [c2/α]σ<sup>2</sup> unpack [, f] = e<sup>1</sup> in f [c2] e<sup>2</sup>

Γ <sup>I</sup> M<sup>1</sup>: Πapα:σ1.σ<sup>2</sup> e<sup>1</sup> Γ <sup>P</sup> M<sup>2</sup>: σ<sup>1</sup> [c2, e2] σ<sup>2</sup> [β:k2. τ2] Γ `<sup>I</sup> M<sup>1</sup> · M<sup>2</sup>: [c2/α]σ<sup>2</sup> unpack [γ, f] = e<sup>1</sup> in pack [γ c2, f [c2] e2] asc2/α

Γ M<sup>1</sup>: σ<sup>1</sup> e<sup>1</sup> Γ M<sup>2</sup>: σ<sup>2</sup> e<sup>2</sup> σ<sup>1</sup> [α1:k1. τ1] σ<sup>2</sup> [α2:k2. τ2] Γ ` hM1, M2i: σ<sup>1</sup> × σ<sup>2</sup> unpack [α1, x1] = e<sup>1</sup> in unpack [α2, x2] = e<sup>2</sup> in pack [hα1, α2i,hx1, x2i] as ∃β:(k<sup>1</sup> × k2). [π1β/α1]τ<sup>1</sup> × [π2β/α2]τ<sup>2</sup>

Γ e: ∃α:k.τ e<sup>1</sup> Γ, α:k, x:τ <sup>I</sup> M: σ e<sup>2</sup> Γ σ: sig Γ <sup>I</sup> unpack [α, x] = e in (M: σ): σ unpack [α, x] = e<sup>1</sup> in e<sup>2</sup>

Γ e: τ e<sup>1</sup> Γ, x:τ <sup>I</sup> M: σ e<sup>2</sup> Γ ` let x = e in M: σ let x = e<sup>1</sup> in e<sup>2</sup>

Γ M<sup>1</sup>: σ<sup>1</sup> e<sup>1</sup> Γ, α/m:σ<sup>1</sup> M<sup>2</sup>: σ<sup>2</sup> e<sup>2</sup> Γ σ<sup>2</sup>: sig Γ let α/m = M<sup>1</sup> in (M<sup>2</sup>: σ2): σ<sup>2</sup> unpack [α, mˆ ] = e<sup>1</sup> in e<sup>2</sup>

Γ <sup>I</sup> M: σ e Γ <sup>I</sup> (M:> σ): σ e

Γ <sup>I</sup> M: σ<sup>1</sup> e Γ σ<sup>1</sup> ≤ σ<sup>2</sup> f σ<sup>2</sup> [α:k2. τ2] Γ `<sup>I</sup> M: σ<sup>2</sup> unpack [α, x] = e in pack [α, f[α]x] as ∃α:k2.τ<sup>2</sup>

Figure 7: The impure module translation

def = Γ, α:k def = Γ, α:k Γ, x:τ def = Γ, x:τ Γ, α/m:σ def <sup>=</sup> <sup>Γ</sup>, α:k, <sup>m</sup><sup>ˆ</sup>:<sup>τ</sup> where <sup>σ</sup> [α:k. τ ]

Figure 8: The context translation

This simply applies the functor's static portion to the argument's, and applies the functor's dynamic portion to the argument's static and dynamic portion. The impure case does the same thing, but first unpacks the functor from an existential package, and afterwards repacks the result.

Observe that, unless one were to do something obviously foolish, both of these rules are completely determined by the signature translation. The same is true for the translation of generative functors:

The static portion of a generative functor is trivial. The dynamic portion takes in the static and dynamic portions of the argument (again α:k<sup>1</sup> and ˆm: τ1)—again following the calling convention—and then computes an existential package (e) containing the static and dynamic portions of the result.

The generative functor application rule:

after extracting the functor's dynamic portion from a trivial existential package simply applies it to the argument's static and dynamic portion.

Again, these rules are determined by the signature translation. The same is true of the rules governing atomic modules and pairs. The translation of let binding is determined simply by the calling convention:

Since M<sup>1</sup> is impure, its translation is an existential package that must be unpacked to follow the calling convention. Once this is done, the right-hand-side is just passed through. Since σ<sup>2</sup> does not mention α, the type of e<sup>2</sup> also will not mention α.

The translation rule corresponding to the "forgetting" rule takes the statically determined static and dynamic components and rolls them into an existential package:

Interestingly, this leaves nothing for the sealing rule to do:

Γ <sup>I</sup> M: σ e Γ <sup>I</sup> (M:> σ): σ e

All the sealing rule does is require that M be translated impurely. This induces the forgetting rule to do the work of sealing M up as an existential package.

Retyping principles Two technically tricky points pertain to the module calculus's retyping principles. The first such principle is the subsumption rule:

Γ <sup>κ</sup> M: σ<sup>1</sup> Γ σ<sup>1</sup> ≤ σ<sup>2</sup> Γ `<sup>κ</sup> M: σ<sup>2</sup>

If σ<sup>1</sup> ≤ σ<sup>2</sup> and σ<sup>i</sup> [α:ki. τi], we can show that k<sup>1</sup> ≤ k2. If we had subtyping (and the full F<sup>≤</sup> subtyping rule [4]) we could also show that τ<sup>1</sup> ≤ τ2. But we do not have subtyping, and it is not the case that τ<sup>1</sup> ≡ τ2, since k <sup>0</sup> ≤ k does not imply ∀α:k.τ ≡ ∀α:k 0.τ. Consequently, the subsumption rule must apply a τ<sup>1</sup> → τ<sup>2</sup> coercion to the dynamic portion:

The coercion is computed by a judgement Γ ` σ<sup>1</sup> ≤ σ<sup>2</sup> f. It is essentially a large eta-expansion; it unrolls a term representing the dynamic portion of a module belonging to σ1, and then re-rolls it at the type corresponding to σ2. Details appear in Appendix A. In a practical implementation, this coercion can very frequently be inlined. Moreover, for fragments without higher-order functors (such as Standard ML), the coercion is always the identity.

The second retyping principle is the calculus's extensional typing rules, such as this rule for module pairs:

Γ <sup>P</sup> π1M: σ<sup>1</sup> Γ <sup>P</sup> π2M: σ<sup>2</sup> Γ `<sup>P</sup> M: σ<sup>1</sup> × σ<sup>2</sup>

The extensional typing rules say that a module belongs to a signature if uses of M produce appropriate results. For instance, M belongs to σ<sup>1</sup> × σ<sup>2</sup> if its left projection belongs to σ<sup>1</sup> and its right to σ2. These rules are never needed when M is an introduction form, but they allow one to ascribe stronger signatures to paths (i.e., series of eliminations starting from a variable) than the elimination rules permit [9]. For example, they allow one to give a path a translucent signature that refers to itself, a procedure whimsically called "selfification." Extensional typing is necessary for higher-order singleton kinds and signatures to work properly (recall parts 2 and 3 of Lemma 2.1).

However, the extensional typing rules cause a problem for the translation. Suppose M translated to [c, e] before using extensionality. The translation rule corresponding to the above rule would produce [hπ1c, π2ci,hπ1e, π2ei]. A similar thing would happen with the extensional typing rule for functors.

Unfortunately, this eta-expansion is not only inefficient, it is incorrect. In an eager operational semantics such as ours, e and hπ1e, π2ei have observably different behavior whenever e has effects.

The solution to this problem is to exploit the fact that the extensional typing rules are needed only for paths. Our translation omits the extensional typing rules, and replaces them with a single "selfifying" translation rule for variables:

Note the typing rule for variables gives m the signature σ, but the translation here gives it S(α: σ). Because of this discrepancy, the translation rules are not in perfect correspondence with the typing rules, but we can nevertheless show that all well-typed expressions translate and vice versa:

Theorem 3.1 If ` Γ ok then:

- Γ σ<sup>1</sup> ≤ σ<sup>2</sup> iff Γ σ<sup>1</sup> ≤ σ<sup>2</sup> f (for some f).
- Γ <sup>P</sup> M: σ iff Γ <sup>P</sup> M: σ [c, e] (for some c, e).

- Γ <sup>I</sup> M: σ iff Γ <sup>I</sup> M: σ e (for some e).
- Γ e: τ iff Γ e: τ e¯ (for some e¯).

We will need more machinery before we can show the translation's full correctness, but at this point we can show its static correctness:

Lemma 3.2 (Static correctness) If ` Γ ok then:

- If Γ σ: sig and σ [α:k. τ ] then Γ k: kind and Γ, α:k ` τ: T.
- If Γ σ<sup>1</sup> ≤ σ<sup>2</sup> f and σ<sup>i</sup> [α:ki. τi] then Γ f: ∀α:k1. τ<sup>1</sup> → τ2.
- If Γ <sup>P</sup> M: σ [c, e] and σ [α:k. τ ] then Γ c: k and Γ ` e: [c/α]τ.
- If Γ <sup>I</sup> M: σ e and σ [α:k. τ ] then Γ e: ∃α:k.τ.
- If Γ e: τ e¯ then Γ e¯: τ.

#### 4 Contextual Equivalence

We follow Crary [2] by defining contextual equivalence as the coarsest congruence that is consistent with execution,<sup>7</sup> and our definitions in this section are adapted from there. However, in contrast to Crary, our indexed relations include a relation on static values. This comes into play in the compatibility rule for polymorphic functions because of the value restriction. Fortunately, this affects the development almost not at all, and ultimately we will prove that the value relation can be ignored (Lemma 4.5).

Definition 4.1 An indexed dynamic relation R is a triple of relations: relations (R<sup>t</sup> and Rv) on terms and static values indexed by a context and type; and a relation (Rm) on modules indexed by a context, signature, and purity class; such that if ` Γ ok then:

- if Γ e R<sup>t</sup> e 0: τ then Γ e, e<sup>0</sup>: τ, and if Γ e R<sup>v</sup> e 0: τ then Γ e, e<sup>0</sup>: τ and e, e 0 are static values, and
- if Γ <sup>κ</sup> M R<sup>m</sup> M<sup>0</sup>: σ then Γ <sup>κ</sup> M, M<sup>0</sup>: σ, and
- if Γ <sup>P</sup> M R<sup>m</sup> M<sup>0</sup>: σ then Γ Fst(M) ≡ Fst(M<sup>0</sup>): Fst(σ).

### Definition 4.2 Suppose R is an indexed dynamic relation.

- R is compatible if it respects the rules in Appendix B. (Informally, R is compatible if R-related expressions can be built from R-related subexpressions.)
- R is substitutive if it respects substitution (of values where appropriate) and weakening for constructor, term, and module hypotheses. (For example, if Γ, α/m:σ, Γ <sup>0</sup> e R<sup>t</sup> e 0: τ and Γ <sup>P</sup> V: σ then Γ, [c/α]Γ<sup>0</sup> ` [Fst(V), V /α, m]e R<sup>t</sup> [Fst(V), V /α, m]e 0: [c/α]τ.)

<sup>7</sup>A more common definition would say that two expressions are contextually equivalent if they produce the same behavior when used to fill a hole in a program. Such a definition would be equivalent to ours, but in the setting of the module calculus, it is too unwieldy to use [2].

- R is a congruence if it is compatible, substitutive, reflexive, transitive, and symmetric.
- R is consistent if it preserves module termination. (That is, if `<sup>I</sup> M R<sup>m</sup> M<sup>0</sup>: σ and M halts then M<sup>0</sup> halts.)

Although we define consistency in terms of module termination, it is easy to show that a consistent, compatible relation also preserves term termination.

Definition 4.3 Contextually equivalence (written Γ e ≈ e 0: τ and Γ e ≈<sup>v</sup> e 0: τ and Γ `<sup>κ</sup> M ≈ M<sup>0</sup>: σ) is defined as the union of all consistent congruences.<sup>8</sup>

# 4.1 Properties of Contextual Equivalence

In proving dynamic correctness of phase separation, we will use several properties of contextual equivalence. One-anda-half of these can be proven directly (the first and the left-to-right direction of the second). But contextual equivalence, which effectively quantifies over all observing contexts that might use the comparees, is awkward to work with. For the rest of the properties, we require a tool to obtain leverage on contextual equivalence. The tool is logical equivalence, which defines the equivalence of comparees intrinsically, rather than extrinsically through their use in surrounding code.

Crary [2] defines logical equivalence for the module calculus and shows that it coincides with contextual equivalence. We use that development off-the-shelf, except that we need a notion of logical equivalence for values. We define it as simply the restriction of logical equivalence to static values.

The desired properties are all corollaries of the coincidence of logical and contextual equivalence. Conveniently, we can state them all without reference to logical equivalence, so we do so in the interest of brevity. Proofs are given in the companion Coq formalization.

First, contextual equivalence is adequate for the operational semantics:

Lemma 4.4 (Adequacy) If Γ e: τ and Γ e 7→ e 0 then Γ ` e ≈ e 0: τ, and similarly for modules.

# Proof Sketch

The compatible, reflexive, and transitive closure of evaluation is a consistent congruence, and therefore is contained in contextual equivalence.

Second, contextual equivalence for values is precisely the restriction of ordinary contextual equivalence to static values. Thus, henceforth we can ignore contextual equivalence for values.

Lemma 4.5 (Value equivalence) Γ sv ≈<sup>v</sup> sv<sup>0</sup>: τ if and only if Γ sv ≈ sv<sup>0</sup>: τ.

# Proof Sketch

Immediate from the definition of logical equivalence and its coincidence with contextual equivalence. Alternatively, for the left-to-right direction, observe that sv ≈ (Λ:1.sv)[?] ≈ (Λ:1.sv<sup>0</sup>)[?] ≈ sv<sup>0</sup>.

Third, we can show two expressions are contextually equivalent by considering their closed instances:

# Lemma 4.6 (Closed instances)

- If Γ e, e<sup>0</sup>: τ and for any substitution γ such that γ: Γ we have γ(e) ≈ γ(e 0): γ(τ), then Γ e ≈ e 0: τ.
- If Γ <sup>I</sup> M, M<sup>0</sup>: σ and for any substitution γ such that γ: Γ we have <sup>I</sup> γ(M) ≈ γ(M<sup>0</sup>): γ(σ), then Γ <sup>I</sup> M ≈ M<sup>0</sup>: σ.
- If Γ <sup>P</sup> M, M<sup>0</sup>: σ and Γ Fst(M) ≡ Fst(M<sup>0</sup>): Fst(σ) and for any substitution γ such that γ: Γ we have <sup>P</sup> γ(M) ≈ γ(M<sup>0</sup>): γ(σ), then Γ `<sup>I</sup> M ≈ M<sup>0</sup>: σ.

Fourth, when two closed expressions have the same termination behavior, we can assume they terminate when showing they are contextually equivalent:

# Lemma 4.7 (Conditional equivalence)

- If e, e<sup>0</sup>: τ and e↓⇔ e 0 ↓, then if e↓ implies e ≈ e 0: τ, then ` e ≈ e 0: τ.
- If <sup>I</sup> M, M<sup>0</sup>: τ and M↓⇔ M<sup>0</sup> ↓, then if M↓ implies <sup>I</sup> M ≈ M<sup>0</sup>: σ, then `<sup>I</sup> M ≈ M<sup>0</sup>: σ.
- If <sup>P</sup> M, M<sup>0</sup>: τ and Fst(M) ≡ Fst(M<sup>0</sup>): Fst(σ) and M↓⇔ M<sup>0</sup> ↓, then if M↓ implies <sup>P</sup> M ≈ M<sup>0</sup>: σ, then <sup>P</sup> M ≈ M<sup>0</sup>: σ.

Fifth, for closed terms and closed, pure modules, we have a variety of extensionality properties:

Lemma 4.8 (Extensionality) Suppose e, e<sup>0</sup>: τ and e↓⇔ e 0 ↓, then e ≈ e 0: τ provided:

- τ = unit, or
- τ = τ<sup>1</sup> →τ<sup>2</sup> and for every v: τ<sup>1</sup> we have e v ≈ e 0 v: τ2, or
- τ = ∀α:k.τ <sup>0</sup> and for every c: k we have e[c] ≈ e 0 [c]: [c/α]τ 0, or
- τ = τ<sup>1</sup> ×τ<sup>2</sup> and π1e ≈ π1e 0: τ<sup>1</sup> and π2e ≈ π2e 0: τ2.

Suppose <sup>P</sup> M, M<sup>0</sup>: σ and M↓⇔ M<sup>0</sup> ↓, then <sup>P</sup> M ≈ M<sup>0</sup>: σ provided:

- σ = 1, or
- <sup>σ</sup> <sup>=</sup> L <sup>k</sup> M and ` Fst(M) <sup>≡</sup> Fst(M<sup>0</sup>): k, or
- σ = h| τ |i and ` Ext M ≈ Ext M<sup>0</sup>: τ, or
- σ = Πgnα:σ1.σ<sup>2</sup> and for every <sup>P</sup> V: σ<sup>1</sup> we have <sup>I</sup> MV ≈ M0V: [Fst(V)/α]σ2, or
- σ = Πapα:σ1.σ<sup>2</sup> and Fst(M) ≡ Fst(M<sup>0</sup>): Fst(Πapα:σ1.σ2) and for every <sup>P</sup> V: σ<sup>1</sup> we have `<sup>P</sup> M · V ≈ M<sup>0</sup> · V: [Fst(V)/α]σ2, or
- σ = Σα:σ1.σ<sup>2</sup> and <sup>P</sup> π1M ≈ π1M<sup>0</sup>: σ<sup>1</sup> and <sup>P</sup> π2M ≈ π2M<sup>0</sup>: [π<sup>1</sup> Fst(M)/α]σ2.

<sup>8</sup> In the Coq formalization, contextual equivalence is given a different definition (the symmetrization of contextual approximation) which is then proved equivalent to this one.

|Snd 1 M |  |  |  |  |
|------------------------- | -------- | -------- | -------- | ----------------------------------------- |
|def | = let |  | = | M in ? |
|Snd L k M M |  |  |  |  |
|def | = let |  | = | M in ? |
|Snd h τ i M |  |  |  |  |
|def | = Ext | M |  |  |
|Snd Π gn α : σ 1 .σ 2 M |  |  |  |  |
|def | = let | m | = | M |
| | in | Λ α | : k | 1 .λx : τ 1 |
| |  |  | let | β/n = m ( Join σ 1 |
| |  |  |  | [ α, x ]) |
| |  |  | in | pack [ β, Snd σ 2 n ] as ∃ β : k 2 .τ 2 |
| | (where |  |  | σ 1 [ α : k 1 τ 1 ] |
| | and |  | σ 2 | [ β : k 2 τ 2 ]) |
|Snd Π ap α : σ 1 .σ 2 M |  |  |  |  |
|def | = let | m | = | M |
| | in | Λ α | : k | 1 .λx : τ 1 |
| |  |  | Snd | σ 2 |
| |  |  |  | ( m ( Join σ 1 |
| |  |  |  | [ α, x ])) |
| | (where |  |  | σ 1 [ α : k 1 τ 1 ]) |
|Snd Σ α : σ 1 .σ 2 M |  |  |  |  |
|def | = let | γ/m |  | = M |
| | in | h Snd |  | σ 1 |
| |  |  |  | ( π 1 m ) , Snd [ π 1 γ/α ] σ 2 |
| |  |  |  | ( π 2 m ) i |
|Join 1 [ c, e ] |  |  |  |  |
|def | = let |  | = | e in ? |
|Join L k M [ c, e ] |  |  |  |  |
|def | = let |  | = | e in L c M |
|Join h τ i [ c, e ] |  |  |  |  |
|def | = h | e i |  |  |
|Join Π gn α : σ 1 .σ 2 |  |  |  |  |
|[ c, e ] |  |  |  |  |
|def | = let | x | = | e |
| | in | λ |  |  |
| |  | gn | α/m | : σ 1 |
| |  |  | unpack | [ β, y ] = x [ α ]( Snd σ 1 m ) |
| |  |  | in | ( Join σ 2 |
| |  |  |  | [ β, y ] : σ 2 ) |
|Join Π ap α : σ 1 .σ 2 |  |  |  |  |
|[ c, e ] |  |  |  |  |
|def | = let | x | = | e |
| | in | λ |  |  |
| |  | ap | α/m | : σ 1 |
| |  |  | Join | σ 2 |
| |  |  |  | [ c α, x [ α ]( Snd σ 1 m )] |
|Join Σ α : σ 1 .σ 2 |  |  |  |  |
|[ c, e ] |  |  |  |  |
|def | = let | x | = | e |
| | in | h Join |  | σ 1 |
| |  |  |  | [ π 1 c, π 1 x ] , |
| |  | Join |  | [ π 1 c/α ] σ 2 |
| |  |  |  | [ π 2 c, π 2 x ] i |

Figure 9: Dynamic Phase Separation

# 5 Correctness

Our main aim is to show that every module is contextually equivalent to its translation, in an appropriate sense. But what is the appropriate sense? Since a module and its translation belong to different types, and indeed different syntactic classes, we require some way to relate them.

We do this using Snd<sup>σ</sup> and Joinσ, two (families of) functions that convert back-and-forth between modules and terms. Given a module, Snd computes its dynamic component, and given a module's static and dynamic component, Join recovers the original module.

The important fact about Snd<sup>σ</sup> and Join<sup>σ</sup> is that they are expressed within the language. They do not traverse the syntax of their arguments the way the translation does. Rather, they operate through the interface given by their arguments' signature/kind/type. We refer to Snd as dynamic phase separation since it does phase separation at run time instead of compile time.

The definitions of Snd and Join are given in Figure 9. The fact that they are definable within the language is interesting in its own right. It shows that modules are a definitional extension of the core language. In other words, modules confer no fundamental expressive power absent in the core. On the other hand, the fact that the definitions are rather baroque shows that modules are nevertheless a useful feature for a language to support.

Lemma 5.1 Suppose Γ ok and Γ σ: sig and σ [α:k. τ ]. Then:

- If Γ <sup>P</sup> M: σ then Γ SndσM: [Fst(M)/α]τ.
- If Γ c: k and Γ e: [c/α]τ then Γ <sup>P</sup> Joinσ[c, e]: σ and Γ c ≡ Fst(Joinσ[c, e]): k.

The main lemmas state that Snd and Join are inverses:

Lemma 5.2 (Join of Snd) If Γ <sup>P</sup> M: σ then Γ <sup>P</sup> M ≈ Joinσ[Fst(M), Sndσ(M)]: σ.

# Proof Sketch

The proof is by induction on the gross structure of σ (that is, considering all atoms (L <sup>k</sup> M or h| <sup>τ</sup> |i) to be identical for the purposes of the induction order).

We give one case, by way of example. Suppose σ = Π apα:σ1.σ2. By the closed instances lemma, we may assume without loss of generality that Γ is empty. (Note that σ's instances have the same gross structure as σ.) It is not hard to show that M↓⇔ Joinσ[Fst(M), Sndσ(M)]↓. Therefore, by the conditional equivalence lemma, we may assume without loss of generality that M is some value V. Let σ<sup>1</sup> [α:k1. τ1]. Then:

Joinσ[Fst(V), Sndσ(V)] = let f = let m = V in Λα:k1.λx:τ1. Snd<sup>σ</sup><sup>2</sup> (m · Join<sup>σ</sup><sup>1</sup> [α, x]) in λ apα/m:σ1. Join<sup>σ</sup><sup>2</sup> Fst(V) α, f[α] ≈ let f = Λα:k1.λx:τ1. Snd<sup>σ</sup><sup>2</sup> (V · Join<sup>σ</sup><sup>1</sup> [α, x]) in λ apα/m:σ1. Join<sup>σ</sup><sup>2</sup> Fst(V) α, f[α] ≈ λ apα/m:σ1. Join<sup>σ</sup><sup>2</sup> [Fst(V) α, (Λα:k1.λx:τ1. Snd<sup>σ</sup><sup>2</sup> (V · Join<sup>σ</sup><sup>1</sup> [α, x])) [α] (Snd<sup>σ</sup>1m)] ≈ λ apα/m:σ1. Join<sup>σ</sup><sup>2</sup> [Fst(V) α, Snd<sup>σ</sup><sup>2</sup> (V · Join<sup>σ</sup><sup>1</sup> [α, Snd<sup>σ</sup>1m])) = λ apα/m:σ1. Join<sup>σ</sup><sup>2</sup> [Fst(V · m), Snd<sup>σ</sup><sup>2</sup> (V · Join<sup>σ</sup><sup>1</sup> [Fst(m), Snd<sup>σ</sup>1m])) ≈ λ apα/m:σ1. Join<sup>σ</sup><sup>2</sup> [Fst(V · m), Snd<sup>σ</sup><sup>2</sup> (V · m)] ≈ λ apα/m:σ1. V · m ≈ V

The last step is by eta equivalence (which follows from extensionality, since V halts), and the previous two steps use the induction hypothesis.

Lemma 5.3 (Snd of Join) If Γ σ: sig and σ [α:k. τ ] and Γ c: k and Γ e: [c/α]τ then Γ e ≈ Sndσ(Joinσ[c, e]): [c/α]τ.

# Proof Sketch

By induction on the gross structure of σ. (But see Section 5.3.)

Next, we establish the correctness of the subsignature coercion judgement. It is equivalent to the function that converts a term to a module at the subsignature, and back to a term at the supersignature:

Lemma 5.4 If Γ σ<sup>1</sup> ≤ σ<sup>2</sup> f and σ<sup>i</sup> [α:ki. τi] then Γ f ≈ Λα:k1.λx:τ1.Snd<sup>σ</sup><sup>2</sup> (Join<sup>σ</sup><sup>1</sup> [α, x]): ∀α:k1. τ<sup>1</sup> → τ2.

# Proof Sketch

By induction on the derivation.

Recall that the variable translation case selfified its signature. To deal with this, we require one more lemma:

Lemma 5.5 Suppose Γ σ: sig and σ [α:k. τ ] and Γ c: k and Γ e: [c/α]τ. Then Γ <sup>P</sup> Joinσ[c, e] ≈ JoinS(c:σ)[c, e]: σ.

# Proof Sketch

We can show that if Γ <sup>P</sup> M, M<sup>0</sup>: σ and Γ Fst(M) ≡ Fst(M<sup>0</sup>): Fst(σ) and if M and M<sup>0</sup> differ only in type annotations, then Γ `<sup>P</sup> M ≈ M<sup>0</sup>: σ.

Let S(c: σ) [α:k 0. τ <sup>0</sup> ]. Then k <sup>0</sup> = S(c: k) and we can show that Γ, α:k <sup>0</sup> τ ≡ τ 0: T, so Γ e: [c/α]τ 0. The first two conditions hold using Lemma 5.1 and S(c: σ) ≤ σ. The third is by inspection.

To mediate the difference between the original context Γ and its translation Γ, we define the substitution Snd<sup>Γ</sup> to map ˆm to Sndσm for every α/m:σ ∈ Γ. Note that Snd<sup>σ</sup> does not touch constructor variables, so we need not apply it to any kinds, constructors, or signatures.

Lemma 5.6 If Γ ok then Γ Snd<sup>Γ</sup>: Γ.

With this, we can finally establish our main theorem:

### Theorem 5.7 (Dynamic correctness)

- If Γ <sup>P</sup> M: σ [c, e] then Γ M ≈ Joinσ[c, SndΓ(e)]: σ.
- If Γ <sup>I</sup> M: σ e then Γ <sup>I</sup> M ≈ unpack [α, x] = SndΓ(e)in (Joinσ[α, x]: σ): σ.
- If Γ e: τ e¯ then Γ e ≈ SndΓ(¯e): τ.

# Proof Sketch

The proof is by induction on the translation derivation. We give a few cases by way of example.

Case:

Then JoinS(α:σ)[α, SndΓ(ˆm)] = JoinS(α:σ)[Fst(m), Sndσ(m)] ≈ Joinσ[Fst(m), Sndσ(m)] ≈ m, the second and third steps using Lemmas 5.5 and 5.2.

Case:

Γ σ<sup>1</sup>: sig Γ, α/m:σ<sup>1</sup> <sup>P</sup> M: σ<sup>2</sup> [c, e] σ<sup>1</sup> [α:k1.τ1] Γ `<sup>P</sup> λ apα/m:σ1.M: Πapα:σ1.σ<sup>2</sup> [λα:k1.c, Λα:k1.λmˆ:τ1.e]

Then:

JoinΠapα:σ1.σ<sup>2</sup> [λα:k1.c, SndΓ(Λα:k1.λmˆ:τ1.e)] = JoinΠapα:σ1.σ<sup>2</sup> [λα:k1.c, Λα:k1.λmˆ:τ1.SndΓ(e)] ≈ λ apα/m:σ1.Join<sup>σ</sup><sup>2</sup> (λα:k1.c)α, (Λα:k1.λmˆ:τ1.SndΓ(e))[α] ≈ λ apα/m:σ1.Join<sup>σ</sup><sup>2</sup> [c, [Snd<sup>σ</sup>1m/mˆ ]SndΓ(e)] = λ apα/m:σ1.Join<sup>σ</sup><sup>2</sup> [c, SndΓ,α/m:σ<sup>1</sup> (e)] ≈ λ apα/m:σ1.M

Case:

Then (unpack [β, x] = SndΓ(pack [c, e] as ∃α:k.τ)in Joinσ[β, x]) = (unpack [β, x] = pack [c, SndΓ(e)] as ∃α:k.τ in Joinσ[β, x]) ≈ Joinσ[c, SndΓ(e)] ≈ M.

Case:

Then Join<sup>σ</sup><sup>2</sup> [c, SndΓ(f [c] e)] = Join<sup>σ</sup><sup>2</sup> [c, f [c] (SndΓ(e))] ≈ Join<sup>σ</sup><sup>2</sup> [c, Snd<sup>σ</sup><sup>2</sup> (Join<sup>σ</sup><sup>1</sup> [c,

SndΓ(e)])] ≈ Join<sup>σ</sup><sup>1</sup> [c, SndΓ(e)] ≈ M. The first step is because f is closed with respect to term variables; the second and third are by Lemmas 5.4 and 5.2.

Observe that for closed terms, the theorem degenerates to if e: τ e¯ then e ≈ e¯: τ.

# 5.1 Abstraction Preservation

It remains to collect some corollaries. We can prove a converse of dynamic correctness:

Corollary 5.8 Let Join<sup>σ</sup> be the substitution that maps m to Joinσ[α, mˆ ] for every α/m:σ ∈ Γ. (So Γ Join<sup>Γ</sup>: Γ whenever Γ ok.) Suppose ` Γ ok. Then:

- If Γ <sup>P</sup> M: σ [c, e] and σ [α:k. τ ] then Γ e ≈ Sndσ(JoinΓ(M)): [c/α]τ.
- If Γ <sup>I</sup> M: σ e and σ [α:k. τ ] then Γ e ≈ let α/m = JoinΓ(M) in pack [α, Sndσm] as ∃α:k.τ: ∃α:k.τ.
- If Γ e: τ e¯ then Γ e¯ ≈ JoinΓ(e): τ.

# Proof Sketch

Consider the first clause. Using compatibility, we can show that contextual equivalence respects functionality, so JoinΓ(SndΓ(e)) ≈ e by Lemma 5.3. By dynamic correctness, M ≈ Joinσ[c, SndΓ(e)]. By substitutivity, JoinΓ(M) ≈ JoinΓ(Joinσ[c, SndΓ(e)]) = Joinσ[c, JoinΓ(SndΓ(e))] ≈ Joinσ[c, e]. Then, again by Lemma 5.3, Sndσ(JoinΓ(M)) ≈ Sndσ(Joinσ[c, e]) ≈ e.

The second clause is similar but messier. The third clause is similar but simpler.

Abstraction preservation follows directly from this. If one neglects (for the moment) the difference between the source and target language, this is the hard direction of full abstraction:

Corollary 5.9 (Abstraction preservation) Suppose ` Γ ok. Then:

- If Γ <sup>P</sup> M<sup>1</sup> ≈ M<sup>2</sup>: σ and σ [α:k. τ ] and Γ <sup>P</sup> M<sup>i</sup>: σ [ci, ei] then Γ ` e<sup>1</sup> ≈ e<sup>2</sup>: [c1/α]τ.
- If Γ <sup>I</sup> M<sup>1</sup> ≈ M<sup>2</sup>: σ and σ [α:k. τ ] and Γ <sup>I</sup> M<sup>i</sup>: σ e<sup>i</sup> then Γ ` e<sup>1</sup> ≈ e<sup>2</sup>: ∃α:k.τ.
- If Γ e<sup>1</sup> ≈ e<sup>2</sup>: τ and Γ e<sup>i</sup>: τ e¯<sup>i</sup> then Γ ` e¯<sup>1</sup> ≈ e¯<sup>2</sup>: τ.

#### Proof Sketch

We give the first clause; the others are similar. Suppose Γ <sup>P</sup> M<sup>1</sup> ≈ M<sup>2</sup>: σ. By substitutivity of contextual equivalence, Γ JoinΓ(M1) ≈ JoinΓ(M2): σ. Therefore e<sup>1</sup> ≈ Sndσ(JoinΓ(M1)) ≈ Sndσ(JoinΓ(M2)) ≈ e<sup>2</sup> by Corollary 5.8 and compatibility.

The coherence of the translation is an immediate consequence of this, using reflexivity for the antecedent:

Corollary 5.10 (Coherence) Suppose ` Γ ok. Then:

- If Γ <sup>P</sup> M: σ and σ [α:k. τ ] and Γ <sup>P</sup> M: σ [ci, ei] (for i = 1, 2) then Γ ` e<sup>1</sup> ≈ e<sup>2</sup>: [c1/α]τ.
- If Γ <sup>I</sup> M: σ and σ [α:k. τ ] and Γ <sup>I</sup> M: σ e<sup>i</sup> (for i = 1, 2) then Γ ` e<sup>1</sup> ≈ e<sup>2</sup>: ∃α:k.τ.
- If Γ e: τ and Γ e: τ e¯<sup>i</sup> (for i = 1, 2) then Γ ` e¯<sup>1</sup> ≈ e¯<sup>2</sup>: τ.

#### 5.2 Full Abstraction

Full abstraction states that expressions are sourceequivalent (i.e., equivalent in the source language) exactly when their translations are target-equivalent. Abstraction preservation gives us most of this: It says that that translations of source-equivalent expressions are source-equivalent. Since the target language is a subset of the source, every observing context in the target is also one in the source, and consequently source-equivalence implies target-equivalence. Thus, abstraction preservation gives us half of full abstraction.

It remains to show that expressions are source-equivalent when their translations are target-equivalent. Dynamic correctness says that source expressions are source-equivalent to their translations, so the result follows by transitivity, provided target-equivalent expressions are sourceequivalent:

Lemma 5.11 Let Γ tgt e ≈ e 0: τ be contextual equivalence for the target, defined analogously to Section 4, but using only the features of the target language. Then Γ tgt e ≈ e 0: τ implies Γ ` e ≈ e 0: τ.

### Proof Sketch

As developed in Crary [2], contextual equivalence coincides with logical equivalence, which is biorthogonally closed [26]. Dynamic correctness tells us that every closed source term has an equivalent target term. Thus, in biorthogonal closure we may assume without loss of generality that the continuations are target terms. It follows that biorthogonally closed sets are closed under target-equivalence.

Corollary 5.12 (Full abstraction) Suppose ` Γ ok. Then:

- If σ [α:k. τ ] and Γ <sup>P</sup> M<sup>i</sup>: σ [ci, ei] then Γ <sup>P</sup> M<sup>1</sup> ≈ M<sup>2</sup>: σ exactly when both Γ c<sup>1</sup> ≡ c<sup>2</sup>: k and Γ tgt e<sup>1</sup> ≈ e<sup>2</sup>: [c1/α]τ.
- If σ [α:k. τ ] and Γ <sup>I</sup> M<sup>i</sup>: σ e<sup>i</sup> then Γ <sup>I</sup> M<sup>1</sup> ≈ M<sup>2</sup>: σ exactly when Γ `tgt e<sup>1</sup> ≈ e<sup>2</sup>: ∃α:k.τ.
- If Γ e<sup>i</sup>: τ e 0 i then Γ e<sup>1</sup> ≈ e<sup>2</sup>: τ exactly when Γ `tgt e 0 <sup>1</sup> ≈ e 0 <sup>2</sup>: τ.

#### 5.3 The Role of the Value Restriction

Observe that Join ◦ Snd and Snd ◦ Join have the effect of eta-expanding their arguments (after evaluating them to values). For example, suppose F is an applicative functor value. As we saw in the proof sketch of Lemma 5.2, Join[Fst(F), Snd(F)] is equivalent, after some simplification, to λm. F · m. The latter is equivalent to F because F is a value.

On the other hand, suppose f is a value, and suppose c and f have an appropriate kind/type to be the static and dynamic components of an applicative functor. Note that f's type must have the form ∀α:k. τ→τ 0. Then Snd(Join[c, f]) is equivalent, after some simplification, to Λα.λx.f[α]x. This is equivalent to f, but only because of the value restriction. Since f is a value, it is certainly equivalent to Λα.f[α], but f[α] is not a value, so without a value restriction, it would not in general be equivalent to λx.f[α]x. The value restriction ensures that f[α] will halt, which is good enough to conclude f[α] ≈ λx.f[α]x. Thus Lemma 5.3 relies crucially on the value restriction.

We can work backward from this observation to obtain a counterexample of full abstraction if the value restriction were omitted. Suppose m is a variable with an applicativefunctor signature. Since m is a value, m ≈ λ apα/n. m·n. But m translates to dynamic component ˆm, whereas λ apα/n. m · n translates to dynamic component Λα.λn. ˆ mˆ [α]ˆn. These translations can be distinguished by the observing context let mˆ = Λα.⊥ in let = [ ] c in? (where c is any constructor of appropriate kind).

This issue with full abstraction does not rely on applicative functors. A similar example can be constructed using a generative functor.

(Both Shan [31] and Rossberg, et al. [27] produce a generally similar translation to ours, but neither of their target languages has a value restriction on polymorphic functions.<sup>9</sup> Consequently neither of them preserves abstraction, so long as their target language is capable of expressing the eager let used in the observing context above.)

Note that this issue does not rule out having a second form of polymorphic function without a value restriction, were one desired. The important thing is that the target language have a form of function able to take in both a constructor and a value at once, without any intervening effects.

One could even have a value restriction in the target and not the source, although having different source and target languages would complicate the development. We also conjecture that the translation would be fully abstract even without a value restriction if it were to translate variables to their full eta-long form. But such a translation is undesirable for efficiency reasons, so we have not explored it carefully.

# 6 Definitional Extensions

The alignment of abstraction with effects in our module calculus suggests a natural treatment of first-class modules [29, 5] as a definitional extension. Suppose we have a new term form mdσ(M), which stands for an encapsulated module and has type md(σ). And suppose such an

<sup>9</sup>Note that it is the target language at issue here, not any value restriction that might exist in the source language. Both Shan and Rossberg et al. target ordinary F<sup>ω</sup> (extended with extra types), which has no value restriction.

encapsulated module can be made back into a module using tmσ(e).

Although this formulation offers less expressive power than systems that allow the propagation of type information through first-class code [9], it supports most important applications of first-class modules such as run-time selection of implementations of abstract data types.

The critical point in the static semantics of first-class modules is that the tm form must be impure. Since the module depends on arbitrary code, it is impossible to determine its type components statically:

Γ <sup>I</sup> M: σ Γ mdσ(M): md(σ) Γ e: md(σ) Γ <sup>I</sup> tmσ(e): σ

Two questions present themselves regarding these firstclass modules: Does the language still respect the phase distinction, and does the extension leave intact the language's existing abstraction properties? At first glance, neither seems certain. The phase distinction depends on the fact that types cannot depend on terms, but first-class modules appear, at least superficially, to provide a way for that to happen. And, first-class modules provide a wealth of new observing contexts that might be used to distinguish between previously indistinguishable modules.

But the machinery developed here allows us easily to answer both questions in the affirmative. We show that we can faithfully define first-class modules as a definitional extension in the original language. This shows that the extension respects the phase distinction, since the original did. It also shows that the extension preserves abstraction, because any observing context in the extended language can be turned into an equivalent observing context in the original language. Consequently, any modules that are indistinguishable in the original language remain so with the extension.

Suppose σ [α:k. τ ]. We define:

md(σ) def = ∃α:k.τ mdσ(M) def <sup>=</sup> let α/m <sup>=</sup> <sup>M</sup> in pack [α, Sndσm] as ∃α:k.τ tmσ(e) def <sup>=</sup> unpack [α, x] = <sup>e</sup> in (Joinσ[α, x]: <sup>σ</sup>)

We can easily show that tmσ(mdσ(N)) ≈ N, thereby simulating the extension's operational semantics.

Another useful extension is an operation purifyS(c:σ) (M) that takes an impure but transparent module and makes it pure [33, 5]. This expresses the fact that in a module whose exported type components are fully specified, any typing effects are benign. This is useful for using generative functors within the implementation of an applicative functor.

Γ c: Fst(σ) Γ <sup>I</sup> M: S(c: σ) Γ `<sup>P</sup> purifyS(c:σ) (M): S(c: σ)

We show that purify is a definitional extension by defining purifyS(c:σ) (M) as:

JoinS(c:σ)[c, let m = M in SndS(c:σ)m]

This trick has two parts: First, by converting M to a term, we disappear any typing effects it might have. Then, since M is transparent, its static component (c) is known without referring to M, so we are able to convert back to a pure module using Join.

When M is a value (and hence pure), we can easily show that purifyS(c:σ) (M) ≈ M, thereby simulating the extension's operational semantics.

Although these definitions are satisfactory from a theoretical standpoint, in practice it may be preferable to translate the extensions directly:

Γ <sup>I</sup> M: σ e Γ mdσ(M): md(σ) e Γ e: md(σ) e¯ Γ <sup>I</sup> tmσ(e): σ e¯

Observe that first-class modules are actually trivial when viewed through the lens of phase separation. On the other hand, the type translation is no longer the identity (md(σ) becomes ∃α:k.τ), which adds a bit of overhead to the compiler.

Γ c: Fst(σ) Γ <sup>I</sup> M: S(c: σ) e Γ `<sup>P</sup> purifyS(c:σ) (M): S(c: σ) [c, unpack [α, x] = e in x]

This translation works because in the unpack, α has the kind S(c: Fst(σ)), so α ≡ c: Fst(σ), so x's type can be expressed without reference to α.

#### 7 Formalization

All the results in this paper are formalized in Coq (version 8.4). We implemented binding using deBruijn indices and explicit substitutions. To make reasoning about relations cleaner, we used the axioms of functional and propositional extensionality.

The full development is 89k lines. (These counts include comments and whitespace.) Of those, 70k are preliminaries or the development of logical equivalence, which are borrowed from Crary [2], with some modest editing, mostly to deal with the value restriction. The all-new material—the translation and its correctness proof—account for 19k lines.

We remarked above that the addition of value restriction had almost no effect on the development of logical equivalence. As a coarse measure of that, updating the logicalequivalence Coq proofs to account for the value restriction took less than one day.

The numerous typing premises involved in showing contextual equivalences rapidly become unmanageable. To manage this, we defined reductive contextual equivalence. We say that Γ e ⇒ e 0 if for any τ, Γ e: τ implies Γ e ≈ e 0: τ (and similarly for modules). One example of how this simplifies proofs is we can say that Γ e 7→ e 0 implies Γ ` e ⇒ e 0, eliminating the typing premise from Lemma 4.4.

#### 8 Additional Discussion of Related Work

As discussed above, the closest work to ours is Shan [31] and Rossberg, et al. [27]. The most significant difference from ours is they do not establish dynamic correctness, but there is a stylistic difference as well. Although they are not fundamentally different from the pattern of the Harper, et al. [12], their translations do not explicitly separate modules into type and term components. Instead, they realize the phase distinction by separating all the opaque type components into a prefix on which the module depends. (Shao [33] calls this prefix the module's flexroot.) In ordinary modules, the prefix is existentially quantified, and in functors it is lambda abstracted. In essence, the module is automatically

rewritten to replace sharing-by-fibration with sharing-byparameterization [14]. An advantage of their presentation is it allows one to dispense with any machinery to control the propagation of type information (such as the singleton kinds we use here).

These two differences may be connected. Our proof technique relies crucially on separating modules into type constructors and terms. It is not clear how to define something like Snd and Join without doing so.

Shan also addresses weak sealing [6], which we do not. He does so by generating a two-stage program. The first stage resolves static effects (in the sense of Dreyer, et al. [6]) that arise from weak sealing, resulting in a program without weak sealing. The second stage then executes that program, resolving the remaining (dynamic) effects as it goes. Rossberg, et al. do something similar. This approach is very plausible, but we do not follow it here, because the equational theory of weak sealing is still not well understood. Specifically, we do not yet know how to reconcile logical equivalence with weak sealing, so we cannot even begin to prove full abstraction.

Elsman, et al. [7, 8] suggest a radically different approach called static interpretation. It resolves all module-level computation (e.g., functor application) at compile time. This sacrifices separate compilation (functors cannot be compiled separately from their arguments), but it makes it easy to optimize across module boundaries. In essence, static interpretation weakens the phase distinction by assigning modulelevel computation to the compile-time phase rather than the run-time phase. Their languages do not include sealing, but do include generative datatypes, which offer a means of abstraction. As with other prior work, they do not show dynamic correctness.

# 9 Conclusion

Our correctness and full abstraction results show that the phase-separation algorithm is canonical, from a theoretical standpoint anyway. Any other algorithm that is dynamically correct (in our sense) is necessarily equivalent to ours.

Nevertheless, there is room for improvement in the language itself. Our module calculus supports only a fragment of the features needed for Standard ML [16]. Many of the missing features are easily supported, but some particularly those involving references, exceptions, or other forms of effects—are more difficult. Another important feature for languages that emphasize applicative functors (such as OCaml [20]) is weak sealing [6]. Still another direction is more powerful module features such as recursive modules [3, 30, 5].

In each of these cases, we anticipate that the general proof strategy employed here should work. However, a precondition for progress in any of these domains is a working account of logical equivalence. These are important avenues for future work.

# A The Term and Subsignature Translations

Γ e: τ e¯ Γ(x) = τ Γ x: τ x Γ `?: unit?

Γ τ<sup>1</sup>: T Γ, x:τ<sup>1</sup> e: τ<sup>2</sup> e¯ Γ ` λx:τ1.e: τ<sup>1</sup> → τ<sup>2</sup> λx:τ1.e¯

Γ e<sup>1</sup>: τ → τ <sup>0</sup> e¯<sup>1</sup> Γ e<sup>2</sup>: τ e¯<sup>2</sup> Γ ` e1e<sup>2</sup>: τ <sup>0</sup> e¯1e¯<sup>2</sup>

Γ e<sup>1</sup>: τ<sup>1</sup> e¯<sup>1</sup> Γ e<sup>2</sup>: τ<sup>2</sup> e¯<sup>2</sup> Γ ` he1, e2i: τ<sup>1</sup> × τ<sup>2</sup> he¯1, e¯2i

Γ e: τ<sup>1</sup> × τ<sup>2</sup> e¯ Γ π1e: τ<sup>1</sup> π1e¯ Γ e: τ<sup>1</sup> × τ<sup>2</sup> e¯ Γ π2e: τ<sup>2</sup> π2e¯

Γ k: kind Γ, α:k sv: τ e¯ Γ ` Λα:k.sv: ∀α:k.τ Λα:k.e¯

Γ e: ∀α:k.τ e¯ Γ c: k Γ ` e[c]: [c/α]τ e¯[c]

Γ c: k Γ e: [c/α]τ e¯ Γ, α:k τ: T Γ pack [c, e] as ∃α:k.τ: ∃α:k.τ pack [c, e¯] as ∃α:k.τ

Γ e<sup>1</sup>: ∃α:k.τ e¯<sup>1</sup> Γ, α:k, x:τ e<sup>2</sup>: τ <sup>0</sup> e¯<sup>2</sup> Γ τ 0: T Γ unpack [α, x] = e<sup>1</sup> in e<sup>2</sup>: τ <sup>0</sup> unpack [α, x] = ¯e<sup>1</sup> in e¯<sup>2</sup>

Γ e: (unit → τ) → τ e¯ Γ fix<sup>τ</sup> e: τ fix<sup>τ</sup> e¯

Γ e<sup>1</sup>: τ<sup>1</sup> e¯<sup>1</sup> Γ, x:τ<sup>1</sup> e<sup>2</sup>: τ<sup>2</sup> e¯<sup>2</sup> Γ ` let x = e<sup>1</sup> in e<sup>2</sup>: τ<sup>2</sup> let x = ¯e<sup>1</sup> in e¯<sup>2</sup>

Γ <sup>I</sup> M: σ e<sup>1</sup> Γ, α/m:σ e: τ e<sup>2</sup> Γ τ: T Γ let α/m = M in e: τ unpack [α, mˆ ] = e<sup>1</sup> in e<sup>2</sup>

Γ <sup>I</sup> M: h| τ |i e Γ Ext M: τ unpack [, x] = e in x

Γ e: τ e¯ Γ τ ≡ τ 0: T Γ ` e: τ <sup>0</sup> e¯

Γ ` σ ≤ σ <sup>0</sup> f

Γ σ ≡ σ 0: sig σ [α:k. τ ] Γ σ ≤ σ <sup>0</sup> Λα:k.λx:τ.x

Γ σ ≤ σ <sup>0</sup> f Γ σ <sup>0</sup> ≤ σ <sup>00</sup> f <sup>0</sup> σ [α:k. τ ] Γ ` σ ≤ σ <sup>00</sup> Λα:k.λx:τ. f<sup>0</sup> [α] (f [α] x)

Γ k ≤ k 0 <sup>Γ</sup> L <sup>k</sup> M <sup>≤</sup> L <sup>k</sup> 0 M <sup>Λ</sup>α:k.λx:unit.x

Γ ` σ 0

<sup>1</sup> ≤ σ<sup>1</sup> f<sup>1</sup> Γ, α: Fst(σ

0

<sup>1</sup>) ` σ<sup>2</sup> ≤ σ

Γ, α: Fst(σ1) ` σ<sup>2</sup>: sig

σ<sup>1</sup> [α:k1.τ1] σ

0 <sup>1</sup> [α:k 0 <sup>1</sup>.τ <sup>0</sup>

σ<sup>2</sup> [β:k2.τ2] σ

0 <sup>2</sup> [β:k 0 <sup>2</sup>.τ <sup>0</sup> 2]

Γ ` Π

gnα:σ1.σ<sup>2</sup> ≤ Π

gnα:σ 0 1.σ<sup>0</sup> 2

Λ:1.λf:(∀α:k1.τ<sup>1</sup> → ∃β:k2.τ2).

Λα:k 0 <sup>1</sup>.λx:τ 0 1.

> unpack [β, y] = f [α] (f<sup>1</sup> [α] x) in pack [β, f<sup>2</sup> [β] y] as ∃β:k

0 <sup>2</sup>.τ <sup>0</sup> 2

Γ ` σ 0

<sup>1</sup> ≤ σ<sup>1</sup> f<sup>1</sup> Γ, α: Fst(σ

0

<sup>1</sup>) ` σ<sup>2</sup> ≤ σ

Γ, α: Fst(σ1) ` σ<sup>2</sup>: sig

σ<sup>1</sup> [α:k1.τ1] σ

0 <sup>1</sup> [α:k 0 <sup>1</sup>.τ <sup>0</sup>

<sup>1</sup>] σ<sup>2</sup> [β:k2.τ2]

Γ ` Π

apα:σ1.σ<sup>2</sup> ≤ Π

apα:σ 0 1.σ<sup>0</sup> Λγ:(Πα:k1.k2).λf:(∀α:k1.τ<sup>1</sup> → [γα/β]τ2).

Λα:k 0 <sup>1</sup>.λx:τ 0 1. f<sup>2</sup> [γα] (f [α] (f<sup>1</sup> [α]x))

Γ ` σ<sup>1</sup> ≤ σ

0

<sup>1</sup> f<sup>1</sup> Γ, α: Fst(σ1) ` σ<sup>2</sup> ≤ σ

Γ, α: Fst(σ

0 <sup>1</sup>) ` σ 0 <sup>2</sup>: sig

σ<sup>1</sup> [α:k1. τ1] σ<sup>2</sup> [β:k2. τ2]

Γ ` Σα:σ1.σ<sup>2</sup> ≤ Σα:σ

0 1.σ<sup>0</sup> 2

Λγ:(Σα:k1.k2).λx:([π1γ/α]τ<sup>1</sup> × [π1γ, π2γ/α, β]τ2). hf<sup>1</sup> [π1γ] (π1x),([π1γ/α]f2) [π2γ] (π2x)i

# B Compatibility

Γ τ<sup>1</sup>: T Γ, x:τ<sup>1</sup> e R<sup>t</sup> e

Γ ` λx:τ1.e R<sup>t</sup> λx:τ1.e<sup>0</sup>

0 <sup>1</sup>: τ → τ

<sup>0</sup> Γ ` e<sup>2</sup> R<sup>t</sup> e

0 <sup>2</sup>: τ

Γ ` e1e<sup>2</sup> R<sup>t</sup> e

0 1e 0 <sup>2</sup>: τ 0

0

<sup>1</sup>: τ<sup>1</sup> Γ ` e<sup>2</sup> R<sup>t</sup> e

Γ ` he1, e2i R<sup>t</sup> he

0 1, e<sup>0</sup>

<sup>2</sup>i: τ<sup>1</sup> × τ<sup>2</sup>

0

Γ ` π1e R<sup>t</sup> π1e

0: τ<sup>1</sup> Γ ` e R<sup>t</sup> e

0

Γ ` π2e R<sup>t</sup> π2e

Γ k: kind Γ, α:k; Γ e R<sup>v</sup> e

0: τ

Γ ` Λα:k.e R<sup>t</sup> Λα:k.e<sup>0</sup>

: ∀α:k.τ

0

: ∀α:k.τ Γ ` c: k

Γ ` e[c] R<sup>t</sup> e

0

[c]: [c/α]τ

Γ c: k Γ e R<sup>t</sup> e

0

: [c/α]τ Γ, α:k ` τ: T

Γ ` pack [c, e] as ∃α:k.τ R<sup>t</sup> pack [c, e<sup>0</sup>

] as ∃α:k.τ: ∃α:k.τ

0

<sup>1</sup>: ∃α:k.τ Γ, α:k, x:τ ` e<sup>2</sup> R<sup>t</sup> e

0 <sup>2</sup>: τ <sup>0</sup> Γ ` τ 0: T

Γ ` unpack [α, x] = e<sup>1</sup> in e<sup>2</sup> R<sup>t</sup> unpack [α, x] = e

0 <sup>1</sup> in e 0 <sup>2</sup>: τ 0

Γ τ: T Γ e R<sup>t</sup> e

0

: (unit → τ) → τ

Γ ` fix<sup>τ</sup> e R<sup>t</sup> fix<sup>τ</sup> e

0: τ

0

<sup>1</sup>: τ<sup>1</sup> Γ, x:τ<sup>1</sup> ` e<sup>2</sup> R<sup>t</sup> e

Γ ` let x = e<sup>1</sup> in e<sup>2</sup> R<sup>t</sup> let x = e

0 <sup>1</sup> in e 0 <sup>2</sup>: τ<sup>2</sup>

Γ ` M R<sup>m</sup> M<sup>0</sup>

: σ Γ, α/m:σ ` e R<sup>t</sup> e

0

: τ Γ ` τ: T

Γ ` let α/m = M in e R<sup>t</sup> let α/m = M<sup>0</sup>

in e 0: τ Γ ` M R<sup>m</sup> M<sup>0</sup>

: h| τ |i

Γ ` Ext M R<sup>t</sup> Ext M<sup>0</sup>

: τ

0

: τ Γ ` τ ≡ τ

0: T

0: τ 0

Γ τ<sup>1</sup>: T Γ, x:τ<sup>1</sup> e R<sup>t</sup> e

Γ ` λx:τ1.e R<sup>v</sup> λx:τ1.e<sup>0</sup>

Γ ` e<sup>1</sup> R<sup>v</sup> e

0

<sup>1</sup>: τ<sup>1</sup> Γ ` e<sup>2</sup> R<sup>v</sup> e

Γ ` he1, e2i R<sup>v</sup> he

0 1, e<sup>0</sup>

<sup>2</sup>i: τ<sup>1</sup> × τ<sup>2</sup>

Γ k: kind Γ, α:k; Γ e R<sup>v</sup> e

0: τ

Γ ` Λα:k.e R<sup>v</sup> Λα:k.e<sup>0</sup>

: ∀α:k.τ

Γ c: k Γ e R<sup>v</sup> e

0

: [c/α]τ Γ, α:k ` τ: T

Γ ` pack [c, e] as ∃α:k.τ R<sup>v</sup> pack [c, e<sup>0</sup>

] as ∃α:k.τ: ∃α:k.τ

Γ ` e R<sup>v</sup> e

0

: τ Γ ` τ ≡ τ

0: T

Γ ` e R<sup>v</sup> e

0: τ 0

Γ c: k <sup>Γ</sup><sup>P</sup> L <sup>c</sup> M <sup>R</sup><sup>m</sup> L <sup>c</sup> M: L <sup>k</sup> M Γ ` e R<sup>t</sup> e

0: τ

Γ `<sup>P</sup> h| e |i R<sup>m</sup> h| e

0 |i: h| τ |i

Γ σ<sup>1</sup>: sig Γ, α/m:σ<sup>1</sup> <sup>I</sup> M R<sup>m</sup> M<sup>0</sup>

: σ<sup>2</sup>

Γ `<sup>P</sup> λ

gnα/m:σ1.M R<sup>m</sup> λ

gnα/m:σ1.M<sup>0</sup>

: Πgnα:σ1.σ<sup>2</sup>

Γ `<sup>I</sup> M<sup>1</sup> R<sup>m</sup> M<sup>0</sup>

<sup>1</sup>: Πgnα:σ.σ<sup>0</sup>

Γ `<sup>P</sup> M<sup>2</sup> R<sup>m</sup> M<sup>0</sup>

<sup>2</sup>: σ Γ ` Fst(M2) c<sup>2</sup>

Γ `<sup>I</sup> M1M<sup>2</sup> R<sup>m</sup> M<sup>0</sup>

1M<sup>0</sup>

<sup>2</sup>: [c2/α]σ

0

Γ σ<sup>1</sup>: sig Γ, α/m:σ<sup>1</sup> <sup>P</sup> M R<sup>m</sup> M<sup>0</sup>

: σ<sup>2</sup>

Γ `<sup>P</sup> λ

apα/m:σ1.M R<sup>m</sup> λ

apα/m:σ1.M<sup>0</sup>

: Πapα:σ1.σ<sup>2</sup>

Γ `<sup>κ</sup> M<sup>1</sup> R<sup>m</sup> M<sup>0</sup>

<sup>1</sup>: Πapα:σ.σ<sup>0</sup>

Γ `<sup>P</sup> M<sup>2</sup> R<sup>m</sup> M<sup>0</sup>

<sup>2</sup>: σ Γ ` Fst(M2) c<sup>2</sup>

Γ `<sup>κ</sup> M<sup>1</sup> · M<sup>2</sup> R<sup>m</sup> M<sup>0</sup>

<sup>1</sup> · M<sup>0</sup>

<sup>2</sup>: [c2/α]σ

0

Γ `<sup>κ</sup> M<sup>1</sup> R<sup>m</sup> M<sup>0</sup>

<sup>1</sup>: σ<sup>1</sup> Γ `<sup>κ</sup> M<sup>2</sup> R<sup>m</sup> M<sup>0</sup>

<sup>2</sup>: σ<sup>2</sup>

Γ `<sup>κ</sup> hM1, M2i R<sup>m</sup> hM<sup>0</sup>

1, M<sup>0</sup>

<sup>2</sup>i: σ<sup>1</sup> × σ<sup>2</sup>

: Σα:σ1.σ<sup>2</sup>

Γ `<sup>P</sup> π1M R<sup>m</sup> π1M<sup>0</sup>

: σ<sup>1</sup>

: Σα:σ1.σ<sup>2</sup> Γ ` Fst(M) c

Γ `<sup>P</sup> π2M R<sup>m</sup> π2M<sup>0</sup>

: [π1c/α]σ<sup>2</sup>

0: ∃α:k.τ

Γ, α:k, x:τ `<sup>I</sup> M R<sup>m</sup> M<sup>0</sup>

: σ Γ ` σ: sig

Γ `<sup>I</sup> unpack [α, x] = e in (M: σ) R<sup>m</sup> unpack [α, x] = e

0 in (M<sup>0</sup>

: σ): σ

0

: τ Γ, x:τ `<sup>κ</sup> M R<sup>m</sup> M<sup>0</sup>

: σ

Γ `<sup>κ</sup> let x = e in M R<sup>m</sup> let x = e

0 in M<sup>0</sup>: σ

Γ `<sup>I</sup> M<sup>1</sup> R<sup>m</sup> M<sup>0</sup>

<sup>1</sup>: σ

Γ, α/m:σ `<sup>I</sup> M<sup>2</sup> R<sup>m</sup> M<sup>0</sup>

<sup>2</sup>: σ

<sup>0</sup> Γ ` σ

0: sig

Γ `<sup>I</sup> let α/m = M<sup>1</sup> in (M<sup>2</sup>: σ

0)

R<sup>m</sup> let α/m = M<sup>0</sup>

<sup>1</sup> in (M<sup>0</sup>

<sup>2</sup>: σ 0): σ 0

Γ `<sup>I</sup> M R<sup>m</sup> M<sup>0</sup>

: σ

Γ `<sup>I</sup> (M:> σ) R<sup>m</sup> (M<sup>0</sup>

:> σ): σ

: σ

Γ `<sup>I</sup> M R<sup>m</sup> M<sup>0</sup>

: σ

Γ `<sup>κ</sup> M R<sup>m</sup> M<sup>0</sup>

: σ Γ ` σ ≤ σ

0

Γ `<sup>κ</sup> M R<sup>m</sup> M<sup>0</sup>

: σ 0

References [1] Val Breazu-Tannen, Thierry Coquand, Carl A. Gunter, and Andre Scedrov. Inheritance as implicit coercion. Information and Computation, 93:172–221, 1991. [2] Karl Crary. Modules, abstraction, and parametric polymorphism. In Forty-Fourth ACM Symposium on Principles of Programming Languages, Paris, France, January 2017. [3] Karl Crary, Robert Harper, and Sidd Puri. What is a recursive module? In 1999 SIGPLAN Conference on Programming Language Design and Implementation, pages 50–63, Atlanta, May 1999. [4] Pierre-Louis Curien and Giorgio Ghelli. Coherence of subsumption, minimum typing and type-checking in F≤. Mathematical Structures in Computer Science, 2(1):55–91, 1992. [5] Derek Dreyer. Understanding and Evolving the ML Module System. PhD thesis, Carnegie Mellon University, School of Computer Science, Pittsburgh, Pennsylvania, May 2005. [6] Derek Dreyer, Karl Crary, and Robert Harper. A type system for higher-order modules. In Thirtieth ACM Symposium on Principles of Programming Languages, pages 236–249, New Orleans, Louisiana, January 2003. [7] Martin Elsman. Static interpretation of modules. In 1999 ACM International Conference on Functional Programming, pages 208–219, Paris, France, 1999. [8] Martin Elsman, Troels Henriksen, Danil Annenkov, and Cosmin E. Oancea. Static interpretation of higherorder modules in Futhark: Functional GPU programming in the large. In 2018 ACM International Conference on Functional Programming, 2018. [9] Robert Harper and Mark Lillibridge. A type-theoretic approach to higher-order modules with sharing. In Twenty-First ACM Symposium on Principles of Programming Languages, pages 123–137, Portland, Oregon, January 1994. [10] Robert Harper, David MacQueen, and Robin Milner. Standard ML. Technical Report ECS-LFCS-86-2, Department of Computer Science, University of Edinburgh, March 1986. [11] Robert Harper and John C. Mitchell. On the type structure of Standard ML. ACM Transactions on Programming Languages and Systems, 15(2):211–252, April 1993. [12] Robert Harper, John C. Mitchell, and Eugenio Moggi. Higher-order modules and the phase distinction. In Seventeenth ACM Symposium on Principles of Programming Languages, pages 341–354, San Francisco, January 1990. [13] Robert Harper and Greg Morrisett. Compiling polymorphism using intensional type analysis. In Twenty-Second ACM Symposium on Principles of Programming Languages, pages 130–141, San Francisco, January 1995. [14] Robert Harper and Benjamin C. Pierce. Design considerations for ML-Style module systems. In Benjamin C. Pierce, editor, Advanced Topics in Types and Programming Languages. The MIT Press, 2005. [15] Robert Harper and Chris Stone. A type-theoretic interpretation of Standard ML. In Proof, Language and Interaction: Essays in Honour of Robin Milner. The MIT Press, 2000. Extended version published as CMU technical report CMU-CS-97-147. [16] Daniel K. Lee, Karl Crary, and Robert Harper. Towards a mechanized metatheory of Standard ML. In Thirty-Fourth ACM Symposium on Principles of Programming Languages, Nice, France, January 2007. [17] Xavier Leroy. Manifest types, modules and separate compilation. In Twenty-First ACM Symposium on Principles of Programming Languages, pages 109–122, Portland, Oregon, January 1994. [18] Xavier Leroy. Applicative functors and fully transparent higher-order modules. In Twenty-Second ACM Symposium on Principles of Programming Languages, San Francisco, January 1995. [19] Xavier Leroy. A proposal for recursive modules in Objective Caml. Available at http://caml.inria. fr/pub/papers/xleroy-recursive_modules-03.pdf, 2003. [20] Xavier Leroy, Damien Doligez, Jacques Garrigue, Didier R´emy, and J´erˆome Vouillon. The OCaml system, release 4.03, Documentation and user's manual. Institut National de Recherche en Informatique et Automatique (INRIA), 2016. [21] David MacQueen. Using dependent types to express modular structure. In Thirteenth ACM Symposium on Principles of Programming Languages, pages 277–286, St. Petersburg Beach, Florida, January 1986. [22] David B. MacQueen and Mads Tofte. A semantics for higher-order functors. In Fifth European Symposium on Programming, volume 788 of Lecture Notes in Computer Science, pages 409–423. Springer, 1994. [23] Robin Milner, Mads Tofte, and Robert Harper. The Definition of Standard ML. The MIT Press, Cambridge, Massachusetts, 1990. [24] John C. Mitchell and Gordon D. Plotkin. Abstract types have existential type. ACM Transactions on Programming Languages and Systems, 10(3):470–502, July 1988. [25] Marco Patrignani, Amal Ahmed, and Dave Clarke. Formal approaches to secure compilation. ACM Computing Surveys, 2019. To appear. [26] Andrew Pitts. Typed operational reasoning. In Benjamin C. Pierce, editor, Advanced Topics in Types and Programming Languages, chapter 7, pages 245–289. The MIT Press, 2005. [27] Andreas Rossberg, Claudio Russo, and Derek Dreyer. F-ing modules. Journal of Functional Programming, 24(5), September 2014.

[28] Claudio V. Russo. Types for Modules. PhD thesis, Edinburgh University, March 1998. [29] Claudio V. Russo. First-class structures for Standard ML. Nordic Journal of Computing, 7(4), 2000. [30] Claudio V. Russo. Recursive structures for Standard ML. In 2001 ACM International Conference on Functional Programming, 2001. [31] Chung-chieh Shan. Higher-order modules in System F<sup>ω</sup> and Haskell. Available at homes.soic.indiana.edu/ ccshan/xlate/xlate.pdf, May 2006. [32] Zhong Shao. Typed cross-module compilation. In 1998 ACM International Conference on Functional Programming, pages 141–152, Baltimore, Maryland, September 1998. [33] Zhong Shao. Transparent modules with fully syntactic signatures. In 1999 ACM International Conference on Functional Programming, pages 220–232, Paris, September 1999. [34] Christopher A. Stone and Robert Harper. Deciding type equivalence in a language with singleton kinds. In Twenty-Seventh ACM Symposium on Principles of Programming Languages, Boston, January 2000. Extended version published as CMU technical report CMU-CS-99-155. [35] Christopher A. Stone and Robert Harper. Extensional equivalence and singleton types. ACM Transactions on Computational Logic, 7(4), October 2006. An earlier version appeared in the 2000 Symposium on Principles of Programming Languages.

(Typographical errors corrected, April 2020.)