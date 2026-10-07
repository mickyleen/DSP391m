## Trang 1

Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop), pages 1291–1304
July 2-7, 2026 ©2026 Association for Computational Linguistics
Thesis Proposal: A Normalization-First Framework for Sound, Complete,
and Utility-Ready Open Information Extraction
Chandan Prakash*
TCS Research, India
IIT Kanpur, India
ch.pr@tcs.com
Pavan Kumar Chittimalli
TCS Research, India
pavan.chittimalli@tcs.com
Arnab Bhattacharya
IIT Kanpur, India
arnabb@cse.iitk.ac.in
Abstract
Open Information Extraction (OIE) has largely
focused on extracting relational tuples from
text, yet in its current form remains unsuitable
for downstream systems due to the absence
of standardized, semantically sound represen￾tations. This thesis argues that the field has
been addressing extraction as a surface-level
prediction problem, leading to outputs that are
semantically incomplete and logically ambigu￾ous, particularly in the presence of modality,
negation, conditionality, quantification, and at￾tribution. We propose a normalization-first
framework that reframes OIE as a structured se￾mantic transformation pipeline, where raw text
is first converted into a lossless, canonical form
of declarative, active-voice, and irreducible sen￾tence units, and extraction is constrained to
atomic unary and binary relations augmented
with explicit semantic annotations. Within a
Probably Approximately Correct (PAC) learn￾ing perspective, we formalize soundness, com￾pleteness, and usefulness as approximate yet
verifiable guarantees over extraction quality, ac￾knowledging the inherent undecidability of full
semantic interpretation. This thesis outlines a
feasible research program to develop the theo￾retical foundations, models, and evaluation pro￾tocols required to produce system-ready OIE
representations, thereby establishing a princi￾pled and executable path toward making OIE
directly usable for downstream reasoning and
machine interpretability.
1 Introduction
Open Information Extraction (OIE) aims to convert
unstructured natural language into relational tuples
without predefined schemas (Etzioni et al., 2008).
It is widely viewed as a general-purpose seman￾tic interface between text and downstream NLP
systems. However, despite substantial progress,
OIE in its current form is not directly usable for
*External PhD Student at IIT Kanpur
downstream systems due to a lack of standardized,
semantically sound representations. Existing ap￾proaches largely treat extraction as a surface-level
prediction problem, producing tuples that appear
plausible but fail to faithfully capture meaning,
especially in the presence of modality, negation,
quantification, attribution, and conditionality.
OIE emerged to address the limitations of classi￾cal Information Extraction, as formalized in MUC￾style systems (Sundheim and Chinchor, 1993; Gr￾ishman and Sundheim, 1996), which relied on
predefined schemas and domain-specific supervi￾sion. By removing schema constraints, OIE en￾abled scalable extraction from open-domain text
(Figure 1). This vision was first realized by Tex￾tRunner (Etzioni et al., 2008), and subsequently
extended through rule-based (Gashteovski et al.,
2017; Mishra et al., 2023), neural (Yu et al., 2021;
Dong et al., 2023), and generative paradigms (Fan
and He, 2023; Zhang et al., 2025). While these
approaches improve flexibility and benchmark per￾formance, they do not address a fundamental issue:
the absence of a representation that is semantically
faithful and directly usable for reasoning.
Current OIE systems implicitly assume that
sentences can be decomposed into independent
facts. This assumption breaks in realistic set￾tings. For instance, a sentence such as “The sys￾tem may automatically approve the loan if the
eligibility criteria are met.” is often reduced to
(system, approve, loan), discarding modality and
conditional dependence. Such outputs are syntac￾tically valid but semantically unsafe, as they con￾flate possibility with certainty and ignore logical
structure. Similar failures arise across benchmarks,
where conditionals, negations, and scope are not
preserved (Table 1). As a result, improvements
in standard evaluation metrics do not correspond
to improvements in faithfulness, completeness, or
downstream utility (Lamarche and Langlais, 2024).
This problem is further amplified by fragmen￾1291

---

## Trang 2

Information Extraction (IE) Open Information Extraction (OIE)
Domain Specific, Formal, and
Structured
Open Domain, Schema Free, and
Semi Structured
(Ram -> Defeated -> Ravan)
(Arjun -> was tutored by -> Guru Dron)
(Ashoka -> fought -> Kalinga War)
(Ramanujan -> discovered -> theta functions)
(Mahabharat -> contains -> Bhagvad Geeta)
(Chandragupt -> founded -> Maurya Dynasty)
Text Corpus
(Domain Specific)
Predefined Schema
Massive Corpus
(Web Scale)
No Schema
Input
Output
AuthorOf
Entity 1 Entity 2
Valmiki Ramayan
Vyas Mahabharat
Kalidas Shakuntala
KingOf
Entity 1 Entity 2
Chandragupta Maurya Empire
Ashoka Maurya Empire
Shivaji Maratha Empire
Figure 1: IE vs OIE Comparison
Sentence Unless the server is rebooted, the update will
not install.
Extractions (the server; is; rebooted), (the
update; will not install; )
Remarks Conditional dependencies are not repre￾sented within the current OIE framework.
Table 1: Representative output from an OIE system
demonstrating gaps in soundness, completeness, and
downstream usefulness.
tation across representations and evaluation prac￾tices. OIE systems vary in extraction formats,
granularity, and assumptions about linguistic struc￾ture, while benchmarks adopt incompatible annota￾tion schemes. Existing metrics are predominantly
string-based and fail to capture semantic correct￾ness or logical consistency. Prior surveys (Niklaus
et al., 2018; Zhou et al., 2022; Pei et al., 2023b;
Pai et al., 2024) document this diversity, but do
not provide a unified formulation grounded in ex￾plicit semantic requirements for downstream use.
Consequently, the field has largely optimized for
extractability rather than usability.
This thesis contends that the central challenge
in OIE is a mis-specified problem formulation:
it should not be modeled as direct tuple predic￾tion from raw text, but as a structured semantic
transformation that yields sound, complete, and
downstream-usable representations. Given the am￾biguity and partial undecidability of natural lan￾guage, these properties are defined and enforced
within a PAC framework (Haussler and Warmuth,
2018), providing approximate yet verifiable guar￾antees.
To this end, we propose a normalization-first
OIE framework that decouples semantic normaliza￾tion from relational extraction. The framework
comprises four stages (Figure 2). This thesis
presents a concrete and feasible research program
to operationalize this formulation, with the follow￾ing primary contributions:
• A formalisation of lossless semantic decom￾position (Table 3) with guarantees of preserva￾tion and consistency within a PAC framework.
• A standardized semantic annotation schema
capturing logic-critical aspects such as modal￾ity, scope, negation, and attribution (Table 2).
• The development of benchmark datasets and
fine-grained evaluation metrics that measure
semantic soundness, completeness, and utility
beyond surface matching.
• A system design that integrates probabilistic
models with deterministic validation under a
PAC framework to ensure reliable extraction.
• Canonicalization and empirical evaluation of
OIE representations for downstream reason￾ing and machine interpretability.
• Extension of the normalization-first frame￾work to multilingual settings to validate its
generality across languages.
This work redefines OIE as a problem of produc￾ing system-ready semantic representations rather
than surface-level extractions. It presents a prin￾cipled and executable path toward making OIE
outputs sound, complete, and directly usable for
downstream NLP systems.
2 Related Work
Since TextRunner (Etzioni et al., 2008), OIE has
evolved through rule-based, neural, and generative
paradigms, yet no generation has produced repre￾sentations that are directly usable by downstream
reasoning systems. The core issue is not architec￾tural but representational: the field has treated OIE
as a surface-level prediction task, producing tuples
that are syntactically plausible but semantically un￾sound. We survey the literature along four dimen￾sions to establish where and why this gap persists,
and to position the proposed normalization-first
framework as the necessary corrective.
1292

---

## Trang 3

Stage - II
Lossless Semantic
Decomposition:
Clause-Level Structural
Decomposition,
Meaning Preservation
Validation,
Lexical Fidelity Enforcement
Heterogeneous Text Input:
Text Corpus,
Domain Specific Documents,
Business Documents,
Web Corpus
Context-Resolved
Sentence Units
Semantically Equivalent
Canonical Sentences
Stage - III
Validated Relational Signal
Extraction:
Open Relational Tuple Derivation, Predicate and Argument Typing, Meaning Consistency Validation,
Logical Form Preservation Check
Stage - IV
Canonical Alignment and
Knowledge Consolidation:
Relation and Argument
Canonicalization,
Canonical Entity Resolution,
Taxonomic and Relational
Hierarchy Induction
Entity-Aligned
Canonical Tuples
Validated Knowledge
Materialization
Semantically and
Logically
Validated OIE Tuples
Stage - I
Linguistic Structuring &
Context Resolution:
Structural Document Decomposition,
Lexical and Syntactic Normalization,
Domain-Aware Linguistic Adaptation,
Sentence Boundary Detection,
Entity and Reference Unification
Figure 2: Proposed End-to-End OIE Pipeline for Knowledge Base Population
2.1 OIE System Architectures
Rule-Based Systems: Early systems grounded
extraction in syntactic parsing, POS tagging, and
semantic role labeling. WOE (Wu and Weld, 2010)
and ReVerb (Fader et al., 2011) improved relation￾phrase coherence. Ollie (Mausam et al., 2012)
partially captured attribution and clausal context.
Kraken (Akbik and Löser, 2012) introduced N-ary
tuples; ClausIE (Del Corro and Gemulla, 2013) and
StanfordIE (Angeli et al., 2015) decomposed sen￾tences into clauses and entailments before extrac￾tion. ReNoun (Yahya et al., 2014) and RelNoun (Pal
and Mausam, 2016) extended relational coverage
to nominalizations. NestIE (Bhutani et al., 2016)
encoded hierarchical propositional dependencies
via recursive representations. MinIE (Gashteovski
et al., 2017) was the first to attach structured seman￾tic annotations; polarity, modality, attribution, and
quantity; to extracted tuples. IndIE (Mishra et al.,
2023) extended rule-based extraction to morpho￾logically rich languages. Despite interpretability,
these systems are constrained by handcrafted pat￾terns and provide no formal guarantees on semantic
preservation.
Neural Tagging Systems. The second generation
reframed OIE as sequence labeling. NeuralOIE
(Cui et al., 2018) applied copy-attention over en￾coder representations. OpenIE6 (Kolluru et al.,
2020a) combined grid labeling with iterative infer￾ence for N-ary extractions. SpanOIE (Zhan and
Zhao, 2020) improved argument boundary detec￾tion at the span level. Later models (Yu et al., 2021;
Dong et al., 2023, 2022; Fatahi Bayat et al., 2022)
added syntactic constraints to promote compact￾ness. These models improve coverage but cannot
represent discontinuous arguments or enforce se￾mantic correctness on outputs.
Neural Generative Systems. Seq2Seq models
offer greater expressiveness. IMOJIE (Kolluru
et al., 2020b) conditioned generation on previously
decoded tuples to reduce repetition. Gen2OIE
(Kolluru et al., 2022) extended this to multilingual
settings. More recent models (Pei et al., 2023a;
Fan and He, 2023; Chen et al., 2024) leverage
pre-trained encoder-decoder architectures. While
enabling abstractive and discontinuous extraction,
generative systems impose no structural or seman￾tic constraints on outputs, making soundness and
completeness unverifiable.
LLMs as OIE Systems. Foundational models
(Google; OpenAI; Anthropic Claude; DeepSeek;
Alibaba Cloud; xAI; Cohere, 2024) have been ap￾plied to OIE in zero and few-shot regimes. Mario
(Zhang et al., 2025) uses chain-of-thought rea￾soning to construct binary extractions iteratively.
Although LLMs achieve competitive benchmark
scores, they hallucinate, are prompt-sensitive, and
their outputs have not been evaluated for seman￾tic soundness or logical completeness within the
PAC learning framework; the gap most directly
motivating this thesis.
2.2 Representation: Structure, Granularity,
and Semantic Annotations
Binary tuples dominate due to benchmark com￾patibility (Stanovsky and Dagan, 2016; Bhardwaj
et al., 2019), but compress complex assertions into
pairwise relations, causing information loss; N-ary
methods (Akbik and Löser, 2012; Del Corro and
Gemulla, 2013) improve fidelity yet lack clear cri￾teria for use, while nested representations (Bhutani
et al., 2016) remain largely unevaluated. More crit￾ically, logic-bearing phenomena such as negation,
modality, conditionality, attribution, and quantifi￾cation are typically discarded, as noted by MinIE
(Gashteovski et al., 2017) and Ollie (Mausam et al.,
2012), but inconsistently encoded and absent from
benchmarks, reducing conditional tuples (Table 4)
to misleading independent assertions. Additionally,
sentence normalization is underdeveloped: clause￾based approaches ClausIE (Del Corro and Gemulla,
1293

---

## Trang 4

2013) and StanfordIE (Angeli et al., 2015) lack
guarantees of meaning preservation, while simplifi￾cation methods (Narayan et al., 2017; Ponce et al.,
2024; Yao et al., 2024) prioritize readability over se￾mantic fidelity, and OIE@OIA (Wang et al., 2022b)
introduces intermediate graphs without ensuring
lossless decomposition; this thesis instead formal￾izes lossless normalization within a PAC frame￾work as a prerequisite for reliable extraction.
2.3 Evaluation Benchmarks and Their
Limitations
Evaluation has progressed from manual inspec￾tion (Mesquita et al., 2013; Xu et al., 2013) to
large-scale automated matching, with OIE2016
(Stanovsky and Dagan, 2016) introducing silver￾standard lexical soft matching, and Wire57
(Lechelle et al., 2019) and CaRB (Bhardwaj et al.,
2019) advancing toward gold-standard N-ary an￾notation; subsequent resources such as AW-OIE
(Stanovsky et al., 2018), RE-OIE2016 (Zhan and
Zhao, 2020), and LSOIE (Solawetz and Larson,
2021) support neural evaluation, while specialized
benchmarks address Chinese (Sun et al., 2018;
Chen et al., 2024), multilingual fact synsets (Gash￾teovski et al., 2022), pre-trained language model
probing (Wang et al., 2022a), cross-domain robust￾ness (Qi et al., 2023), and domain generalization
(Yu et al., 2022), with BenchIE FL (Lamarche and
Langlais, 2024) aligning evaluation with down￾stream utility via flexible matching; however, three
limitations persist: reliance on lexical overlap that
ignores semantic equivalence and logical correct￾ness, lack of evaluation for semantic annotations
such as polarity, modality, and conditionality, and
inconsistent annotation conventions across bench￾marks that hinder reliable comparison (Lamarche
and Langlais, 2024), so reported gains do not reli￾ably reflect improved system-readiness for reason￾ing.
2.4 Multilinguality
Multilingual OIE has been explored via rule-based
systems for Spanish and Portuguese (Gamallo and
Garcia, 2015) and for Hindi, Tamil, Telugu, and
Urdu (Mishra et al., 2023); neural tagging for Span￾ish, Portuguese (Ro et al., 2020; Vasilkovsky et al.,
2022), Arabic, and Galician (Kotnis et al., 2022);
and generative alignment for cross-lingual trans￾fer (Kolluru et al., 2022). Benchmark resources
exist for Chinese (Sun et al., 2018; Gashteovski
et al., 2022; Chen et al., 2024), German (Gash￾teovski et al., 2022), Arabic, Galician, and Hindi.
Yet OIE for morphologically diverse languages re￾mains underexplored, and no work has applied
normalization-based preprocessing to non-English
languages where coreference, implicit reference,
and clause boundary detection are substantially
harder. We outline multilingual extension as a fu￾ture direction. Preliminary investigation is required
to assess how normalization assumptions transfer
across typologically diverse languages.
2.5 Downstream Utility
The ultimate criterion for OIE is downstream util￾ity across tasks such as knowledge base popula￾tion, question answering, relation discovery, natu￾ral language inference, and machine reading com￾prehension (Mausam, 2016); however, BenchIE
FL (Lamarche and Langlais, 2024) shows that
benchmark scores poorly predict application perfor￾mance, indicating that optimizing existing metrics
does not yield system-ready representations. A key
bottleneck is canonicalization: while prior work
addresses relation and entity normalization (Chris￾tensen et al., 2011), the joint alignment of tuples en￾riched with polarity, modality, conditionality, and
attribution remains unresolved. This thesis intro￾duces a canonicalization and consolidation stage,
followed by evaluation on natural language to logi￾cal reasoning tasks, providing an executable path
toward usable outputs. Existing surveys (Niklaus
et al., 2018; Zhou et al., 2022; Pei et al., 2023b;
Pai et al., 2024) cover architectural, neural, appli￾cation, and chronological views, yet overlook the
core representational deficit, as successive methods
improve benchmarks without resolving semantic
incompleteness and logical ambiguity; this thesis
instead formulates OIE as a structured semantic
transformation pipeline with PAC-grounded guar￾antees on soundness, completeness, and utility.
3 Proposed Framework and System
We contend that the primary limitation of exist￾ing OIE systems lies not in extraction accuracy,
but in representation design. Specifically, current
approaches generate surface-level tuple fragments
(Examples in Figure 1 and Table 1) that lack seman￾tic grounding and structural information, as shown
in Table 4, making them unsuitable for downstream
reasoning or inference tasks.
To address this, we reconceptualize OIE not as
a span-labeling or relation-detection problem, but
1294

---

## Trang 5

Table 2: Semantic Annotation Schema for Unary and
Binary OIE Tuples
Attribute Definition and Possible Values
Tuple ID Unique identifier (T1, T2, . . .) used for
referencing tuples in scope and depen￾dency layers.
Type Unary: P(x) representing a property or
state.
Binary: R(x, y) representing a relation￾ship between two arguments.
Predicate The verb phrase (span or non-span).
Arg 1 (Subject) Noun phrase (span or non-span) repre￾senting the first argument.
Arg 2 (Object) Noun phrase (span or non-span) repre￾senting the second argument, or NULL
for unary tuples.
Polarity Positive (Assertion), Negative (Nega￾tion or Denial), Neutral (Ambiguous or
underspecified).
Modality Fact (Is), Possibility (May / Can), Obli￾gation (Must / Should), Necessity (Will
/ Essential), Permitted, Prohibited.
Quantification Singular (Default/One), Universal (All
/ Every), Existential (Some / A few),
Cardinal (Specific number), None.
Attribution Author (Default), an explicitly stated en￾tity acting as the source of the claim, or
SYSTEM_INFERENCE
Scope & Depen￾dency
Conjunction / Disjunction:
AND(ID_list), OR(ID_list)
Conditional: IF(Antecedent_IDs),
THEN(Consequent_IDs)
as a normalization-first problem. In this view, the
task involves systematically transforming uncon￾strained natural language sentences into simplified,
normalized sentences (as illustrated in Table 3),
followed by their conversion into a semantically
faithful and structurally standardized OIE repre￾sentation (Defined in Table 2), as shown in Table
4.
The proposed framework operationalizes this
perspective through a four-stage pipeline (Figure 2),
where each stage enforces a verifiable linguistic
contract over its output. The pipeline prioritizes
text normalization, motivated by the observation
that although existing OIE frameworks claim do￾main independence, empirical studies (Qi et al.,
2023; Yu et al., 2022) demonstrate that structural
heterogeneity in raw corpora (e.g., business docu￾ments versus web-scraped text) adversely affects
extraction performance. Accordingly, the normal￾ization stage standardizes sentence structure to pro￾duce consistent and well-formed sentence units.
The framework is designed to satisfy the key prop￾Table 3: Sentence Simplification to Declarative, Ac￾tive Voice, and Atomic Irreducible Simple or Complex
Sentences.
Original Sentence Simplified Sentences
The system may au￾tomatically approve
or reject a loan ap￾plication if the ap￾plicant meets all eli￾gibility criteria.
S1: The system may au￾tomatically approve a loan
application if the applicant
meets all eligibility criteria.
S2: The system may auto￾matically reject a loan appli￾cation if the applicant meets
all eligibility criteria.
According to the
company policy,
no employee shall
access customer
records without
authorization.
S3: No employee shall ac￾cess customer records with￾out authorization.
According to Dr.
Smith, the medica￾tion must be taken
after meals, but it
should not be con￾sumed if the patient
feels dizzy.
S4: Dr. Smith states that the
patient must take the medi￾cation after the patient eats
meals.
S5: Dr. Smith states that the
patient should not consume
the medication if the patient
feels dizzy.
erties of soundness, completeness, and usefulness
in the extracted information.
3.1 Formal Definitions
We formalize these properties at the sentence level
to define a principled semantic interface between
an unstructured input sentence S and its extracted
representation T. This formulation is grounded in
the central claim that existing OIE systems fail to
produce representations that are directly usable for
downstream reasoning due to the absence of stan￾dardized and semantically faithful structure. Ac￾cordingly, we define the requirements for system￾ready representations in terms of soundness, com￾pleteness, and usefulness, interpreted within the
PAC learning framework. The proposed represen￾tation is related to Semantic Web formalisms such
as RDF (Resource Description Framework) triples
and reification, but differs in its explicit model￾ing of modality, attribution, and conditional scope,
which are typically not represented within such
frameworks.
Soundness (Semantic Faithfulness): An extrac￾tion is sound if every tuple t ∈ T is supported by
the meaning of the source sentence S, i.e., S |= t.
This ensures that the extracted representation does
not introduce unsupported or hallucinated informa￾tion. Given the inherent ambiguity and variability
1295

---

## Trang 6

Table 4: Illustrative OIE Tuple with Semantic Annotations. Sentence ID refers to Table 3; annotation schema
defined in Table 2.
Sent. Tuple Predicate Argument 1 Argument 2 Pol. Modality Attribution Scope & Depen￾dency
S3 T1 access employee
Quant: All
customer
records
Quant: All
-ve Prohibited ORG(policy) IF ([T2])
THEN ([T1])
T2 have
authoriza￾tion
employee
Quant: All
NA
Quant:
-ve Fact Author
of natural language, this guarantee is interpreted
within the PAC learning framework, where sound￾ness holds with high probability under a distribu￾tion over sentences.
Completeness (Information Preservation): An
extraction is complete if the combined semantics
of all tuples in T preserves the meaning of the orig￾inal sentence S, i.e., V
t∈T
t ≈ S. This requires
that critical semantic phenomena such as modal￾ity, negation, and conditionality are retained in the
transformation. As exact equivalence is generally
undecidable for natural language, completeness is
defined in a PAC sense, where the representation
approximately preserves meaning with bounded
error.
Usefulness (Reasoning Readiness): An extrac￾tion is useful if the representation T is structured
and semantically explicit enough to support down￾stream reasoning tasks without requiring access to
the original sentence S. This includes enabling in￾ference over entities, relations, and their associated
semantic constraints. Usefulness reflects the ability
of T to support correct reasoning outcomes with
high probability.
While we adopt PAC terminology to frame
soundness and completeness as approximate guar￾antees, we operationalize these notions through
measurable proxies. In practice, entailment is ap￾proximated using a combination of natural lan￾guage inference models and human validation.
Meaning preservation is evaluated via reconstruc￾tion fidelity and semantic annotation coverage.
Specifically, soundness is evaluated via entailment￾based verification between source sentences and
extracted tuples, using both language models and
human validation. Completeness is approximated
through reconstruction fidelity and coverage of an￾notated semantic phenomena such as modality and
negation. Rather than deriving formal PAC bounds,
this work interprets PAC as a guiding principle for
defining probabilistic guarantees over extraction
quality under realistic linguistic uncertainty.
These properties collectively redefine OIE as
a representation problem rather than an extrac￾tion problem. The tuple extraction examples pre￾sented under the existing OIE framework in Ta￾ble 1 are neither sound nor complete, and they
are not directly useful for downstream reasoning
tasks. In contrast, the examples under the pro￾posed framework, shown in Table 4, are sound,
complete, and useful for downstream reasoning
tasks. To operationalize this perspective, we pro￾pose a normalization-first pipeline (Figure 2) that
systematically transforms unstructured text into se￾mantically grounded, structurally standardized rep￾resentations suitable for machine interpretability
and downstream inference.
3.2 Stage I: Linguistic Structuring and
Context Resolution
Despite claims of domain independence, existing
OIE systems degrade under structural variability
in real-world text (Qi et al., 2023; Yu et al., 2022).
This reveals a fundamental issue: OIE has focused
on extraction without first ensuring that the input is
linguistically well-formed for consistent interpreta￾tion.
In contrast, our framework treats preprocessing
as a semantic structuring step. Given an input text,
this stage produces a set of standardized sentence
units with resolved coreference and explicit con￾textual links. This transformation reduces ambigu￾ity and ensures that each unit is self-contained for
downstream processing. Soundness at this stage,
interpreted within the PAC learning framework,
requires that contextual resolution preserves the
intended referential meaning with high probability
under a distribution of inputs.
Exploration Status: We have explored both
1296

---

## Trang 7

dependency-based rule systems and LLM-based ap￾proaches for segmentation and context resolution.
Our findings indicate that early resolution of coref￾erence and implicit links is necessary for achiev￾ing semantically faithful representations. Ongoing
work investigates domain-adaptive preprocessing
strategies for structurally complex corpora such as
legal and technical text.
3.3 Stage II: Lossless Semantic Decomposition
Natural language sentences exhibit significant func￾tional and structural variability. Functionally, they
may be Declarative, Interrogative, Imperative, or
Exclamatory; structurally, they range from Simple
to Compound-Complex, it can be in Active or Pas￾sive voice, which current OIE systems attempt to
handle implicitly, leading to inconsistent outputs.
We instead formalize decomposition as a normal￾ization problem. Given a sentence S, we construct
a set of simplified sentences in Canonical Normal
Form (CNF), denoted as
Scf = {s1, s2, . . . , sn},
where each si
is declarative, in active voice, and
structurally irreducible.
This transformation is governed by two con￾straints:
1. Irreducibility: Each si ∈ Scf cannot be fur￾ther decomposed without breaking a logical
dependency. For example, conditional con￾structions are preserved as single units. This
ensures that the decomposition aligns with
semantic structure rather than surface syntax.
2. Bounded Lexical Fidelity: Let V (·) denote
the vocabulary of a sentence. We require that
1 −
|V (Scf ) ∩ V (S)|
|V (Scf )|
≤ ϵ, (1)
ensuring that introduced tokens are limited to
syntactic transformations rather than semantic
alterations. This constraint enforces semantic
faithfulness while allowing necessary normal￾ization operations.
Completeness of the transformation that Scf ap￾proximately preserves the full meaning of S is ver￾ified via two complementary checks: bidirectional
entailment (S |=
V
si and V
si
|= S) and recon￾struction, where S is regenerated from the aggre￾gate content of Scf and compared to the original.
Sentence Albert Einstein died in Princeton in 1955.
Existing
Framework
Extractions
(Albert Einstein; died), (Albert
Einstein; died; in Princeton; in
1955 )
Proposed
Framework
Extractions
T1:(Albert Einstein; died),
T2:(Albert Einstein; died in;
Princeton ), T3:(Albert Einstein;
died in; 1955 ), AND(T2,T3)
Table 5: Decomposition of an n-ary event into compo￾sitional unary and binary relations with explicit depen￾dency structure under the proposed normalization-first
framework.
Both checks are interpreted as PAC guarantees with
bounded approximation error.
Exploration Status: We have experimented with
fine-tuned small language models for this trans￾formation. To validate semantic preservation
(S ≡ Scf ), we explore bidirectional entailment
and reconstruction-based checks, both interpreted
under PAC guarantees.
3.4 Stage III: Validated Relational Signal
Extraction
Once sentences are transformed into canonical
form, the extraction problem becomes structurally
constrained. This enables a shift from heuristic
extraction to schema-driven interpretation. We re￾strict the representation to atomic unary (Entity →
Property) and binary (Subject → Object) relations
(Table 2), augmented with a semantic annotation
layer A capturing polarity, modality, quantification,
condition, and attribution.
The restriction to unary and binary relations is
a deliberate design choice to enable standardiza￾tion, interpretability, and tractable evaluation. Al￾though natural language frequently expresses n-ary
or event-centric structures, we posit that a large
class of such phenomena can be systematically de￾composed into sets of interdependent unary and
binary relations, augmented with explicit scope
and dependency annotations (Table 5). This com￾positional representation prioritizes semantic trans￾parency and operational consistency over represen￾tational compactness. While certain inherently n￾ary constructs may require approximation, the cen￾tral objective of this work is to determine whether
semantically faithful and reasoning-ready represen￾tations can be achieved within a constrained yet
standardized relational framework.
This design reflects the central thesis: OIE
should produce semantically explicit and struc￾turally standardized representations rather than
1297

---

## Trang 8

loosely defined tuples. Soundness and complete￾ness of the extracted representation are enforced
through consistency with the canonical sentences,
interpreted within the PAC framework to account
for uncertainty in language understanding.
Exploration Status: Our experiments indicate
that rule-based extraction over normalized sen￾tences achieves higher structural consistency than
end-to-end neural systems, which exhibit schema
drift and introduce vocabulary absent from the
source, consistent with the limitations documented
in recent survey work (Pei et al., 2023b). Current
efforts focus on constructing a fine-grained evalua￾tion benchmark that measures annotation accuracy
for A, moving beyond the lexical overlap metrics
that dominate existing OIE evaluation (Yu et al.,
2022).
3.5 Stage IV: Canonical Alignment and
Representation Consolidation
The final stage enforces global consistency across
extracted representations by aligning semantically
equivalent expressions and resolving variation in
surface forms. This process ensures that the output
representation is stable, comparable across inputs,
and suitable for downstream reasoning.
Rather than treating extracted tuples as isolated
fragments, this stage organizes them into a coher￾ent semantic representation with consistent rela￾tional forms and entity references. Within the PAC
learning framework, this alignment is treated as an
approximate consistency guarantee, ensuring that
semantically equivalent inputs yield comparable
representations with high probability.
Exploration Status: We have explored clustering￾based approaches (Vashishth et al., 2018) to iden￾tify equivalent relational expressions. Ongoing
work focuses on integrating these methods with
the earlier stages to produce end-to-end consistent
representations, bridging the gap between proba￾bilistic language processing and reliable system￾ready outputs.
3.6 Benchmark Construction and Evaluation
Protocol
A recurring problem in OIE research is that evalu￾ation is decoupled from the properties that matter.
Existing benchmarks measure token-level overlap
against human-annotated tuples (Yu et al., 2022),
rewarding systems that produce fluent-looking out￾put regardless of whether it is sound, complete,
or useful for downstream reasoning. Benchmark
scores consequently do not correlate with down￾stream utility (Pei et al., 2023b). A central contri￾bution of this thesis is therefore a benchmark and
evaluation protocol designed specifically to mea￾sure the properties defined in Section 3.1.
Corpus Design: The benchmark draws sentences
from several typologically distinct domains, includ￾ing Web, News, Literature, Banking, Law, Medi￾cal, Automobile, and Transportation, among others.
This diversity is not incidental, it is the primary
mechanism for measuring domain independence,
which OIE systems claim but rarely demonstrate
empirically. The distribution of sentences will
reflect real-world data, encompassing both short
and sufficiently long sentences, where most ex￾isting OIE systems tend to fail. The corpus is de￾signed to exceed the scale of the current largest fine￾grained OIE benchmark, BenchIE FL (Lamarche
and Langlais, 2024), which contains only 300 sen￾tences, providing broader coverage for statistically
meaningful domain-stratified analysis.
Annotation Schema: Each source sentence S
is paired with two layers of annotation: (i) a set
of normalised sentences Scf as defined in Section
3.3, and (ii) a set of gold tuples extracted from Scf
with full semantic annotations A covering polarity,
modality, quantification, and attribution as defined
in Section 3.4.
The CNF annotation serves two roles: it de￾fines a reference for normalization quality via a
bounded lexical fidelity constraint (Equation 1),
ensuring high lexical overlap with S so that both
normalization-first and direct extraction systems
remain comparably evaluable on the same bench￾mark, and it provides reusable, high-overlap sen￾tence variants that support adjacent tasks such as
sentence simplification, textual entailment, and ma￾chine translation evaluation.
3.6.1 Evaluation Metrics.
We define a hierarchical scoring scheme that maps
directly onto the formal desiderata. For each sen￾tence, partial and full credit is assigned across four
dimensions:
Argument Identification Score: measures
whether the extracted arguments (subject, object,
entity) match the gold arguments, assessed via
lexical and semantic overlap.
Relation Phrase Score: measures the accuracy
of the extracted predicate against the gold relation
1298

---

## Trang 9

phrase.
Complete Relation Score: a joint score over the
full tuple (subject, predicate, object), rewarded
only when all three components are jointly correct,
forming the basis for the soundness requirement.
Semantic Annotation Score: measures the accu￾racy of the annotation layer A polarity, modality,
quantification, and attribution, against gold labels,
operationalising completeness for the logical phe￾nomena that current benchmarks ignore entirely.
An aggregate system score is computed as a
weighted combination of four dimensions, with
domain-stratified scores reported separately to ex￾pose domain generalization gaps hidden by aggre￾gate metrics; this reflects the central premise of
the thesis that OIE systems should be evaluated
on their ability to produce structurally coherent,
semantically correct tuples across domains, rather
than optimizing token overlap on narrow bench￾marks.
The proposed evaluation metrics serve as empir￾ical proxies for PAC-style guarantees. Specifically,
tuple-level soundness is assessed through the com￾bination of complete relation accuracy and seman￾tic annotation correctness, ensuring that extracted
tuples are both structurally and semantically faith￾ful to the source. Completeness is approximated
via semantic equivalence, sentence reconstruction
accuracy, and entailment-based consistency, which
together measure the extent to which the full mean￾ing of the source sentence is preserved. Usefulness
is reflected through aggregate performance, includ￾ing evaluation on explicit downstream applications,
where task-specific objectives provide a direct mea￾sure of the practical utility of the extracted repre￾sentations.
We emphasize that the proposed framework is
not intended as a fully deterministic or complete
semantic parser. Instead, it defines a structured
approximation pipeline where each stage incremen￾tally improves semantic fidelity under practical con￾straints. The goal is not perfect normalization, but
controlled and measurable improvements over ex￾isting extraction paradigms.
Conclusion
This thesis argues that OIE has been misformu￾lated as a surface-level extraction task, resulting
in outputs that are not directly usable for down￾stream systems due to the lack of standardized,
semantically sound representations, and proposes a
normalization-first framework that redefines OIE as
a structured semantic transformation problem. By
introducing lossless decomposition into canonical
sentence units, constraining extraction to atomic
relations enriched with explicit semantic annota￾tions, and enforcing consistency through canonical
alignment, the framework ensures that meaning
is preserved and made interpretable for reasoning,
with guarantees defined and evaluated within a PAC
learning framework. It further establishes a con￾crete and feasible research program to formalize
decomposition, design a unified annotation schema,
develop benchmarks and metrics aligned with se￾mantic soundness and utility, and build models that
integrate learning with validation under PAC con￾straints. Together, this work provides a principled
and executable path to transform OIE from heuris￾tic tuple generation into a system-ready semantic
interface, directly addressing the core limitation
of current approaches and repositioning the field
toward representations that are reliable, complete,
and usable for downstream NLP tasks.
Limitations
This work has several limitations that reflect both
the complexity of natural language and the scope of
the proposed formulation. First, the normalization￾first framework depends on the reliability of up￾stream linguistic processes such as coreference res￾olution and syntactic parsing, and errors in these
components can propagate and affect the semantic
fidelity of the final OIE output, even when guaran￾tees are defined within a PAC learning framework.
Second, enforcing lossless semantic decomposition
and explicit annotation introduces additional com￾putational overhead, creating a trade-off between
efficiency and semantic soundness that must be
carefully managed within PAC-constrained approx￾imations. Third, the restriction to unary and binary
relations, while enabling standardization and inter￾pretability, may limit the direct representation of
inherently n-ary or event-centric phenomena, re￾quiring further abstraction or decomposition that
may not always be minimal or unique. Fourth, al￾though the proposed semantic annotation schema is
designed to capture core aspects such as modality,
negation, scope, and attribution, it may not fully
cover all linguistic nuances, particularly in infor￾mal, noisy, or highly context-dependent text, high￾lighting the limits of any fixed schema under the
1299

---

## Trang 10

inherent ambiguity of language within a PAC set￾ting. Finally, the evaluation of semantic soundness,
completeness, and usefulness relies on carefully
constructed annotated datasets, which are costly,
potentially subjective, and difficult to standardize
at scale, making robust and generalizable evalua￾tion an open challenge for the proposed research
program.
References
Alan Akbik and Alexander Löser. 2012. KrakeN: N-ary
facts in open information extraction. In Proceedings
of the Joint Workshop on Automatic Knowledge Base
Construction and Web-scale Knowledge Extraction
(AKBC-WEKEX), pages 52–56, Montréal, Canada.
Association for Computational Linguistics.
Alibaba Cloud. Alibaba cloud model studio.
Gabor Angeli, Melvin Jose Johnson Premkumar, and
Christopher D. Manning. 2015. Leveraging linguis￾tic structure for open domain information extraction.
In Proceedings of the 53rd Annual Meeting of the As￾sociation for Computational Linguistics and the 7th
International Joint Conference on Natural Language
Processing (Volume 1: Long Papers), pages 344–354,
Beijing, China. Association for Computational Lin￾guistics.
Anthropic Claude. Anthropic claude.
Sangnie Bhardwaj, Samarth Aggarwal, and Mausam.
2019. CaRB: A crowdsourced benchmark for open
IE. In Proceedings of the 2019 Conference on Empiri￾cal Methods in Natural Language Processing and the
9th International Joint Conference on Natural Lan￾guage Processing (EMNLP-IJCNLP), pages 6262–
6267, Hong Kong, China. Association for Computa￾tional Linguistics.
Nikita Bhutani, H. V. Jagadish, and Dragomir Radev.
2016. Nested propositions in open information ex￾traction. In Proceedings of the 2016 Conference on
Empirical Methods in Natural Language Processing,
pages 55–64, Austin, Texas. Association for Compu￾tational Linguistics.
Zhen Chen, Jingping Liu, Deqing Yang, Yanghua Xiao,
Huimin Xu, Zongyu Wang, Rui Xie, and Yunsen
Xian. 2024. Exploiting duality in open information
extraction with predicate prompt. In Proceedings
of the 17th ACM International Conference on Web
Search and Data Mining, WSDM ’24, page 125–133,
New York, NY, USA. Association for Computing
Machinery.
Janara Christensen, Mausam, Stephen Soderland, and
Oren Etzioni. 2011. An analysis of open informa￾tion extraction based on semantic role labeling. In
Proceedings of the Sixth International Conference
on Knowledge Capture, K-CAP ’11, page 113–120,
New York, NY, USA. Association for Computing
Machinery.
Cohere. 2024. Cohere. Accessed: September 13, 2024.
Lei Cui, Furu Wei, and Ming Zhou. 2018. Neural open
information extraction. In Proceedings of the 56th
Annual Meeting of the Association for Computational
Linguistics (Volume 2: Short Papers), pages 407–413,
Melbourne, Australia. Association for Computational
Linguistics.
DeepSeek. Deepseek models.
Luciano Del Corro and Rainer Gemulla. 2013. Clausie:
clause-based open information extraction. In Pro￾ceedings of the 22nd International Conference on
World Wide Web, WWW ’13, page 355–366, New
York, NY, USA. Association for Computing Machin￾ery.
Kuicai Dong, Aixin Sun, Jung-Jae Kim, and Xiaoli Li.
2022. Syntactic multi-view learning for open infor￾mation extraction. In Proceedings of the 2022 Con￾ference on Empirical Methods in Natural Language
Processing, pages 4072–4083, Abu Dhabi, United
Arab Emirates. Association for Computational Lin￾guistics.
Kuicai Dong, Aixin Sun, Jung-jae Kim, and Xiaoli
Li. 2023. Open information extraction via chunks.
In Proceedings of the 2023 Conference on Empiri￾cal Methods in Natural Language Processing, pages
15390–15404, Singapore. Association for Computa￾tional Linguistics.
Oren Etzioni, Michele Banko, Stephen Soderland, and
Daniel S. Weld. 2008. Open information extraction
from the web. Commun. ACM, 51(12):68–74.
Anthony Fader, Stephen Soderland, and Oren Etzioni.
2011. Identifying relations for open information ex￾traction. In Proceedings of the 2011 Conference on
Empirical Methods in Natural Language Processing,
pages 1535–1545, Edinburgh, Scotland, UK. Associ￾ation for Computational Linguistics.
Zhiyuan Fan and Shizhu He. 2023. Efficient data learn￾ing for open information extraction with pre-trained
language models. In Findings of the Association
for Computational Linguistics: EMNLP 2023, pages
13056–13063, Singapore. Association for Computa￾tional Linguistics.
Farima Fatahi Bayat, Nikita Bhutani, and H. Jagadish.
2022. CompactIE: Compact facts in open informa￾tion extraction. In Proceedings of the 2022 Confer￾ence of the North American Chapter of the Associ￾ation for Computational Linguistics: Human Lan￾guage Technologies, pages 900–910, Seattle, United
States. Association for Computational Linguistics.
Pablo Gamallo and Marcos Garcia. 2015. Multilin￾gual open information extraction. In Portuguese
conference on artificial intelligence, pages 711–722.
Springer.
1300

---

## Trang 11

Kiril Gashteovski, Rainer Gemulla, and Luciano del
Corro. 2017. MinIE: Minimizing facts in open in￾formation extraction. In Proceedings of the 2017
Conference on Empirical Methods in Natural Lan￾guage Processing, pages 2630–2640, Copenhagen,
Denmark. Association for Computational Linguis￾tics.
Kiril Gashteovski, Mingying Yu, Bhushan Kotnis, Car￾olin Lawrence, Mathias Niepert, and Goran Glavaš.
2022. BenchIE: A framework for multi-faceted fact￾based open information extraction evaluation. In
Proceedings of the 60th Annual Meeting of the As￾sociation for Computational Linguistics (Volume 1:
Long Papers), pages 4472–4490, Dublin, Ireland. As￾sociation for Computational Linguistics.
Google. Google gemini models.
Ralph Grishman and Beth Sundheim. 1996. Message
Understanding Conference- 6: A brief history. In
COLING 1996 Volume 1: The 16th International
Conference on Computational Linguistics.
David Haussler and Manfred Warmuth. 2018. The prob￾ably approximately correct (pac) and other learning
models. The Mathematics of Generalization, pages
17–36.
Keshav Kolluru, Vaibhav Adlakha, Samarth Aggarwal,
Mausam, and Soumen Chakrabarti. 2020a. OpenIE6:
Iterative Grid Labeling and Coordination Analysis for
Open Information Extraction. In Proceedings of the
2020 Conference on Empirical Methods in Natural
Language Processing (EMNLP), pages 3748–3761,
Online. Association for Computational Linguistics.
Keshav Kolluru, Samarth Aggarwal, Vipul Rathore,
Mausam, and Soumen Chakrabarti. 2020b. IMo￾JIE: Iterative memory-based joint open information
extraction. In Proceedings of the 58th Annual Meet￾ing of the Association for Computational Linguistics,
pages 5871–5886, Online. Association for Computa￾tional Linguistics.
Keshav Kolluru, Muqeeth Mohammed, Shubham
Mittal, Soumen Chakrabarti, and Mausam. 2022.
Alignment-augmented consistent translation for mul￾tilingual open information extraction. In Proceedings
of the 60th Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers),
pages 2502–2517, Dublin, Ireland. Association for
Computational Linguistics.
Bhushan Kotnis, Kiril Gashteovski, Daniel Rubio, Am￾mar Shaker, Vanesa Rodriguez-Tembras, Makoto
Takamoto, Mathias Niepert, and Carolin Lawrence.
2022. MILIE: Modular & iterative multilingual open
information extraction. In Proceedings of the 60th
Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), pages 6939–
6950, Dublin, Ireland. Association for Computational
Linguistics.
Fabrice Lamarche and Philippe Langlais. 2024.
BenchIE^FL: A manually re-annotated fact-based
open information extraction benchmark. In Findings
of the Association for Computational Linguistics:
ACL 2024, pages 8372–8394, Bangkok, Thailand.
Association for Computational Linguistics.
William Lechelle, Fabrizio Gotti, and Phillippe Langlais.
2019. WiRe57 : A fine-grained benchmark for open
information extraction. In Proceedings of the 13th
Linguistic Annotation Workshop, pages 6–15, Flo￾rence, Italy. Association for Computational Linguis￾tics.
Mausam, Michael Schmitz, Stephen Soderland, Robert
Bart, and Oren Etzioni. 2012. Open language learn￾ing for information extraction. In Proceedings of the
2012 Joint Conference on Empirical Methods in Nat￾ural Language Processing and Computational Natu￾ral Language Learning, pages 523–534, Jeju Island,
Korea. Association for Computational Linguistics.
Mausam Mausam. 2016. Open information extraction
systems and downstream applications. In Proceed￾ings of the twenty-fifth international joint conference
on artificial intelligence, pages 4074–4077.
Filipe Mesquita, Jordan Schmidek, and Denilson Bar￾bosa. 2013. Effectiveness and efficiency of open re￾lation extraction. In Proceedings of the 2013 Confer￾ence on Empirical Methods in Natural Language Pro￾cessing, pages 447–457, Seattle, Washington, USA.
Association for Computational Linguistics.
Ritwik Mishra, Simranjeet Singh, Rajiv Ratn Shah, Pon￾nurangam Kumaraguru, and Pushpak Bhattacharyya.
2023. IndIE: A multilingual open information ex￾traction tool for Indic languages. In Findings of the
Association for Computational Linguistics: IJCNLP￾AACL 2023 (Findings), pages 312–326, Nusa Dua,
Bali. Association for Computational Linguistics.
Shashi Narayan, Claire Gardent, Shay B. Cohen, and
Anastasia Shimorina. 2017. Split and rephrase. In
Proceedings of the 2017 Conference on Empirical
Methods in Natural Language Processing, pages 606–
616, Copenhagen, Denmark. Association for Compu￾tational Linguistics.
Christina Niklaus, Matthias Cetto, André Freitas, and
Siegfried Handschuh. 2018. A survey on open infor￾mation extraction. arXiv preprint arXiv:1806.05599.
OpenAI. Openai models.
Liu Pai, Wenyang Gao, Wenjie Dong, Lin Ai, Ziwei
Gong, Songfang Huang, Li Zongsheng, Ehsan Hoque,
Julia Hirschberg, and Yue Zhang. 2024. A survey on
open information extraction from rule-based model to
large language model. In Findings of the Association
for Computational Linguistics: EMNLP 2024, pages
9586–9608, Miami, Florida, USA. Association for
Computational Linguistics.
Harinder Pal and Mausam. 2016. Demonyms and com￾pound relational nouns in nominal open IE. In Pro￾ceedings of the 5th Workshop on Automated Knowl￾edge Base Construction, pages 35–39, San Diego,
CA. Association for Computational Linguistics.
1301

---

## Trang 12

Kevin Pei, Ishan Jindal, and Kevin Chang. 2023a. Ab￾stractive open information extraction. In Proceed￾ings of the 2023 Conference on Empirical Methods
in Natural Language Processing, pages 6146–6158,
Singapore. Association for Computational Linguis￾tics.
Kevin Pei, Ishan Jindal, Kevin Chen-Chuan Chang,
ChengXiang Zhai, and Yunyao Li. 2023b. When
to use what: An in-depth comparative empirical anal￾ysis of OpenIE systems for downstream applications.
In Proceedings of the 61st Annual Meeting of the
Association for Computational Linguistics (Volume
1: Long Papers), pages 929–949, Toronto, Canada.
Association for Computational Linguistics.
David Ponce, Thierry Etchegoyhen, Jesús Calleja, and
Harritxu Gete. 2024. Split and rephrase with large
language models. In Proceedings of the 62nd An￾nual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), pages 11588–
11607, Bangkok, Thailand. Association for Compu￾tational Linguistics.
Ji Qi, Chuchun Zhang, Xiaozhi Wang, Kaisheng Zeng,
Jifan Yu, Jinxin Liu, Lei Hou, Juanzi Li, and Xu Bin.
2023. Preserving knowledge invariance: Rethink￾ing robustness evaluation of open information ex￾traction. In Proceedings of the 2023 Conference on
Empirical Methods in Natural Language Processing,
pages 5876–5890, Singapore. Association for Com￾putational Linguistics.
Youngbin Ro, Yukyung Lee, and Pilsung Kang. 2020.
Multi^2OIE: Multilingual open information extrac￾tion based on multi-head attention with BERT. In
Findings of the Association for Computational Lin￾guistics: EMNLP 2020, pages 1107–1117, Online.
Association for Computational Linguistics.
Jacob Solawetz and Stefan Larson. 2021. LSOIE: A
large-scale dataset for supervised open information
extraction. In Proceedings of the 16th Conference of
the European Chapter of the Association for Compu￾tational Linguistics: Main Volume, pages 2595–2600,
Online. Association for Computational Linguistics.
Gabriel Stanovsky and Ido Dagan. 2016. Creating a
large benchmark for open information extraction.
In Proceedings of the 2016 Conference on Empir￾ical Methods in Natural Language Processing, pages
2300–2305, Austin, Texas. Association for Computa￾tional Linguistics.
Gabriel Stanovsky, Julian Michael, Luke Zettlemoyer,
and Ido Dagan. 2018. Supervised open information
extraction. In Proceedings of the 2018 Conference of
the North American Chapter of the Association for
Computational Linguistics: Human Language Tech￾nologies, Volume 1 (Long Papers), pages 885–895,
New Orleans, Louisiana. Association for Computa￾tional Linguistics.
Mingming Sun, Xu Li, Xin Wang, Miao Fan, Yue Feng,
and Ping Li. 2018. Logician: A unified end-to-end
neural approach for open-domain information extrac￾tion. In Proceedings of the Eleventh ACM Interna￾tional Conference on Web Search and Data Mining,
WSDM ’18, page 556–564, New York, NY, USA.
Association for Computing Machinery.
Beth M. Sundheim and Nancy A. Chinchor. 1993. Sur￾vey of the Message Understanding Conferences. In
Human Language Technology: Proceedings of a
Workshop Held at Plainsboro, New Jersey, March
21-24, 1993.
Shikhar Vashishth, Prince Jain, and Partha Talukdar.
2018. Cesi: Canonicalizing open knowledge bases
using embeddings and side information. In Proceed￾ings of the 2018 World Wide Web Conference, pages
1317–1327.
Michael Vasilkovsky, Anton Alekseev, Valentin Ma￾lykh, Ilya Shenbin, Elena Tutubalina, Dmitriy Sa￾likhov, Mikhail Stepnov, Andrey Chertok, and Sergey
Nikolenko. 2022. Detie: Multilingual open infor￾mation extraction inspired by object detection. In
Proceedings of the AAAI Conference on Artificial
Intelligence, volume 36, pages 11412–11420.
Chenguang Wang, Xiao Liu, and Dawn Song. 2022a.
IELM: An open information extraction benchmark
for pre-trained language models. In Proceedings of
the 2022 Conference on Empirical Methods in Nat￾ural Language Processing, pages 8417–8437, Abu
Dhabi, United Arab Emirates. Association for Com￾putational Linguistics.
Xin Wang, Minlong Peng, Mingming Sun, and Ping Li.
2022b. OIE@OIA: an adaptable and efficient open
information extraction framework. In Proceedings
of the 60th Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers),
pages 6213–6226, Dublin, Ireland. Association for
Computational Linguistics.
Fei Wu and Daniel S. Weld. 2010. Open information
extraction using Wikipedia. In Proceedings of the
48th Annual Meeting of the Association for Computa￾tional Linguistics, pages 118–127, Uppsala, Sweden.
Association for Computational Linguistics.
xAI. xai grok models.
Ying Xu, Mi-Young Kim, Kevin Quinn, Randy Goebel,
and Denilson Barbosa. 2013. Open information ex￾traction with tree kernels. In Proceedings of the
2013 Conference of the North American Chapter
of the Association for Computational Linguistics:
Human Language Technologies, pages 868–877, At￾lanta, Georgia. Association for Computational Lin￾guistics.
Mohamed Yahya, Steven Whang, Rahul Gupta, and
Alon Halevy. 2014. ReNoun: Fact extraction for
nominal attributes. In Proceedings of the 2014 Con￾ference on Empirical Methods in Natural Language
Processing (EMNLP), pages 325–335, Doha, Qatar.
Association for Computational Linguistics.
1302

---

## Trang 13

Peiran Yao, Kostyantyn Guzhva, and Denilson Barbosa.
2024. Semantic graphs for syntactic simplification:
A revisit from the age of LLM. In Proceedings
of TextGraphs-17: Graph-based Methods for Nat￾ural Language Processing, pages 105–115, Bangkok,
Thailand. Association for Computational Linguistics.
Bowen Yu, Yucheng Wang, Tingwen Liu, Hongsong
Zhu, Limin Sun, and Bin Wang. 2021. Maximal
clique based non-autoregressive open information
extraction. In Proceedings of the 2021 Conference
on Empirical Methods in Natural Language Process￾ing, pages 9696–9706, Online and Punta Cana, Do￾minican Republic. Association for Computational
Linguistics.
Bowen Yu, Zhenyu Zhang, Jingyang Li, Haiyang Yu,
Tingwen Liu, Jian Sun, Yongbin Li, and Bin Wang.
2022. Towards generalized open information extrac￾tion. In Findings of the Association for Computa￾tional Linguistics: EMNLP 2022, pages 1439–1453,
Abu Dhabi, United Arab Emirates. Association for
Computational Linguistics.
Junlang Zhan and Hai Zhao. 2020. Span model for
open information extraction on accurate corpus. In
Proceedings of the AAAI Conference on Artificial
Intelligence, volume 34, pages 9523–9530.
Donghai Zhang, SHuangtao Yang, Dong Xiaozheng,
Wei Song, and Bo Fu. 2025. MARIO-0.5B: A multi￾agent lightweight model for real-time open informa￾tion extraction in low-resource settings. In Find￾ings of the Association for Computational Linguis￾tics: EMNLP 2025, pages 13085–13094, Suzhou,
China. Association for Computational Linguistics.
Shaowen Zhou, Bowen Yu, Aixin Sun, Cheng Long,
Jingyang Li, Haiyang Yu, Jian Sun, and Yongbin
Li. 2022. A survey on neural open information ex￾traction: Current status and future directions. arXiv
preprint arXiv:2205.11725.
A Appendix
We define an extraction as a structured object
e = ⟨r, A, Σ⟩,
where r denotes the relation expression, A =
{a1, . . . , an} represents an ordered or unordered
set of arguments, and Σ denotes an optional set of
semantic annotations such as polarity, modality, or
attribution. Differences across Open Information
Extraction (OIE) systems can be viewed as varia￾tions in the constraints imposed on the arity n, the
permissible forms of r and A, and whether Σ is
included.
Most existing OIE systems focus on binary re￾lations and typically omit semantic annotations.
While some approaches extend to n-ary representa￾tions, the semantic annotation component remains
largely underexplored, and there is currently no
standardized benchmark for its evaluation. The
examples in Table 6 are described in light of both
current system capabilities and the proposed frame￾work, which is essential for ensuring the soundness,
completeness, and practical utility of extracted in￾formation. In Table 6, Row 1 illustrates a sim￾ple binary extraction, while Rows 2 and 3 demon￾strate discontinuous and overlapping binary extrac￾tions. Row 5 illustrates an N-ary extraction, and
Row 9 illustrates a nested extraction. Rows 10–
14 present extractions with semantic annotations,
while Rows 6, 7, and 8 illustrate implicit extrac￾tions.
1303

---

## Trang 14

ID Sentence Extractions
1 Driver is authorized to drive the car. (Driver, is authorized to drive, the car)
2 The cook baked and ate the cake. (the cook, baked, the cake)
(the cook, ate, the cake)
3 Bell distributes electronic and building prod￾ucts.
(Bell, distributes, electronic products)
(Bell, distributes, building products)
4 Elvis moved to Memphis in 1948. (Elvis, moved to, Memphis)
(Elvis, moved in, 1948)
5 Albert Einstein died in Princeton in 1955. (Albert Einstein, died)
(Albert Einstein, died, in Princeton, in 1955)
6 NIH’s director, Francis Collins (Francis Collins, [is] director [of], NIH)
7 United States President Obama (Obama, [is] President [of], United States)
8 Seattle historian Feliks (Feliks, [is] historian [from], Seattle)
9 A senior official in Iraq said the body, which
was found by U.S. military police, appeared to
have been thrown from a vehicle.
P1: (body, appeared to have been thrown, ∅)
P2: (P1, from, vehicle)
P3: (A senior official in Iraq, said, P2)
P4: (U.S. military police, found, body)
10 No people were hurt in the fire. (people, were hurt in, fire) Negative Polarity
11 All young rabbits drink milk. (rabbits, drink, milk) Not all rabbits
12 Early astronomers believed that earth is flat. (earth, is, flat) Possibility
13 It has been proven that earth is round. (earth, is, round) Certainty
14 If he wins five key states, Romney will be
elected President.
(Romney, will be elected, President) Conse￾quent
(Romney, wins, five key states) Antecedent
Table 6: Different Types of OIE Extractions. The colour coding is used, blue for arguments, orange for relation
phrases, and red for additional information.
1304
