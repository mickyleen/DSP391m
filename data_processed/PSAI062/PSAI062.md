## Trang 1

Thesis Proposal:
Cross-Lingual Transfer of Linguistic and Metalinguistic Knowledge
via Lexical Borrowing
Yulia Tsvetkov
Language Technologies Institute
School of Computer Science
Carnegie Mellon University
ytsvetko@cs.cmu.edu
Thesis committee
Chris Dyer (chair), Carnegie Mellon University
Alan W Black, Carnegie Mellon University
Noah A. Smith, Carnegie Mellon University
Jacob Eisenstein, Georgia Institute of Technology

---

## Trang 2

1 Introduction
As global development brings connectivity to more and more people, hundreds of millions of people spea￾king resource-limited1
languages will have access to the software applications built upon natural language
processing (NLP) technology. While accessibility of technology will improve, a linguistic divide will re￾main. The rich ecosystem of intelligent, language-aware applications rely on state-of-the-art NLP tools,
such as text parsing, speech recognition and synthesis, text and speech translation, semantic analysis and
inference, which, in turn, depend on data resources that exist only for a few resource-rich languages. Re￾cent work has developed techniques for projecting resources from resource-rich languages (e.g., Yarowsky
et al. 2001, Diab and Resnik 2002, Hwa et al. 2005, Ganchev et al. 2009, Padó and Lapata 2009, Das and
Petrov 2011, Täckström et al. 2013), but these have required large amounts of parallel (translated) data.
However, while small parallel corpora—translated chiefly to English—do exist for many languages, large
parallel corpora are expensive. Furthermore, while English is a high-resource language, it is linguistically
a typological outlier in a number of respects (e.g., relatively simple morphology, complex system of verbal
auxiliaries, large lexicon, etc.), and the construction-level parallelism that projection techniques exploit may
be problematic.
Thus, there is an urgent need for the development of methodologies that do not rely on large-scale
parallel corpora: without new strategies, most of the 7,000+ languages in the world—many with millions of
speakers—will remain resource-poor from the standpoint of NLP.
In this thesis, I propose techniques for automatically constructing language-specific resources, even in
languages with no resources other than raw text corpora. Our main motivation is research in linguistic bor￾rowing—the phenomenon of transferring linguistic constructions (lexical, phonological, morphological, and
syntactic) from a “donor” language to a “recipient” language as a result of contacts between communities
speaking different languages (Thomason and Kaufman 2001). Borrowed words (also called loanwords) are
found in nearly all languages, and routinely account for 10–70% of the vocabulary. Borrowing occurs across
genetically and typologically unrelated languages (for example, about 40% of Swahili’s vocabulary is bor￾rowed from Arabic). Importantly, since resource-rich languages are (historically) geopolitically important
languages, borrowed words often bridge between resource-rich and resource-limited languages.
Although borrowing is pervasive and a topic of enduring interest for historical and theoretical linguists
(Haugen 1950, Weinreich 1979), only limited work in computational modeling has addressed this phenome￾non. However, it is a topic well-suited to computational models. For example, the systematic phonological
changes that occur during borrowing can be modeled using established computational primitives such as fi￾nite state transducers, and—as this proposal contends—models of borrowing have useful applications. Any
where cross-lingual lexical correspondences are needed, we can learn them from the borrowing models;
since we need only monolingual resources, we have the ability to apply this to many languages with mi￾nimal effort without solving a complete decipherment problem. The proposed work can be summarized as
the development of a computational model of lexical borrowing and an exploration of its applications to
augment language resources and computational approaches to NLP in resource-limited languages.
This thesis work seeks to answer the following questions:
Q1. How to model lexical borrowing to learn structural commonalities across languages? Al￾though borrowed words are assimilated in language and are not perceived as foreign by native speakers (e.g.,
‘orange’ and ‘sugar’ are English words borrowed from Arabic l
.

	
PA	
K (nArnj)
2
and QºË@ (Alskr), respecti￾1Languages with limited availability of digitally stored material, and a dearth of manually-constructed linguistic resources.
2We use Buckwalter notation to write Arabic glosses.
1

---

## Trang 3

vely), the ontological difference between borrowed and (phylogenetically) native vocabulary often reveals
itself through analysis (Itô and Mester 1995). We operationalize existing morpho-phonological accounts of
the borrowing process in terms of Optimality Theory (McCarthy and Prince 1994, Prince and Smolensky
2008) to formulate a computationally and statistically efficient model of the transformation and assimilation
process. To validate our approach, we develop lexical borrowing models for typologically diverse resource￾limited languages and extract donor–recipient bilingual lexicons using the models (§3,§5.1; Tsvetkov et al.
2015).
Q2. How to leverage borrowing models to reduce the dependence on parallel data in NLP applica￾tions? Many applications, such as machine translation and linguistic resource projection techniques, use
parallel data (corpora of translated sentences) to learn cross-lingual lexical correspondences. We leverage the
borrowing models to augment (or replace, if parallel data do not exist for a language pair) cross-lingual le￾xicons obtained from parallel data. To validate this, we will adapt existing cross-lingual resource-projection
approaches to non-parallel settings. We will concentrate on the following downstream tasks: translation
(§4; Tsvetkov and Dyer 2015a), part-of-speech tagging (§5.2; cf. Täckström et al. 2013), and dependency
parsing (§5.2; cf. McDonald et al. 2011).
Q3. How to leverage borrowing models to quantify the socio-economic, political, and demographic
factors motivating lexical borrowing? Twitter and other social media corpora provide particularly fru￾itful conditions to investigate the emergence and diffusion of lexical borrowing: these texts are an example
of rapid language development, of emergence and diffusion of neologisms, of dense interaction between di￾verse multilingual populations all over the world. Importantly, written neologisms are often phonetic forms
of spoken words, and are influenced by the linguistic system of the source language (Eisenstein 2015).
Presence of morpho-phonological influence indicates some level of linguistic adaptation, i.e., borrowing.
While previous studies investigated the emergence and diffusion of lexical change in English Twitter data,
relying only on word frequencies (Eisenstein et al. 2014), our goal is to extend this research direction to
multiple languages, and to explore examples containing morpho-phonological signals. We will first learn
to distinguish borrowed items among all neologisms, using the learned morpho-phonological features from
the first phase of this thesis. Then, we will investigate demographic and geographic factors influencing bor￾rowing and its linguistic pathways (§5.3; cf. Eisenstein et al. 2014). This study will result in tools that can
improve social media applications analyzing and predicting human behavior, and will help us gain better
understanding of motives, determinants, and impacts of lexical borrowing.
Thesis statement. This thesis addresses the phenomenon of lexical borrowing with computational
models. Discovering and modeling cross-lingual borrowing is an interesting task in and of itself,
as it provides a better understanding of a pervasive linguistic phenomenon. Practically, computatio￾nal models of borrowing can facilitate cross-lingual transfer—from resource-rich to resource-limited
languages—of linguistic (lexical, morpho-phonological, syntactic) and metalinguistic (socio-economic,
cultural, behavioral) knowledge, thereby advancing NLP applications for resource-limited languages.
The rest of this proposal is structured as follows. In §2 we provide background and motivation. In
sections §3 and §4 we discuss recent studies we conducted to substantiate our assertions and establish the
feasibility of the project. The proposed future work is in §5. We conclude with the timeline for thesis
completion (§6).
2

---

## Trang 4

2 Background and Motivation
ͪपÜपलȣ
pippalī
Sanskrit
پلپل
pilpil
Persian
פלפל
falafel’
Hebrew
فلافل
falāfil
Arabic
pilipili
Swahili
parpaare
Gawwada
Fig. 1: An example of the multilingual borrowing from
Sanskrit into typologically diverse, low- and high-resource
languages (Haspelmath and Tadmor 2009).
Lexical borrowing Borrowed words (e.g., in fi￾gure 1) are lexical items adopted from another lan￾guage and integrated (nativized) in the recipient lan￾guage (Haugen 1950). Borrowing occurs as a result
of linguistic contact, typically on the part of mino￾rity language speakers, from the language of wider
communication into the minority language (Sankoff
2002); that is one reason why donor languages are
often resource-rich. Nouns are borrowed preferen￾tially, then other parts of speech, then affixes, in￾flections, and phonemes (Whitney 1881, Moravcsik
1978, Myers-Scotton 2002; p. 240). Borrowing is a
distinctive and pervasive phenomenon: all languages borrowed from other languages at some point in their
lifetime, and borrowed words constitute a large fraction (10–70%) of most language lexicons (Haspelmath
2009).
Loanword nativization is primarily a phonological process. Donor words undergo phonological repairs
to adapt a foreign word to the segmental, phonotactic, suprasegmental and morpho-phonological constraints
of the recipient language (Holden 1976, Van Coetsem 1988, Ahn and Iverson 2004, Kawahara 2008, Hock
and Joseph 2009, Calabrese and Wetzels 2009, Kang 2011; inter alia). Phonological repair strategies amo￾unt to feature/phoneme epenthesis, elision, degemination, and assimilation. When speakers encounter a
foreign word (either a lemma or an inflected form), they analyze it morphologically as a stem; morpho￾logical loanword integration thus amounts to picking a donor surface form (out of existing inflections of
the same lemma), and applying the recipient language morphology (Repetti 2006). Adapted loanwords can
freely undergo recipient language inflectional and derivational processes.
The task of modeling borrowing is unexplored in computational linguistics. With the exception of a
study conducted by Blair and Ingram (2003) on generation of borrowed phonemes in English–Japanese
language pair (the method does not generalize from borrowed phonemes to borrowed words, and does not
rely on linguistic insights), we are not aware of any prior work on computational modeling of lexical bor￾rowing. Few papers only mention or tangentially address borrowing, we briefly list them here. Daumé III
(2009) focuses on areal effects on linguistic typology, a broader phenomenon that includes borrowing and
genetic relations across languages. This study is aimed at discovering language areas based on typological
features of languages. Garley and Hockenmaier (2012) train a maxent classifier with character n-gram and
morphological features to identify anglicisms (which they compare to loanwords) in an online community
of German hip hop fans. List and Moran (2013) publish a toolkit for computational tasks in historical lingu￾istics, however, the only algorithm that addresses borrowing in the toolkit is based on a non-computational
study on relation of cognacy and borrowing in language evolution (Nelson-Sathi et al. 2010). Furthermore,
List and Moran (2013) admit that “Automatic approaches for borrowing detection are still in their infancy
in historical linguistics.” More dedicated approaches are required to facilitate computational models and
applications of lexical borrowing. This is indeed the main goal of the proposed research.
We propose to model borrowing from an (input) donor to an (output) recipient using Optimality The￾ory (OT), a constraint-based theory of phonology, which has shown that complex surface phenomena can
be well-explained as the interaction of morpho-phonological constraints on the form of outputs and the
3

---

## Trang 5

relationships of inputs and outputs (Kager 1999). OT posits that surface phonetic words (in the case of
borrowing, loanwords) emerge from underlying phonological forms (donor words) according to a two-stage
process: first, various candidates for the surface form are enumerated for consideration (the ‘generation’
or GEN phase); then, these candidates are weighed against one another to see which most closely con￾forms to—or equivalently, least egregiously violates—the phonological preferences of the language (while
the preferences themselves are thought to be a universal component of human linguistic competence, the
ranking of the preferences varies across languages). When the preferences are correctly ranked, then the
actual surface form should be selected as the most optimal realization of the underlying form.3 Although
originally a theory of monolingual phonology, OT has been adapted to account for borrowing by treating
the donor language word as the underlying form for the recipient language; that is, the phonological system
of the recipient language is encoded as a system of constraints, and these constraints account for how the
donor word is adapted when it is borrowed. There has been a lot of work on borrowing in the OT paradigm
(Yip 1993, Davidson and Noyer 1997, Jacobs and Gussenhoven 2000, Kang 2003, Broselow 2004, Adler
2006, Rose and Demuth 2006, Kenstowicz and Suchato 2006, Kenstowicz 2007), but none of it has lead to
computational realizations.
The most closely related NLP research directions to modeling borrowing are modeling transliteration
and cognate forms. Borrowing, however, is different from the two fields. Borrowing vs. transliteration:
Transliteration refers to writing in a different orthography, whereas borrowing refers to expanding a langu￾age to include words adapted from another language. Unlike borrowing, transliteration is more amenable
to orthographic—rather than morpho-phonological—features, although see (Knight and Graehl 1998). Bor￾rowed words might have entered a language originally as transliterations, but a characteristic of borrowed
words is that they become assimilated in the morph-phonological system of the recipient language. Bor￾rowing vs. inheritance: Cognates are words in related languages inherited from one word in a common
ancestral language (the proto-language). Loanwords, on the other hand, can occur between any languages,
either related or not, that historically came into contact. Theoretical analysis of cognates has tended to be
concerned with a diachronic point of view, i.e., modeling word changes across time. While cognacy is of
immense scientific interest, borrowing offers a unique opportunity to reason about lexical material in many
languages, even those that are only distantly related to other living.
Machine translation and other cross-lingual NLP tasks. Machine translation has been a phenomenal
success for language pairs for which large amounts of parallel data exist; however, for low-resource langu￾age pairs with few example translations performance lags behind (Bojar et al. 2014). While some intriguing
results suggest that cryptanalysis has promise to help identify translation across languages (Dou and Knight
2013, Ravi and Knight 2011), identifying example translations using reliable cross-lingual evidence—such
as parallel corpora or bilingual dictionaries—is a key component in effectively inferring high-quality le￾xical translations from data (Dou et al. 2014). In effect, these high-quality lexical translation “anchors”
are sufficient to bootstrap cross-lingual models so that monolingual representations can be exploited more
3
Preferences are expressed as violable constraints (‘violable’ because in many cases there may be no candidate that satisfies all of
them). They consist of markedness constraints (McCarthy and Prince 1995), which describe unnatural (dispreferred) patterns in the
language, and faithfulness constraints (Prince and Smolensky 2008), which reward correspondences between the underlying form
and the surface candidates. To clarify the distinction between faithfulness and markedness constraint groups to the NLP readership,
we can draw the following analogy to the components of machine translation or speech recognition: faithfulness constraints are
analogical to the translation model or acoustic model (reflecting input), while markedness constraints are analogical to the language
model (requiring well-formedness of the output). Without faithfulness constraints, the optimal surface form could differ arbitrarily
from the underlying form.
4

---

## Trang 6

effectively (Saluja et al. 2014, Mikolov et al. 2013a, Marton et al. 2009, Callison-Burch et al. 2006). Un￾fortunately, few resources exist for finding reliable translation anchors, and borrowing promises to be a new
resource for finding translations. Beyond machine translation, lexical alignments have been widely used to
project annotations from high- to low-resource languages (Hwa et al. 2005, Täckström et al. 2013, Ganchev
et al. 2009, Tsvetkov et al. 2014a; inter alia). And, as with translation, the languages where cross-lingual
projection is most urgently needed to bootstrap linguistic resources are the languages where no parallel data
is available.
Why lexical borrowing in cross-lingual NLP? We hypothesize that lexical borrowing is a plausible al￾ternative to parallel corpora in methods employing cross-lingual data transfer. First, loanword adaptation
is not a random but rather systematic and predictable process, depending on phonotactics of donor and re￾cipient languages, thus can be modeled computationally. Loanword adaptation analyses typically employ
constraint-based models, such as OT (Kang 2011). Constraint-based models are well-suited to standard
computational string-transduction approaches, and we have already built the first successful prototype of
a language-independent OT-based loanword adaptation system (§3). Second, much linguistic research and
resource-collection has been done on borrowing in numerous language pairs. These studies will facilitate
development and evaluation of lexical-borrowing systems. Third, unlike parallel corpora which is limited or
unavailable for most language pairs, borrowing is pervasive: loanwords constitute a large fraction of most
language lexicons.4 Cross-lingual data transfer via borrowing is thus applicable at a much larger scale than
via parallel corpus. Finally, the diversity of donor languages and projection via multiple donors (rather than
via English word-alignments) will allow us to adjust model parameters to typological traits of a specific
target language (Täckström et al. 2013).
3 Constraint-Based Models of Lexical Borrowing
Our task is to identify plausible donor–loan word pairs in a language pair. While modeling string trans￾ductions is a well-studied problem in NLP, we wish to be able to learn the cross-lingual correspondences
from minimal training data, we propose a model whose features are motivated by linguistic knowledge.
We formulate a scoring model inspired by OT, in which borrowing candidates are ranked by universal con￾straints posited to underly the human faculty of language, and the candidates are determined by transduction
processes articulated in prior studies of contact linguistics.
As illustrated in figure 2, our model is conceptually divided into three main parts: (1) a mapping of
orthographic word forms in two languages into a common phonetic space; (2) generation of loanword pro￾nunciation candidates from a donor word; and (3) ranking of generated loanword candidates, based on
linguistic constraints of the donor and recipient languages. In our proposed system, parts (1) and (2) are
rule-based; whereas (3) is learned. Each component of the model is discussed in detail in the rest of this
section.
4
For example, 30–70% of the vocabulary in Japanese, Vietnamese, Korean, Cantonese, and Thai—resource-limited languages
spoken by over 400 million people—are borrowed from resource-rich languages: Chinese and English. Similarly, African languages
have been greatly influenced by Arabic, Spanish, English, and French, due to colonization, a prolonged period of language contact
in the Indian Ocean trading, as well as the influence of Islam; Swahili, Zulu, Malagasy, Hausa, Tarifit, Yoruba, spoken by 200
million, contain up to 40% of loanwords. Indo-Iranian languages—Hindustani, Hindi, Urdu, Bengali, Persian, Pashto—spoken by
860 million, also extensively borrowed from Arabic and English (Haspelmath and Tadmor 2009). In short, at least a billion people
are speaking languages whose lexicons are heavily borrowed from resource-rich languages.
5

---

## Trang 7

donor
word
To 
IPA
loan 
word
Ranking with 
OT constraints
Morphological 
adaptation Syllabification
From 
IPA
Phonological 
adaptation
GEN - generate loanword candidates EVAL - rank candidates
1 2 2 2 3 1
Fig. 2: Our morpho-phonological borrowing model conceptually has three main parts: (1) conversion of orthographic
word forms to pronunciations in IPA format; (2) generation of loanword pronunciation candidates; (3) ranking of
generated candidates using Optimality-Theoretic constraints. Part (1) and (2) are rule-based, (1) uses pronunciation
dictionaries, (2) is based on prior linguistic studies; part (3) is learned. In (3) we learn OT constraint weights from a
few dozen automatically extracted training examples.
The model is implemented as a cascade of finite-state transducers. Parts (1) and (2) amount to unwei￾ghted string transformation operations. In (1), we convert orthographic word forms to their pronunciations
in the International Phonetic Alphabet (IPA), these are pronunciation transducers. In (2) we syllabify donor
pronunciations, then perform insertion, deletion, and substitution of phonemes and morphemes (affixes), to
generate multiple loanword candidates from a donor word. Although string transformation transducers in
(2) can generate loanword candidates that are not found in a recipient language vocabulary, such candidates
are filtered out due to composition with the recipient language lexicon acceptor.
Our model performs string transformations from donor to recipient (recapitulating the historical pro￾cess). However, the resulting relation (i.e., the final composed transducer) is a bidirectional model which
can just as well be used to reason about underlying donor forms given recipient forms. In a probabilistic cas￾cade, Bayes’ rule could be used to reverse the direction and infer underlying donor forms given a loanword.
However, we instead opt to train the model discriminatively to find the most likely underlying form, given a
loanword. In part (3), candidates are “evaluated” (i.e., scored) with a weighted sum of universal constraint
violations. The non-negative weights, which we call the “cost vector”, constitute our model parameters and
are learned using a small training set of donor–recepient pairs. We use a shortest path algorithm to find the
path with the minimal cost.
3.1 Case Study: Arabic–Swahili Borrowing
In this section, we use the Arabic–Swahili5
language-pair to describe the prototypical linguistic adaptation
processes that words undergo when borrowed. Then, we describe how we model these processes.
The Swahili lexicon has been influenced by Arabic due to a prolonged period of language contact in
the Indian Ocean trading (800 A.D.–1920), as well as the influence of Islam (Rothman 2002). According
to several independent studies, Arabic loanwords constitute from 18% (Hurskainen 2004) to 40% (Johnson
1939) of Swahili word types. Despite a strong susceptibility of Swahili to borrowing and a large fraction
of Swahili words originating from Arabic, the two languages are typologically distinct with profoundly dis￾similar phonological and morpho-syntactic systems. Therefore, Arabic loanwords have been substantially
adapted to conform to Swahili phonotactics, which we survey briefly. First, Arabic has five syllable pat￾terns:6 CV, CVV, CVC, CVCC, and CVVC (McCarthy 1985; pp. 23–28), whereas Swahili (like other Bantu
languages) is characterized by the syllable ending with a vowel and CV or V syllable structure. At the
5
For simplicity, we subsume Omani Arabic and other historical dialects of Arabic under the label “Arabic”; similarly, we
subsume Swahili, its dialects and protolanguages under “Swahili”.
6C stands for consonant, and V for vowel.
6

---

## Trang 8

segment level, Swahili loanword adaptation thus involves extensive vowel epenthesis in consonant clusters
and at a syllable final position if the syllable ends with a consonant, e.g., : H.
A

J»(ktAb) → kitabu ‘book’ (Po￾lomé 1967, Schadeberg 2009, Mwita 2009). Second, phonological adaptation in Swahili loanwords includes
shortening of vowels (unlike Arabic, Swahili does not have phonemic length); substitution of consonants
that are found in Arabic but not in Swahili (e.g., emphatic (pharyngealized) /tQ
/→/t/, voiceless velar fri￾cative /x/→/k/, dental fricatives /T/→/s/, /D/→/z/, and the voiced velar fricative /G/→/g/); adoption of
Arabic phonemes that were not originally present in Swahili /T/, /D/, /G/ (e.g.,QK

	
Ym

(tH*yr)→ tahadhari
‘warning’); degemination of Arabic geminate consonants (e.g., Qå

 ($r~)→ shari ‘evil’). Finally, adapted
loanwords can freely undergo Swahili inflectional and derivational processes, e.g.,QK

	PñË@ (Alwzyr) → waziri
‘minister’, mawaziri ‘ministers’, kiuwaziri ‘ministerial’ (Zawawi 1979, Schadeberg 2009).
3.2 Arabic–Swahili Borrowing Transducers
We describe unweighted transducers for pronunciation, syllabification, and morphological and phonological
adaptation. An example that illustrates some of the possible string transformations by individual components
of the model is shown in figure 3. The goal of these transducers is to minimally overgenerate Swahili adapted
forms of Arabic words, based on the adaptations described above.
ku.ta<DEP-V>ta<PEAK>.ba.li<DEP-MORPH>.
ku.ta<DEP-V>ta<PEAK>.ba.li.
ku.tta<*COMPLEX>.ba.
ki.ta.bu<IDENT-IO-V>.
ki.ta.bu<DEP-V>.
vi<DEP-MORPH>.ki.ta.bu<IDENT-IO-V>. 
كتابا
kuttaba
kitaba
...
ku.tta.ba.
ku.t.ta.ba.
...
ki.ta.ba.
ki.ta.b.
...
ku.ta.ba. [degemination]
ku.tata.ba. [epenthesis]
ku.ta.bu. [final vowel subst.]
ki.ta.bu. [final vowel subst.]
ki.ta.bu. [epenthesis]
...
ku.tata.ba.li.
ku.tata.ba.
vi.ki.ta.bu. 
ki.ta.bu.
ki.ta.bu. 
...
kitabu
Arabic word Syllabification
to IPA
Phonological 
adaptation
Morphological 
adaptation
IPA to 
Swahili word
Ranking with 
OT constraints
Fig. 3: An example of an Arabic word AK
.
A

J»(ktAbA) ‘book.sg.indef’ transformed by our model into a Swahili loanword
kitabu.
Pronunciation Based on the IPA, we assign shared symbols to sounds that exist in both sound systems of
Arabic and Swahili (e.g., nasals /n/, /m/; voiced stops /b/, /d/), and language-specific unique symbols to
sounds that are unique to the phonemic inventory of Arabic (e.g., pharyngeal voiced and voiceless fricatives
/è/, /Q/) or Swahili (e.g., velar nasal /N/). For Swahili, we construct a pronunciation dictionary based on
the Omniglot grapheme-to-IPA mapping.7
In Arabic, we use the CMU Arabic vowelized pronunciation
dictionary containing about 700K types which has an average of four pronunciations per word (Metze et al.
2010).8 We then design four transducers—Arabic and Swahili word-to-IPA and IPA-to-word transducers—
each as a union of linear chain transducers, as well as one acceptor per pronunciation dictionary listing.
Syllabification Arabic words borrowed into Swahili undergo a repair of violations of the Swahili segmen￾tal and phonotactic constraints, for example via vowel epenthesis in a consonant cluster. Importantly, repair
7www.omniglot.com
8
Since we are working at the level of word types which have no context, we cannot disambiguate the intended form, so we
include all options. For example, for the input word AK
.
A

J»(ktAbA) ‘book.sg.indef’, we use both pronunciations /kitAbA/ and /kut￾tAbA/.
7

---

## Trang 9

depends upon syllabification. To simulate plausible phonological repair processes, we generate multiple
syllabification variants for input pronunciations. The syllabification transducer optionally inserts syllable
separators between phones. For example, for an input phonetic sequence /kuttAbA/, the output strings in￾clude /ku.t.tA.bA/, /kut.tA.bA/, and /ku.ttA.bA/ as syllabification variants; each variant violates different
constraints and consequently triggers different phonological adaptation.
Phonological adaptation Phonological adaptation of syllabified phone sequences is the crux of the
loanword adaptation process. We implement phonological adaptation transducers as a composition of pla￾usible context-dependent insertions, deletions, and substitutions of phone subsets, based on prior studies
summarized in §3.1. In what follows, we list phonological adaptation components in the order of transducer
composition in the borrowing model. The vowel deletion transducer shortens Arabic long vowels and vowel
clusters. The consonant degemination transducer shortens Arabic geminate consonants, e.g., it degemina￾tes /tt/ in /ku.ttA.bA/, outputting /ku.tA.bA/. The substitution of similar phonemes transducer substitutes
similar phonemes and phonemes that are found in Arabic but not in Swahili (Polomé 1967; p. 45). For exam￾ple, the emphatic /tQ
/, /dQ
/, /sQ
/ are replaced by the corresponding non-emphatic segments [t], [d], [s]. The
vowel epenthesis transducer inserts a vowel between pairs of consonants (/ku.ttA.bA/ → /ku.tatA.bA/), and
at the end of a syllable, if the syllable ends with a consonant (/ku.t.tA.bA/ → /ku.ta.tA.bA/). Sometimes it
is possible to predict the final vowel of a word, depending on the word-final coda consonant of its Arabic
counterpart: /u/ or /o/ added if an Arabic donor ends with a labial, and /i/ or /e/ added after coronals
and dorsals (Mwita 2009). Following these rules, the final vowel substitution transducer complements the
inventory of final vowels in loanword candidates.
Morphological adaptation Both Arabic and Swahili have significant morphological processes that alter
the appearance of lemmas. To deal with morphological variants, we construct morphological adaptation
transducers that optionally strip Arabic concatenative affixes and clitics, and then optionally append Swahili
affixes, generating a superset of all possible loanword hypotheses. We obtain the list of Arabic affixes
from the Arabic morphological analyzer SAMA (Maamouri et al. 2010); the Swahili affixes are taken from
a hand-crafted Swahili morphological analyzer (Littell et al. 2014).
3.3 Learning Constraint Weights
Due to the computational problems of working with OT (Eisner 1997; 2002), we make simplifying assump￾tions by (1) bounding the theoretically infinite set of underlying forms with a small linguistically-motivated
subset of allowed transformations on donor pronunciations, as described in §3.2; (2) imposing a priori
restrictions on the set of the surface realizations by intersecting the candidate set with the recipient pronun￾ciation lexicon; (3) assuming that the set of constraints is finite and regular (Ellison 1994); and (4) assigning
linear weights to constraints, rather than learning an ordinal constraint ranking (Boersma and Hayes 2001,
Goldwater and Johnson 2003).
OT distinguishes “markedness” constraints (McCarthy and Prince 1995), which detect dispreferred pho￾netic patterns in the language, and “faithfulness” constraints (Prince and Smolensky 2008), which ensure
correspondences between the underlying form and the surface candidates.9 The implemented constraints are
9To clarify the distinction between faithfulness and markedness constraint groups to the NLP readership, we can draw the
following analogy to the components of machine translation or speech recognition: faithfulness constraints are analogical to the
translation model or acoustic model (reflecting input), while markedness constraints are analogical to the language model (requ￾8

---

## Trang 10

Faithfulness constraints
MAX-IO-MORPH no (donor) affix deletion
MAX-IO-C no consonant deletion
MAX-IO-V no vowel deletion
DEP-IO-MORPH no (recipient) affix epenthesis
DEP-IO-V no vowel epenthesis
IDENT-IO-C no consonant substitution
IDENT-IO-C-M no subst. in manner of pronunciation
IDENT-IO-C-A no subst. in place of articulation
IDENT-IO-C-S no subst. in sonority
IDENT-IO-C-P no pharyngeal consonant substitution
IDENT-IO-C-G no glottal consonant substitution
IDENT-IO-C-E no emphatic consonant substitution
IDENT-IO-V no vowel substitution
IDENT-IO-V-O no subst. in vowel openness
IDENT-IO-V-R no subst. in vowel roundness
IDENT-IO-V-F no subst. in vowel frontness
IDENT-IO-V-FIN no final vowel substitution
Tab. 1: Faithfulness constraints prefer pronounced realizations completely congruent with their underlying forms.
listed in tables 1 and 2. Faithfulness constraints are integrated in phonological transformation components as
transitions following each insertion, deletion, or substitution. Markedness constraints are implemented as
standalone identity transducers: inputs are equal outputs, but path weights representing candidate evaluation
with respect to violated constraints are different.
The final “loanword transducer” is the composition of all transducers described in §3.2 and OT constraint
transducers. A path in the transducer represents a syllabified phonemic sequence along with (weighted) OT
constraints it violates, and shortest path outputs are those, whose cumulative weight of violated constraints
is minimal.
OT constraints are realized as features in our linear model, and feature weights are learned in a discri￾iring well-formedness of the output). Without faithfulness constraints, the optimal surface form could differ arbitrarily from the
underlying form.
Markedness constraints
NO-CODA syllables must not have a coda
ONSET syllables must have onsets
PEAK there is only one syllabic peak
SSP complex onsets rise in sonority,
complex codas fall in sonority
*COMPLEX-S no consonant clusters on syllable margins
*COMPLEX-C no consonant clusters within a syllable
*COMPLEX-V no vowel clusters
Tab. 2: Markedness constraints impose language-specific structural well-formedness of surface realizations.
9

---

## Trang 11

minative training to maximize the accuracy obtained by the loanword transducer on a small development
set of donor–recipient pairs. For parameter estimation, we employ the Nelder–Mead algorithm (Nelder and
Mead 1965), a heuristic derivative-free method that iteratively optimizes, based on an objective function
evaluation, the convex hull of n + 1 simplex vertices.10 The objective function is the “soft accuracy” of
the development set, defined as the proportion of correctly identified donor words in the total set of 1-best
outputs.
3.4 Adapting the Model to a New Language
The Arabic–Swahili case study shows that, in principle, a borrowing model can be constructed. But a
reasonable question to ask is: how much work is required to build a similar system for a new language pair?
We claim that our design permits rapid development in new language pairs. First, string transformation
operations, as well as OT constraints are language-universal. The only adaptation required is a linguistic
analysis to identify plausible morpho-phonological repair strategies for the new language pair (i.e., a subset
of allowed insertions, deletions and substitutions of phonemes and morphemes). Since we need only to
overgenerate candidates (the OT constraints will filter bad outputs), the effort is minimal relative to many
other grammar engineering exercises. The second language-specific component is the grapheme-to-IPA
converter. While this can be a non-trivial problem in some cases, the problem is well studied, and many
under-resourced languages (e.g., Swahili), have “phonographic” systems where orthography corresponds to
phonology.11
To illustrate the ease with which a language pair can be engineered, we applied our borrowing model to
the French–Romanian language pair. Although French and Romanian are sister languages (both descending
from Latin), about 12% of Romanian types are true French borrowings that came into the language in the
past few centuries (Schulte 2009). We employ the GLOBALPHONE pronunciation dictionary for French
(Schultz and Schlippe 2014) (we convert it to IPA), and automatically construct a Romanian pronunciation
dictionary using Omniglot grapheme-to-IPA conversion rules.
3.5 Intrinsic Evaluation of Models of Lexical Borrowing
Our experimental setup is defined as follows. The input to the borrowing model is a loanword candidate in
Swahili/Romanian, the outputs are plausible donor words in the Arabic/French monolingual lexicon (i.e.,
any word in pronunciation dictionary). We train the borrowing model using a small set of training examples,
and then evaluate it using a held-out test set. In the rest of this section we describe in detail our datasets,
tools, and experimental results.
Resources We employ Arabic–English and Swahili–English bitexts to extract a training set (corpora of
sizes 5.4M and 14K sentence pairs, respectively), using a cognate discovery technique (cf. Kondrak 2001).
Phonetically and semantically similar strings are classified as cognates; phonetic similarity is the string
10The decision to use Nelder–Mead rather than more conventional gradient-based optimization algorithms was motivated purely
by practical limitations of the finite-state toolkit we used which made computing derivatives with latent structure impractical from
an engineering standpoint.
11This tendency can be explained by the fact that, in many cases, lower-resource languages have developed orthography relatively
recently, rather than having organically evolved written forms that preserve archaic or idiosyncratic spellings that are more distantly
related to the current phonology of the language such as we see in, e.g., English.
10

---

## Trang 12

similarity between phonetic representations, and semantic similarly is approximated by translation.12 We
thereby extract Arabic and Swahili pairs ha, si that are phonetically similar ( ∆(a,s)
min(|a|,|s|) < 0.5) where ∆(a, s)
is the Levenshtein distance between a and s and that are aligned to the same English word e. FastAlign (Dyer
et al. 2013) is used for word alignments. Given an extracted word pair ha, si, we also extract word pairs
{ha
0
, si} for all proper Arabic words a
0 which share the same lemma with a producing on average 33 Arabic
types per Swahili type. We use MADA (Habash et al. 2009) for Arabic morphological expansion.
From the resulting dataset of 490 extracted Arabic–Swahili borrowing examples,13 we set aside rando￾mly sampled 73 examples (15%) for evaluation,14 and use the remaining 417 examples for model parameter
optimization. For French–Romanian language pair, we use an existing small annotated set of borrowing
examples,15 with 282 training and 50 (15%) randomly sampled test examples.
We use pyfst—a Python interface to OpenFst (Allauzen et al. 2007)—for the borrowing model imple￾mentation.16
Baselines We compare our model to several baselines. In the Levenshtein (L) distance baselines we chose
the closest word (either surface or pronunciation-based). In the Levenshtein-weighted (L-W) baselines,
we evaluate a variant of the Levenshtein distance tuned to identify cognates (Mann and Yarowsky 2001,
Kondrak and Sherif 2006); this method was identified by Kondrak and Sherif (2006) among the top three
cognate identification methods. In the CRF baselines we generate plausible “transliterations” of the input
Swahili (or Romanian) words in the donor lexicon using the model of Ammar et al. (2012), with multiple
references in a lattice and without reranking. The CRF transliteration model is a linear-chain CRF where
we label each source character with a sequence of target characters. The features are label unigrams, label
bigrams, and label conjoined with a moving window of source characters. In the OT-uniform baseline, we
evaluate the accuracy of the borrowing model with uniform weights, thus shortest paths in the loanwords
transducer will be forms violating the fewest constraints.
Evaluation In addition to predictive accuracy on all models (if a model produces multiple hypotheses
with the same 1-best weight, we count the proportion of correct outputs in this set), we evaluate two par￾ticular aspects of our proposed model: (1) appropriateness of the model family, and (2) the quality of the
learned OT constraint weights. The first aspect is designed to evaluate whether the morpho-phonological
transformations implemented in the model are required and sufficient to generate loanwords from the donor
inputs. We report two evaluation measures: model reachability and ambiguity. Reachability is a percentage
of test samples that are reachable (i.e., there is a path from the input test example to a correct output) in the
loanword transducer. A naïve model which generates all possible strings would score 100% reachability,
but it will be hard to set the model parameters such that it discriminates between good and bad candidates.
In order to capture this trade-off, we also report the inherent ambiguity of our model, which is the average
12This cognate discovery technique is sufficient to extract a small training set, but is not generally applicable, as it requires
parallel corpora or manually constructed dictionaries to measure semantic similarity. Large parallel corpora are unavailable for
most language pairs, including Swahili–English.
13In each training/test example one Swahili word corresponds to all extracted Arabic donor words.
14We manually verified that our test set contains clear Arabic–Swahili borrowings. For example, we extract Swahili kusafiri,
safari and Arabic Q
	
®Ë@,Q
	
®


, Q
	
® (Alsfr, ysAfr, sfr) all aligned to ‘travel’.
15http://wold.clld.org/vocabulary/8
16https://github.com/vchahun/pyfst
11

---

## Trang 13

AR–SW FR–RO
Reachability 87.7% 82.0%
Ambiguity 857 12
Tab. 3: The evaluation of the borrowing model design. Reachability is a percentage of donor–recipient pairs that are
reachable from a donor to a recipient language. Ambiguity is an average number of outputs that the model generates
per one input.
Accuracy (%)
AR–SW FR–RO
Orthographic L 8.9 38.0
CRF 16.4 36.0
Phonetic L 19.8 26.3
L-W 19.7 30.7
OT OT-U 29.3 58.5
OT 48.4 75.6
Tab. 4: The evaluation of the borrowing model accuracy. The baselines are orthographic (surface) and phonetic
(based on pronunciation lexicon) Levenshtein distance (L), heuristic Levenshtein distance with lower penalty on vowel
updates and similar letter/phone substitutions (L-W), CRF transliteration, and our model with uniform (OT-U) and
learned OT constraint weights assignment.
number of outputs potentially generated per input. A generic Arabic–Swahili transducer, for example, has
an ambiguity of 786,998—the size of the Arabic pronunciation lexicon.
Results The borrowing model reachability and ambiguity are listed in table 3. The model obtains high
reachability, while significantly reducing the average number of possible outputs per input: in Arabic from
787K to 857 words, in French from 62K to 12. This result shows that the loanword transducer design, based
on the prior linguistic analysis, is a plausible model of word borrowing. Yet, there are on average 33 correct
Arabic words out of the possible 857 outputs, thus the second part of the model—OT constraint weights
optimization—is crucial.
The accuracy results in table 4 show how challenging the task of modeling lexical borrowing between
two distinct languages is, and importantly, that orthographic and phonetic baselines including the state￾of-the-art generative model of transliteration are not suitable for this task. Phonetic baselines for Arabic–
Swahili perform better than orthographic ones, but substantially worse than OT-based models, even if OT
constraints are not weighted. Crucially, the performance of the borrowing model with the learned OT wei￾ghts corroborates the assumption made in numerous linguistic accounts that OT is an adequate analysis of
the lexical borrowing phenomenon.
EN AR gloss AR pronunciation SW syllabification Violated OT constraints
book ktAb kitAb ki.ta.bu. IDENT-IO-C-GhA, ai, DEP-IO-Vh, ui
palace AlqSr AlqaSr ka.sri MAX-IO-MORPHhAl, i, IDENT-IO-C-Shq, ki,
IDENT-IO-C-EhS, si, *COMPLEX-Chsri, DEP-IO-Vh, ii
wage Ajrh Aujrah u.ji.ra. MAX-IO-VhA, i, ONSEThui ,
DEP-IO-Vh, ii, MAX-IO-Chh, i
Tab. 5: Examples of syllabification and OT constraint violations produced by our borrowing model.
12

---

## Trang 14

Qualitative evaluation The constraint ranking learned by the borrowing model (constraints are listed
in tables 1, 2) is in line with prior linguistic analysis. In Swahili NO-CODA dominates all other mar￾kedness constraints, as expected. Both *COMPLEX-S and *COMPLEX-C, restricting consonant clusters, do￾minate *COMPLEX-V, confirming that Swahili is more permissive to vowel clusters. SSP—sonority-based
constraint—captures a common pattern of consonant clustering, found across languages, and is also learned
by our model as undominated by most competitors in Swahili, and as a dominating markedness constraint in
Romanian. Finally, vowel epenthesis DEP-IO-V is the most common strategy in Arabic loanword adaptation,
and is ranked lower according to the model; however, it is ranked highly in the French–Romanian model,
where vowel insertion is rare.
A second interesting by-product of our model is an inferred syllabification. While we did not conduct
a systematic quantitative evaluation, higher-ranked Swahili outputs tend to contain linguistically plausible
syllabifications, although the syllabification transducer inserts optional syllable boundaries between every
pair of phones. This result further attests to the plausible constraint ranking learned by the model. Example
Swahili syllabifications17 along with the OT constraint violations produced by the borrowing model are
depicted in table 5.
4 Models of Lexical Borrowing in Statistical Machine Translation
We now introduce an external application where the borrowing model will be used as a component—
machine translation. We rely on the borrowing model to project translation information from a high-resource
donor language into a low-resource recipient language, thus mitigating the deleterious effects of out-of￾vocabulary (OOV) words.
4.1 Pivoting via Borrowing for Translating OOV Words
OOVs are a ubiquitous and difficult problem in MT. When a translation system encounters an OOV—a
word that was not observed in the training data, and the trained system thus lacks its translation variants—it
usually outputs the word just as it is in the source language, producing erroneous and disfluent translations.
All MT systems, even when trained on billion-sentence-size parallel corpora, are prone to OOVs. These are
often named entities and neologisms. However, OOV problem is much more serious in morphologically￾rich and low-resource scenarios: there, OOVs are primarily not lexicon-peripheral items such as names and
specialized/technical terms, but regular content words. Since borrowed words are a component of the regular
lexical content of a language, projecting translations onto the recipient language by identifying borrowed
lexical material is a plausible strategy for solving this problem.
Procuring translations for OOVs has been a subject of active research for decades. Translation of named
entities is usually generated using transliteration techniques (Al-Onaizan and Knight 2002, Hermjakob et al.
2008, Habash 2008). Extracting a translation lexicon for recovering OOV content words and phrases is
done by mining bi-lingual and monolingual resources (Rapp 1995, Callison-Burch et al. 2006, Haghighi
et al. 2008, Marton et al. 2009, Razmara et al. 2013, Saluja et al. 2014). In addition, OOV content words
can be recovered by exploiting cognates, by transliterating and then pivoting via a closely-related resource￾richer language, when such a language exists (Hajic et al. 2000, Mann and Yarowsky 2001, Kondrak et al. ˇ
2003, De Gispert and Marino 2006, Durrani et al. 2010, Wang et al. 2012, Nakov and Ng 2012, Dholakia
17We chose examples from the Arabic–Swahili system because this is a more challenging case due to linguistic discrepancies.
13

---

## Trang 15

and Sarkar 2014). Our work is similar in spirit to the latter line of research, but we show how to obtain
translations for OOV content words by pivoting via an unrelated, often typologically distant resource-rich
language.
SWAHILI‒ENGLISH
 safari ||| *OOV*
 kituruki ||| *OOV*
TRANSLATION
CANDIDATES
ARABIC‒ENGLISH
یسافر) ysAfr) ||| travel
تركي) trky) ||| turkish
ARABIC -to- SWAHILI
BORROWING
Fig. 4: To improve a resource-poor Swahili–English
MT system, we extract translation candidates for
OOV Swahili words borrowed from Arabic using
the Swahili-to-Arabic borrowing system and Arabic–
English resource-rich MT.
Our high-level solution is depicted in figure 4. Given
an OOV word in resource-poor MT, we plug it into a bor￾rowing system that identifies the list of plausible donor
words in the donor language. Then, using the resource￾rich MT, we translate the donor words to the same target
language as in the resource-poor MT (here, English). Fi￾nally, we integrate translation candidates in the resource￾poor system.
We now discuss integrating translation candidates
acquired via borrowing plus resource-rich translation.
Phrase-based translation works as follows. A set of
candidate translations for an input sentence is created by
matching contiguous spans of the input against an in￾ventory of phrasal translations, reordering them into a
target-language appropriate order, and choosing the best
one according to a discriminative model that combines
features of the phrases used, reordering patterns, and target language model (Koehn et al. 2003). This re￾latively simple approach to translation can be remarkably effective, and, since its introduction, it has been
the basis for further innovations. However, phrase-based MT can only generate input/output phrase pairs
that were directly observed in the training corpus. In resource-limited languages we can expect the standard
phrasal inventory to be incomplete due to domain specificity and scarcity of available resources. Thus, the
decoder’s only hope for producing a good output is to find a fluent, meaning-preserving translation using
incomplete translation lexicons. We have introduced synthetic phrases (Tsvetkov et al. 2013, Chahuneau
et al. 2013, Schlinger et al. 2013, Ammar et al. 2013, Tsvetkov et al. 2014b, Tsvetkov and Dyer 2015b) as a
strategy of integrating translated phrases directly in the MT translation model, rather than via pre- or post￾processing MT inputs and outputs. Synthetic phrases are phrasal translations that are not directly extractable
from the training data, generated by auxiliary translation and postediting processes (for example, extracted
from a borrowing model). An important advantage of synthetic phrases is that they are recall-oriented, al￾lowing the system to leverage good translations that are missing in the default phrase inventory, while being
stable to noisy translation hypotheses.
For each OOV, the borrowing system produces the n-best list of plausible donors; for each donor we
then extract the k-best list of its translations.18 Then, we pair the OOV with the resulting n × k translation
candidates. The translation candidates are noisy: some of the generated donors may be erroneous, the
errors are then propagated in translation.19 To allow the low-resource translation system to leverage good
translations that are missing in the default phrase inventory, while being able to learn how trustworthy they
18We set n and k to 5, we did not experiment with other values.
19We give as input into the borrowing system all OOV words, although, clearly, not all OOVs are loanwords, and not all loanword
OOVs are borrowed from the donor language. However, an important property of the borrowing model is that its operations are not
general, but specific to the language-pair and reduced only to a small set of plausible changes that the donor word can undergo in
the process of assimilation in the recipient language. Thus, the borrowing system only minimally overgenerates the set of output
candidates given an input. If the borrowing system encounters an input word that was not borrowed from the target donor language,
it usually (but not always) produces an empty output.
14

---

## Trang 16

are, we integrate the borrowing-model acquired translation candidates as synthetic phrases.
To let the translation model learn whether to trust these phrases, the translation options obtained from the
borrowing model are augmented with a boolean translation feature indicating that the phrase was generated
externally. Additional features annotating the integrated OOV translations correspond to properties of the
donor–loan words’ relation; their goal is to provide an indication of plausibility of the pair (to mark possible
errors in the outputs of the borrowing system).
We employ two types of features: phonetic and semantic. Since borrowing is primarily a phonological
phenomenon, phonetic features will provide an indication of how typical (or atypical) pronunciation of the
word in a language; loanwords are expected to be less typical than core vocabulary words. The goal of
semantic features is to measure semantic similarity between donor and loan words: erroneous candidates
and borrowed words that changed meaning over time are expected to have different meaning from the OOV.
Phonetic features To compute phonetic features we first train a (5-gram) language model (LM) of
IPA pronunciations of the donor/recipient language vocabulary (phoneLM). Then, we re-score pronun￾ciations of the donor and loanword candidates using the LMs. We hypothesize that in donor–loanword
pairs the donor phoneLM score is higher but the loanword score is lower (i.e., the loanword phonology
is atypical in the recipient language). We capture this intuition in three features: f1=PphoneLM (donor),
f2=PphoneLM (loanword), and the harmonic mean between the two scores f3=
2f1f2
f1+f2
.
Semantic features We compute a semantic similarity feature between the candidate donor and the OOV
loanword as follows. We first train, using large monolingual corpora, 100-dimensional word vector repre￾sentations for donor and recipient language vocabularies.20 Then, we employ canonical correlation analysis
(CCA) with small donor–loanword dictionaries (training sets in the borrowing models) to project the word
embeddings into 50-dimensional vectors with maximized correlation between their dimensions. The seman￾tic feature annotating the synthetic translation candidates is cosine distance between the resulting donor and
loanword vectors. We use the WORD2VEC tool (Mikolov et al. 2013b) to train monolingual vectors,21 and
the CCA-based tool (Faruqui and Dyer 2014) for projecting word vectors.22
4.2 Evaluation of Pivoting via Borrowing in MT
We now turn to an extrinsic evaluation, looking at two low-resource translation tasks: Swahili–English
translation (donor language: Arabic), and Romanian–English translation (donor language: French). We
begin by reviewing the datasets used, and then discuss two oracle experiments that attempt to quantify how
much value could we obtain from a perfect borrowing model (since not all mistakes made by MT systems
involve borrowed words). Armed with this understanding, we then explore how much improvement can be
obtained using our system.
Datasets and software The Swahili–English parallel corpus was crawled from the Global Voices pro￾ject website23. To simulate resource-poor scenario for the Romanian–English language pair, we sample a
parallel corpus of same size from the transcribed TED talks (Cettolo et al. 2012). To evaluate translation
20We assume that while parallel data is limited in the recipient language, monolingual data is available.
21code.google.com/p/word2vec
22github.com/mfaruqui/eacl14-cca
23sw.globalvoicesonline.org
15

---

## Trang 17

improvement on corpora of different sizes we conduct experiments with sub-sampled 4K, 8K, and 14K pa￾rallel sentences from the training corpora (the smaller the training corpus, the more OOVs it has). Corpora
sizes along with statistics of source-side OOV tokens and types are given in tables 6 and 7. Statistics of the
held-out dev and test sets used in all translation experiments are given in table 8. In all the MT experiments,
we use the cdec24 toolkit (Dyer et al. 2010), and optimize parameters with MERT (Och 2003). English
4-gram language models with Kneser-Ney smoothing (Kneser and Ney 1995) are trained using KenLM
(Heafield 2011) on the target side of the parallel training corpora and on the Gigaword corpus (Graff et al.
2007). Results are reported using case-insensitive BLEU with a single reference (Papineni et al. 2002). We
train three systems for each MT setup; reported BLEU scores are averaged over systems.
4K 8K 14K
Tokens 84,764 170,493 300,648
Types 14,554 23,134 33,288
OOV tokens 4,465 (12.7%) 3,509 (10.0%) 2,965 (8.4%)
OOV types 3,610 (50.3%) 2,950 (41.1%) 2,523 (35.1%)
Tab. 6: Statistics of the Swahili–English corpora and source-side OOV for 4K, 8K, 14K parallel training sentences.
4K 8K 14K
Tokens 35,978 71,584 121,718
Types 7,210 11,144 15,112
OOV tokens 3,268 (16.6%) 2,585 (13.1%) 2,177 (11.1%)
OOV types 2,382 (55.0%) 1,922 (44.4%) 1,649 (38.1%)
Tab. 7: Statistics of the Romanian–English corpora and source-side OOV for 4K, 8K, 14K parallel training sentences.
SW–EN RO–EN
dev test dev test
Sentences 1,552 1,732 2,687 2,265
Tokens 33,446 35,057 24,754 19,659
Types 7,008 7,180 5,141 4,328
Tab. 8: Dev and test corpora sizes.
Baselines and oracles The goal of our experiments is not only to evaluate the contribution of the OOV
dictionaries that we extract when pivoting via borrowing, but also to understand the potential contribution
of exploiting borrowing: what is the overall improvement that can be achieved if we correctly translate all
OOVs that were borrowed from another language? We answer this question with the help of an “oracle”
experiment. In the oracle experiment we word-align all available parallel corpora, including dev and test
sets, and extract from the alignments translations of OOV words. Then, we append the extracted OOV
dictionaries to the translation system’s training corpus and re-train the system with the augmented training
data. Translation scores of the resulting system provide an upper bound of an improvement from correctly
24www.cdec-decoder.org
16

---

## Trang 18

translating all OOVs. When we append oracle translations of the subset of OOV dictionaries, in particular
translations of all OOVs for which the output of the borrowing system is not empty, we obtain an upper
bound that can be achieved using our method (if the borrowing system provided perfect outputs). Under￾standing the upper bounds is relevant not only for our experiments, but for any experiments that involve
augmenting translation dictionaries; however, we are not aware of prior work providing similar analysis
of upper bounds, and we recommend this as a calibrating procedure for future work on OOV mitigation
strategies.
Borrowing-augmented setups We integrate translations of OOV loanwords in the translation model using
the synthetic phrase paradigm. Due to data sparsity, we conjecture that non-OOVs that occur only few times
in the training corpus can also lack appropriate translation candidates, i.e., these are target-language OOVs.
We therefore plug into the borrowing system OOVs and non-OOV words that occur less than 3 times in the
training corpus. We list in table 9 sizes of resulting borrowed lexicons that we integrate in translation tables.
4K 8K 14K
Loan OOVs in SW–EN 2,670 2,162 1,840
Loan OOVs in RO–EN 174 133 105
Tab. 9: Sizes of dictionaries extracted using pivoting via borrowing and integrated in translation models.
Results Translation results are shown in tables 10 and 11. We evaluate separately the contribution of the
integrated OOV translations, and the same translations annotated with phonetic and semantic features. We
also provide oracle scores for integrated loanword dictionaries (Oracle-loan) as well as for recovering all
OOVs (Oracle-all).
4K 8K 14K
Baseline 13.2 15.1 17.1
+ Loan OOVs 14.3 15.7 18.2
+ Features 14.8 16.4 18.4
Oracle-loan 18.9 19.1 20.7
Oracle-all 19.2 20.4 21.1
Tab. 10: Swahili–English MT experiments.
4K 8K 14K
Baseline 15.8 18.5 20.7
+ Loan OOVs 16.0 18.7 20.7
+ Features 15.9 18.6 20.6
Oracle-loan 16.6 19.4 20.9
Oracle-all 28.0 28.8 30.4
Tab. 11: Romanian–English MT experiments.
17

---

## Trang 19

Swahili–English MT performance is improved by up to +1.6 BLEU when we augment it with translated
OOV loanwords leveraged from the Arabic–Swahili borrowing and then Arabic–English MT. The contri￾bution of the borrowing dictionaries is +0.6–1.1 BLEU, and phonetic and semantic features contribute
additional half BLEU. More importantly, oracle results show that the system can be improved more sub￾stantially with better dictionaries of OOV loanwords. This result confirms that OOV borrowed words is an
important type of OOVs, and with proper modeling it has the potential to improve translation by a large
margin. Romanian–English systems obtain only small improvement. However, this is expected as the rate
of borrowing from French into Romanian is smaller, and, as the result, the integrated loanword dictionaries
are small. Still, even with these imperfect and small dictionaries the translations improve, and even almost
approach the oracle results.
5 Future Work
5.1 Models of Lexical Borrowing for Typologically Diverse Languages
We introduced the Swahili–Arabic and Romanian–French borrowing systems. To establish the robustness
and generality of our approach, in future work we will build borrowing systems for a diverse set of languages,
listed in table 12. We selected the list of focus languages, based on the following considerations:
• Recipients are susceptible to borrowing, typologically diverse, and also diverse in terms of availability
of resources, from resource-rich English to extremely resource-poor Yoruba. We also paid attention to
selecting recipient languages that have more than one prominent donor language.
• Donors are resource-rich and typologically diverse.
• Donor–recipient language pairs have been extensively studied in contact linguistics, in particular using
Optimality Theoretic view, and linguistic studies contain lexicons of donor–loanword examples that we
can use as training sets.
• Availability of pronunciation dictionaries (or phonographic writing system); availability of small para￾llel corpora, dependency treebanks and POS tagged corpora to enable extrinsic evaluation; and, when
possible, language presence it Twitter data.
5.2 Models of Lexical Borrowing in Cross-Lingual Core-NLP
Approaches to low-resource NLP can roughly be categorized into unsupervised (Christodoulopoulos et al.
2010, Berg-Kirkpatrick and Klein 2010, Cohen et al. 2011, Naseem et al. 2012), and semi-supervised me￾thods relying on cross-lingual projection from resource-rich languages via parallel data. Cross-lingual semi￾supervised learning strategies of syntactic structure—both shallow and deep—have been a promising vein
of research over the last years; we will continue this research direction, but will augment or replace word
alignments with multilingual borrowing lexicons.
The majority of semi-supervised approaches project annotations from English, both in POS tagging
(Yarowsky et al. 2001, Das and Petrov 2011, Li et al. 2012, Täckström et al. 2013), and in induction of
dependency relations (Wu 1997, Kuhn 2004, Smith and Smith 2004, Hwa et al. 2005, Xi and Hwa 2005,
Burkett and Klein 2008, Snyder et al. 2009, Ganchev et al. 2009, Tiedemann 2014). We hypothesize that
in the case of syntactic annotation, projection via borrowing is a more plausible method than projection via
18

---

## Trang 20

Recipient Family # speakers
(millions) Resource-rich donors Studies on lexical borrowing
English Germanic 1500 French, German, Spanish, Arabic (Grant 2009, Durkin 2014)
Russian Slavic 260 English (Benson 1959, Styblo Jr 2007)
Japanese Altaic 125 English, Chinese (Kay 1995, Daulton 2008, Schmidt 2009)
Vietnamese Austro-Asiatic 80 Chinese, French (Barker 1969, Alves 2009)
Korean Koreanic 75 English, Chinese (Kang 2003, Kenstowicz 2005)
Swahili Bantu 40 Arabic (Mwita 2009, Schadeberg 2009)
Yoruba Edekiri 28 English (Ojo 1977, Kenstowicz 2006)
Romanian Romance 24 French (Friesner 2009, Schulte 2009)
Quechua Quechuan 9 Spanish (Rendón 2008, Rendón and Adelaar 2009)
Hebrew Semitic 7.5 English, Arabic (Schwarzwald 1998, Cohen 2009; 2013)
Finnish Uralic 5 German, English (Orešnik 1982, Kallio 2006, Johnson 2014)
Tab. 12: Recipient and donor languages to be used for borrowing systems constructed in this project.
word alignment, especially when large parallel corpora are unavailable. First, projecting via borrowing will
enable annotation projection from typologically more similar languages to the target language. For example,
some Austronesian languages (e.g., Malagasy) have borrowed extensively from Arabic, and these are typolo￾gically closer to Arabic than to English (e.g., like Arabic, these are verb-subject-object languages). Second,
linguistic studies report statistics on “borrowability” of syntactic categories pertaining to specific languages;
Haspelmath and Tadmor (2009), for example, provide relative percentages of loan nouns, verbs, adjectives,
and adverbs for 41 languages. We will use this prior knowledge to bias the learned taggers/parsers. Finally,
integrating borrowing will allow us to use signals from multiple source languages, which have proven to
work better than solely exploiting English (McDonald et al. 2011, Berg-Kirkpatrick and Klein 2010, Cohen
et al. 2011, Naseem et al. 2012).
We will experiment with existing cross-lingual approaches to POS tagging (cf. Täckström et al. 2013),
adapted to projecting via donor–loan lexicons. There, we will employ borrowing both in projecting token
annotations (in addition to or instead of parallel corpora), and in projecting tag dictionaries. Similarly, we
will adapt techniques for cross-lingual dependency grammar induction (cf. McDonald et al. 2011). Prior
work on non-parallel cross-lingual structure prediction has already shown that phylogenetic relations are a
valuable signal (Berg-Kirkpatrick and Klein 2010), and we will continue this vein of research, focusing on
non-parallel projection via borrowing.
The universal POS tagset (Petrov et al. 2012) and the universal dependency treebank (McDonald et al.
2013) will be used to train resource-rich taggers/parsers, the sources of projection. We will use the Leipzig
Corpora Collection (Biemann et al. 2007) as a source of monolingual data, and publicly available parallel or
multi-parallel corpora such as WIT3
(translated TED talks) (Cettolo et al. 2012) and Common Crawl parallel
data (Smith et al. 2013) for translation and cross-lingual projection. In addition, we will use Wiktionary25
as a source of multilingual tag dictionaries (cf. Li et al. 2012, Garrette and Baldridge 2013), and the World
Atlas of Language Structures (WALS) (Dryer and Haspelmath 2013) as a source of linguistic typological
features (cf. Naseem et al. 2012). We will evaluate an accuracy our taggers and parsers on existing tagged
and parsed corpora (e.g., Erjavec 2004, Hajic et al. 2009). We will also evaluate the effectiveness of our ˇ
methodology by simulating resource-rich to resource-poor scenario in a resource-rich language pair (e.g.,
English–Spanish, English–French). We will conduct manual qualitative evaluation and error analysis, and,
25www.wiktionary.org
19

---

## Trang 21

importantly, will investigate the impact of typological similarity on the quality of cross-lingual projection.
5.3 Modeling the Sociolinguistic Aspects of Lexical Borrowing
As pointed out by Appel and Muysken (2005; p. 174), the literature on lexical borrowing combines an im￾mense number of case studies with the absence of general works. Linguistic case studies focus on morpho￾phonological properties of lexical, morphological, phonological, and grammatical borrowing; sociolinguis￾tic case studies explore social and cultural determinants of borrowing. While in the first phases of this
research we will develop general data-driven approaches to identify and model lexical borrowing as a lin￾guistic phenomenon, the goal of the current phase is to develop general approaches to statistically model
borrowing as a social and cultural phenomenon. We will focus on two research questions: (1) what are
demographic and geographic conditions to the emergence and diffusion of borrowing?; and (2) is there a
correlation between socio-political status quo in contact communities and meaning/semantic polarity that
loanwords acquire in borrowing? Answering these questions using robust statistical methods, will help
researchers better understand and exploit lexical borrowing in NLP applications. In addition, these com￾putational studies will corroborate or refute the generality of claims made in individual sociolinguistic case
studies on borrowing, thereby contributing to sociolinguistic research.
5.3.1 Emergence and Diffusion of Borrowing
Linguistic borrowing emerges in bilingualism over time; wider-spread and longer language contact triggers
more common and more far-reaching borrowing (McMahon 1994). Twitter and other social media cor￾pora provide particularly fruitful conditions to investigate the emergence and diffusion of lexical borrowing:
these texts are an example of rapid language development, of emergence and diffusion of neologisms (An￾droutsopoulos 2000, Anis 2007, Herring 2012), of dense interaction between diverse multilingual popula￾tions all over the world. Importantly, written neologisms—“neography” (Anis 2007)—are often phonetic
forms of spoken words, and, as recent research shows, are influenced by the phonological system of the
source language (Eisenstein 2013; 2015). Presence of morpho-phonological influence indicates some level
of linguistic adaptation, i.e., borrowing. While previous studies investigated the emergence and diffusion
of lexical change in English Twitter data, relying only on word frequencies (Eisenstein et al. 2014), our
goal is to extend this research direction to multiple languages/dialects, and to explore examples containing
morpho-phonological signals.
We will first learn to distinguish borrowed items among all neologisms, using the classifiers and learned
morpho-phonological features from the first phase of this research. Then, we will investigate demographic
and geographic factors influencing borrowing and its linguistic pathways (cf. Eisenstein et al. 2014): web￾user age, social status, influence, geographic location, and metropolitan area influence. Our research hypo￾theses, based on linguistic accounts (Guy 1990, McMahon 1994, Sankoff 2002, Appel and Muysken 2005;
among many others), are that borrowing emerges “from above”, i.e., being initiated by higher-influence gro￾ups (of users, locations, languages) and adopted “from below”, by lower-influence groups (as in the Labov’s
seminal work on dialect importation (1966)); that while phonetic transcription and context-switching are
used by younger users, borrowing requires mature linguistic experience of adults to correctly identify and
adopt the borrowed features.
20

---

## Trang 22

5.3.2 Relation between Prestige and Sentiment Polarity in Borrowing
Susceptibility of a language to borrowing is determined by both linguistic and socio-political factors. Lin￾guistic considerations involve attempts to fill a lexical gap for a concept that has no word in the recipient
language (new information or technology, contact with foreign culture, or foreign flora and fauna, etc.).
Socio-political factors are determined by political and social prestige. Presumably, speakers borrow from
a prestige-group, although not always—when loanwords enter from less prestigious to more prestigious
language, these often connote derogatory meanings (McMahon 1994). For example, Romanian loanwords
from Slavic tend to have positive semantic orientation, while loanwords from Turkish have more negative
connotations, e.g., prieten ‘friend’ (Romanian, borrowed from Slavic prijatel) vs. dus,man ‘enemy’ (from
Turkish dü¸sman) (Schulte 2009). Turkish, in turn, frequently borrowed words from Arabic and Persian,
but with the founding of the modern Turkish state and the related rise of nationalism and national identity,
this borrowing ceased more or less instantly (Curnow 2001). We will conduct a qualitative study to measure
correlation between sentiment polarity of borrowed words and prestige relations of lending/borrowing users.
Studies on emergence and diffusion of borrowing, and on dynamics in semantics of borrowing can shed
new light to the longstanding goal of social studies—linguistic and computational—understanding the rela￾tionship between social forces and linguistic outcomes. Practically, this study will result in new analytics
tools that can improve social media applications analyzing and predicting human behavior, e.g., predicting
public opinion from social media feeds (O’Connor et al. 2010), predicting personal attributes like geogra￾phic location, age, gender, and race/ethnicity of social media users (Nguyen et al. 2011, Mislove et al.
2011), measuring power differences between individuals based the patterns of words they speak or write
(Danescu-Niculescu-Mizil et al. 2012).
In all our experiments we will use geo-tagged Twitter data from the Twitter Gardenhose stream, which
is a sample of approximately 10% of all publicly available Twitter messages (tweets). In addition to the
messages themselves, we have information about the identity of the message sender, whether or not it was
a “retweet” of another message, partial information from the “follower graph,” and, for some subset of
the tweets, geographic location of the message sender (which can be, e.g., correlated with demographic
information). All donor and recipient focus languages—except Swahili, Yoruba, and Quechua—are well￾represented in the CMU Twitter archive (table 13).
6 Timeline
• Summer 2015: finalize models of borrowing for multiple languages (§5.1); publicly release multilingual
borrowing lexicons.
• Summer, Fall 2015: investigate integrating borrowing in core-NLP (§5.2); submit a TACL paper.
• Spring, Summer 2016: explore borrowing in social media in monolingual and cross-lingual settings
(§5.3); write a paper.
• Summer 2016: thesis defense
21

---

## Trang 23

Language # of tweets
English 12,194,934
Japanese 6,257,572
Spanish 4,444,441
Arabic 1,963,931
French 792,591
Korean 456,838
Russian 428,989
German 184,889
Finnish 57,214
Vietnamese 17,594
Chinese 14,435
Romanian 7,555
Hebrew 4,835
Tab. 13: Statistics of the multilingual tweets.
References
Allison N Adler. Faithfulness and perception in loanword adaptation: A case study from Hawaiian. Lingua,
116(7):1024–1045, 2006.
Sang-Cheol Ahn and Gregory K Iverson. Dimensions in Korean laryngeal phonology. Journal of East Asian
Linguistics, 13(4):345–379, 2004.
Yaser Al-Onaizan and Kevin Knight. Machine transliteration of names in Arabic text. In Proc. the ACL
workshop on Computational Approaches to Semitic Languages, pages 1–13, 2002.
Cyril Allauzen, Michael Riley, Johan Schalkwyk, Wojciech Skut, and Mehryar Mohri. OpenFst: A general
and efficient weighted finite-state transducer library. In Implementation and Application of Automata,
pages 11–23. Springer, 2007.
Mark Alves. Loanwords in Vietnamese. In Martin Haspelmath and Uri Tadmor, editors, Loanwords in the
World’s Languages: A Comparative Handbook, pages 617–637. Max Planck Institute for Evolutionary
Anthropology, 2009.
Waleed Ammar, Chris Dyer, and Noah A. Smith. Transliteration by sequence labeling with lattice encodings
and reranking. In Proc. NEWS workshop at ACL, 2012.
Waleed Ammar, Victor Chahuneau, Michael Denkowski, Greg Hanneman, Wang Ling, Austin Matthews,
Kenton Murray, Nicola Segall, Yulia Tsvetkov, Alon Lavie, and Chris Dyer. The cmu machine translation
systems at WMT 2013: Syntax, synthetic translation options, and pseudo-references. In Proc. WMT,
2013.
Jannis K Androutsopoulos. Non-standard spellings in media texts: The case of German fanzines. Journal
of Sociolinguistics, 4(4):514–533, 2000.
Jacques Anis. Neography: Unconventional spelling in French SMS text messages. The multilingual internet:
Language, culture, and communication online, pages 87–115, 2007.
René Appel and Pieter Muysken. Language contact and bilingualism. Amsterdam University Press, 2005.
Milton E Barker. The phonological adaptation of French loanwords io Vietnamese. Mon-Khmer Studies
Journal, 3:138–147, 1969.
Morton Benson. English loanwords in Russian. The Slavic and East European Journal, 3(3):248–267, 1959.
22

---

## Trang 24

Taylor Berg-Kirkpatrick and Dan Klein. Phylogenetic grammar induction. In Proc. ACL, pages 1288–1297,
2010.
Chris Biemann, Gerhard Heyer, Uwe Quasthoff, and Matthias Richter. The leipzig corpora collection￾monolingual corpora of standard size. In Proc. Corpus Linguistic, 2007.
Alan D Blair and John Ingram. Learning to predict the phonological structure of English loanwords in
Japanese. Applied Intelligence, 19(1-2):101–108, 2003.
Paul Boersma and Bruce Hayes. Empirical tests of the gradual learning algorithm. Linguistic inquiry, 32
(1):45–86, 2001.
Ondˇrej Bojar, Christian Buck, Christian Federmann, Barry Haddow, Philipp Koehn, Johannes Leveling,
Christof Monz, Pavel Pecina, Matt Post, Herve Saint-Amand, Radu Soricut, Lucia Specia, and Aleš
Tamchyna. Findings of the 2014 workshop on statistical machine translation. In Proc. WMT, pages
12–58, 2014.
Ellen Broselow. Language contact phonology: richness of the stimulus, poverty of the base. In Proc. NELS,
volume 34, pages 1–22, 2004.
David Burkett and Dan Klein. Two languages are better than one (for syntactic parsing). In Proc. EMNLP,
pages 877–886, 2008.
Andrea Calabrese and W Leo Wetzels. Loan phonology, volume 307. John Benjamins Publishing, 2009.
Chris Callison-Burch, Philipp Koehn, and Miles Osborne. Improved statistical machine translation using
paraphrases. In Proc. ACL, 2006.
Mauro Cettolo, Christian Girardi, and Marcello Federico. WIT3
: Web inventory of transcribed and translated
talks. In Proc. EAMT, pages 261–268, 2012.
Victor Chahuneau, Eva Schlinger, Noah A Smith, and Chris Dyer. Translating into morphologically rich
languages with synthetic phrases. In Proc. EMNLP, pages 1677–1687, 2013.
Christos Christodoulopoulos, Sharon Goldwater, and Mark Steedman. Two decades of unsupervised POS
induction: How far have we come? In Proc. EMNLP, pages 575–584, 2010.
Evan-Gary Cohen. The role of similarity in phonology: Evidence from loanword adaptation in Hebrew.
PhD thesis, Tel Aviv University, 2009.
Evan-Gary Cohen. The emergence of the unmarked: Vowel harmony in Hebrew loanword adaptation.
Lingua, 131:66–79, 2013.
Shay B. Cohen, Dipanjan Das, and Noah A. Smith. Unsupervised structure prediction with non-parallel
multilingual guidance. In Proc. EMNLP, 2011.
Timothy Jowan Curnow. What language features can be ‘borrowed’. Areal diffusion and genetic inheritance:
problems in comparative linguistics, pages 412–436, 2001.
Cristian Danescu-Niculescu-Mizil, Lillian Lee, Bo Pang, and Jon Kleinberg. Echoes of power: Language
effects and power differences in social interaction. In Proc. WWW, pages 699–708, 2012.
Dipanjan Das and Slav Petrov. Unsupervised part-of-speech tagging with bilingual graph-based projections.
In Proc. ACL, pages 600–609, 2011.
Frank E Daulton. Japan’s built-in lexicon of English-based loanwords, volume 26. Multilingual Matters,
2008.
Hal Daumé III. Non-parametric Bayesian areal linguistics. In Proc. NAACL, pages 593–601, 2009.
Lisa Davidson and Rolf Noyer. Loan phonology in Huave: nativization and the ranking of faithfulness
constraints. In Proc. WCCFL, volume 15, pages 65–79, 1997.
23

---

## Trang 25

Adrià De Gispert and Jose B Marino. Catalan-English statistical machine translation without parallel corpus:
bridging through Spanish. In Proc. LREC, pages 65–68, 2006.
Rohit Dholakia and Anoop Sarkar. Pivot-based triangulation for low-resource languages. In Proc. AMTA,
2014.
Mona Diab and Philip Resnik. An unsupervised method for word sense tagging using parallel corpora. In
Proc. ACL, 2002.
Qing Dou and Kevin Knight. Dependency-based decipherment for resource-limited machine translation. In
Proc. EMNLP, 2013.
Qing Dou, Ashish Vaswani, and Kevin Knight. Beyond parallel data: Joint word alignment and decipher￾ment improves machine translation. In Proc. EMNLP, 2014.
Matthew S Dryer and Martin Haspelmath. Wals online. Max Planck Institute for Evolutionary Anthropology,
Leipzig, 2013.
Philip Durkin. Borrowed Words: A History of Loanwords in English. Oxford University Press, 2014.
Nadir Durrani, Hassan Sajjad, Alexander Fraser, and Helmut Schmid. Hindi-to-Urdu machine translation
through transliteration. In Proc. ACL, pages 465–474, 2010.
Chris Dyer, Adam Lopez, Juri Ganitkevitch, Johnathan Weese, Ferhan Ture, Phil Blunsom, Hendra Setia￾wan, Vladimir Eidelman, and Philip Resnik. cdec: A decoder, alignment, and learning framework for
finite-state and context-free translation models. In Proc. ACL, 2010.
Chris Dyer, Victor Chahuneau, and Noah A. Smith. A simple, fast, and effective reparameterization of IBM
Model 2. In Proc. NAACL, 2013.
Jacob Eisenstein. Phonological factors in social media writing. In Proc. NAACL, pages 11–19, 2013.
Jacob Eisenstein. Systematic patterning in phonologically-motivated orthographic variation. Journal of
Sociolinguistics, 2015.
Jacob Eisenstein, Brendan O’Connor, Noah A Smith, and Eric P Xing. Diffusion of lexical change in social
media. PloS ONE, 9(11):e113114, 2014.
Jason Eisner. Efficient generation in primitive Optimality Theory. In Proc. EACL, pages 313–320, 1997.
Jason Eisner. Comprehension and compilation in Optimality Theory. In Proc. ACL, pages 56–63, 2002.
T Mark Ellison. Phonological derivation in Optimality Theory. In Proc. CICLing, pages 1007–1013, 1994.
Tomaz Erjavec. Multext-east version 3: Multilingual morphosyntactic specifications, lexicons and corpora.
In Proc. LREC, 2004.
Manaal Faruqui and Chris Dyer. Improving vector space word representations using multilingual correlation.
In Proc. EACL, 2014.
Michael L Friesner. The adaptation of romanian loanwords from Turkish and French. Calabrese & Wetzels
(2009), pages 115–130, 2009.
Kuzman Ganchev, Jennifer Gillenwater, and Ben Taskar. Dependency grammar induction via bitext projec￾tion constraints. In Proc. ACL, pages 369–377. Association for Computational Linguistics, 2009.
Matt Garley and Julia Hockenmaier. Beefmoves: dissemination, diversity, and dynamics of English bor￾rowings in a German hip hop forum. In Proc. ACL, pages 135–139, 2012.
Dan Garrette and Jason Baldridge. Learning a part-of-speech tagger from two hours of annotation. In Proc.
HLT-NAACL, pages 138–147, 2013.
Sharon Goldwater and Mark Johnson. Learning OT constraint rankings using a maximum entropy model.
In Proc. the Stockholm workshop on variation within Optimality Theory, pages 111–120, 2003.
24

---

## Trang 26

D. Graff, J. Kong, K. Chen, and K. Maeda. English gigaword third edition, 2007.
Anthony Grant. Loanwords in British English. In Martin Haspelmath and Uri Tadmor, editors, Loanwords in
the World’s Languages: A Comparative Handbook, pages 360–383. Max Planck Institute for Evolutionary
Anthropology, 2009.
Gregory R Guy. The sociolinguistic types of language change. Diachronica, 7(1):47–67, 1990.
Nizar Habash. Four techniques for online handling of out-of-vocabulary words in Arabic-English statistical
machine translation. In Proc. ACL, pages 57–60, 2008.
Nizar Habash, Owen Rambow, and Ryan Roth. MADA+TOKAN: A toolkit for Arabic tokenization, diacri￾tization, morphological disambiguation, POS tagging, stemming and lemmatization. In Proc. MEDAR,
pages 102–109, 2009.
Aria Haghighi, Percy Liang, Taylor Berg-Kirkpatrick, and Dan Klein. Learning bilingual lexicons from
monolingual corpora. In Proc. ACL, pages 771–779, 2008.
Jan Hajic, Jan Hric, and Vladislav Kubo ˇ n. Machine translation of very close languages. In ˇ Proc. ANLP,
pages 7–12, 2000.
Jan Hajic, Massimiliano Ciaramita, Richard Johansson, Daisuke Kawahara, Maria Antònia Martí, Lluís ˇ
Màrquez, Adam Meyers, Joakim Nivre, Sebastian Padó, Jan Štepánek, et al. The conll-2009 shared task: ˇ
Syntactic and semantic dependencies in multiple languages. In Proc. CoNLL: Shared Task, pages 1–18,
2009.
Martin Haspelmath. Lexical borrowing: concepts and issues. Loanwords in the World’s Languages: a
comparative handbook, pages 35–54, 2009.
Martin Haspelmath and Uri Tadmor, editors. Loanwords in the World’s Languages: A Comparative Han￾dbook. Max Planck Institute for Evolutionary Anthropology, Leipzig, 2009. URL http://wold.
clld.org/.
Einar Haugen. The analysis of linguistic borrowing. Language, pages 210–231, 1950.
Kenneth Heafield. KenLM: Faster and smaller language model queries. In Proc. WMT, 2011.
Ulf Hermjakob, Kevin Knight, and Hal Daumé III. Name translation in statistical machine translation￾learning when to transliterate. In Proc. ACL, pages 389–397, 2008.
Susan C Herring. Grammar and electronic communication. The Encyclopedia of Applied Linguistics, 2012.
Hans Henrich Hock and Brian D Joseph. Language history, language change, and language relationship:
An introduction to historical and comparative linguistics, volume 218. Walter de Gruyter, 2009.
Kyril Holden. Assimilation rates of borrowings and phonological productivity. Language, pages 131–147,
1976.
Arvi Hurskainen. Loan words in Swahili. In Katrin Bromber and Birgit Smieja, editors, Globalisation and
African Languages, pages 199–218. Walter de Gruyter, 2004.
Rebecca Hwa, Philip Resnik, Amy Weinberg, Clara Cabezas, and Okan Kolak. Bootstrapping parsers via
syntactic projection across parallel texts. Natural Language Engineering, 11(3), 2005.
Junko Itô and Armin Mester. The core-periphery structure of the lexicon and constraints on reranking.
Papers in Optimality Theory, 18:181–209, 1995.
Haike Jacobs and Carlos Gussenhoven. Loan phonology: perception, salience, the lexicon and OT. Opti￾mality Theory: Phonology, syntax, and acquisition, pages 193–209, 2000.
Frederick Johnson. Standard Swahili-English dictionary. Oxford University Press, 1939.
Mirva Johnson. Trends of loanword origins in 20th century Finnish. Honors Theses, paper 74, 2014.
25

---

## Trang 27

René Kager. Optimality Theory. Cambridge University Press, 1999.
Petri Kallio. On the earliest Slavic loanwords in Finnic. Slavica Helsingiensia, 27:154–166, 2006.
Yoonjung Kang. Perceptual similarity in loanword adaptation: English postvocalic word-final stops in
Korean. Phonology, 20(2):219–274, 2003.
Yoonjung Kang. Loanword phonology. In Mark van Oostendorp, Colin Ewen, Elizabeth Hume, and Keren
Rice, editors, Companion to Phonology. Wiley–Blackwell, 2011.
Shigeto Kawahara. Phonetic naturalness and unnaturalness in Japanese loanword phonology. Journal of
East Asian Linguistics, 17(4):317–330, 2008.
Gillian Kay. English loanwords in Japanese. World Englishes, 14(1):67–76, 1995.
Michael Kenstowicz. The phonetics and phonology of Korean loanword adaptation. In Proceedings of the
first European conference on Korean linguistics, volume 1, pages 17–32, 2005.
Michael Kenstowicz. Tone loans: The adaptation of English loanwords into Yoruba. In Selected proceedings
of the 35th annual conference on African Linguistics, pages 136–146, 2006.
Michael Kenstowicz. Salience and similarity in loanword adaptation: a case study from Fijian. Language
Sciences, 29(2):316–340, 2007.
Michael Kenstowicz and Atiwong Suchato. Issues in loanword adaptation: A case study from Thai. Lingua,
116(7):921–949, 2006.
Reinhard Kneser and Hermann Ney. Improved backing-off for m-gram language modeling. In Proc. ICA￾SSP, volume 1, pages 181–184. IEEE, 1995.
Kevin Knight and Jonathan Graehl. Machine transliteration. Computational Linguistics, 24(4):599–612,
1998.
Philipp Koehn, Franz Josef Och, and Daniel Marcu. Statistical phrase-based translation. In Proc. NAACL￾HLT, pages 48–54, 2003.
Grzegorz Kondrak. Identifying cognates by phonetic and semantic similarity. In Proc. NAACL, pages 1–8,
2001.
Grzegorz Kondrak and Tarek Sherif. Evaluation of several phonetic similarity algorithms on the task of
cognate identification. In Proc. the Workshop on Linguistic Distances, pages 43–50. Association for
Computational Linguistics, 2006.
Grzegorz Kondrak, Daniel Marcu, and Kevin Knight. Cognates can improve statistical translation models.
In Proc. HLT-NAACL, pages 46–48, 2003.
Jonas Kuhn. Experiments in parallel-text based grammar induction. In Proc. ACL, page 470, 2004.
William Labov. The social stratification of English in New York city. 1966.
Shen Li, Joao V Graça, and Ben Taskar. Wiki-ly supervised part-of-speech tagging. In Proc. EMNLP, pages
1389–1398, 2012.
Johann-Mattis List and Steven Moran. An open source toolkit for quantitative historical linguistics. In Proc.
ACL (System Demonstrations), pages 13–18, 2013.
Patrick Littell, Kaitlyn Price, and Lori Levin. Morphological parsing of Swahili using crowdsourced lexical
resources. In Proc. LREC, 2014.
Mohamed Maamouri, Dave Graff, Basma Bouziri, Sondos Krouna, and Seth Kulick. LDC Standard Arabic
morphological analyzer (SAMA) v. 3.1. LDC Catalog No. LDC2010L01. ISBN, pages 1–58563, 2010.
Gideon S Mann and David Yarowsky. Multipath translation lexicon induction via bridge languages. In Proc.
HLT-NAACL, pages 1–8, 2001.
26

---

## Trang 28

Yuval Marton, Chris Callison-Burch, and Philip Resnik. Improved statistical machine translation using
monolingually-derived paraphrases. In Proc. EMNLP, pages 381–390, 2009.
John J McCarthy. Formal problems in Semitic phonology and morphology. PhD thesis, MIT, 1985.
John J McCarthy and Alan Prince. The emergence of the unmarked: Optimality in prosodic morphology.
1994.
John J McCarthy and Alan Prince. Faithfulness and reduplicative identity. Beckman et al. (Eds.), pages
249–384, 1995.
Ryan McDonald, Slav Petrov, and Keith Hall. Multi-source transfer of delexicalized dependency parsers. In
Proc. EMNLP, pages 62–72, 2011.
Ryan T McDonald, Joakim Nivre, Yvonne Quirmbach-Brundage, Yoav Goldberg, Dipanjan Das, Kuzman
Ganchev, Keith B Hall, Slav Petrov, Hao Zhang, Oscar Täckström, et al. Universal dependency annotation
for multilingual parsing. In Proc. ACL, pages 92–97, 2013.
April M S McMahon. Understanding language change. Cambridge University Press, 1994.
Florian Metze, Roger Hsiao, Qin Jin, Udhyakumar Nallasamy, and Tanja Schultz. The 2010 CMU GALE
speech-to-text system. In Proc. INTERSPEECH, pages 1501–1504, 2010.
Tomas Mikolov, Quoc V. Le, and Ilya Sutskever. Exploiting similarities among languages for machine
translation. CoRR, abs/1309.4168, 2013a.
Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S. Corrado, and Jeff Dean. Distributed representations of
words and phrases and their compositionality. In Proc. NIPS, 2013b.
Alan Mislove, Sune Lehmann, Yong-Yeol Ahn, Jukka-Pekka Onnela, and J Niels Rosenquist. Understanding
the demographics of Twitter users. In Proc. ICWSM, pages 554–557, 2011.
Edith Moravcsik. Language contact. Universals of human language, 1:93–122, 1978.
Leonard Chacha Mwita. The adaptation of Swahili loanwords from Arabic: A constraint-based analysis.
Journal of Pan African Studies, 2009.
Carol Myers-Scotton. Contact linguistics: Bilingual encounters and grammatical outcomes. Oxford Uni￾versity Press Oxford, 2002.
Preslav Nakov and Hwee Tou Ng. Improving statistical machine translation for a resource-poor language
using related resource-rich languages. Journal of Artificial Intelligence Research, pages 179–222, 2012.
Tahira Naseem, Regina Barzilay, and Amir Globerson. Selective sharing for multilingual dependency par￾sing. In Proc. ACL, pages 629–637, 2012.
John A Nelder and Roger Mead. A simplex method for function minimization. Computer journal, 7(4):
308–313, 1965.
Shijulal Nelson-Sathi, Johann-Mattis List, Hans Geisler, Heiner Fangerau, Russell D Gray, William Mar￾tin, and Tal Dagan. Networks uncover hidden lexical borrowing in Indo-European language evolution.
Proceedings of the Royal Society B: Biological Sciences, page rspb20101917, 2010.
Dong Nguyen, Noah A. Smith, and Carolyn P. Rosé. Author age prediction from text using linear regres￾sion. In Proc. the ACL Workshop on Language Technology for Cultural Heritage, Social Sciences, and
Humanities, 2011.
Franz Josef Och. Minimum error rate training in statistical machine translation. In Proc. ACL, pages 160–
167, 2003.
Brendan O’Connor, Ramnath Balasubramanyan, Bryan Routledge, and Noah A. Smith. From tweets to
polls: Linking text sentiment to public opinion time series. In Proc. ICWSM, 2010.
27

---

## Trang 29

Valentine Ojo. English-Yoruba language contact in Nigeria. Universität Tübingen, 1977.
Birgitta Orešnik. On the adaptation of English loanwords into Finnish. The English Element in European
Languages, 2:180–212, 1982.
Sebastian Padó and Mirella Lapata. Cross-lingual annotation projection for semantic roles. Journal of
Artificial Intelligence Research, 36(1):307–340, 2009.
Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. BLEU: a method for automatic evaluation
of machine translation. In Proc. ACL, pages 311–318. Association for Computational Linguistics, 2002.
Slav Petrov, Dipanjan Das, and Ryan McDonald. A universal part-of-speech tagset. In Proc. LREC, 2012.
Edgar C Polomé. Swahili Language Handbook. ERIC, 1967.
Alan Prince and Paul Smolensky. Optimality Theory: Constraint interaction in generative grammar. John
Wiley & Sons, 2008.
Reinhard Rapp. Identifying word translations in non-parallel texts. In Pro. ACL, pages 320–322, 1995.
Sujith Ravi and Kevin Knight. Deciphering foreign language. In Proc. ACL, 2011.
Majid Razmara, Maryam Siahbani, Reza Haffari, and Anoop Sarkar. Graph propagation for paraphrasing
out-of-vocabulary words in statistical machine translation. In Proc. ACL, pages 1105–1115, 2013.
J Gómez Rendón. Spanish lexical borrowing in Imbabura Quichua: In search of constraints on language
contact. Empirical Approaches to Language Typology, 39:95, 2008.
J Gómez Rendón and Willem Adelaar. Loanwords in Imbabura Quichua. In Martin Haspelmath and Uri
Tadmor, editors, Loanwords in the World’s Languages: A Comparative Handbook, pages 944–967. Max
Planck Institute for Evolutionary Anthropology, 2009.
Lori Repetti. The emergence of marked structures in the integration of loans in Italian. Amsterdam Studies
in the Theory and History of Linguistic Science Series 4, 274:209, 2006.
Yvan Rose and Katherine Demuth. Vowel epenthesis in loanword adaptation: Representational and phonetic
considerations. Lingua, 116(7):1112–1139, 2006.
Norman C Rothman. Indian Ocean trading links: The Swahili experience. Comparative Civilizations
Review, 46:79–90, 2002.
Avneesh Saluja, Hany Hassan, Kristina Toutanova, and Chris Quirk. Graph-based semi-supervised learning
of translation models from monolingual data. In Proc. ACL, pages 676–686, 2014.
Gillian Sankoff. Linguistic outcomes of language contact. In Jack Chambers, Peter Trudgill, and Natalie
Schilling-Estes, editors, Handbook of Sociolinguistics, pages 638–668. Blackwell, 2002.
Thilo C Schadeberg. Loanwords in Swahili. In Martin Haspelmath and Uri Tadmor, editors, Loanwords in
the World’s Languages: A Comparative Handbook, pages 76–102. Max Planck Institute for Evolutionary
Anthropology, 2009.
Eva Schlinger, Victor Chahuneau, and Chris Dyer. morphogen: Translation into morphologically rich
languages with synthetic phrases. The Prague Bulletin of Mathematical Linguistics, 100:51–62, 2013.
Christopher K. Schmidt. Loanwords in Japanese. In Martin Haspelmath and Uri Tadmor, editors, Loanwords
in the World’s Languages: A Comparative Handbook, pages 545–574. Max Planck Institute for Evolutio￾nary Anthropology, 2009.
Kim Schulte. Loanwords in Romanian. In Martin Haspelmath and Uri Tadmor, editors, Loanwords in the
World’s Languages: A Comparative Handbook, pages 230–259. Max Planck Institute for Evolutionary
Anthropology, 2009.
28

---

## Trang 30

Tanja Schultz and Tim Schlippe. Globalphone: Pronunciation dictionaries in 20 languages. In Proc. LREC,
2014.
Ora Schwarzwald. Word foreignness in modern Hebrew. Hebrew Studies, pages 115–142, 1998.
David A Smith and Noah A Smith. Bilingual parsing with factored estimation: Using english to parse
korean. In Proc. EMNLP, pages 49–56, 2004.
Jason R Smith, Herve Saint-Amand, Magdalena Plamada, Philipp Koehn, Chris Callison-Burch, and Adam
Lopez. Dirt cheap web-scale parallel text from the Common Crawl. In Proc. ACL, pages 1374–1383,
2013.
Benjamin Snyder, Tahira Naseem, and Regina Barzilay. Unsupervised multilingual grammar induction. In
Proc. ACL/AFNLP, pages 73–81, 2009.
Miroslav Styblo Jr. English loanwords in modern Russian language. Master’s thesis, University of North
Carolina, 2007.
Oscar Täckström, Dipanjan Das, Slav Petrov, Ryan McDonald, and Joakim Nivre. Token and type con￾straints for cross-lingual part-of-speech tagging. Transactions of the Association for Computational Lin￾guistics, 1:1–12, 2013.
Oscar Täckström, Ryan McDonald, and Joakim Nivre. Target language adaptation of discriminative transfer
parsers. In Proc. NAACL-HLT, pages 1061–1071, 2013.
Sarah Grey Thomason and Terrence Kaufman. Language contact. Edinburgh University Press Edinburgh,
2001.
Jörg Tiedemann. Rediscovering annotation projection for cross-lingual parser induction. In Proc. COLING,
2014.
Yulia Tsvetkov and Chris Dyer. Cross-lingual bridges with models of lexical borrowing. In Submission to
JAIR, 2015a.
Yulia Tsvetkov and Chris Dyer. Lexicon stratification for translating out-of-vocabulary words. In Submission
to ACL (short), 2015b.
Yulia Tsvetkov, Chris Dyer, Lori Levin, and Archna Bhatia. Generating English determiners in phrase-based
translation with synthetic translation options. In Proc. WMT, 2013.
Yulia Tsvetkov, Leonid Boytsov, Anatole Gershman, Eric Nyberg, and Chris Dyer. Metaphor detection with
cross-lingual model transfer. In Proc. ACL, 2014a.
Yulia Tsvetkov, Florian Metze, and Chris Dyer. Augmenting translation models with simulated acoustic
confusions for improved spoken language translation. In Proc. EACL, pages 616–625, 2014b.
Yulia Tsvetkov, Waleed Ammar, and Chris Dyer. Constraint-based models of lexical borrowing. In Proc.
HLT-NAACL, 2015.
Frans Van Coetsem. Loan phonology and the two transfer types in language contact. Walter de Gruyter,
1988.
Pidong Wang, Preslav Nakov, and Hwee Tou Ng. Source language adaptation for resource-poor machine
translation. In Proc. EMNLP, pages 286–296, 2012.
Uriel Weinreich. Languages in contact: Findings and problems. Walter de Gruyter, 1979.
William Dwight Whitney. On mixture in language. Transactions of the American Philological Association
(1870), pages 5–26, 1881.
Dekai Wu. Stochastic inversion transduction grammars and bilingual parsing of parallel corpora. Computa￾tional linguistics, 23(3):377–403, 1997.
29

---

## Trang 31

Chenhai Xi and Rebecca Hwa. A backoff model for bootstrapping resources for non-English languages. In
Proc. EMNLP, pages 851–858, 2005.
David Yarowsky, Grace Ngai, and Richard Wicentowski. Inducing multilingual text analysis tools via robust
projection across aligned corpora. In Proc. HLT, pages 1–8, 2001.
Moira Yip. Cantonese loanword phonology and Optimality Theory. Journal of East Asian Linguistics, 2(3):
261–291, 1993.
Sharifa Zawawi. Loan words and their effect on the classification of Swahili nominals. Leiden: E.J. Brill,
1979.
30
