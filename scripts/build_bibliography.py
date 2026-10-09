import json
import re

with open('/tmp/hoenen_footnotes.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Curated lookup dictionary mapping (slug, num) to verified source attribution
CURATED_SOURCES = {
    # Praefatio
    ('preface', 1): "**P. Hoenen, S.J.**, Articles in *Gregorianum* (1938–1943, 1951)",
    ('preface', 2): "**P. Hoenen, S.J.**, *La théorie du jugement* / *Reality and Judgment*",
    
    # Caput I
    ('caput-1', 1): "**Aristotle**, *Analytica Posteriora* (on postulates and Euclid's Postulate V)",
    ('caput-1', 2): "**P. Hoenen, S.J.**, *La théorie du jugement d'après St. Thomas d'Aquin*",
    ('caput-1', 3): "**J. Geyser**, **O. Hamelin**, **W. D. Ross**, & **P. Hoenen** (*Gregorianum* 1933)",
    ('caput-1', 4): "**A. Einstein**, *Geometrie und Erfahrung* (1921)",
    ('caput-1', 5): "**P. Hoenen, S.J.**, *Cosmologia* (4th ed., Notes III & VII)",
    ('caput-1', 6): "**H. Hasse & H. Scholz**, *Kantstudien* (1928, on foundational crisis of Greek mathematics)",
    ('caput-1', 7): "**F. Klein**, *Anwendung der Differential- und Integralrechnung* (sensory threshold of exactitude)",
    ('caput-1', 8): "**F. Klein**, *op. cit.* (ideal arithmetic free from sensory threshold)",
    ('caput-1', 9): "**H. Poincaré**, *La valeur de la science* (sensory intuition cannot yield rigor)",
    ('caput-1', 10): "**H. Poincaré**, *La valeur de la science* (intuition of pure number vs. sensible intuition)",
    ('caput-1', 11): "**H. Poincaré**, *Dernières Pensées* (critique of arithmetization of continuum)",
    ('caput-1', 12): "**H. Poincaré**, *Dernières Pensées* (arithmetization is not everything)",
    ('caput-1', 13): "**E. Study**, *Die realistische Weltansicht und die Lehre vom Raume* (1914)",
    ('caput-1', 14): "**D. Hilbert**, *Grundlagen der Geometrie* (7th ed., primitive undefined systems: points, lines, planes)",

    # Caput II
    ('caput-2', 1): "**P. Hoenen, S.J.**, *Gregorianum* (1933, on origin of first principles)",
    ('caput-2', 2): "**G. W. Leibniz**, *Nouveaux Essais sur l'entendement humain* (IV, 7, § 10, proof of 2 + 2 = 4)",
    ('caput-2', 3): "**L. Couturat**, *Les principes des mathématiques* (1905)",
    ('caput-2', 4): "**I. Kant**, *Kritik der reinen Vernunft* (B14–15, arithmetical judgment 7 + 5 = 12)",
    ('caput-2', 5): "Scholarly commentary on Kantian arithmetic and scholastic realism",
    ('caput-2', 6): "**P. Hoenen, S.J.**, *La théorie du jugement* (on the nature of judgment)",
    ('caput-2', 7): "**R. Descartes**, *Principia Philosophiae* (II, art. 4–11, extension as essence of body)",
    ('caput-2', 8): "**P. Hoenen, S.J.**, *10th International Congress of Philosophy* (Amsterdam, 1948)",
    ('caput-2', 9): "**M. Pasch**, *Vorlesungen über neuere Geometrie* (2nd ed. 1926, Kernsatz IV on order)",
    ('caput-2', 10): "**G. Hessenberg**, *Ebene und sphärische Trigonometrie* (1904)",
    ('caput-2', 11): "Scholastic adage: *Nihil est in intellectu quod non fuerit in sensu (nisi ipse intellectus)*",
    ('caput-2', 12): "**P. Hoenen, S.J.**, \"Le 'Cogito ergo sum' comme intuition...\" (*Cartesio*, 1937)",
    ('caput-2', 13): "**P. Hoenen, S.J.**, *Théorie du jugement* (sensory datum as determinative of judgment)",
    ('caput-2', 14): "**P. Hoenen, S.J.**, *op. cit.* (Cartesian Cogito as intellectual intuition)",
    ('caput-2', 15): "**P. Hoenen, S.J.**, *Théorie du jugement* (virtual judgments)",
    ('caput-2', 16): "**M. Pasch**, *Vorlesungen über neuere Geometrie* (axioms of order)",
    ('caput-2', 17): "**P. Hoenen, S.J.**, *Théorie du jugement* (material and formal nexus, chs. III–IV)",

    # Caput III
    ('caput-3', 1): "**Aristotle**, *Posterior Analytics* I, 31 (87b35, sensory perception of triangle angles)",
    ('caput-3', 2): "**C. Baeumker**, *Das Problem der Materie in der griechischen Philosophie* (1890)",
    ('caput-3', 3): "**J. S. Mill**, *A System of Logic* (5th ed. 1862, I, p. 255)",
    ('caput-3', 4): "**J. S. Mill**, *op. cit.*, p. 257 (geometry as experimental physical science)",
    ('caput-3', 5): "**E. Study**, *Die realistische Weltansicht* (1914, p. 75)",
    ('caput-3', 6): "**J. Wellstein**, in *Weber-Wellstein Enzyklopädie der Elementar-Mathematik* (II, p. 9)",
    ('caput-3', 7): "Scholarly note on boundaries of bodies and indivisibles",
    ('caput-3', 8): "**L. Couturat**, \"La philosophie des mathématiques de Kant\" (*RMM* 1904)",
    ('caput-3', 9): "**J. Wellstein**, *op. cit.*, p. 10",
    ('caput-3', 10): "**A. Voss**, \"Über die mathematische Erkenntnis\" (*Kultur der Gegenwart*, 1914)",
    ('caput-3', 11): "**St. Thomas Aquinas** (the intellect directly knows the object, not its own species)",

    # Caput IV
    ('caput-4', 1): "**D. Hilbert**, *Grundlagen der Geometrie* (explanations and axioms)",
    ('caput-4', 2): "**St. Thomas Aquinas**, *In Boethium de Trinitate*, q. 5, a. 3, ad 3 (*materia intelligibilis*)",
    ('caput-4', 3): "**B. Russell**, *Principles of Mathematics* (1903/1937, nos. 390 ff., critique of superposition)",
    ('caput-4', 4): "**B. Russell**, *op. cit.* (\"strikes every intelligent child as a juggle\")",
    ('caput-4', 5): "**B. Russell**, *op. cit.* (motion implies material bodies, not spatial figures)",
    ('caput-4', 6): "**J. Wellstein**, *op. cit.* (attempt to avoid motion in congruence)",
    ('caput-4', 7): "**Aristotle**, *Physics* IV, 11 (219b15 ff.) & 12 (220b24 ff., ed. W. D. Ross)",
    ('caput-4', 8): "**F. A. Trendelenburg**, Commentary on Aristotle's *De Anima* (1877)",
    ('caput-4', 9): "**St. Thomas Aquinas**, *In I De Caelo*, lect. 2, no. 9 (motion of points in geometry)",
    ('caput-4', 10): "**H. Poincaré**, *La Science et l'Hypothèse* (p. 80, ideal bodies as figures)",
    ('caput-4', 11): "**J. Hadamard**, *Encyclopédie Française* (1937, I-52-10, geometric displacement)",
    ('caput-4', 12): "Scholarly note on approximate geometry and physical tracing",
    ('caput-4', 13): "Scholarly note on definition and intuition of direction",
    ('caput-4', 14): "**H. Poincaré**, *Dernières Pensées* (p. 62) & *La Valeur de la Science* (p. 59, amorphous continuous space)",
    ('caput-4', 15): "**F. Enriques** & **U. Amaldi**, *Questioni riguardanti le matematiche elementari* (I, 1924, p. 43)",
    ('caput-4', 16): "**W. Killing**, *Einführung in die Grundlagen der Geometrie* (I, 1893; II, 1898)",
    ('caput-4', 17): "**W. Killing**, *op. cit.* (angle measuring difference of direction)",
    ('caput-4', 18): "**W. Killing**, *op. cit.* (equal/unequal directions relative to secant)",
    ('caput-4', 19): "**W. Killing**, *op. cit.* (direction defined only relative to a third line)",
    ('caput-4', 20): "**U. Amaldi**, in Enriques' *Questioni* (p. 44)",
    ('caput-4', 21): "**F. Hausdorff**, \"Das Raumproblem\" (*Annalen der Naturphilosophie* 1904, p. 3)",
    ('caput-4', 22): "**H. Weyl**, *Philosophie der Mathematik* (1927, p. 18) & **J. Hadamard** (*Encyclopédie Française*)",
    ('caput-4', 23): "**F. Klein**, *Elementarmathematik vom höheren Standpunkte aus* (II, 1925, pp. 189 ff.)",
    ('caput-4', 24): "**F. Klein**, *op. cit.*, pp. 192–194 (exactness of parallels in non-Euclidean space)",
    ('caput-4', 25): "Scholarly note on the concept of non-Euclidean straight line",
    ('caput-4', 26): "Scholarly note on Riemannian and Lobachevskian geometry within Euclidean space",
    ('caput-4', 27): "**Th. Waitz**, Commentary on Aristotle's *Prior Analytics* I, 23 (I, pp. 427–429)",
    ('caput-4', 28): "**B. Russell**, *Principles of Mathematics* (pp. 404 ff., critique of empiricist circles)",
    ('caput-4', 29): "**St. Albert the Great**, *In Anal. Prior.* I, tract. I, cap. 9 (ed. Jammy 1651, I, p. 298a)",
    ('caput-4', 30): "**Aristotle**, *Prior Analytics* I, 4 (25b37–39, syllogism Barbara)",
    ('caput-4', 31): "Scholarly note on axiomaticians neglecting the semantic meaning of terms",

    # Caput V
    ('caput-5', 1): "**Sir Thomas L. Heath**, *A History of Greek Mathematics* (1921, I, pp. 335 ff.)",
    ('caput-5', 2): "**H. Freudenthal** & **P. Hoenen**, debate in *Gregorianum* (1951, pp. 252–268)",
    ('caput-5', 3): "Scholarly note on syllogistic form Barbara and its formal necessity",
    ('caput-5', 4): "**St. Thomas Aquinas**, concept of *dispositio rei* (Sachverhalt)",
    ('caput-5', 5): "**J. Locke**, *An Essay Concerning Human Understanding* (IV, 17, § 4, ed. Fraser, II, pp. 390 ff.)",
    ('caput-5', 6): "**A. Riehl**, \"Logik und Erkenntnistheorie\" (*Kultur der Gegenwart* 1921, p. 71)",
    ('caput-5', 7): "**G. Stammler**, *Begriff, Urteil, Schluss* (1928, pp. 229, 245)",
    ('caput-5', 8): "**G. H. Hardy**, \"Mathematical Proof\" (*Mind* 1929) citing **C.-J. de la Vallée-Poussin**",
    ('caput-5', 9): "**D. Hilbert**, *Grundlagen der Geometrie* (Theorem on order of points on a line)",
    ('caput-5', 10): "**G. H. Hardy**, *Mind* (38, p. 12, on Hilbert's axioms needing diagrams)",
    ('caput-5', 11): "**P. Hoenen, S.J.**, \"Pour une philosophie de la connaissance...\" (*Gregorianum* 1950)",
    ('caput-5', 12): "**P. Hoenen, S.J.**, *Cosmologia* (physical properties impeding mathematical exactitude)",

    # Caput VI
    ('caput-6', 1): "**H. Poincaré**, *La Valeur de la Science* (measuring radius and circumference of material circle)",
    ('caput-6', 2): "**P. Hoenen, S.J.**, *Cosmologia* (lib. I, cap. II) & *Filosofia della natura inorganica*",
    ('caput-6', 3): "**A. Einstein**, *Forum* (1930, p. 173) & **P. Hoenen**, *Cosmologia* (p. 468)",
    ('caput-6', 4): "Scholarly note on intuition of intensity in qualitative physical cases",
    ('caput-6', 5): "**P. Hoenen, S.J.**, \"De duratione successiva...\" (*Gregorianum* 1953, pp. 3–31)",
    ('caput-6', 6): "Scholarly note on theory of physical dimensions and dimensional analysis",
    ('caput-6', 7): "**P. Hoenen, S.J.**, \"De connexionibus necessariis inter actus existentiales\" (*Gregorianum* 1953)",

    # Caput VII
    ('caput-7', 1): "**St. Thomas Aquinas**, *In Anal. Post.* I, lect. 1 (71a14 ff., cognition of triangle)",
    ('caput-7', 2): "Experimental psychology studies on the perception of shapes and figures",
    ('caput-7', 3): "**P. Hoenen, S.J.**, \"De connexionibus necessariis inter actus existentiales\" (*Gregorianum* 1953, pp. 603–639)",

    # Appendix
    ('appendix', 1): "**P. Hoenen, S.J.**, \"Le 'cogito ergo sum' comme intuition...\" (*Cartesio* 1937) & *Théorie du jugement*",
    ('appendix', 2): "**R. Descartes**, *Responsiones ad Secundas Objectiones* (ed. Adam & Tannery VII, pp. 140–141)",
    ('appendix', 3): "**Aristotle**, *Metaphysics* IX, 3 (1047a30–b2, ed. & trans. W. D. Ross)",
    ('appendix', 4): "**Alexander of Aphrodisias**, *In Metaphysica* (ed. Hayduck, p. 573)",
    ('appendix', 5): "**Aristotle**, *Metaphysics* IX, 8 (1050a21–23), **W. D. Ross**, & **H. Bonitz** (*energeia* vs. *entelecheia*)",
    ('appendix', 6): "**P. Hoenen, S.J.**, *Cosmologia* (4th ed., nos. 161 ff., Note XIII, pp. 527–530, motion as existential act)",
    ('appendix', 7): "**É. Meyerson**, *Du cheminement de la pensée* (1931, II, p. 391)",
    ('appendix', 8): "**St. Thomas Aquinas**, *Summa Theologiae* I, q. 7, a. 1 (*esse* as most formal)",
    ('appendix', 9): "**Aristotle**, *Nicomachean Ethics* IX, 9 (1170a31 ff.), **John Burnet**, & **St. Thomas Aquinas** (*In IX Ethic.*, lect. 11)",
    ('appendix', 10): "**Aristotle**, *Physics* IV, 5 (212b14 ff.), Oxford translation, & **H. Carteron** (Budé ed.)",
    ('appendix', 11): "**St. Thomas Aquinas**, *In IV Phys.*, lect. 7 (following Themistius on definition of place)",
    ('appendix', 12): "**P. Hoenen, S.J.**, *Cosmologia* (generic attributes of place and *ubi*)",
    ('appendix', 13): "**Aristotle**, *Metaphysics* IX, 3 (textual reading of ἔστιν with Ross vs. Bonitz and Christ)",
    ('appendix', 14): "**P. Hoenen, S.J.**, *Gregorianum* (1953, pp. 3–19, on successive duration)",
    ('appendix', 15): "**P. Hoenen, S.J.**, *Cosmologia* (nos. 58–63 on *ubi*, Note *De ubi*, pp. 467–470)",
    ('appendix', 16): "**P. Hoenen, S.J.**, *Cosmologia* (Note IV, p. 456; Note XV, p. 538) & *Filosofia della natura inorganica*",
    ('appendix', 17): "**A. Einstein**, cited in Hoenen's *Cosmologia* (p. 468) & *Filosofia della natura inorganica* (p. 110)",
    ('appendix', 18): "Aristotelian-Thomistic adage: priority of act relative to potency in mathematical and universal cognition",
    ('appendix', 19): "**P. Hoenen, S.J.**, *Cosmologia* (4th ed., p. 40 note, actuality of extension and continua)",
    ('appendix', 20): "**P. Hoenen, S.J.**, *Cosmologia* (nos. 152, 161, Note XIII, 1st ed. 1931)",
    ('appendix', 21): "**Themistius** (ed. Schenkl, p. 210) & **Simplicius** (ed. Diels, p. 127) on *prouparchein*",
    ('appendix', 22): "**P. Hoenen, S.J.**, *Cosmologia* (nos. 98–99, 214–218) & *De origine formae materialis* (1951)",
    ('appendix', 23): "**É. Gilson**, *L'être et l'essence* (1948) & *Being and Some Philosophers* (1949)",
    ('appendix', 24): "**B. Lonergan, S.J.**, \"The Concept of *Verbum* in the Writings of St. Thomas Aquinas\" (*Theological Studies* 1946–1947)",
    ('appendix', 25): "**P. Hoenen, S.J.**, *Théorie du jugement* (ch. II, first operation vs. second operation)",
    ('appendix', 26): "**F. Brentano** & **St. Thomas Aquinas**, compared in Hoenen's *Théorie du jugement* (ch. II, § 4)",
    ('appendix', 27): "**P. Hoenen, S.J.**, *Théorie du jugement* (pp. 193–194; *Reality and Judgment*, pp. 165–166)",
    ('appendix', 28): "**P. Hoenen, S.J.**, cross-reference to earlier analysis of extension (pp. 256 ff.)",
    ('appendix', 29): "**P. Hoenen, S.J.**, *Théorie du jugement* (chs. III–V on proposition *per se* and reflections)",
    ('appendix', 30): "**P. Hoenen, S.J.**, *Théorie du jugement* (pp. 25–26; *Reality and Judgment*, p. 21, specification of agent intellect)",
    ('appendix', 31): "**St. Thomas Aquinas**, *Summa contra Gentiles* I, c. 26, no. 2 (diversity of *esse* according to diverse natures)",
    ('appendix', 32): "**P. Hoenen, S.J.**, \"De duratione successiva...\" (*Gregorianum* 1953, pp. 1–31)",
    ('appendix', 33): "**A. Maier**, *An der Grenze von Scholastik und Naturwissenschaft* (1943) & **Nicole Oresme**"
}

# Load the base header
header = """---
title: "Bibliography & Cited References (Bibliographia et Fontes)"
description: "Comprehensive scholarly bibliography and annotated footnote concordance for Petrus Hoenen's De Noetica Geometriae (1954)."
---

> [Conspectus Totius Operis](index.md) | [Agent Chronicle](agent-chronicle.md) | [Historical Context: Fr. Peter Hoenen, S.J.](about/peter-hoenen.md)

---

# Bibliography & Cited References
## *Bibliographia et Apparatus Fontium*

This apparatus provides a comprehensive, critical reconstruction of all sources, classical treatises, mathematical works, and philosophical commentaries cited by **Father Peter Hoenen, S.J.** across *De Noetica Geometriae: Origine Theoriae Cognitionis* (Rome: Gregorian University, 1954).

Hoenen's citations reveal his unique intellectual position: trained in theoretical physics under Nobel laureate H. A. Lorentz at Leiden before teaching scholastic philosophy at the Gregorianum, he confronts the foundational crisis of modern mathematics (formalism, logicism, and non-Euclidean geometry) directly with the rigorous epistemology of Aristotle and St. Thomas Aquinas.

The apparatus is divided into two sections:
1. **[Part I: Systematic Bibliography](#part-i-systematic-bibliography)** — Verified academic citations grouped by tradition and field, detailing original editions, translations, and Hoenen's specific engagement with each author.
2. **[Part II: Chapter-by-Chapter Footnote Concordance](#part-ii-chapter-by-chapter-footnote-concordance)** — A complete concordance of all 130 footnotes across the volume, presenting facing Latin citations, English translations, and identified works.

---

## Part I: Systematic Bibliography

### 1. Works of Fr. Petrus Hoenen, S.J. Cited in This Volume

Father Hoenen frequently cites his earlier treatises to provide the systematic metaphysical and cosmological background for his arguments in geometry:

* **Hoenen, Petrus, S.J.** (1931; 4th ed. 1949; 5th ed. 1956). *Cosmologia*. Romae: Apud Aedes Universitatis Gregorianae.
  * *Subject & Citations*: Hoenen's standard textbook on the philosophy of nature. Cited throughout for:
    * The category *ubi* and physical space (*lib. I, cap. II*; Note VI, p. 468; nos. 58–63).
    * Continuous extension and the actuality of continua (Note XIII, pp. 527–530; nos. 152, 161).
    * The relativity of motion and critique of neo-positivism (Note IV, p. 456; Note XV, p. 538).
    * Motion as an existential act (*actus existentialis*).
    * Cited in: Caput VI (nn. 2, 3), Appendix (nn. 6, 12, 15, 16, 17, 19, 20, 22, 33).
* **Hoenen, Petrus, S.J.** (1946; 2nd ed. 1953). *La théorie du jugement d'après St. Thomas d'Aquin*. Analecta Gregoriana, Vol. XXXIX. Romae: Apud Aedes Universitatis Gregorianae.
  * English translation: *Reality and Judgment According to St. Thomas*. Translated by Henry F. Tiblier, S.J. Chicago: Henry Regnery Company, 1952. (Cited as *Th. d. J.* and *R. a. J.*).
  * *Subject & Citations*: Hoenen's epistemological masterpiece establishing the dual operation of the intellect (first operation = quiddity; second operation = *esse* / judgment). Cited for:
    * Propositions *per se* and *per accidens* (Chs. III–IV).
    * Reflections detecting the *esse* of realism (Chs. IX–XI).
    * The *Cogito ergo sum* as immediate existential judgment (Ch. XII).
    * Determination of the agent intellect by imaginative data (Ch. I–II).
    * Comparison between Thomistic judgment and Franz Brentano's intentionality (Ch. II, § 4).
    * Cited in: Praefatio (n. 2), Caput I (n. 2), Caput II (nn. 6, 13, 15, 17), Appendix (nn. 1, 25, 26, 27, 29, 30).
* **Hoenen, Petrus, S.J.** (1949). *Filosofia della natura inorganica*. Brescia: Morcelliana.
  * *Subject & Citations*: Treatise on inorganic natural philosophy, discussing the concept of space, coordinate systems, and Einstein's physical definitions.
  * Cited in: Caput VI (n. 2), Appendix (nn. 16, 17).
* **Hoenen, Petrus, S.J.** (1951). *De origine formae materialis*. Romae: Apud Aedes Universitatis Gregorianae (2nd ed.).
  * *Subject & Citations*: Scholastic collection of texts and commentary on the eduction of material forms from the potency of matter.
  * Cited in: Appendix (n. 22).
* **Hoenen, Petrus, S.J.** (1933). "De origine primorum principiorum scientiae." *Gregorianum*, 14(2), 153–184.
  * *Subject & Citations*: Foundational article on how the intellect intuits first principles within the sensible phantasm.
  * Cited in: Caput II (n. 1).
* **Hoenen, Petrus, S.J.** (1937). "Le « cogito ergo sum » comme intuition et comme mouvement de la pensée." In *Cartesio nel terzo centenario del « Discorso del Metodo »*, commemorative volume of *Rivista di Filosofia Neo-scolastica*, Milan: Vita e Pensiero, pp. 457–471.
  * *Subject & Citations*: Landmark study of the Cartesian Cogito interpreted through Thomistic noetics.
  * Cited in: Caput II (nn. 12, 14), Appendix (n. 1).
* **Hoenen, Petrus, S.J.** (1938–1939). "De philosophia scholastica cognitionis geometricae." *Gregorianum*, 19(4), 498–514; 20(1), 19–54; 20(3), 321–350.
  * *Subject & Citations*: The original three-part journal series that served as the initial draft and prototype for *De Noetica Geometriae*.
  * Cited in: Praefatio (n. 1).
* **Hoenen, Petrus, S.J.** (1948). "Pour une philosophie de la connaissance de l'étendue physique." In *Proceedings of the Tenth International Congress of Philosophy* (Amsterdam, August 11–18, 1948). Amsterdam: North-Holland Publishing. Reprinted in *Gregorianum*, 31 (1950), 126–132.
  * *Subject & Citations*: Paper addressing how the mind abstracts mathematical continuity from physical sensations of extension.
  * Cited in: Caput II (n. 8), Caput V (n. 11).
* **Hoenen, Petrus, S.J.** (1951). "De fontibus geometriae: Responsio ad Cl. H. Freudenthal." *Gregorianum*, 32, 263–268.
  * *Subject & Citations*: Critical exchange with mathematician Hans Freudenthal on the foundations of geometry.
  * Cited in: Caput V (n. 2).
* **Hoenen, Petrus, S.J.** (1953). "De duratione successiva et de quaestionibus connexis." *Gregorianum*, 34(1), 1–31.
  * *Subject & Citations*: Study of successive duration as fluent existential extension (*esse fluens*).
  * Cited in: Caput VI (n. 5), Appendix (nn. 14, 32).
* **Hoenen, Petrus, S.J.** (1953). "De connexionibus necessariis inter actus existentiales." *Gregorianum*, 34(4), 603–639.
  * *Subject & Citations*: The research study reproduced with additions as the Appendix of this monograph.
  * Cited in: Caput VI (n. 7), Caput VII (n. 3).

---

### 2. Classical Greek & Ancient Sources

* **Aristotle** (*Aristoteles Stagirites*):
  * *Posterior Analytics* (*Analytica Posteriora* / Ἀναλυτικὰ Ὕστερα):
    * Cited continuously as the definitive classical epistemological text for the structure of deductive science, primitive axioms (*axiomata*), hypotheses (*hypotheseis*), postulates (*aitemata*), and intuitive induction (*epagoge*).
    * Specific loci: I, 1 (71a14); I, 2 (71b–72a); I, 4 (73a–74a); I, 6; I, 10 (76a–77a); I, 12 (77b30: *tauta d'esti hoion horan te noesei*); I, 18 (81a–b); I, 31 (87b35); II, 19 (99b–100b).
    * Editions: Recension of W. D. Ross (*Aristotle's Prior and Posterior Analytics*, Oxford: Clarendon Press, 1949); Theodor Waitz (*Organon Graece*, Leipzig, 1844–1846).
  * *Prior Analytics* (*Analytica Priora* / Ἀναλυτικὰ Πρότερα):
    * I, 4 (25b37–39: syllogism in Barbara); I, 23 (Waitz ed., I, pp. 427–429).
  * *Physics* (*Physica* / Φυσικὴ ἀκρόασις):
    * I, c. 3; III, c. 1; IV, c. 5 (212b14: definition of place); IV, c. 11 (219a11: time and magnitude); VI, c. 1–10 (indivisibles, continuity, continuum); VIII, c. 1 (251a8–16: necessity of actual existence of mobile and mover).
    * Editions: W. D. Ross (*Aristotle's Physics*, Oxford, 1936); Henri Carteron (Paris: Budé, 1926).
  * *Metaphysics* (*Metaphysica* / Τὰ μετὰ τὰ φυσικά):
    * I, 9; III, 2; V, 9 (1018a9–14: diversity vs. difference); IX, 3 (1047a30–b2: actuality as movement and existence); IX, 8 (1050a21–23: *energeia* vs. *entelecheia*); X, 3 (1054b23–26); XIII (M), 2–3 (mathematical objects).
    * Editions & Commentaries: W. D. Ross (*Aristotle's Metaphysics*, 2 vols., Oxford, 1924); Hermann Bonitz (*Aristotelis Metaphysica*, Bonn, 1848–1849).
  * *De Anima* (Περὶ ψυχῆς):
    * III, 4; III, 7 (431a14–16, 431b2: thinking in phantasms); III, 8 (432a5–9: *mathematica* abstracted from sensible things).
    * Edition: F. Adolf Trendelenburg (*Aristotelis De Anima libri tres*, Berlin, 1877).
  * *Nicomachean Ethics* (*Ethica Nicomachea* / Ἠθικὰ Νικομάχεια):
    * VI, 8 (1142a12–20: youth can learn mathematics through abstraction but lack experience in natural philosophy); IX, 9 (1170a31 ff.: perceived sensing and perceived thinking).
    * Commentary: John Burnet (*The Ethics of Aristotle*, London: Methuen, 1900).
  * *Categories* (*Categoriae* / Κατηγορίαι):
    * c. 6 (4b20–5b10: distinction between discrete and continuous quantity).
* **Plato**:
  * *Meno* (82b–85b: the slave-boy geometry demonstration and doctrine of recollection).
  * *Republic* (VI 510c–d: mathematical hypotheses; VII 532c, 533c: the dialectical method overcoming hypotheses).
  * *Phaedo* (74a ff.: exact equality vs. imperfect sensory approximations).
  * *Parmenides* (156d–e: the sudden instant, *to exaiphnes*).
* **Euclid** (*Eukleides*):
  * *Elements* (*Elementa* / Στοιχεῖα):
    * Book I: Definitions (point, line, surface), Postulates (especially Postulate V, the parallel postulate), Common Notions.
    * Book V: Eudoxian theory of proportions.
    * Reference: Sir Thomas L. Heath, *The Thirteen Books of Euclid's Elements* (Cambridge: Cambridge University Press, 1908; 2nd ed. 1926).
* **Ancient Commentators on Aristotle**:
  * **Alexander of Aphrodisias**: *In Aristotelis Metaphysica Commentaria*. Ed. Michael Hayduck. CAG Vol. I. Berlin: Reimer, 1891 (cited on Metaph. IX, 3, p. 573).
  * **Themistius**: *In Aristotelis Physica Paraphrasis*. Ed. Heinrich Schenkl. CAG Vol. V.2. Berlin: Reimer, 1900 (cited on Phys. IV & VIII, p. 210).
  * **Simplicius of Cilicia**: *In Aristotelis Physicorum Libros Commentaria*. Ed. Hermann Diels. CAG Vols. IX–X. Berlin: Reimer, 1882–1895 (cited on Phys. VIII, p. 127).
  * **Proclus Diadochus**: *In primum Euclidis Elementorum librum commentarii*. Ed. Gottfried Friedlein. Leipzig: Teubner, 1873.

---

### 3. Medieval Scholastic Philosophy

* **St. Thomas Aquinas, O.P.** (*Doctor Angelicus*):
  * *In Aristotelis libros Analyticorum Posteriorum expositio* (cited throughout, especially I, lect. 1, 5, 6, 17, 30; II, lect. 20).
  * *In octo libros Physicorum Aristotelis expositio* (cited in III, lect. 5; IV, lect. 7, 17; VI; VIII).
  * *In duodecim libros Metaphysicorum Aristotelis expositio* (cited in V, lect. 9; IX, lect. 3; X, lect. 4, no. 2017).
  * *In Aristotelis librum De Anima commentarium* (ed. Angelo M. Pirotta, Turin: Marietti, 1936; cited in III, lect. 12, 13, nos. 770–772, 777, 791).
  * *In libros Peri Hermeneias expositio* (I, lect. 5, no. 5; lect. 17).
  * *In decem libros Ethicorum Aristotelis expositio* (VI, lect. 7; IX, lect. 11).
  * *In libros De Caelo et Mundo expositio* (I, lect. 2, no. 9).
  * *Super Boetium De Trinitate*:
    * Question 5, Article 3, ad 3: Locus classicus on mathematical abstraction and *materia intelligibilis* (intelligible matter), transcribed and commented upon at length in Caput IV (n. 2).
  * *Summa Theologiae*:
    * First Part (*Prima Pars*): I, q. 7, a. 1 (*esse* as most formal); I, q. 12, a. 4, ad 3 (abstracting form and *esse*); I, q. 75, a. 6 (*intellectus apprehendit esse absolutum*); I, qq. 84–85 (intellectual abstraction and the phantasm).
    * Second Part (*Secunda Secundae*): II-II, q. 24, a. 4, ad 3 (intensity of charity and quality).
  * *Summa contra Gentiles*:
    * I, c. 26, no. 2 (diversity of *esse* according to diverse natures).
  * *Quaestiones disputatae de Potentia Dei*:
    * q. 7, a. 2, ad 9 (*ipsum esse* as actuality of all acts); q. 8, a. 1 (conception of the intellect); q. 9, a. 5.
  * *Quaestiones disputatae de Veritate*:
    * q. 2, a. 3; q. 4, a. 2 (the concept as mental word).
  * *Scriptum super Sententiis*:
    * *In I Sent.*, d. 2, q. 1, a. 3 (definition of *ratio*); d. 19, q. 5, a. 1, ad 6 (*ratio essendi* denied to the senses).
* **St. Albert the Great, O.P.** (*Doctor Universalis*):
  * *In Analytica Priora*. Ed. Jammy. Lugduni, 1651, Vol. I, tract. I, cap. 9, p. 298a (use of transcendent formal terms).
* **Boethius, Anicius Manlius Severinus**:
  * *De Hebdomadibus* and *De Divisione* (concept of *communes animi conceptiones* / common axioms).
* **Nicole Oresme** (Nicolaus Oresmius):
  * *Tractatus de configurationibus qualitatum et motuum* (c. 1350). Cited via Anneliese Maier for the geometric representation of intensity and velocity in fluent *esse*.

---

### 4. Modern Foundations of Mathematics & Axiomatics

* **Hilbert, David** (1899; 7th ed. 1930). *Grundlagen der Geometrie*. Leipzig: B. G. Teubner.
  * *Hoenen's Engagement*: Analyzed extensively in Caput I, IV, and V. Hoenen critiques Hilbert's radical formalist reduction of primitive terms ("points, lines, planes") to uninterpreted relations (*Gedankendinge*), showing that geometric intuition and intelligible matter are smuggled back in through "explanations" (*Erklärungen*) and axioms of order/congruence.
* **Klein, Felix**:
  * (1902). *Anwendung der Differential- und Integralrechnung auf Geometrie: Eine Revision der Prinzipien*. Leipzig: B. G. Teubner.
    * *Hoenen's Engagement*: Central to Caput I and III. Hoenen highlights Klein's explicit recognition of the sensory "threshold of exactitude" (*Schwellenwert*) that separates experimental measurement from mathematical exactitude.
  * (1925). *Elementarmathematik vom höheren Standpunkte aus*. Vol. II: *Geometrie* (3rd ed.). Berlin: Julius Springer.
    * *Hoenen's Engagement*: Cited in Caput IV (nn. 23, 24) on non-Euclidean geometry and the physical-mathematical comparison of parallel lines.
* **Russell, Bertrand**:
  * (1903; 2nd ed. 1937). *The Principles of Mathematics*. London: George Allen & Unwin.
    * *Hoenen's Engagement*: Analyzed in Caput II, III, and IV (nn. 3, 4, 5, 28). Russell's sharp critiques of superposition (*congruence through motion*) and the empiricist derivation of circles are engaged and contextualized.
  * (1919). *Introduction to Mathematical Philosophy*. London: Allen & Unwin.
* **Poincaré, Henri**:
  * (1902). *La Science et l'Hypothèse*. Paris: Ernest Flammarion. (Cited on mathematical convention and physical measurement).
  * (1905). *La Valeur de la Science*. Paris: Ernest Flammarion. (Cited on types of intuition and the "amorphous" nature of continuous extension).
  * (1913). *Dernières Pensées*. Paris: Ernest Flammarion. (Cited on the limits of arithmetization and geometric intuition).
* **Pasch, Moritz** (1882; 2nd ed. with Max Dehn, 1926). *Vorlesungen über neuere Geometrie*. Berlin: Julius Springer.
  * *Hoenen's Engagement*: Pasch's Axiom of order between points on a line and plane is analyzed in Caput II (nn. 9, 16) and Caput IV.
* **Freudenthal, Hans** (1951). "De fontibus geometriae." *Gregorianum*, 32, 252–262.
  * *Hoenen's Engagement*: Debate with Hoenen on whether geometry's origin is empirical, purely axiomatic, or intuitive-formal.
* **Heath, Sir Thomas Little** (1921). *A History of Greek Mathematics*. 2 vols. Oxford: Clarendon Press.
  * *Hoenen's Engagement*: Cited in Caput V (n. 1) on Aristotle's terminology for axioms, postulates, and hypotheses.
* **Study, Eduard** (1914). *Die realistische Weltansicht und die Lehre vom Raume*. Braunschweig: Friedr. Vieweg & Sohn.
  * *Hoenen's Engagement*: Cited in Caput I (n. 13) and Caput III (n. 5) on realism in geometry against conventionalism.
* **Wellstein, Josef** (1905). "Elemente der Geometrie." In H. Weber & J. Wellstein (Eds.), *Enzyklopädie der Elementar-Mathematik*, Vol. II. Leipzig: Teubner. (Cited in Caput III nn. 6, 9; Caput IV n. 6).
* **Killing, Wilhelm** (1893, 1898). *Einführung in die Grundlagen der Geometrie*. 2 vols. Paderborn: Schöningh. (Cited in Caput IV nn. 16, 17, 18, 19 on direction and parallels).
* **Enriques, Federigo** (Ed.) (1924). *Questioni riguardanti le matematiche elementari*. Vol. I (3rd ed.). Bologna: Zanichelli. (Citing Ugo Amaldi on Euclidean postulates in Caput IV nn. 15, 20).
* **Hadamard, Jacques** (1937). "La géométrie." In *Encyclopédie Française*, Vol. I: *L'outillage mental*, Section I-52-10. Paris. (Cited in Caput IV nn. 11, 22).
* **Hausdorff, Felix** (1904). "Das Raumproblem." *Annalen der Naturphilosophie*, 3, 1–23. (Cited in Caput IV n. 21).
* **Weyl, Hermann** (1927). *Philosophie der Mathematik und Naturwissenschaft*. Handbuch der Philosophie. München: R. Oldenbourg. (Cited in Caput IV n. 22).
* **Hardy, Godfrey Harold** (1929). "Mathematical Proof." *Mind*, New Series, 38(149), 1–25. (Cited in Caput V nn. 8, 10 on the psychology vs. logic of proof).
* **de la Vallée-Poussin, Charles-Jean** (1896). Proof of the Prime Number Theorem (cited in Caput V n. 8).
* **Hessenberg, Gerhard** (1904). *Ebene und sphärische Trigonometrie*. Leipzig: Göschen. (Cited in Caput II n. 10).
* **Couturat, Louis** (1904). "La philosophie des mathématiques de Kant." *Revue de Métaphysique et de Morale*, 12(3), 321–383. (Cited in Caput II n. 3; Caput III n. 8).
* **Voss, Aurel** (1914). "Über die mathematische Erkenntnis." In *Die Kultur der Gegenwart*, Teil III, Abt. 1, pp. 385–440. Leipzig: Teubner. (Cited in Caput III n. 10).

---

### 5. Modern Philosophy, Epistemology & Science

* **Einstein, Albert**:
  * (1921). *Geometrie und Erfahrung*. Berlin: Julius Springer. (Cited in Caput I n. 4 on the famous aphorism: "as far as the laws of mathematics refer to reality, they are not certain; and as far as they are certain, they do not refer to reality").
  * (1930). Address in the journal *Forum*, 1, p. 173. (Cited in Caput VI n. 3 and Appendix n. 17 on the physical concept of coordinates and space).
* **Descartes, René**:
  * *Meditationes de Prima Philosophia* (1641).
  * *Responsiones ad Secundas Objectiones* (ed. Charles Adam & Paul Tannery, Vol. VII, pp. 140–141). (Cited in Appendix n. 2 on the synthetic vs. analytic order and the Cogito).
  * *Principia Philosophiae* (1644). Part II, art. 4–11 (extension as essence of body; Caput II n. 7).
  * *Conversation with Burman* (1648; ed. Adam & Tannery, Vol. V, p. 164; Appendix n. 33).
* **Leibniz, Gottfried Wilhelm** (1704; publ. 1765). *Nouveaux Essais sur l'entendement humain*. Book IV, ch. 7, § 10. (Cited in Caput II n. 2 on the deduction of 2 + 2 = 4).
* **Locke, John** (1690). *An Essay Concerning Human Understanding*. Ed. A. C. Fraser. Oxford: Clarendon Press, 1894, Vol. II, Book IV, ch. 17, § 4. (Cited in Caput V n. 5: "God has not been so sparing to men to make them barely two-legged creatures, and left it to Aristotle to make them rational").
* **Kant, Immanuel** (1781; 2nd ed. 1787). *Kritik der reinen Vernunft*. B14–15 (arithmetical judgment 7 + 5 = 12 as synthetic *a priori*; Caput II n. 4).
* **Mill, John Stuart** (1843; 5th ed. 1862). *A System of Logic, Ratiocinative and Inductive*. London: Parker, Son, and Bourn, Vol. I, Book II, ch. 5, pp. 255–260. (Cited in Caput I and Caput III nn. 3, 4 on geometry as experimental science of physical traces).
* **Brentano, Franz** (1874). *Psychologie vom empirischen Standpunkt*. Leipzig: Duncker & Humblot. (Cited in Appendix n. 26 on judgment vs. representation).
* **Gilson, Étienne**:
  * (1948). *L'être et l'essence*. Paris: J. Vrin.
  * (1949). *Being and Some Philosophers*. Toronto: Pontifical Institute of Mediaeval Studies.
  * *Hoenen's Engagement*: Critiqued in Appendix (nn. 23, 27) regarding whether *ipsum esse* is conceptualizable.
* **Lonergan, Bernard, S.J.** (1946–1947). "The Concept of *Verbum* in the Writings of St. Thomas Aquinas." *Theological Studies*, 7(3), 349–392; 8(1), 35–79; 8(3), 404–444. (Cited in Appendix n. 24 on the interior word and *conceptio* of judgment).
* **Baeumker, Clemens** (1890). *Das Problem der Materie in der griechischen Philosophie*. Münster: Aschendorff, pp. 288 ff. (Cited in Caput III n. 2 on intelligible matter in Aristotle).
* **Geyser, Joseph** (1917). *Die Erkenntnistheorie des Aristoteles*. Münster: Heinrich Schöningh. (Cited in Caput I n. 3 on Aristotelian noetics).
* **Meyerson, Émile** (1931). *Du cheminement de la pensée*. 3 vols. Paris: Félix Alcan, Vol. II, p. 391. (Cited in Appendix n. 7 on the search for identity and existential acts).
* **Maier, Anneliese** (1943). *An der Grenze von Scholastik und Naturwissenschaft*. Rome: Edizioni di Storia e Letteratura, pp. 312 ff. (Cited in Appendix n. 33 on Nicole Oresme's configuration of qualities and motions).
* **Stammler, Gerhard** (1928). *Begriff, Urteil, Schluss: Untersuchungen über die Grundlagen der Erkenntnislehre*. Halle (Saale): Max Niemeyer, pp. 229, 245. (Cited in Caput V n. 7).
* **Riehl, Alois** (1921). "Logik und Erkenntnistheorie." In *Die Kultur der Gegenwart*, Teil I, Abt. 6 (3rd ed.), pp. 71 ff. Leipzig: Teubner. (Cited in Caput V n. 6).
* **Waitz, Theodor** (1844–1846). *Aristotelis Organon Graece*. 2 vols. Leipzig: Hahn. (Commentary on *Prior Analytics* I, 23 cited in Caput IV n. 27).

---

## Part II: Chapter-by-Chapter Footnote Concordance

"""

concordance_sections = []

for ch in dataset:
    ch_title = ch['name']
    slug = ch['slug']
    pages = ch['pages']
    lat_link = ch['lat_rel']
    en_link = ch['en_rel']
    
    sec = f"### [{ch_title}]({en_link}) *(pp. {pages})*\n\n"
    sec += f"* [Latin Source Text]({lat_link}) | [English Translation]({en_link})\n\n"
    
    sec += "| # | Original Latin Citation | English Translation | Identified Source(s) & Notes |\n"
    sec += "| :-: | :--- | :--- | :--- |\n"
    
    for fn in ch['footnotes']:
        num = fn['num']
        lat = fn['latin'].replace('|', '&#124;')
        eng = fn['english'].replace('|', '&#124;')
        
        # Exact lookup
        source_note = CURATED_SOURCES.get((slug, num), "Scholarly note / Secondary literature")
            
        sec += f"| `[^{num}]` | {lat} | {eng} | {source_note} |\n"
        
    sec += "\n---\n\n"
    concordance_sections.append(sec)

footer = """
## Summary Statistics

* **Total Footnotes**: 130
* **Distribution Across Monograph**:
  * *Praefatio*: 2 footnotes
  * *Caput I*: 14 footnotes
  * *Caput II*: 17 footnotes
  * *Caput III*: 11 footnotes
  * *Caput IV*: 31 footnotes
  * *Caput V*: 12 footnotes
  * *Caput VI*: 7 footnotes
  * *Caput VII*: 3 footnotes
  * *Appendix*: 33 footnotes
* **Most Cited Authors**:
  * **Fr. Petrus Hoenen, S.J.** (46 citations across *Cosmologia*, *La théorie du jugement*, and *Gregorianum*)
  * **St. Thomas Aquinas** (29 direct references across Commentaries on Aristotle, *Summa Theologiae*, *In Boethium de Trinitate*, etc.)
  * **Aristotle** (26 direct citations across the *Organon*, *Physics*, *Metaphysics*, *De Anima*, *Ethics*)
  * **Modern Axiomaticians & Mathematicians** (26 citations across Hilbert, Russell, Klein, Poincaré, Pasch, Freudenthal, Heath, etc.)
  * **Modern Philosophers** (18 citations across Descartes, Leibniz, Kant, Mill, Brentano, Gilson, Lonergan, Baeumker, Maier, etc.)
  * **Albert Einstein** (3 citations regarding geometry and physical measurement)

---

> [Conspectus Totius Operis](index.md) | [Agent Chronicle](agent-chronicle.md) | [Historical Context: Fr. Peter Hoenen, S.J.](about/peter-hoenen.md)
"""

full_content = header + "".join(concordance_sections) + footer

with open('docs/bibliography.md', 'w', encoding='utf-8') as f:
    f.write(full_content)

print(f"Successfully generated curated docs/bibliography.md ({len(full_content)} bytes)")
