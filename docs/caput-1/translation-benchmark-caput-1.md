> [Latin](caput-1.md) | [English](caput-1-en.md) | [Summary](caput-1-summary.md) | Notes | [Model 3.1](caput-1-en-3.1.md) | [Table of Contents](../index.md)

---

# Translation Benchmark & Translator's Notes: Caput I

**Author:** Antigravity (Google DeepMind)  
**Subject:** Comparative Benchmark and Philological Commentary for Chapter 1 (*De Origine Cognitionis Geometricae et de Eius Problematica*, pp. 8–28)  
**Repository:** [geometor/hoenen](https://github.com/geometor/hoenen)  
**Date:** October 1, 2026  

---

## 1. Executive Summary

Chapter 1 of Father Petrus Hoenen's *De Noetica Geometriae* sets the epistemological stage for the entire treatise. In it, Hoenen contrasts the classical Aristotelian-Thomistic doctrine—which grounds geometric knowledge in an intellective intuition of spatial extension abstracted from sensory phantasms—with the modern formalist and axiomatic revolutions of the 19th and 20th centuries.

This benchmark compares the translation produced by **Model 3.1** against the fresh translation executed from scratch by **Antigravity**. The comparison reveals:
1. **Critical Citation Bug Fixes**: Model 3.1 mistook ancient Greek Bekker chapter and line numbers for modern Markdown footnote tags, corrupting the document's link structure.
2. **Elimination of Page-Break Debris**: Unstitched line splits and orphan words from the physical 1954 edition were healed.
3. **Restoration of Aristotelian & Scholastic Terminology**: Deepened precision in rendering Greek epistemology (ἐπιστήμη, νοῦς, ἀξιώματα, ὑποθέσεις, αἰτήματα) and Scholastic concepts (*logica iudicativa*, *intellectus agens*, *extensum ut extensum*).
4. **Historical & Mathematical Contextualization**: Added scholarly notes identifying the German, French, and Greek sources cited by Hoenen (Hilbert, Klein, Poincaré, Study, Einstein, Eudoxus).

---

## 2. Critical Defect Remediations

### A. The "Aristotle Bekker Citation" Hallucination
In § 2 (p. 11 of the 1954 edition), Hoenen cites Aristotle’s *Posterior Analytics* and *De Anima*. The physical text contained citations with numbers such as Book I, chapter 12, Bekker line 77b30:
$$\text{Anal. Post. I 12, 77 b 30} \quad \text{and} \quad \text{De An. III 8, 432 a 5–9}$$
Because the automated transcription scripts wrapped naked digits in brackets, the source text contained:
`Anal. Post. I [^12], 77 b [^30]` and `De An. III [^8]` and `ibid. III [^7]`.

* **Model 3.1 Behavior**: Blindly copied these bracketed numbers directly into the English translation:
  > *"the mind indeed inspects natures by mental intuition (Anal. Post. I [^12], 77 b [^30]): ... Cf. De An. III [^8], 432 a 5-9 ... ibid. III [^7], 431a 14-16"*
  
  In a Markdown viewer, clicking on Aristotle's Chapter 12 or line 30 jumped the reader down to **Footnote 12 (Poincaré on arithmetization)** and **Footnote 8 (Felix Klein on precision thresholds)**!
* **Antigravity Remediation**: Correctly identified the Bekker pagination and chapter divisions of the Aristotelian corpus, removed the false footnote markers, and formatted the citations cleanly:
  > *"...the intellect directly inspects natures through mental intuition (Anal. Post. I, 12, 77b30): 'these things are, as it were, to see by intellection' (ταῦτα δ' ἐστὶν οἷον ὁρᾶν τῇ νοήσει). Cf. De Anima III, 8, 432a5–9 ... ibid. III, 7, 431a14–16"*

### B. The Bogus Footnote 22
At the end of § 4, Hoenen quotes Henri Poincaré’s *La valeur de la science*, citing pages 22–23 (*pagg. 22 sq.*). Because of a line split in the transcription, `(pagg.` was separated from `[^22]: sq.)`.
* **Model 3.1**: Allowed a phantom `[^22]` footnote anchor to linger between Footnote 10 and Footnote 11.
* **Antigravity**: Rejoined the page citation into the body of Footnote 10: `(pp. 22 sq.)`, restoring the footnote numbering to an unbroken sequence from 1 to 14.

### C. Gutter and Margin Dehyphenation
Model 3.1 left several split fragments unmerged:
* `Unum / nunc afferimus` (pp. 10–11)
* `non prop- / ter theoriam` (pp. 12–13)
* `« insieme » omnium / proportionum` (pp. 16–17)
* `” arithmetizare ” conati / sunt` (pp. 19–20)
All of these were smoothly unified into continuous prose in the Antigravity edition.

---

## 3. Side-by-Side Thematic Comparison

| Section & Theme | Model 3.1 Translation | Antigravity Translation | Scholarly & Epistemological Rationale |
| :--- | :--- | :--- | :--- |
| **§ 1: Episteme vs. Nous**<br>`Haec principaliter agunt de « scientia » sensu stricto (ἐπιστήμη)... quae contradistinguitur ab « intellectu » sensu proprio (νοῦς)...` | *These principally treat of "science" in the strict sense (ἐπιστήμη) which constructs apodictic demonstrations, which is contradistinguished from "intellect" in the proper sense (νοῦς) which regards the first principles...* | *These treat principally of "science" in the strict sense (episteme, ἐπιστήμη), which constructs apodictic demonstrations, and which is distinguished from "intellect" or intuitive understanding in the proper sense (nous, νοῦς), which apprehends the first principles...* | Antigravity provides both the Greek script and standard philosophical transliteration, clarifying *nous* as "intuitive understanding" to prevent confusion with generic intellect. |
| **§ 1: Judicative Logic**<br>`Unde processus « logicae iudicativae » per se ducit ad problema: unde oritur in ipsa mente humana cognitio certa principiorum...` | *Whence the process of "judicative logic" by itself leads to the problem: whence arises in the human mind itself the certain knowledge of principles...* | *Whence the process of "judicative logic" leads by its very nature to the fundamental problem: whence arises in the human mind certain knowledge of principles, and whence is obtained certain knowledge of their necessity?* | Emphasizes Hoenen’s central epistemological category: *logica iudicativa* (the logic of judgment, truth, and intentionality) as opposed to purely formal syllogistics. |
| **§ 1: Eliciting Judgments as Specimens**<br>`Ut autem ipsum iudicium diiudicemus non sufficit, ut definitionem quandam generalem iudicii praemittamus... sed revera quaedam iudicia determinata elicienda sunt...` | *...it is not enough that we premise a certain general definition of judgment and resolve it; but indeed certain determinate judgments must be elicited — they must therefore arise in our mind — and these judgments must be considered...* | *...it is not sufficient to posit a general definition of judgment and analyze it abstractly; rather, certain determinate, concrete judgments must be actively elicited—they must arise in our living consciousness—and their origin and validity must be critically inspected.* | Hoenen is making a phenomenological point: epistemology cannot proceed by armchair definition; the philosopher must actively perform a geometric judgment to observe how the mind grasps necessary connections. |
| **§ 2: Objects of Abstraction**<br>`Aristoteles tenebat « mathematica » (τὰ ἐξ ἀφαιρέσεως) haberi per abstractionem...` | *Aristotle held that "mathematicals" (τὰ ἐξ ἀφαιρέσεως) are had by abstraction from sensitive data...* | *Aristotle maintained that "mathematicals" (τὰ ἐξ ἀφαιρέσεως, objects of abstraction) are acquired by abstraction from sensitive data...* | Clarifies Aristotle's technical Greek idiom: τὰ ἐξ ἀφαιρέσεως literally means "things resulting from abstraction." |
| **§ 3: Threshold of Exactitude**<br>`Pro omni cognitione sensitiva adest « limen exactitudinis » quod sensus pertransire non possunt.` | *For all sensitive cognition there is a "threshold of exactitude" which the senses cannot cross over.* | *For all sensory cognition, there exists a finite threshold of exactitude (limen exactitudinis) that the senses cannot transcend.* | Connects directly with Felix Klein's technical mathematical term *Schwellenwert der Genauigkeit*. |
| **§ 3: Einstein's Dilemma**<br>`...in quantum theses mathematicae referuntur ad realitatem, non sunt certae; in quantum certae sunt, non respiciunt realitatem.` | *"in so far as the propositions of mathematics refer to reality, they are not certain, and in so far as they are certain, they do not refer to reality."* | *"Insofar as the propositions of mathematics refer to reality, they are not certain; and insofar as they are certain, they do not refer to reality."* | Quotation from Einstein's celebrated address to the Prussian Academy of Sciences (1921). Hoenen's wry gloss on "$2 \times 2 = 4$" is given its full satirical bite. |
| **§ 4: Ratios vs. Real Numbers**<br>`...sicut Graeci habebant « continuum proportionum » quod est « insieme » omnium proportionum... ita moderni habent continuum numerorum, « insieme » « numerorum realium »...` | *...just as the Greeks had a "continuum of proportions" which is the "ensemble" of all proportions... so the moderns have a continuum of numbers, the "ensemble" of "real numbers"...* | *...just as the Greeks had a "continuum of ratios"—an ensemble of all continuous proportions—so the moderns developed the continuum of real numbers: an ensemble containing not only integers and fractions, but also irrational numbers...* | Hoenen uses Italian *insieme* (set/ensemble), reflecting his Roman academic milieu. Antigravity translates this as "ensemble/set" and specifies the mathematical domain. |
| **§ 6: Hilbert's Formalism**<br>`Cogitamus tria diversa systemata rerum...` | *We think of three different systems of things: the things of the f i r s t system we call points...* | *We think of three different systems of things: the things of the first system we call points and designate them by letters $A, B, C, \dots$...* | Formats mathematical variables with clean KaTeX notation ($A, B, C, \dots$; $a, b, c, \dots$; $\alpha, \beta, \gamma, \dots$) instead of raw typewriter spacing. |

---

## 4. Translator's Commentary & Contextual Notes for Scholars

### 1. Aristotle’s *Posterior Analytics* and the Foundations of Geometry
In § 1, Hoenen argues that Aristotle used geometry not merely as one convenient example among many, but as the **paradigmatic type** of demonstrative science. The distinction between an **axiom** (ἀξίωμα, a proposition whose truth is immediately evident to anyone who understands the terms) and a **postulate** (αἴτημα, a proposition not self-evident which must be assumed on trust or demonstrated by a higher science) is the historical foundation of all subsequent axiomatic debates.

### 2. The *Intellectus Agens* and Mathematical Intuition
In § 2, Hoenen stakes out his Thomistic position against both Kantian subjectivism and modern formalist nominalism. For Hoenen, mathematical abstraction is not a passive sensory registration, nor an imposition of a subjective mental form (Kant), but an active intellective penetration:
$$\text{Sensory Phantasm} \xrightarrow{\text{Intellectus Agens}} \text{Intelligible Nature (Extensum ut Extensum)}$$
The mind "sees through intellection" (ὁρᾶν τῇ νοήσει) the necessary relations embedded in the quantitative essence of the phantasm.

### 3. The Arithmetization of the Continuum (Klein, Poincaré, Hölder)
In § 4, Hoenen addresses the late 19th-century movement led by Weierstrass, Dedekind, and Cantor to eliminate spatial intuition from mathematics in favor of purely arithmetic set theory. Hoenen shows profound sympathy with Poincaré’s lament that purely arithmetic definitions "strip the continuum of its intuitive richness." Hoenen presciently notes that while arithmetization is formally legitimate, it cannot solve the philosophical problem of how mathematics relates to real physical space.

### 4. Axiomatics and the Problem of Mathematical Existence
In § 6, Hoenen evaluates David Hilbert’s formal axiomatization. Hoenen does not dismiss Hilbert; on the contrary, he praises axiomatics for its ability to isolate the minimal independent premises of a theorem and to demonstrate consistency. However, Hoenen insists that formal consistency is only a negative criterion of truth; it does not replace the intellect's grasp of objective essences. He points toward the Thomistic theory of *possibilia*—beings whose notes contain no internal contradiction—as the proper ontological home for modern non-Euclidean spaces.

---

## 5. Status & Next Step

* Translation [`docs/caput-1-en.md`](caput-1-en.md) is complete and verified.
* All 14 footnotes are checked and fully expanded.
* Ready to proceed to **Chapter 2 (*De Problemate Necessitatis*, pp. 29–64)**.

---

> [Latin](caput-1.md) | [English](caput-1-en.md) | [Summary](caput-1-summary.md) | Notes | [Model 3.1](caput-1-en-3.1.md) | [Table of Contents](../index.md)
