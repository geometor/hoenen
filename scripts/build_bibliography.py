import unicodedata

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")

import json
import re

# Load footnote data
with open('/tmp/hoenen_footnotes.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

fn_lookup = {}
for ch in dataset:
    for fn in ch['footnotes']:
        fn_lookup[(ch['slug'], fn['num'])] = {
            'chapter': ch['name'],
            'pages': ch['pages'],
            'lat_rel': ch['lat_rel'],
            'en_rel': ch['en_rel'],
            'latin': fn['latin'],
            'english': fn['english']
        }

authors = []

def add_author(name, alpha_key, born_died, death_sort, works):
    authors.append({
        'name': name,
        'alpha_key': alpha_key,
        'born_died': born_died,
        'death_sort': death_sort,
        'works': works
    })

# ==========================================
# 1. Eudoxus of Cnidus (c. 408 – c. 355 BC)
# ==========================================
add_author(
    "Eudoxus of Cnidus", "Eudoxus of Cnidus", "c. 408 – c. 355 BC", -355,
    [
        {
            'title': "Theoria Proportionum (in Euclidis Elementa, Liber V)",
            'english_title': "Theory of Proportions (in Euclid's Elements, Book V)",
            'year': "c. 370 BC",
            'notes': "Preserved in Book V of Euclid's Elements; formulated the first rigorous definition of proportionality for both commensurable and incommensurable continuous geometric magnitudes.",
            'citations': [
                {
                    'ref': "Caput I, § 4 (p. 21) & Caput I, [^6]",
                    'loc_link': "caput-1/caput-1-en.md#4-on-the-arithmetization-of-the-continuum",
                    'refers_to': "The Eudoxian theory of proportions as the Greek mathematical solution to the crisis of irrational/incommensurable ratios (e.g., diagonal and side of a square).",
                    'supports_text': "Demonstrates that ancient Greek mathematics treated continuous extension as primary and sui generis. Instead of attempting to force continuous magnitude into discrete numerical fractions or arithmetic real numbers, Eudoxus developed a purely geometric theory of proportions, thereby demonstrating that geometric continuity cannot be reduced to discrete arithmetic."
                }
            ]
        }
    ]
)

# ==========================================
# 2. Plato (c. 428/427 – c. 348/347 BC)
# ==========================================
add_author(
    "Plato", "Plato", "c. 428/427 – c. 348/347 BC", -348,
    [
        {
            'title': "Meno (Μένων)",
            'english_title': "Meno",
            'year': "c. 385 BC",
            'notes': "Socratic dialogue on virtue and learning; contains the famous geometry demonstration with an uneducated slave boy.",
            'citations': [
                {
                    'ref': "Caput I, § 2 (82b–85b)",
                    'loc_link': "caput-1/caput-1-en.md#2-on-the-origin-of-mathematical-notions",
                    'refers_to': "Socrates eliciting geometric demonstrations (doubling the area of a square) from the slave boy through guided questioning without direct instruction.",
                    'supports_text': "Illustrates the classical recognition that mathematical knowledge possesses an intrinsic, necessary certainty that cannot be acquired merely through empirical generalization. While Plato explained this necessity through recollection (anamnesis) of transcendent Forms, Hoenen shows that the true ground is the intellect's intuitive formal abstraction reading necessary relations directly within the imaginative sensible presentation."
                }
            ]
        },
        {
            'title': "Respublica (Πολιτεία)",
            'english_title': "The Republic",
            'year': "c. 375 BC",
            'notes': "Plato's foundational dialogue on justice and political philosophy; Books VI and VII formulate the divided line and the epistemology of mathematical hypotheses and dialectic.",
            'citations': [
                {
                    'ref': "Caput I, § 1 (VI 510c, VII 532c, 533c)",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "Plato's observation that geometers assume primitive principles (the odd and the even, figures, three kinds of angles) as unquestioned hypotheses (hypotheseis), and that the dialectician must investigate and destroy (anairei) these hypotheses to attain unhypothetical first principles.",
                    'supports_text': "Establishes the fundamental division of labor in the epistemology of mathematics: geometers construct their science from primitive postulates, but it belongs exclusively to the philosopher (the dialectician, metaphysician, or noeticist) to investigate the origin, truth, and necessity of those starting points."
                }
            ]
        }
    ]
)

# ==========================================
# 3. Aristotle (384 – 322 BC)
# ==========================================
add_author(
    "Aristotle", "Aristotle", "384 – 322 BC", -322,
    [
        {
            'title': "Analytica Posteriora (Ἀναλυτικὰ Ὕστερα)",
            'english_title': "Posterior Analytics",
            'year': "c. 350 BC",
            'notes': "The foundational peripatetic treatise on the structure of demonstrative science (episteme), first principles (nous), and intuitive induction (epagoge). Standard recension by W. D. Ross (Oxford, 1949); edition and commentary by Theodor Waitz (Leipzig, 1844–1846).",
            'citations': [
                {
                    'ref': "Caput I, § 1 (I, c. 1–2, 71a–72a; I, c. 10, 76a–77a)",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "Aristotle's classification of the primitive propositions of science: axioms (communes animi conceptiones / dignitates), hypotheses (suppositiones), and postulates (petitiones / aitemata).",
                    'supports_text': "Provides Hoenen with the structural architecture of deductive demonstration, proving that analysis cannot regress infinitely or circulate, and demonstrating that geometry is the primary historical prototype of apodictic science."
                },
                {
                    'ref': "Caput I, [^1]",
                    'loc_link': "caput-1/caput-1-en.md#fn-1",
                    'refers_to': "Aristotle's conception of postulates (aitemata) as propositions assumed by the teacher without the student's initial assent, potentially including propositions like Euclid's Fifth Postulate.",
                    'supports_text': "Clarifies the difference between self-evident axioms and geometric postulates that demand assent without immediate self-evidence."
                },
                {
                    'ref': "Caput I, § 2 (I, c. 12, 77b30)",
                    'loc_link': "caput-1/caput-1-en.md#2-on-the-origin-of-mathematical-notions",
                    'refers_to': "The famous dictum: ταῦτα δ' ἐστὶν οἷον ὁρᾶν τῇ νοήσει ('these mathematical things are as it were seen by intellectual vision').",
                    'supports_text': "Serves as the textual cornerstone of Hoenen's entire treatise, proving that for Aristotle, mathematical cognition is an authentic intellectual intuition (intuitus mentis) that perceives formal natures within the sensible imagination."
                },
                {
                    'ref': "Caput III, [^1] (I, c. 31, 87b35)",
                    'loc_link': "caput-3/caput-3-en.md#fn-1",
                    'refers_to': "Aristotle's argument: καὶ εἰ ἦν αἰσθάνεσθαι τὸ τρίγωνον ὅτι δυσὶν ὀρθαῖς ἴσας ἔχει τὰς γωνίας... ('even if it were possible to perceive by sense that a triangle has angles equal to two right angles, we should still look for a demonstration and not possess scientific knowledge of it').",
                    'supports_text': "Refutes sensory empiricism (such as John Stuart Mill's): sense perception only grasps contingent, individual particulars; scientific exactitude and universal necessity require intellectual cognition."
                },
                {
                    'ref': "Caput VII, [^1] (I, c. 1, 71a14 ff.)",
                    'loc_link': "caput-7/caput-7-en.md#fn-1",
                    'refers_to': "The crux of commentators regarding whether 'triangle' in Aristotle's opening demonstration is treated as a subject or as a passion/attribute (passio).",
                    'supports_text': "Analyzed via St. Thomas to demonstrate that the intellect constructs geometric figures in intelligible matter and reads their necessary attributes directly within that construction."
                }
            ]
        },
        {
            'title': "Analytica Priora (Ἀναλυτικὰ Πρότερα)",
            'english_title': "Prior Analytics",
            'year': "c. 350 BC",
            'notes': "Treatise on formal syllogistic logic and the validity of syllogistic figures. Edition and commentary by Theodor Waitz (Leipzig, 1844–1846).",
            'citations': [
                {
                    'ref': "Caput IV, [^30] (I, c. 4, 25b37–39)",
                    'loc_link': "caput-4/caput-4-en.md#fn-30",
                    'refers_to': "The formulation of the syllogism in Barbara: 'If A is predicated of all B, and B of all C, necessarily A is predicated of all C.'",
                    'supports_text': "Proves that Aristotle's use of algebraic-like letters (A, B, C) was not an uninterpreted formalist calculus, but represented intelligible universal natures whose necessary connections are seen by the intellect."
                },
                {
                    'ref': "Caput IV, [^27] (I, c. 23, Waitz ed., I, pp. 427–429)",
                    'loc_link': "caput-4/caput-4-en.md#fn-27",
                    'refers_to': "Aristotle's resolution of geometric arguments into syllogisms, and Waitz's commentary on the role of geometric diagrams.",
                    'supports_text': "Shows that geometric reasoning relies upon the mental inspection of intelligible matter even when formulated syllogistically."
                }
            ]
        },
        {
            'title': "Physica (Φυσικὴ ἀκρόασις)",
            'english_title': "Physics",
            'year': "c. 350 BC",
            'notes': "Treatise on natural philosophy, motion, the continuum, time, and place. Edition by W. D. Ross (Oxford, 1936); French edition by Henri Carteron (Budé, 1926).",
            'citations': [
                {
                    'ref': "Caput IV, [^7] (IV, c. 11, 219b15 ff.; IV, c. 12, 220b24 ff.)",
                    'loc_link': "caput-4/caput-4-en.md#fn-7",
                    'refers_to': "Aristotle's definition of time as the number of motion according to before and after, and the continuity of time following the magnitude of the trajectory.",
                    'supports_text': "Grounds successive duration and motion in the prior continuity of geometric magnitude, illustrating that motion in geometry is conceived within intelligible extension."
                },
                {
                    'ref': "Appendix, [^10] (IV, c. 5, 212b14 ff.)",
                    'loc_link': "appendix/appendix-en.md#fn-10",
                    'refers_to': "Aristotle's definition of place (topos) as the innermost motionless boundary of the containing body, and the textual variants (est id / est et).",
                    'supports_text': "Supports Hoenen's analysis of the category ubi and demonstrates that local motion requires a real relation to an actually existing surrounding body."
                },
                {
                    'ref': "Appendix, [^13] & § 6 (VIII, c. 1, 251a8–16)",
                    'loc_link': "appendix/appendix-en.md#fn-13",
                    'refers_to': "The principle that things capable of being moved and the moving cause must actually exist (hyparchein / estin) prior to motion.",
                    'supports_text': "Demonstrates that Aristotle's physics explicitly establishes connections between existential acts (actual existences), proving that Aristotle was deeply concerned with the act of existing."
                }
            ]
        },
        {
            'title': "Metaphysica (Τὰ μετὰ τὰ φυσικά)",
            'english_title': "Metaphysics",
            'year': "c. 350 BC",
            'notes': "Aristotle's first philosophy, investigating being qua being, substance, act and potency, and the ontology of mathematicals. Editions and commentaries by W. D. Ross (Oxford, 1924) and Hermann Bonitz (Bonn, 1848–1849).",
            'citations': [
                {
                    'ref': "Caput II, § 4 (V, c. 9, 1018a9–14; X, c. 3, 1054b23–26)",
                    'loc_link': "caput-2/caput-2-en.md#4-on-the-material-and-formal-nexus",
                    'refers_to': "The precise metaphysical distinction between diversity (diversum) and difference (differens): things are diverse by their whole selves (seipsis totis), whereas things are different through added differentiating marks.",
                    'supports_text': "Provides the ontological framework for understanding diverse modes of being (substance vs. accidents; essence vs. existential act) which differ by their whole nature rather than through added generic/specific marks."
                },
                {
                    'ref': "Appendix, [^3] & [^5] (IX, c. 3, 1047a30–b2; IX, c. 8, 1050a21–23)",
                    'loc_link': "appendix/appendix-en.md#fn-3",
                    'refers_to': "Aristotle's definition of actuality (energeia) as extended from movements to other things, and the distinction between energeia (activity) and entelecheia (perfection).",
                    'supports_text': "Proves that non-existent things cannot be moved, and confirms that motion is an existential act that attributes actual being to its mobile subject."
                },
                {
                    'ref': "Appendix, [^18] (IX, c. 9, 1051a21–33)",
                    'loc_link': "appendix/appendix-en.md#fn-18",
                    'refers_to': "The principle that potential geometric divisions are actualized by drawing constructions: 'geometrical constructions are discovered by an actualization; for it is by dividing that they discover them.'",
                    'supports_text': "Shows that the intellect actualizes potential mathematical relations by constructing divisions in intelligible matter, grounding mathematical discovery in the priority of act over potency."
                }
            ]
        },
        {
            'title': "De Anima (Περὶ ψυχῆς)",
            'english_title': "On the Soul",
            'year': "c. 350 BC",
            'notes': "Treatise on the soul, sensible perception, imagination (phantasia), and intellect (nous). Edition and commentary by F. Adolf Trendelenburg (Berlin, 1877).",
            'citations': [
                {
                    'ref': "Caput I, § 2 (III, c. 7, 431a14–16, 431b2; III, c. 8, 432a5–9)",
                    'loc_link': "caput-1/caput-1-en.md#2-on-the-origin-of-mathematical-notions",
                    'refers_to': "The peripatetic law that the intellect never thinks without a phantasm (οὐδέποτε νοεῖ ἄνευ φαντάσματος ἡ ψυχή), and that mathematical objects (ta ex aphaireseos) are abstracted from sensible things.",
                    'supports_text': "Serves as the foundation of Thomistic-Aristotelian noetics: even the highest geometric abstractions remain intrinsically dependent on the imaginative sensible representation, where the intellect intuits formal necessity."
                }
            ]
        },
        {
            'title': "Ethica Nicomachea (Ἠθικὰ Νικομάχεια)",
            'english_title': "Nicomachean Ethics",
            'year': "c. 350 BC",
            'notes': "Treatise on ethics and moral psychology; commentary by John Burnet (London, 1900).",
            'citations': [
                {
                    'ref': "Caput I, § 1 (VI, c. 8, 1142a12–20)",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "Aristotle's observation that young men can become mathematicians and geometers, but cannot have practical wisdom (phronesis) or natural philosophy, because mathematics proceeds by abstraction while physics and ethics require extensive experience.",
                    'supports_text': "Confirms that geometric knowledge does not depend on extensive inductive experience of the physical world, but on immediate formal abstraction accessible to any rational mind."
                },
                {
                    'ref': "Appendix, [^9] (IX, c. 9, 1170a31 ff.)",
                    'loc_link': "appendix/appendix-en.md#fn-9",
                    'refers_to': "The argument on perception of self-existence: 'he who sees perceives that he sees, and he who hears perceives that he hears... and if we perceive, we perceive that we exist.'",
                    'supports_text': "Provides the ancient Aristotelian foundation for the Cartesian Cogito: in perceiving our own cognitive acts, we immediately perceive our own existential act of being."
                }
            ]
        },
        {
            'title': "Categoriae (Κατηγορίαι)",
            'english_title': "Categories",
            'year': "c. 350 BC",
            'notes': "Treatise on the ten categories of being, predicaments, and postpredicaments.",
            'citations': [
                {
                    'ref': "Caput I, § 4 (c. 6, 4b20–5b10)",
                    'loc_link': "caput-1/caput-1-en.md#4-on-the-arithmetization-of-the-continuum",
                    'refers_to': "The division of quantity into continuous (magnitude, line, surface, body) and discrete (multitude, number).",
                    'supports_text': "Underpins Hoenen's entire defense of geometry against modern arithmetization: continuous magnitude is an irreducibly distinct category from discrete number, and cannot be constructed out of isolated zero-dimensional points."
                }
            ]
        }
    ]
)

# ==========================================
# 4. Euclid of Alexandria (fl. c. 300 BC)
# ==========================================
add_author(
    "Euclid of Alexandria", "Euclid of Alexandria", "fl. c. 300 BC (died c. 270 BC)", -270,
    [
        {
            'title': "Elementa (Στοιχεῖα)",
            'english_title': "Elements",
            'year': "c. 300 BC",
            'notes': "The thirteen books of Euclid's Elements; standard critical edition and commentary by Sir Thomas L. Heath (Cambridge, 1908; 2nd ed. 1926).",
            'citations': [
                {
                    'ref': "Caput I, § 1, § 4, § 5",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "Euclid's definitions of point, line, and surface; the Common Notions (axioms); Postulate V (the parallel postulate); and Book V on proportions.",
                    'supports_text': "Represents the historical paradigm of axiomatic deductive geometry for twenty centuries. Hoenen examines Euclid's definitions to show how intuitive spatial concepts served as the necessary foundation of classical geometry."
                },
                {
                    'ref': "Caput IV, § 4, § 5 & [^1]",
                    'loc_link': "caput-4/caput-4-en.md#4-on-exact-figures",
                    'refers_to': "Euclid's fifth postulate and the notion of direction in defining straight lines and parallels.",
                    'supports_text': "Analyzes the transition from classical Euclidean geometry to non-Euclidean systems, demonstrating that non-Euclidean systems alter the geometric framework but do not invalidate the intuitive necessity of Euclidean relationships in intelligible matter."
                }
            ]
        }
    ]
)

print("Added ancient Greek authors up to Euclid.")

# ==============================================================
# 5. Alexander of Aphrodisias (fl. c. 200 AD; died c. 215 AD)
# ==============================================================
add_author(
    "Alexander of Aphrodisias", "Alexander of Aphrodisias", "fl. late 2nd – early 3rd c. AD (died c. 215 AD)", 215,
    [
        {
            'title': "In Aristotelis Metaphysica Commentaria",
            'english_title': "Commentary on Aristotle's Metaphysics",
            'year': "c. 200 AD",
            'notes': "The premier ancient peripatetic commentary on the Metaphysics; edited by Michael Hayduck in Commentaria in Aristotelem Graeca (CAG Vol. I, Berlin: Reimer, 1891).",
            'citations': [
                {
                    'ref': "Appendix, [^4] (ed. Hayduck, p. 573, line 16)",
                    'loc_link': "appendix/appendix-en.md#fn-4",
                    'refers_to': "Alexander's formulation of the first known principle: τὸ κινούμενον ἢ ἐνεργοῦν ὄν τί ἐστιν ('that which is moved or acts is a certain being').",
                    'supports_text': "Confirms that ancient Greek commentators recognized motion as an existential act: movement can only belong to actually existing things, establishing a direct connection between physical mutation and existential being."
                }
            ]
        }
    ]
)

# ==============================================================
# 6. Themistius (c. 317 – c. 388 AD)
# ==============================================================
add_author(
    "Themistius", "Themistius", "c. 317 – c. 388 AD", 388,
    [
        {
            'title': "In Aristotelis Physica Paraphrasis",
            'english_title': "Paraphrase of Aristotle's Physics",
            'year': "c. 370 AD",
            'notes': "Peripatetic paraphrase of the Physics; edited by Heinrich Schenkl in CAG Vol. V.2 (Berlin: Reimer, 1900).",
            'citations': [
                {
                    'ref': "Appendix, [^11]",
                    'loc_link': "appendix/appendix-en.md#fn-11",
                    'refers_to': "Themistius's resolution of the definition of place, adopted and praised by St. Thomas Aquinas in In IV Phys., lect. 7.",
                    'supports_text': "Supports the realistic definition of place as the surrounding actual entity, grounding the category ubi in actual physical bodies."
                },
                {
                    'ref': "Appendix, [^21] (ed. Schenkl, p. 210)",
                    'loc_link': "appendix/appendix-en.md#fn-21",
                    'refers_to': "Themistius's repeated use of the technical Greek term προϋπάρχειν (prouparchein, to pre-exist) regarding the actual existence of mobile and mover.",
                    'supports_text': "Provides decisive textual evidence from late antiquity that existential actualities must pre-exist before physical interactions occur, refuting the claim that Aristotle and his school ignored existential acts."
                }
            ]
        }
    ]
)

# ==============================================================
# 7. Proclus Diadochus (412 – 485 AD)
# ==============================================================
add_author(
    "Proclus Diadochus", "Proclus Diadochus", "412 – 485 AD", 485,
    [
        {
            'title': "In primum Euclidis Elementorum librum commentarii",
            'english_title': "Commentary on the First Book of Euclid's Elements",
            'year': "c. 470 AD",
            'notes': "Neoplatonic philosophical commentary on Euclid; edited by Gottfried Friedlein (Leipzig: Teubner, 1873); English translation by Glenn R. Morrow (Princeton, 1970).",
            'citations': [
                {
                    'ref': "Caput I, § 1 & Caput IV, § 4",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "Proclus's exposition of the nature of mathematical imagination (phantasia) and historical documentation of Euclid's fifth postulate and definitions.",
                    'supports_text': "Corroborates the ancient understanding that geometric figures are projected into an imaginative medium that serves as the screen for mathematical reflection."
                }
            ]
        }
    ]
)

# ==============================================================
# 8. Boethius, Anicius Manlius Severinus (c. 477 – 524 AD)
# ==============================================================
add_author(
    "Boethius, Anicius Manlius Severinus", "Boethius", "c. 477 – 524 AD", 524,
    [
        {
            'title': "De Hebdomadibus (Quomodo substantiae...)",
            'english_title': "How Substances Are Good in Virtue of Their Existence (De Hebdomadibus)",
            'year': "c. 520 AD",
            'notes': "Theological and philosophical opusculum formulating the axiomatic method in philosophy; translated and commented on extensively by St. Thomas Aquinas.",
            'citations': [
                {
                    'ref': "Caput I, § 1 & Appendix, § 7",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "The concept of communes animi conceptiones (common conceptions of the soul / self-evident axioms), which are evident to anyone once the terms are known.",
                    'supports_text': "Supplies the classic definition of self-evident first principles adopted by St. Thomas and Hoenen: principles whose predicate is contained in the intelligible ratio of the subject."
                }
            ]
        }
    ]
)

# ==============================================================
# 9. Simplicius of Cilicia (c. 490 – c. 560 AD)
# ==============================================================
add_author(
    "Simplicius of Cilicia", "Simplicius of Cilicia", "c. 490 – c. 560 AD", 560,
    [
        {
            'title': "In Aristotelis Physicorum Libros Commentaria",
            'english_title': "Commentary on Aristotle's Physics",
            'year': "c. 535 AD",
            'notes': "The monumental Neoplatonic commentary on the Physics; edited by Hermann Diels in CAG Vols. IX–X (Berlin: Reimer, 1882–1895).",
            'citations': [
                {
                    'ref': "Appendix, [^21] (ed. Diels, p. 127, lines 9 and 14)",
                    'loc_link': "appendix/appendix-en.md#fn-21",
                    'refers_to': "Simplicius confirming with Themistius that the active cause and passive subject must actually pre-exist (prouparchein) in nature before any act of change occurs.",
                    'supports_text': "Affirms the scholastic thesis that existential actualities are necessarily presupposed for physical activity and motion."
                }
            ]
        }
    ]
)

# ==============================================================
# 10. St. Thomas Aquinas, O.P. (1225 – 1274)
# ==============================================================
add_author(
    "Thomas Aquinas, St., O.P.", "Thomas Aquinas, St.", "1225 – 1274", 1274,
    [
        {
            'title': "In Aristotelis libros Analyticorum Posteriorum expositio",
            'english_title': "Commentary on Aristotle's Posterior Analytics",
            'year': "c. 1270–1272",
            'notes': "Aquinas's definitive epistemological commentary on scientific demonstration, certitude, and the cognition of first principles. Standard Leonine edition, Vol. I* (1989).",
            'citations': [
                {
                    'ref': "Caput I, § 1 (I, lect. 1, n. 10; lect. 5, n. 7; lect. 6; lect. 17, n. 4)",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "St. Thomas explaining why mathematics has the most certain mode of demonstration ('propter certissimum modum demonstrationis'), and how higher sciences (metaphysics and natural philosophy) defend and establish the first principles of special sciences.",
                    'supports_text': "Establishes that mathematics is the epistemological model of science, and proves that examining mathematical first principles belongs properly to the philosopher."
                },
                {
                    'ref': "Caput VII, [^1] (I, lect. 1, 71a14 ff.)",
                    'loc_link': "caput-7/caput-7-en.md#fn-1",
                    'refers_to': "St. Thomas's analysis of the crux regarding triangle as subject vs. passion/attribute.",
                    'supports_text': "Demonstrates that the human intellect constructs geometric figures in intelligible matter and discerns their properties through active mental operations."
                }
            ]
        },
        {
            'title': "Super Boetium De Trinitate",
            'english_title': "Commentary on Boethius's De Trinitate",
            'year': "c. 1257–1259",
            'notes': "Aquinas's profound treatise on the division and methods of the sciences; Question 5, Article 3 is the locus classicus on mathematical abstraction.",
            'citations': [
                {
                    'ref': "Caput IV, [^2] (q. 5, a. 3, ad 3)",
                    'loc_link': "caput-4/caput-4-en.md#fn-2",
                    'refers_to': "The complete transcribed text: 'Quantitas autem indeterminata... dicitur materia intelligibilis... non tamen abstrahit a materia intelligibili individuali...'",
                    'supports_text': "The cornerstone of Hoenen's noetics: St. Thomas establishes that mathematics does not abstract from all matter, but retains **intelligible matter** (materia intelligibilis—continuous extended quantity imagined without sensible qualities). This resolves the problem of exactitude and individuation in geometry."
                }
            ]
        },
        {
            'title': "Summa Theologiae",
            'english_title': "Summa Theologiae",
            'year': "c. 1265–1274",
            'notes': "The Angelic Doctor's systematic theological synthesis. Primary editions: Leonine (Rome, 1888–1906); Marietti (Turin, 1952).",
            'citations': [
                {
                    'ref': "Appendix, [^8] (I, q. 7, a. 1)",
                    'loc_link': "appendix/appendix-en.md#fn-8",
                    'refers_to': "The dictum: 'illud quod est maxime formale omnium, est ipsum esse' ('that which is most formal of all is esse itself').",
                    'supports_text': "Supports Hoenen's metaphysical thesis that actual existence (esse) is the ultimate actuality and formal perfection of every entity."
                },
                {
                    'ref': "Appendix, § 7 (I, q. 12, a. 4, ad 3 & I, q. 75, a. 6)",
                    'loc_link': "appendix/appendix-en.md#the-abstract-concept-of-being-ratio-essendi",
                    'refers_to': "The teaching that 'intellectus apprehendit esse absolutum, et secundum omne tempus' ('the intellect apprehends absolute esse, and according to all time').",
                    'supports_text': "Refutes the existentialist claim (Étienne Gilson) that esse cannot be conceptualized: St. Thomas explicitly affirms that the human intellect apprehends absolute esse in abstraction."
                },
                {
                    'ref': "Appendix, § 7 (II-II, q. 24, a. 4, ad 3)",
                    'loc_link': "appendix/appendix-en.md#3-permanent-qualities-and-modes-of-inherence",
                    'refers_to': "St. Thomas's difficult teaching on the increase of accidental forms (charity and qualities) through greater participation in the subject.",
                    'supports_text': "Shows that intensity in qualities represents a diverse mode of being within the existential order."
                }
            ]
        },
        {
            'title': "In octo libros Physicorum Aristotelis expositio",
            'english_title': "Commentary on Aristotle's Physics",
            'year': "c. 1268–1270",
            'notes': "Aquinas's commentary on the physical world, movement, and the continuum. Leonine edition, Vol. II (1884).",
            'citations': [
                {
                    'ref': "Appendix, [^11] (IV, lect. 7) & Appendix, § 7 (III, lect. 5)",
                    'loc_link': "appendix/appendix-en.md#fn-11",
                    'refers_to': "St. Thomas adopting Themistius's solution to place, and formulating the principle: 'modi essendi proportionales sunt modis praedicandi' ('modes of being are proportional to modes of predicating').",
                    'supports_text': "Demonstrates that the Aristotelian categories are derived directly from diverse modes of actual being rather than mere grammatical distinctions."
                }
            ]
        },
        {
            'title': "In duodecim libros Metaphysicorum Aristotelis expositio",
            'english_title': "Commentary on Aristotle's Metaphysics",
            'year': "c. 1270–1273",
            'notes': "Aquinas's profound metaphysical commentary. Edited by M.-R. Cathala and R. Spiazzi (Turin: Marietti, 1950).",
            'citations': [
                {
                    'ref': "Caput II, § 4 & Appendix, § 7 (V, lect. 9; IX, lect. 3; X, lect. 4, no. 2017)",
                    'loc_link': "appendix/appendix-en.md#the-diversity-of-modes-of-being-act-determined-by-potency",
                    'refers_to': "St. Thomas explaining diversity by whole selves (seipsis totis) and the division of being into diverse modes of being.",
                    'supports_text': "Underpins the distinction between quidditative differences and existential diversities."
                }
            ]
        },
        {
            'title': "In Aristotelis librum De Anima commentarium",
            'english_title': "Commentary on Aristotle's De Anima",
            'year': "c. 1267–1268",
            'notes': "Aquinas's commentary on the soul, sensory faculties, and intellectual cognition. Edited by Angelo M. Pirotta (Turin: Marietti, 1936).",
            'citations': [
                {
                    'ref': "Caput I, § 2 (III, lect. 12, 13; Pirotta nos. 770–772, 777, 791) & Appendix, § 7 (II, lect. 16)",
                    'loc_link': "caput-1/caput-1-en.md#2-on-the-origin-of-mathematical-notions",
                    'refers_to': "The necessity of conversion to the phantasm (conversio ad phantasmata) for all human intellectual cognition, and the analysis of sound as an entity with fluent rather than resting esse.",
                    'supports_text': "Grounds Hoenen's doctrine of intuitive formal abstraction: the intellect reads necessary relations directly within the imaginative presentation."
                }
            ]
        },
        {
            'title': "In libros De Caelo et Mundo expositio",
            'english_title': "Commentary on Aristotle's On the Heavens",
            'year': "c. 1272–1273",
            'notes': "Aquinas's commentary on cosmology and astronomy. Leonine edition, Vol. III (1886).",
            'citations': [
                {
                    'ref': "Caput IV, [^9] (I, lect. 2, no. 9)",
                    'loc_link': "caput-4/caput-4-en.md#fn-9",
                    'refers_to': "St. Thomas noting: 'He uses the mode of speaking used by geometers, imagining that a point by its motion describes a line, and a line a surface, and a surface a body.'",
                    'supports_text': "Confirms that classical geometry legitimately constructs figures through imagined motion in intelligible matter."
                }
            ]
        },
        {
            'title': "Summa contra Gentiles",
            'english_title': "Summa contra Gentiles",
            'year': "c. 1259–1265",
            'notes': "Aquinas's philosophical defense of the Catholic faith against the gentiles. Leonine edition, Vols. XIII–XV (1918–1930).",
            'citations': [
                {
                    'ref': "Appendix, [^31] (I, c. 26, no. 2)",
                    'loc_link': "appendix/appendix-en.md#fn-31",
                    'refers_to': "The teaching that diverse esse are not diverse according to species, but things have 'diverse natures, by which esse is acquired in diverse ways.'",
                    'supports_text': "Proves that the diversity of modes of being flows from the diverse essences and quiddities that are actuated by esse."
                }
            ]
        },
        {
            'title': "Quaestiones disputatae de Potentia Dei",
            'english_title': "Disputed Questions on the Power of God",
            'year': "c. 1265–1266",
            'notes': "Disputed questions on divine power, creation, and the Trinity. Marietti edition by P. Bazzi et al. (Turin, 1953).",
            'citations': [
                {
                    'ref': "Appendix, § 7 (q. 7, a. 2, ad 9; q. 8, a. 1; q. 9, a. 5)",
                    'loc_link': "appendix/appendix-en.md#is-esse-conceptualizable",
                    'refers_to': "The definition: 'This that I call esse is the actuality of all acts, and on account of this is the perfection of perfections... esse is not so determined by another as potency by act, but rather as act by potency.'",
                    'supports_text': "Provides the decisive Thomistic formulation proving that esse is not an abstract quiddity, but the ultimate act determined by essence as act is determined by potency."
                }
            ]
        },
        {
            'title': "Scriptum super Sententiis",
            'english_title': "Commentary on the Sentences of Peter Lombard",
            'year': "c. 1252–1256",
            'notes': "Aquinas's early masterpiece of theology. Edited by P. Mandonnet and M. F. Moos (Paris: Lethielleux, 1929–1947).",
            'citations': [
                {
                    'ref': "Appendix, § 7 (In I Sent., d. 2, q. 1, a. 3 & d. 19, q. 5, a. 1, ad 6)",
                    'loc_link': "appendix/appendix-en.md#the-abstract-concept-of-being-ratio-essendi",
                    'refers_to': "The definition of ratio as that which the intellect apprehends of the meaning of a name, and the teaching that the ratio essendi is denied to the senses.",
                    'supports_text': "Proves that understanding being (esse) requires an intellectual operation of reflection, which the sensory faculties are incapable of performing."
                }
            ]
        }
    ]
)

# ==============================================================
# 11. St. Albert the Great, O.P. (c. 1200 – 1280)
# ==============================================================
add_author(
    "Albert the Great, St., O.P.", "Albert the Great, St.", "c. 1200 – 1280", 1280,
    [
        {
            'title': "In Analytica Priora",
            'english_title': "Commentary on the Prior Analytics",
            'year': "c. 1250",
            'notes': "The Universal Doctor's commentary on formal logic; edited by Pierre Jammy (Lugduni, 1651, Vol. I, tract. I, cap. 9, p. 298a).",
            'citations': [
                {
                    'ref': "Caput IV, [^29]",
                    'loc_link': "caput-4/caput-4-en.md#fn-29",
                    'refers_to': "St. Albert's teaching: 'We use transcendent terms (A, B, C) in the place of things, because the necessity of consequence is better seen in transcendent terms than in particular matters.'",
                    'supports_text': "Demonstrates that scholastic logic understood formal symbolic variables not as meaningless empty marks, but as universal formal placeholders expressing intelligible necessity."
                }
            ]
        }
    ]
)

# ==============================================================
# 12. Nicole Oresme (c. 1320/1325 – 1382)
# ==============================================================
add_author(
    "Nicole Oresme", "Nicole Oresme", "c. 1320/1325 – 1382", 1382,
    [
        {
            'title': "Tractatus de configurationibus qualitatum et motuum",
            'english_title': "Treatise on the Configurations of Qualities and Motions",
            'year': "c. 1350",
            'notes': "Medieval mathematical and physical treatise pioneering the coordinate graphing of velocities and intensities; cited via Anneliese Maier (1943).",
            'citations': [
                {
                    'ref': "Appendix, § 7 and [^33]",
                    'loc_link': "appendix/appendix-en.md#2-velocity-intensity-and-nicole-oresmes-configurations",
                    'refers_to': "Oresme's geometric configurations representing the intensity of qualities and the velocity of motion across temporal duration.",
                    'supports_text': "Shows that medieval scholasticism already recognized that fluent existential acts (motion, velocity) possess structural and qualitative configurations analogous to geometric figures in continuous extension."
                }
            ]
        }
    ]
)

# ==============================================================
# 13. René Descartes (1596 – 1650)
# ==============================================================
add_author(
    "Descartes, René", "Descartes, René", "1596 – 1650", 1650,
    [
        {
            'title': "Meditationes de Prima Philosophia & Responsiones ad Secundas Objectiones",
            'english_title': "Meditations on First Philosophy & Replies to the Second Objections",
            'year': "1641",
            'notes': "Descartes's foundational metaphysical work; critical edition by Charles Adam & Paul Tannery (AT VII, Paris: Vrin).",
            'citations': [
                {
                    'ref': "Appendix, [^2] (AT VII, pp. 140, 18 – 141, 2)",
                    'loc_link': "appendix/appendix-en.md#fn-2",
                    'refers_to': "Descartes explaining that the Cogito ('I think, therefore I am') is not a syllogism deduced from a universal major premise, but an immediate mental intuition of the singular existent.",
                    'supports_text': "Supports Hoenen's Thomistic interpretation of the Cogito: it is an immediate existential judgment in which the intellect perceives its own act of being directly within its cognitive exercise."
                }
            ]
        },
        {
            'title': "Principia Philosophiae",
            'english_title': "Principles of Philosophy",
            'year': "1644",
            'notes': "Descartes's systematic exposition of metaphysics and natural philosophy; critical edition AT VIII-1.",
            'citations': [
                {
                    'ref': "Caput II, [^7] (Part II, art. 4–11)",
                    'loc_link': "caput-2/caput-2-en.md#fn-7",
                    'refers_to': "Descartes's definition of the essence of body as extension alone (res extensa).",
                    'supports_text': "Critiqued by Hoenen: while Descartes erred in reducing the entire physical nature of bodies to geometric extension, he correctly perceived that divisibility is an intrinsic and necessary proper attribute of extended quantity."
                }
            ]
        },
        {
            'title': "Entretien avec Burman",
            'english_title': "Conversation with Burman",
            'year': "1648",
            'notes': "Recorded interview of Descartes by Frans Burman on April 16, 1648; critical edition AT V, p. 164.",
            'citations': [
                {
                    'ref': "Appendix, § 7 (AT V, p. 164)",
                    'loc_link': "appendix/appendix-en.md#4-contact-aggregates-imitating-essential-continua",
                    'refers_to': "Descartes denying any real difference between a continuous body and an aggregate of parts touching each other in contact.",
                    'supports_text': "Illustrates the philosophical confusion that results from failing to distinguish between an essential continuum (intrinsic continuous quantity) and a mere aggregate of contact (accidental existential unity)."
                }
            ]
        }
    ]
)

# ==============================================================
# 14. John Locke (1632 – 1704)
# ==============================================================
add_author(
    "Locke, John", "Locke, John", "1632 – 1704", 1704,
    [
        {
            'title': "An Essay Concerning Human Understanding",
            'english_title': "An Essay Concerning Human Understanding",
            'year': "1690",
            'notes': "Locke's foundational epistemological work; critical edition by Alexander Campbell Fraser (Oxford: Clarendon Press, 1894, 2 vols.).",
            'citations': [
                {
                    'ref': "Caput V, [^5] (Book IV, ch. 17, § 4; Fraser ed., II, pp. 390 ff.)",
                    'loc_link': "caput-5/caput-5-en.md#fn-5",
                    'refers_to': "Locke's famous critique of formal syllogistics: 'God has not been so sparing to men to make them barely two-legged creatures, and left it to Aristotle to make them rational.'",
                    'supports_text': "Employed by Hoenen to demonstrate that syllogistic reasoning is an intrinsic, natural mental activity prior to any verbal formulation or symbolic calculus, confirming the psychological and noetic reality of deduction."
                }
            ]
        }
    ]
)

# ==============================================================
# 15. Gottfried Wilhelm Leibniz (1646 – 1716)
# ==============================================================
add_author(
    "Leibniz, Gottfried Wilhelm", "Leibniz, Gottfried Wilhelm", "1646 – 1716", 1716,
    [
        {
            'title': "Nouveaux Essais sur l'entendement humain",
            'english_title': "New Essays on Human Understanding",
            'year': "1704 (publ. 1765)",
            'notes': "Leibniz's detailed chapter-by-chapter reply to Locke's Essay; Book IV treats knowledge, truth, and necessary principles.",
            'citations': [
                {
                    'ref': "Caput II, [^2] (Book IV, ch. 7, § 10)",
                    'loc_link': "caput-2/caput-2-en.md#fn-2",
                    'refers_to': "Leibniz's attempted proof of 2 + 2 = 4 using definitions (2 is 1+1, 3 is 2+1, 4 is 3+1) and the single axiom of substituting equals.",
                    'supports_text': "Hoenen subjects Leibniz's proof to rigorous forensic analysis: Leibniz applies the axiom not once, but at *every single step* of the substitution. This proves that even 'analytic' deductions depend upon repeated intuitive grasps of equality in intelligible matter."
                }
            ]
        }
    ]
)

# ==============================================================
# 16. Immanuel Kant (1724 – 1804)
# ==============================================================
add_author(
    "Kant, Immanuel", "Kant, Immanuel", "1724 – 1804", 1804,
    [
        {
            'title': "Kritik der reinen Vernunft",
            'english_title': "Critique of Pure Reason",
            'year': "1781 (2nd ed. 1787)",
            'notes': "The foundational text of critical idealism; cited from the 1787 B edition (B14–15 on arithmetic judgments).",
            'citations': [
                {
                    'ref': "Caput I, § 2 & § 3",
                    'loc_link': "caput-1/caput-1-en.md#2-on-the-origin-of-mathematical-notions",
                    'refers_to': "Kant's theory of space and time as subjective a priori forms of external sensibility.",
                    'supports_text': "Hoenen credits Kant with recognizing that mathematical knowledge requires sensible intuition (Anschauung) and possesses strict necessity, but refutes Kant's subjectivism, demonstrating that extension is an objective property of being known through abstraction."
                },
                {
                    'ref': "Caput II, [^4] (B14–15)",
                    'loc_link': "caput-2/caput-2-en.md#fn-4",
                    'refers_to': "Kant's famous analysis of 7 + 5 = 12 as a synthetic a priori proposition that cannot be derived through mere conceptual analysis without recourse to intuition (counting points or fingers).",
                    'supports_text': "Hoenen uses Kant's example to show that arithmetic judgments require sensible phantasms, but demonstrates that the necessity is grasped by the intellect reading formal connections within intelligible matter."
                }
            ]
        }
    ]
)

print("Added authors up to Kant.")

# ==============================================================
# 17. Theodor Waitz (1821 – 1864)
# ==============================================================
add_author(
    "Waitz, Theodor", "Waitz, Theodor", "1821 – 1864", 1864,
    [
        {
            'title': "Aristotelis Organon Graece",
            'english_title': "Aristotle's Organon in Greek",
            'year': "1844–1846",
            'notes': "Critical Greek text and Latin commentary on the Organon (2 vols., Leipzig: Hahn).",
            'citations': [
                {
                    'ref': "Caput IV, [^27] (Vol. I, pp. 427–429)",
                    'loc_link': "caput-4/caput-4-en.md#fn-27",
                    'refers_to': "Waitz's commentary on Prior Analytics I, 23 regarding the conversion of geometric proofs into formal syllogisms.",
                    'supports_text': "Supports the view that geometric reasoning operates with essential terms and diagrams rather than empty formal symbols."
                }
            ]
        }
    ]
)

# ==============================================================
# 18. August Ferdinand Möbius (1790 – 1868)
# ==============================================================
add_author(
    "Möbius, August Ferdinand", "Mobius, August Ferdinand", "1790 – 1868", 1868,
    [
        {
            'title': "Ueber die Bestimmung des Inhaltes eines Polyëders (Das Möbiusband)",
            'english_title': "On the Determination of the Volume of a Polyhedron (The Möbius Strip)",
            'year': "1858 (publ. 1865)",
            'notes': "Memoir presenting the discovery of the non-orientable one-sided surface (Möbius strip) in topology.",
            'citations': [
                {
                    'ref': "Caput II, § 2 & Caput III, § 2",
                    'loc_link': "caput-2/caput-2-en.md#6-on-the-section-of-a-cylinder-and-the-mobius-strip",
                    'refers_to': "The section of a cylinder and a Möbius strip as an objection against classical geometric intuition.",
                    'supports_text': "Hoenen analyzes the cutting of a Möbius strip (which results in a single longer two-sided loop rather than two separate strips), proving that this counter-intuitive result is rigorously deduced from the intuitive axioms of continuous sectioning rather than contradicting them."
                }
            ]
        }
    ]
)

# ==============================================================
# 19. Friedrich Adolf Trendelenburg (1802 – 1872)
# ==============================================================
add_author(
    "Trendelenburg, Friedrich Adolf", "Trendelenburg, Friedrich Adolf", "1802 – 1872", 1872,
    [
        {
            'title': "Aristotelis De Anima libri tres",
            'english_title': "Aristotle's Three Books On the Soul",
            'year': "1877 (ed. altera)",
            'notes': "Renowned critical edition and commentary on Aristotle's De Anima (Berlin: Weber).",
            'citations': [
                {
                    'ref': "Caput IV, [^8]",
                    'loc_link': "caput-4/caput-4-en.md#fn-8",
                    'refers_to': "Trendelenburg's note asking who are the ancient thinkers who spoke of points moving to generate lines.",
                    'supports_text': "Traces the historical pedigree of motion in geometry back to ancient Peripatetic discussions."
                }
            ]
        }
    ]
)

# ==============================================================
# 20. John Stuart Mill (1806 – 1873)
# ==============================================================
add_author(
    "Mill, John Stuart", "Mill, John Stuart", "1806 – 1873", 1873,
    [
        {
            'title': "A System of Logic, Ratiocinative and Inductive",
            'english_title': "A System of Logic, Ratiocinative and Inductive",
            'year': "1843 (5th ed. 1862)",
            'notes': "Mill's magnum opus on epistemology, empiricism, and induction (London: Parker, Son, and Bourn, 2 vols.).",
            'citations': [
                {
                    'ref': "Caput I, § 2",
                    'loc_link': "caput-1/caput-1-en.md#2-on-the-origin-of-mathematical-notions",
                    'refers_to': "Mill's radical empiricist theory that mathematics is an inductive physical science of material bodies, lacking apodictic necessity and exactitude.",
                    'supports_text': "Presents the classical empiricist challenge: Mill honestly admits that if mathematical ideas are drawn from senses alone, they can never attain absolute necessity or exactitude."
                },
                {
                    'ref': "Caput III, [^3] & [^4] (Vol. I, Book II, ch. 5, pp. 255–257)",
                    'loc_link': "caput-3/caput-3-en.md#fn-3",
                    'refers_to': "Mill's assertions: 'A line is length without breadth; but is there in nature such a thing as a line without breadth? There is not... none of these things exist in nature.'",
                    'supports_text': "Hoenen uses Mill's formulation to sharpen the Problem of Exactitude: because physical senses only perceive rough bodies with finite width, the mind's exact geometric notions (point, line, surface) must arise through intellectual abstraction of boundaries within continuous quantity."
                }
            ]
        }
    ]
)

# ==============================================================
# 21. Hermann Bonitz (1814 – 1888)
# ==============================================================
add_author(
    "Bonitz, Hermann", "Bonitz, Hermann", "1814 – 1888", 1888,
    [
        {
            'title': "Aristotelis Metaphysica: Commentarius",
            'english_title': "Commentary on Aristotle's Metaphysics",
            'year': "1848–1849",
            'notes': "Classic Philological commentary on the Greek text of the Metaphysics (Bonn: Marcus, 2 vols.).",
            'citations': [
                {
                    'ref': "Appendix, [^5] (Vol. II, p. 387)",
                    'loc_link': "appendix/appendix-en.md#fn-5",
                    'refers_to': "Bonitz's linguistic analysis distinguishing energeia (action bringing possibility to essence) from entelecheia (full perfection of the thing).",
                    'supports_text': "Clarifies the precise Aristotelian vocabulary of act and actuality in existential changes."
                },
                {
                    'ref': "Appendix, [^13] (Vol. II, p. 401)",
                    'loc_link': "appendix/appendix-en.md#fn-13",
                    'refers_to': "Bonitz's explanation of Metaphysics IX, 3: 'hanc causam motricem actu existere necesse est' ('it is necessary that this moving cause actually exist').",
                    'supports_text': "Confirms the textual necessity that motion presupposes the actual existence in time of the active cause."
                }
            ]
        }
    ]
)

# ==============================================================
# 22. Karl Weierstrass (1815 – 1897)
# ==============================================================
add_author(
    "Weierstrass, Karl", "Weierstrass, Karl", "1815 – 1897", 1897,
    [
        {
            'title': "Vorlesungen über die Theorie der Funktionen",
            'english_title': "Lectures on the Theory of Functions",
            'year': "1872 (publ. 1886)",
            'notes': "Pioneering lectures establishing the epsilon-delta arithmetization of mathematical analysis without geometric intuition.",
            'citations': [
                {
                    'ref': "Caput I, § 4",
                    'loc_link': "caput-1/caput-1-en.md#4-on-the-arithmetization-of-the-continuum",
                    'refers_to': "Weierstrass's program of arithmetizing analysis, eliminating geometric intuition and infinitesimals in favor of pure number sequences.",
                    'supports_text': "Represents the historical movement that attempted to solve the problem of geometric inexactitude by reducing all continuous extension to discrete integer calculations."
                }
            ]
        }
    ]
)

# ==============================================================
# 23. Octave Hamelin (1856 – 1907)
# ==============================================================
add_author(
    "Hamelin, Octave", "Hamelin, Octave", "1856 – 1907", 1907,
    [
        {
            'title': "Le Système d'Aristote",
            'english_title': "The System of Aristotle",
            'year': "1920 (posthumous)",
            'notes': "Comprehensive philosophical reconstruction of Aristotle's thought, edited by Léon Robin (Paris: Alcan).",
            'citations': [
                {
                    'ref': "Caput I, [^3] (pp. 234 sq., 258 sq.)",
                    'loc_link': "caput-1/caput-1-en.md#fn-3",
                    'refers_to': "Hamelin's analysis of Aristotelian abstraction and the relationship between sensible data and intellectual principles.",
                    'supports_text': "Provides scholarly authority confirming that Aristotle derived first principles through intuitive induction from sensible experience."
                }
            ]
        }
    ]
)

# ==============================================================
# 24. Henri Poincaré (1854 – 1912)
# ==============================================================
add_author(
    "Poincaré, Henri", "Poincare, Henri", "1854 – 1912", 1912,
    [
        {
            'title': "La Science et l'Hypothèse",
            'english_title': "Science and Hypothesis",
            'year': "1902",
            'notes': "Poincaré's classic work on the philosophy of science, conventionalism, and the nature of space (Paris: Flammarion).",
            'citations': [
                {
                    'ref': "Caput IV, [^10] (p. 80; cf. p. 60)",
                    'loc_link': "caput-4/caput-4-en.md#fn-10",
                    'refers_to': "Poincaré's observation that geometric figures are ideal bodies, and that geometric axioms are disguised conventions chosen for convenience.",
                    'supports_text': "Hoenen engages Poincaré's conventionalism, showing that while physical bodies are imperfect, ideal geometric figures have an objective nature grasped through formal abstraction."
                }
            ]
        },
        {
            'title': "La Valeur de la Science",
            'english_title': "The Value of Science",
            'year': "1905",
            'notes': "Epistemological essays on intuition, logic, and the physical sciences (Paris: Flammarion).",
            'citations': [
                {
                    'ref': "Caput I, [^9] & [^10] (pp. 17, 22–23)",
                    'loc_link': "caput-1/caput-1-en.md#fn-9",
                    'refers_to': "Poincaré's distinction between three kinds of intuition: the appeal to sense and imagination, generalization by induction, and the intuition of pure number.",
                    'supports_text': "Highlights Poincaré's admission that modern analysis eliminated sensible intuition, but shows that Poincaré still required an irreducible 'intuition of pure number,' confirming that mathematics cannot exist without intuition."
                },
                {
                    'ref': "Caput IV, [^14] (p. 59) & Caput VI, [^1]",
                    'loc_link': "caput-4/caput-4-en.md#fn-14",
                    'refers_to': "Poincaré describing continuous space as formless and 'amorphous' until metric relations are imposed, and his thought experiment on measuring a physical circle.",
                    'supports_text': "Hoenen agrees with Poincaré that physical continuous extension is amorphous regarding fixed coordinate systems, but shows that it possesses intrinsic intelligible properties (divisibility, boundaries, dimensionality)."
                }
            ]
        },
        {
            'title': "Dernières Pensées",
            'english_title': "Last Thoughts",
            'year': "1913 (posthumous)",
            'notes': "Final collection of essays on mathematics, logic, and physics (Paris: Flammarion).",
            'citations': [
                {
                    'ref': "Caput I, [^11] & [^12] (p. 65) & Caput IV, [^14] (p. 62)",
                    'loc_link': "caput-1/caput-1-en.md#fn-11",
                    'refers_to': "Poincaré's sharp warning against arithmetization: 'This definition makes cheap of the intuitive origin of the notion of the continuum... I do not mean to say that this arithmetization of mathematics is a bad thing, I say it is not everything.'",
                    'supports_text': "Provides decisive modern mathematical backing for Hoenen's central thesis: arithmetization leaves out the essential intuitive nature of continuous extension, which the philosopher must recover."
                }
            ]
        }
    ]
)

# ==============================================================
# 25. Louis Couturat (1868 – 1914)
# ==============================================================
add_author(
    "Couturat, Louis", "Couturat, Louis", "1868 – 1914", 1914,
    [
        {
            'title': "La philosophie des mathématiques de Kant",
            'english_title': "The Philosophy of Mathematics of Kant",
            'year': "1904",
            'notes': "Major critical study in Revue de Métaphysique et de Morale (Vol. 12, No. 3, pp. 321–383).",
            'citations': [
                {
                    'ref': "Caput II, [^3] & Caput III, [^8]",
                    'loc_link': "caput-2/caput-2-en.md#fn-3",
                    'refers_to': "Couturat's logicist deduction of arithmetic propositions (7 + 5 = 12) from definitions and logical substitution without Kantian intuition.",
                    'supports_text': "Hoenen analyzes Couturat's deductions to reveal that Couturat unconsciously presupposes intuitive operations at each deductive step, proving that logicism cannot dispense with intelligible intuition."
                }
            ]
        },
        {
            'title': "Les principes des mathématiques",
            'english_title': "The Principles of Mathematics",
            'year': "1905",
            'notes': "Systematic exposition of Russell and Peano's logicism for continental audiences (Paris: Alcan).",
            'citations': [
                {
                    'ref': "Caput II, [^3]",
                    'loc_link': "caput-2/caput-2-en.md#fn-3",
                    'refers_to': "Couturat's exposition of the formal logical derivation of mathematical addition.",
                    'supports_text': "Demonstrates that formal arithmetic definitions presuppose an intuitive understanding of multitude and equality."
                }
            ]
        }
    ]
)

# ==============================================================
# 26. Richard Dedekind (1831 – 1916)
# ==============================================================
add_author(
    "Dedekind, Richard", "Dedekind, Richard", "1831 – 1916", 1916,
    [
        {
            'title': "Stetigkeit und irrationale Zahlen",
            'english_title': "Continuity and Irrational Numbers",
            'year': "1872",
            'notes': "Landmark treatise constructing real numbers via Dedekind cuts on sets of rational numbers (Braunschweig: Vieweg).",
            'citations': [
                {
                    'ref': "Caput I, § 4",
                    'loc_link': "caput-1/caput-1-en.md#4-on-the-arithmetization-of-the-continuum",
                    'refers_to': "Dedekind's definition of continuity as an arithmetic cut in the domain of rational numbers.",
                    'supports_text': "Analyzed as a prime example of the arithmetization of the continuum: Dedekind defines continuity through discrete sets, which inverts the true cognitive order where discrete number is abstracted from continuous magnitude."
                }
            ]
        }
    ]
)

# ==============================================================
# 27. Franz Brentano (1838 – 1917)
# ==============================================================
add_author(
    "Brentano, Franz", "Brentano, Franz", "1838 – 1917", 1917,
    [
        {
            'title': "Psychologie vom empirischen Standpunkt",
            'english_title': "Psychology from an Empirical Standpoint",
            'year': "1874",
            'notes': "Brentano's seminal work re-introducing intentionality and establishing the fundamental classification of mental phenomena (Leipzig: Duncker & Humblot).",
            'citations': [
                {
                    'ref': "Appendix, § 7 and [^26]",
                    'loc_link': "appendix/appendix-en.md#the-abstract-concept-of-being-ratio-essendi",
                    'refers_to': "Brentano's doctrine that judgment (Urteil—acknowledging or rejecting existence) is fundamentally diverse from representation (Vorstellung), constituting distinct basic classes of mental acts.",
                    'supports_text': "Hoenen compares Brentano's insight directly to St. Thomas Aquinas: both recognize that judging existence (esse) is fundamentally distinct from apprehending quiddity, validating the realism of judgment."
                }
            ]
        }
    ]
)

# ==============================================================
# 28. Georg Cantor (1845 – 1918)
# ==============================================================
add_author(
    "Cantor, Georg", "Cantor, Georg", "1845 – 1918", 1918,
    [
        {
            'title': "Grundlagen einer allgemeinen Mannigfaltigkeitslehre",
            'english_title': "Foundations of a General Theory of Aggregates",
            'year': "1883",
            'notes': "Foundational treatise on set theory, transfinite numbers, and the continuum (Leipzig: Teubner).",
            'citations': [
                {
                    'ref': "Caput I, § 4 & Caput II, § 2",
                    'loc_link': "caput-1/caput-1-en.md#4-on-the-arithmetization-of-the-continuum",
                    'refers_to': "Cantor's construction of the mathematical continuum as an infinite aggregate (insieme) of discrete real numbers with the cardinality of the power set of integers.",
                    'supports_text': "Represents the ultimate modern formal replacement of the intuitive continuum with infinite discrete point sets, contrasting with the Aristotelian continuum whose parts are only in potency."
                }
            ]
        }
    ]
)

# ==============================================================
# 29. Josef Wellstein (1869 – 1919)
# ==============================================================
add_author(
    "Wellstein, Josef", "Wellstein, Josef", "1869 – 1919", 1919,
    [
        {
            'title': "Elemente der Geometrie (in Weber-Wellstein Enzyklopädie, Band II)",
            'english_title': "Elements of Geometry (in Weber-Wellstein Encyclopedia, Vol. II)",
            'year': "1905",
            'notes': "Comprehensive German reference work on elementary mathematics from an advanced viewpoint (Leipzig: Teubner).",
            'citations': [
                {
                    'ref': "Caput III, [^6] & [^9] (Vol. II, pp. 9–10)",
                    'loc_link': "caput-3/caput-3-en.md#fn-6",
                    'refers_to': "Wellstein's analysis of sensory inexactitude and his attempt to formulate geometric congruence purely through static axioms without motion.",
                    'supports_text': "Illustrates modern axiomatic attempts to bypass motion; Hoenen shows that even static congruence axioms secretly presuppose the imaginative mental translation of shapes in intelligible matter."
                },
                {
                    'ref': "Caput IV, [^6]",
                    'loc_link': "caput-4/caput-4-en.md#fn-6",
                    'refers_to': "Wellstein's treatment of congruence and the avoidance of superposition.",
                    'supports_text': "Demonstrates that avoiding physical motion in geometric proofs does not eliminate the intellect's constructive abstraction."
                }
            ]
        }
    ]
)

# ==============================================================
# 30. Wilhelm Killing (1847 – 1923)
# ==============================================================
add_author(
    "Killing, Wilhelm", "Killing, Wilhelm", "1847 – 1923", 1923,
    [
        {
            'title': "Einführung in die Grundlagen der Geometrie",
            'english_title': "Introduction to the Foundations of Geometry",
            'year': "1893, 1898",
            'notes': "Pioneering two-volume treatise on geometric foundations and Lie algebras (Paderborn: Schöningh).",
            'citations': [
                {
                    'ref': "Caput IV, [^16], [^17], [^18], [^19] (Vol. I, pp. 48–52)",
                    'loc_link': "caput-4/caput-4-en.md#fn-16",
                    'refers_to': "Killing's thorough dissection of the concept of 'direction' (Richtung): 'Der Winkel misst den Richtungsunterschied zweier Geraden... Man darf nur sagen: sie haben gleiche oder ungleiche Richtung in Bezug auf eine bestimmte dritte Gerade.'",
                    'supports_text': "Decisive support for Hoenen's critique of attempts to define straight lines and parallels via direction: Killing demonstrates that direction cannot be defined without already presupposing the very parallel straight lines one is trying to define."
                }
            ]
        }
    ]
)

# ==============================================================
# 31. Clemens Baeumker (1853 – 1924)
# ==============================================================
add_author(
    "Baeumker, Clemens", "Baeumker, Clemens", "1853 – 1924", 1924,
    [
        {
            'title': "Das Problem der Materie in der griechischen Philosophie",
            'english_title': "The Problem of Matter in Greek Philosophy",
            'year': "1890",
            'notes': "Monumental historical investigation of ancient Greek concepts of matter (Münster: Aschendorff).",
            'citations': [
                {
                    'ref': "Caput III, [^2] (pp. 288 ff.)",
                    'loc_link': "caput-3/caput-3-en.md#fn-2",
                    'refers_to': "Baeumker's historical documentation of intelligible matter (materia intelligibilis / hyle noete) in Aristotle's Metaphysics and Physics.",
                    'supports_text': "Provides definitive historical authority for Hoenen's Thomistic doctrine: mathematical objects retain extension as intelligible matter within imagination, while abstracting from physical matter."
                }
            ]
        }
    ]
)

# ==============================================================
# 32. Alois Riehl (1844 – 1924)
# ==============================================================
add_author(
    "Riehl, Alois", "Riehl, Alois", "1844 – 1924", 1924,
    [
        {
            'title': "Logik und Erkenntnistheorie (in Die Kultur der Gegenwart)",
            'english_title': "Logic and Theory of Knowledge (in The Culture of the Present)",
            'year': "1921",
            'notes': "Systematic epistemological essay in Die Kultur der Gegenwart (Teil I, Abt. 6, 3rd ed., Leipzig: Teubner, pp. 71 ff.).",
            'citations': [
                {
                    'ref': "Caput V, [^6] (p. 71)",
                    'loc_link': "caput-5/caput-5-en.md#fn-6",
                    'refers_to': "Riehl's analysis of the objective logical relationship between concepts in syllogistic deduction.",
                    'supports_text': "Supports Hoenen's thesis that the mental syllogism expresses an objective connection between essences, which cannot be reduced to verbal formalism."
                }
            ]
        }
    ]
)

# ==============================================================
# 33. Felix Klein (1849 – 1925)
# ==============================================================
add_author(
    "Klein, Felix", "Klein, Felix", "1849 – 1925", 1925,
    [
        {
            'title': "Anwendung der Differential- und Integralrechnung auf Geometrie: Eine Revision der Prinzipien",
            'english_title': "Application of Differential and Integral Calculus to Geometry: A Revision of Principles",
            'year': "1902 (2nd ed. 1907)",
            'notes': "Famous lectures re-evaluating the foundational principles of calculus and geometry (Leipzig: Teubner).",
            'citations': [
                {
                    'ref': "Caput I, [^7] & [^8] (pp. 7, 11)",
                    'loc_link': "caput-1/caput-1-en.md#fn-7",
                    'refers_to': "Klein's explicit formulation: 'In allen diesen praktischen Gebieten gibt es einen Schwellenwert der Genauigkeit... Im ideellen Gebiet der Arithmetik gibt es keinen endlichen Schwellenwert.'",
                    'supports_text': "The primary modern formulation of the **Problem of Exactitude**: Klein proves that all physical measurements have a finite threshold of exactitude, whereas mathematics demands infinite exactitude, proving that geometry is not an empirical science."
                }
            ]
        },
        {
            'title': "Elementarmathematik vom höheren Standpunkte aus (Band II: Geometrie)",
            'english_title': "Elementary Mathematics from an Advanced Standpoint (Vol. II: Geometry)",
            'year': "1925 (3rd ed.)",
            'notes': "Klein's celebrated masterwork on geometric pedagogy and foundations (Berlin: Springer).",
            'citations': [
                {
                    'ref': "Caput IV, [^23] & [^24] (Vol. II, pp. 189–194)",
                    'loc_link': "caput-4/caput-4-en.md#fn-23",
                    'refers_to': "Klein's demonstration that within physical measurement limits, Euclidean and non-Euclidean geometry are indistinguishable, and his discussion of the threshold of exactitude regarding parallel lines.",
                    'supports_text': "Proves that physical experiment cannot decide between Euclidean and non-Euclidean geometry, confirming that geometric structures are evaluated by the intellect."
                }
            ]
        }
    ]
)

# ==============================================================
# 34. Gerhard Hessenberg (1874 – 1925)
# ==============================================================
add_author(
    "Hessenberg, Gerhard", "Hessenberg, Gerhard", "1874 – 1925", 1925,
    [
        {
            'title': "Ebene und sphärische Trigonometrie",
            'english_title': "Plane and Spherical Trigonometry",
            'year': "1904",
            'notes': "Textbook comparing physical observation with geometric proof (Leipzig: Göschen).",
            'citations': [
                {
                    'ref': "Caput II, [^10]",
                    'loc_link': "caput-2/caput-2-en.md#fn-10",
                    'refers_to': "Hessenberg's comparison between physical judgments and mathematical judgments.",
                    'supports_text': "Illustrates the fundamental epistemological divide: physical judgments are contingent hypotheses subject to revision, while geometric judgments are perceived with apodictic necessity."
                }
            ]
        }
    ]
)

# ==============================================================
# 35. Henri Carteron (1891 – 1927)
# ==============================================================
add_author(
    "Carteron, Henri", "Carteron, Henri", "1891 – 1927", 1927,
    [
        {
            'title': "Aristote: Physique (Collection Budé)",
            'english_title': "Aristotle: Physics (Budé Edition)",
            'year': "1926",
            'notes': "Standard French critical edition and translation of the Physics (Paris: Les Belles Lettres, 2 vols.).",
            'citations': [
                {
                    'ref': "Appendix, [^10] (Vol. I, p. 134)",
                    'loc_link': "appendix/appendix-en.md#fn-10",
                    'refers_to': "Carteron's French rendering of Aristotle's definition of place in Physics IV, 5.",
                    'supports_text': "Provides philological backing for Hoenen's translation and interpretation of the containment relation in place."
                }
            ]
        }
    ]
)

# ==============================================================
# 36. John Burnet (1863 – 1928)
# ==============================================================
add_author(
    "Burnet, John", "Burnet, John", "1863 – 1928", 1928,
    [
        {
            'title': "The Ethics of Aristotle",
            'english_title': "The Ethics of Aristotle",
            'year': "1900",
            'notes': "Masterly critical edition and commentary on the Nicomachean Ethics (London: Methuen).",
            'citations': [
                {
                    'ref': "Appendix, [^9] (on EN IX, 9)",
                    'loc_link': "appendix/appendix-en.md#fn-9",
                    'refers_to': "Burnet's analytical outline of Aristotle's argumentation on consciousness and existence in Chapter 9.",
                    'supports_text': "Confirms the rigorous structural unity of Aristotle's deduction of self-existence from the exercise of perception and thought."
                }
            ]
        }
    ]
)

# ==============================================================
# 37. Eduard Study (1862 – 1930)
# ==============================================================
add_author(
    "Study, Eduard", "Study, Eduard", "1862 – 1930", 1930,
    [
        {
            'title': "Die realistische Weltansicht und die Lehre vom Raume",
            'english_title': "The Realistic Worldview and the Doctrine of Space",
            'year': "1914",
            'notes': "Trenchant philosophical treatise defending mathematical realism against conventionalism and logicism (Braunschweig: Vieweg).",
            'citations': [
                {
                    'ref': "Caput I, [^13] (p. 131)",
                    'loc_link': "caput-1/caput-1-en.md#fn-13",
                    'refers_to': "Study's declaration: 'Ausschlaggebend für die Beurtheilung der Sachlage scheint uns der Umstand zu sein, dass eine von der Analysis wirklich unabhängige Geometrie, wie das antike Ideal sie eigentlich verlangen würde, sich als eine Utopie herausgestellt hat.'",
                    'supports_text': "Highlights the contemporary mathematician's despair of saving synthetic geometry from pure analysis; Hoenen accepts Study's historical assessment while restoring the realistic noetic foundation."
                },
                {
                    'ref': "Caput III, [^5] (p. 75)",
                    'loc_link': "caput-3/caput-3-en.md#fn-5",
                    'refers_to': "Study on the reality of geometric spatial structures against pure nominalist formalism.",
                    'supports_text': "Supports Hoenen's realism against purely formalist interpretations of geometry."
                }
            ]
        }
    ]
)

# ==============================================================
# 38. Moritz Pasch (1843 – 1930)
# ==============================================================
add_author(
    "Pasch, Moritz", "Pasch, Moritz", "1843 – 1930", 1930,
    [
        {
            'title': "Vorlesungen über neuere Geometrie",
            'english_title': "Lectures on Modern Geometry",
            'year': "1882 (2nd ed. with Max Dehn, 1926)",
            'notes': "Pioneering foundation of modern projective and axiomatic geometry; formulated Pasch's Axiom of order (Berlin: Springer).",
            'citations': [
                {
                    'ref': "Caput II, [^9] & [^16] (pp. 5–8, 20)",
                    'loc_link': "caput-2/caput-2-en.md#fn-9",
                    'refers_to': "Pasch's Kernsatz IV and axioms of order: if a straight line enters a triangle through one side, it must exit through one of the other two sides.",
                    'supports_text': "Hoenen shows that Pasch's Axiom is an undeniable, immediate necessary intuition: Euclid omitted it because it is so visually and intellectually obvious. Its discovery proves that geometry relies on intuitive topological continuity rather than pure uninterpreted symbols."
                }
            ]
        }
    ]
)

# ==============================================================
# 39. Aurel Voss (1845 – 1931)
# ==============================================================
add_author(
    "Voss, Aurel", "Voss, Aurel", "1845 – 1931", 1931,
    [
        {
            'title': "Über die mathematische Erkenntnis (in Die Kultur der Gegenwart)",
            'english_title': "On Mathematical Knowledge (in The Culture of the Present)",
            'year': "1914",
            'notes': "Epistemological treatise on mathematical cognition (Teil III, Abt. 1, Leipzig: Teubner, pp. 385–440).",
            'citations': [
                {
                    'ref': "Caput III, [^10]",
                    'loc_link': "caput-3/caput-3-en.md#fn-10",
                    'refers_to': "Voss's analysis of the relationship between mathematical concepts and sensory representation.",
                    'supports_text': "Affirms that mathematical exactitude transcends sensory perception through an intellectual process of conceptual idealization."
                }
            ]
        }
    ]
)

# ==============================================================
# 40. Giuseppe Peano (1858 – 1932)
# ==============================================================
add_author(
    "Peano, Giuseppe", "Peano, Giuseppe", "1858 – 1932", 1932,
    [
        {
            'title': "Arithmetices principia, nova methodo exposita",
            'english_title': "The Principles of Arithmetic, Presented by a New Method",
            'year': "1889",
            'notes': "Groundbreaking treatise introducing Peano's axioms and modern symbolic logic (Turin: Bocca).",
            'citations': [
                {
                    'ref': "Caput I, § 6 & Caput II, § 1",
                    'loc_link': "caput-1/caput-1-en.md#6-on-so-called-axiomatics",
                    'refers_to': "Peano's symbolic axiomatization of natural numbers and geometric foundations.",
                    'supports_text': "Hoenen demonstrates that Peano's axioms cannot be understood or applied without intuitive knowledge of the primitive notions (number, successor, equality) which they symbolically designate."
                }
            ]
        }
    ]
)

# ==============================================================
# 41. Émile Meyerson (1859 – 1933)
# ==============================================================
add_author(
    "Meyerson, Émile", "Meyerson, Emile", "1859 – 1933", 1933,
    [
        {
            'title': "Du cheminement de la pensée",
            'english_title': "The Progression of Thought",
            'year': "1931",
            'notes': "Meyerson's three-volume magnum opus on the epistemology of science and the human intellect's demand for ontological identity (Paris: Alcan).",
            'citations': [
                {
                    'ref': "Appendix, [^7] (Vol. II, p. 391, n. 232)",
                    'loc_link': "appendix/appendix-en.md#fn-7",
                    'refers_to': "Meyerson's observation that the human mind inherently seeks the identity of being across change and recognizes reality beyond phenomenal sensations.",
                    'supports_text': "Supports Hoenen's thesis that the mind's grasp of existential connections is an innate, essential function of intellectual cognition."
                }
            ]
        }
    ]
)

# ==============================================================
# 42. Angelo M. Pirotta, O.P. (1871 – 1939)
# ==============================================================
add_author(
    "Pirotta, Angelo M., O.P.", "Pirotta, Angelo M.", "1871 – 1939", 1939,
    [
        {
            'title': "S. Thomae Aquinatis in Aristotelis librum De Anima commentarium",
            'english_title': "St. Thomas Aquinas's Commentary on Aristotle's De Anima",
            'year': "1936",
            'notes': "Standard Marietti edition with critical paragraph numbering (Turin: Marietti).",
            'citations': [
                {
                    'ref': "Caput I, § 2 (nos. 770–772, 777, 791)",
                    'loc_link': "caput-1/caput-1-en.md#2-on-the-origin-of-mathematical-notions",
                    'refers_to': "Pirotta's paragraph numbers for Aquinas's commentary on intellectual abstraction from phantasms.",
                    'supports_text': "Provides precise textual citations for the Thomistic doctrine of conversion to the phantasm in mathematical cognition."
                }
            ]
        }
    ]
)

# ==============================================================
# 43. Sir Thomas Little Heath (1861 – 1940)
# ==============================================================
add_author(
    "Heath, Sir Thomas Little", "Heath, Sir Thomas Little", "1861 – 1940", 1940,
    [
        {
            'title': "A History of Greek Mathematics",
            'english_title': "A History of Greek Mathematics",
            'year': "1921",
            'notes': "The definitive two-volume history of Greek mathematics (Oxford: Clarendon Press).",
            'citations': [
                {
                    'ref': "Caput V, [^1] (Vol. I, pp. 335 ff.)",
                    'loc_link': "caput-5/caput-5-en.md#fn-1",
                    'refers_to': "Heath's historical documentation that Aristotle and Greek mathematicians rigorously distinguished axioms (evident to all), hypotheses (propositions accepted by the student), and postulates (demands made without student agreement).",
                    'supports_text': "Validates Hoenen's classical division of scientific principles against the modern collapse of all principles into arbitrary uninterpreted postulates."
                }
            ]
        },
        {
            'title': "The Thirteen Books of Euclid's Elements",
            'english_title': "The Thirteen Books of Euclid's Elements",
            'year': "1908 (2nd ed. 1926)",
            'notes': "Standard English translation and monumental commentary on Euclid (Cambridge University Press, 3 vols.).",
            'citations': [
                {
                    'ref': "Caput I, § 1 & Caput IV, § 4",
                    'loc_link': "caput-1/caput-1-en.md#1-on-the-proper-place-of-this-investigation-in-philosophy",
                    'refers_to': "Heath's historical notes on the fifth postulate, the definitions of line and surface, and the Eudoxian theory of Book V.",
                    'supports_text': "Serves as the scholarly authority throughout Hoenen's textual analysis of Euclidean mathematics."
                }
            ]
        }
    ]
)

# ==============================================================
# 44. Felix Hausdorff (1868 – 1942)
# ==============================================================
add_author(
    "Hausdorff, Felix", "Hausdorff, Felix", "1868 – 1942", 1942,
    [
        {
            'title': "Das Raumproblem",
            'english_title': "The Problem of Space",
            'year': "1904",
            'notes': "Philosophical paper published in Annalen der Naturphilosophie (Vol. 3, pp. 1–23).",
            'citations': [
                {
                    'ref': "Caput IV, [^21] (p. 3)",
                    'loc_link': "caput-4/caput-4-en.md#fn-21",
                    'refers_to': "Hausdorff's statement: 'Die Mathematik hat sich vom Raume losgesagt; sie ist rein logisch geworden... Der Raum ist für sie ein Gedankending.' ('Mathematics has detached itself from space; it has become purely logical... Space is for it a mere mental thing.')",
                    'supports_text': "Quotes Hausdorff as an authoritative witness to modern mathematics' abandonment of intuitive physical space, sharpening Hoenen's critique of extreme formalism."
                }
            ]
        }
    ]
)

# ==============================================================
# 45. David Hilbert (1862 – 1943)
# ==============================================================
add_author(
    "Hilbert, David", "Hilbert, David", "1862 – 1943", 1943,
    [
        {
            'title': "Grundlagen der Geometrie",
            'english_title': "Foundations of Geometry",
            'year': "1899 (7th ed. 1930)",
            'notes': "Hilbert's revolutionary work establishing the formal axiomatic method for Euclidean geometry (Leipzig: Teubner).",
            'citations': [
                {
                    'ref': "Caput I, [^14] (7th ed., p. 2)",
                    'loc_link': "caput-1/caput-1-en.md#fn-14",
                    'refers_to': "Hilbert's opening declaration: 'Wir denken uns drei verschiedene Systeme von Dingen: die Dinge des ersten Systems nennen wir Punkte... des zweiten Systems Geraden... des dritten Systems Ebenen...' ('We conceive three different systems of things: the things of the first system we call points... the second straight lines... the third planes...')",
                    'supports_text': "Exposes the core thesis of modern formalism: points, lines, and planes are defined purely by implicit relations rather than intuitive essences. Hoenen demonstrates that this program cannot sustain geometry without intuitive intelligible matter."
                },
                {
                    'ref': "Caput IV, [^1]",
                    'loc_link': "caput-4/caput-4-en.md#fn-1",
                    'refers_to': "Hilbert's use of intuitive 'explanations' (Erklärungen) interspersed among his formal axioms.",
                    'supports_text': "Hoenen demonstrates a crucial inconsistency in Hilbert's method: Hilbert smuggles intuitive geometric meaning back into his system through informal 'explanations,' revealing that pure formalism is impossible in practice."
                },
                {
                    'ref': "Caput V, [^9] & [^10]",
                    'loc_link': "caput-5/caput-5-en.md#fn-9",
                    'refers_to': "Hilbert's theorem on the linear order of points: 'Sind irgendeine endliche Anzahl von Punkten einer Geraden gegeben...' and G. H. Hardy's critique.",
                    'supports_text': "Shows that Hilbert's proof of the linear ordering of points relies on spatial diagrams and visual inspection rather than purely mechanical deduction."
                }
            ]
        }
    ]
)

# ==============================================================
# 46. Federigo Enriques (1871 – 1946)
# ==============================================================
add_author(
    "Enriques, Federigo", "Enriques, Federigo", "1871 – 1946", 1946,
    [
        {
            'title': "Questioni riguardanti le matematiche elementari",
            'english_title': "Questions Regarding Elementary Mathematics",
            'year': "1924 (3rd ed.)",
            'notes': "Influential Italian collection on geometric foundations, edited by Enriques (Bologna: Zanichelli).",
            'citations': [
                {
                    'ref': "Caput IV, [^15] & [^20] (Vol. I, pp. 43–44)",
                    'loc_link': "caput-4/caput-4-en.md#fn-15",
                    'refers_to': "Articles by Enriques and Ugo Amaldi examining Euclidean postulates and the circularity of defining parallel lines via direction.",
                    'supports_text': "Corroborates Hoenen's finding that direction cannot replace Euclid's parallel postulate without covert circularity."
                }
            ]
        }
    ]
)

# ==============================================================
# 47. Godfrey Harold Hardy (1877 – 1947)
# ==============================================================
add_author(
    "Hardy, Godfrey Harold", "Hardy, Godfrey Harold", "1877 – 1947", 1947,
    [
        {
            'title': "Mathematical Proof",
            'english_title': "Mathematical Proof",
            'year': "1929",
            'notes': "Philosophical paper in Mind (New Series, Vol. 38, No. 149, pp. 1–25).",
            'citations': [
                {
                    'ref': "Caput V, [^8] & [^10] (pp. 12, 18)",
                    'loc_link': "caput-5/caput-5-en.md#fn-8",
                    'refers_to': "Hardy's candid confession: 'I believe the prime Number Theorem because of de la Vallée-Poussin's proof of it, but I do not believe that 2 + 2 = 4 because of a proof by Russell... If Hilbert's axioms are to mean anything to us, we must draw figures.'",
                    'supports_text': "Decisive testimonial evidence from a world-class pure mathematician: formal axiomatic deductions depend on intuitive conviction, and Hilbert's axioms are completely sterile without imaginative diagrams."
                }
            ]
        }
    ]
)

# ==============================================================
# 48. Joseph Geyser (1869 – 1948)
# ==============================================================
add_author(
    "Geyser, Joseph", "Geyser, Joseph", "1869 – 1948", 1948,
    [
        {
            'title': "Die Erkenntnistheorie des Aristoteles",
            'english_title': "The Epistemology of Aristotle",
            'year': "1917",
            'notes': "Thorough Neoscholastic epistemological study of Aristotelian noetics (Münster: Schöningh).",
            'citations': [
                {
                    'ref': "Caput I, [^3] (chs. VI and XII)",
                    'loc_link': "caput-1/caput-1-en.md#fn-3",
                    'refers_to': "Geyser's analysis of how the intellect abstracts first principles and necessary propositions from sensible particulars.",
                    'supports_text': "Affirms Hoenen's peripatetic thesis: intellectual abstraction does not invent forms out of nothing, but reads necessary intelligible relations within sensible data."
                }
            ]
        }
    ]
)

print("Added authors up to Geyser.")

# ==============================================================
# 49. Albert Einstein (1879 – 1955)
# ==============================================================
add_author(
    "Einstein, Albert", "Einstein, Albert", "1879 – 1955", 1955,
    [
        {
            'title': "Geometrie und Erfahrung",
            'english_title': "Geometry and Experience",
            'year': "1921",
            'notes': "Expanded lecture to the Prussian Academy of Sciences on January 27, 1921 (Berlin: Springer).",
            'citations': [
                {
                    'ref': "Caput I, [^4]",
                    'loc_link': "caput-1/caput-1-en.md#fn-4",
                    'refers_to': "Einstein's celebrated dictum: 'Insofern sich die Sätze der Mathematik auf die Wirklichkeit beziehen, sind sie nicht sicher, und insofern sie sicher sind, beziehen sie sich nicht auf die Wirklichkeit.' ('As far as the laws of mathematics refer to reality, they are not certain; and as far as they are certain, they do not refer to reality.')",
                    'supports_text': "Hoenen takes this as the quintessential expression of the modern crisis: if applied mathematics is purely empirical physics, its certainty vanishes; if pure mathematics is certain, it has no relation to reality. Hoenen refutes this dilemma by showing that geometry abstracts intelligible matter from the real world, retaining necessary truth that applies necessarily to real physical extension."
                }
            ]
        },
        {
            'title': "Address in the journal Forum",
            'english_title': "Address in the Journal Forum",
            'year': "1930",
            'notes': "Discussion on the concept of space and coordinate systems in modern physics (Forum, I, p. 173; cited via Cosmologia, 4th ed., p. 468).",
            'citations': [
                {
                    'ref': "Caput VI, [^3] & Appendix, [^17]",
                    'loc_link': "caput-6/caput-6-en.md#fn-3",
                    'refers_to': "Einstein explaining that coordinate systems in physics require physical solid bodies of reference, and that empty space without matter has no independent physical reality.",
                    'supports_text': "Integrates Einstein's relativistic physical coordinates into the Thomistic cosmology of the category ubi: coordinates describe the physical surrounding container, confirming the realistic grounding of space."
                }
            ]
        }
    ]
)

# ==============================================================
# 50. Hermann Weyl (1885 – 1955)
# ==============================================================
add_author(
    "Weyl, Hermann", "Weyl, Hermann", "1885 – 1955", 1955.5,
    [
        {
            'title': "Philosophie der Mathematik und Naturwissenschaft",
            'english_title': "Philosophy of Mathematics and Natural Science",
            'year': "1927",
            'notes': "Treatise in the Handbuch der Philosophie (München: Oldenbourg; revised English ed., Princeton, 1949).",
            'citations': [
                {
                    'ref': "Caput IV, [^22] (p. 18)",
                    'loc_link': "caput-4/caput-4-en.md#fn-22",
                    'refers_to': "Weyl's observation that modern axiomatics turns geometry into a branch of pure logic, detaching it from spatial perception.",
                    'supports_text': "Demonstrates that even the foremost mathematical physicists recognize that formal axiomatics leaves the intuitive reality of geometric space behind."
                }
            ]
        }
    ]
)

# ==============================================================
# 51. Heinrich Scholz (1884 – 1956)
# ==============================================================
add_author(
    "Scholz, Heinrich", "Scholz, Heinrich", "1884 – 1956", 1956,
    [
        {
            'title': "Warum haben die Griechen die Irrationalzahlen nicht aufgebaut?",
            'english_title': "Why Did the Greeks Not Construct Irrational Numbers?",
            'year': "1928",
            'notes': "Historical-epistemological paper in Kantstudien (Vol. 33, pp. 35–72).",
            'citations': [
                {
                    'ref': "Caput I, [^6]",
                    'loc_link': "caput-1/caput-1-en.md#fn-6",
                    'refers_to': "Scholz's historical investigation into why the Greeks refused to treat incommensurable geometric ratios as arithmetic fractions.",
                    'supports_text': "Corroborates Hoenen's view that ancient mathematics possessed a profound philosophical respect for the irreducible distinction between continuous geometric magnitude and discrete arithmetic number."
                }
            ]
        }
    ]
)

# ==============================================================
# 52. Ugo Amaldi (1875 – 1957)
# ==============================================================
add_author(
    "Amaldi, Ugo", "Amaldi, Ugo", "1875 – 1957", 1957,
    [
        {
            'title': "Sui concetti fondamentali della geometria (in Enriques' Questioni)",
            'english_title': "On the Fundamental Concepts of Geometry",
            'year': "1924",
            'notes': "Monograph on elementary geometry and parallel postulates in Enriques' Questioni riguardanti le matematiche elementari (Vol. I, pp. 43–44).",
            'citations': [
                {
                    'ref': "Caput IV, [^15] & [^20]",
                    'loc_link': "caput-4/caput-4-en.md#fn-15",
                    'refers_to': "Amaldi's critical analysis of definitions of direction and parallelism.",
                    'supports_text': "Confirms that trying to define parallel lines by identity of direction is a circular definition, proving that direction cannot supersede the intuitive necessity of Euclid's parallel postulate."
                }
            ]
        }
    ]
)

# ==============================================================
# 53. Petrus Hubertus Jacobus Hoenen, S.J. (1880 – 1961)
# ==============================================================
add_author(
    "Hoenen, Petrus Hubertus Jacobus, S.J.", "Hoenen, Petrus Hubertus Jacobus, S.J.", "1880 – 1961", 1961,
    [
        {
            'title': "Cosmologia",
            'english_title': "Cosmology",
            'year': "1931 (4th ed. 1949; 5th ed. 1956)",
            'notes': "Hoenen's standard Latin manual of the philosophy of nature at the Gregorian University (Rome: Gregorianum).",
            'citations': [
                {
                    'ref': "Caput I, [^5] (Notes III & VII, pp. 446–455, 471–482)",
                    'loc_link': "caput-1/caput-1-en.md#fn-5",
                    'refers_to': "Expositions of non-Euclidean geometry and physical space coordinates.",
                    'supports_text': "Provides the cosmological framework establishing that physical space is not an empty absolute container but a system of relations among extended bodies."
                },
                {
                    'ref': "Caput V, [^12] & Caput VI, [^2], [^3]",
                    'loc_link': "caput-5/caput-5-en.md#fn-12",
                    'refers_to': "Physical proper attributes impeding exactitude in bodies, and the analysis of the category ubi.",
                    'supports_text': "Shows how physical matter fluctuates while mathematical intelligible matter admits immutable exactitude."
                },
                {
                    'ref': "Appendix, [^6], [^12], [^15], [^16], [^17], [^19], [^20], [^22]",
                    'loc_link': "appendix/appendix-en.md#fn-6",
                    'refers_to': "Detailed references to Note IV (relativity of motion, p. 456), Note VI (ubi, p. 468), Note XIII (motion as an existential act, pp. 527–530), Note XV (neo-positivism, p. 538), and the actuality of continua (p. 40).",
                    'supports_text': "Supplies the foundational metaphysics for the entire Appendix: motion is an existential act (actus existentialis), extension is an actuality of continua, and the category ubi establishes real relations between physical existents."
                }
            ]
        },
        {
            'title': "La théorie du jugement d'après St. Thomas d'Aquin",
            'english_title': "The Theory of Judgment According to St. Thomas Aquinas (Reality and Judgment)",
            'year': "1946 (2nd ed. 1953; English trans. 1952)",
            'notes': "Hoenen's epistemological masterwork in Analecta Gregoriana (Vol. XXXIX; English translation Reality and Judgment by H. F. Tiblier, Chicago: Regnery, 1952). Cited as Th. d. J. and R. a. J.",
            'citations': [
                {
                    'ref': "Praefatio, [^2] & Caput I, [^2]",
                    'loc_link': "preface/preface-en.md#fn-2",
                    'refers_to': "The fundamental doctrine of the two operations of the intellect: first operation = apprehension of quiddity; second operation = judgment attributing esse.",
                    'supports_text': "The epistemological matrix of De Noetica Geometriae: mathematical knowledge begins in apprehension of quiddities in intelligible matter, but culminates in affirmative judgments of necessary existence."
                },
                {
                    'ref': "Caput II, [^6], [^13], [^15], [^17]",
                    'loc_link': "caput-2/caput-2-en.md#fn-6",
                    'refers_to': "Analysis of the sensory datum as 'determinative' rather than 'motive' of judgment; virtual judgments; and the material and formal nexus (chs. III–IV).",
                    'supports_text': "Solves the Problem of Necessity: the sensory phantasm determines the occasion of judgment, but the intellect itself is the active motive force perceiving formal necessity."
                },
                {
                    'ref': "Appendix, [^1], [^25], [^26], [^27], [^29], [^30]",
                    'loc_link': "appendix/appendix-en.md#fn-1",
                    'refers_to': "The Cogito as immediate judgment (ch. XII); comparison with Franz Brentano (ch. II, § 4); definition of realism (pp. 190–194); and determination of the agent intellect by accepted data (pp. 25–26).",
                    'supports_text': "Underpins the metaphysics of the Appendix: validates the concept of being (ratio essendi) and proves that the second operation of the intellect directly grasps the existential act of realism."
                }
            ]
        },
        {
            'title': "Filosofia della natura inorganica",
            'english_title': "Philosophy of Inorganic Nature",
            'year': "1949",
            'notes': "Italian treatise on inorganic natural philosophy (Brescia: Morcelliana).",
            'citations': [
                {
                    'ref': "Caput VI, [^2] & Appendix, [^16], [^17] (pp. 110, 112, 220)",
                    'loc_link': "caput-6/caput-6-en.md#fn-2",
                    'refers_to': "The philosophical definition of physical space, coordinate bodies, and the critique of relativistic positivism.",
                    'supports_text': "Reinforces the realistic interpretation of coordinate frames and spatial extension in physical nature."
                }
            ]
        },
        {
            'title': "De origine formae materialis",
            'english_title': "On the Origin of Material Form",
            'year': "1951 (2nd ed.)",
            'notes': "Latin textbook compiling classical Thomistic texts on the eduction of material forms (Rome: Gregorianum).",
            'citations': [
                {
                    'ref': "Appendix, [^22]",
                    'loc_link': "appendix/appendix-en.md#fn-22",
                    'refers_to': "The twofold function of material form: quidditative (constituting essence) and existential (determining the mode of being).",
                    'supports_text': "Demonstrates that form does not merely define what a thing is, but determines how it exercises its existential act of being."
                }
            ]
        },
        {
            'title': "Articles in Gregorianum and Commemorative Volumes",
            'english_title': "Scholarly Papers in Gregorianum and Festschriften",
            'year': "1933–1953",
            'notes': "Major peer-reviewed research papers in Gregorianum and international philosophy congresses.",
            'citations': [
                {
                    'ref': "Praefatio, [^1] (Gregorianum 1938, 1939, 1943, 1951)",
                    'loc_link': "preface/preface-en.md#fn-1",
                    'refers_to': "The four-part series 'De philosophia scholastica cognitionis geometricae' and the reply to Freudenthal.",
                    'supports_text': "The primary journal papers that formed the initial drafts of the chapters of De Noetica Geometriae."
                },
                {
                    'ref': "Caput II, [^1] & Caput I, [^3] (Gregorianum 1933, pp. 153–184)",
                    'loc_link': "caput-2/caput-2-en.md#fn-1",
                    'refers_to': "'De origine primorum principiorum scientiae' (On the Origin of the First Principles of Science).",
                    'supports_text': "Presents the foundational epistemology of how first principles are abstracted intuitively from sensible phantasms."
                },
                {
                    'ref': "Caput II, [^12], [^14] & Appendix, [^1] (Cartesio, 1937, pp. 457–471)",
                    'loc_link': "caput-2/caput-2-en.md#fn-12",
                    'refers_to': "'Le « cogito ergo sum » comme intuition et comme mouvement de la pensée'.",
                    'supports_text': "Establishes the Thomistic interpretation of the Cartesian Cogito as an intellectual intuition of existential actuality."
                },
                {
                    'ref': "Caput II, [^8] & Caput V, [^11] (10th Phil. Congress 1948; Gregorianum 1950, pp. 126–132)",
                    'loc_link': "caput-2/caput-2-en.md#fn-8",
                    'refers_to': "'Pour une philosophie de la connaissance de l'étendue physique'.",
                    'supports_text': "Addresses how the intellect abstracts exact mathematical continuity from physical perceptions of extended bodies."
                },
                {
                    'ref': "Caput V, [^2] (Gregorianum 1951, pp. 263–268)",
                    'loc_link': "caput-5/caput-5-en.md#fn-2",
                    'refers_to': "'De fontibus geometriae: Responsio ad Cl. H. Freudenthal'.",
                    'supports_text': "Direct defense of the intuitive origin of geometry against Hans Freudenthal's formalist critique."
                },
                {
                    'ref': "Caput VI, [^5] & Appendix, [^14], [^32] (Gregorianum 1953, pp. 1–31)",
                    'loc_link': "caput-6/caput-6-en.md#fn-5",
                    'refers_to': "'De duratione successiva et de quaestionibus connexis'.",
                    'supports_text': "Establishes that successive duration is fluent existential extension (esse fluens), distinct from permanent geometric extension."
                },
                {
                    'ref': "Caput VI, [^7] & Caput VII, [^3] (Gregorianum 1953, pp. 603–639)",
                    'loc_link': "caput-6/caput-6-en.md#fn-7",
                    'refers_to': "'De connexionibus necessariis inter actus existentiales'.",
                    'supports_text': "The extensive study that was directly incorporated with additions as the Appendix of this monograph."
                }
            ]
        }
    ]
)

# ==============================================================
# 54. Charles-Jean de la Vallée-Poussin (1866 – 1962)
# ==============================================================
add_author(
    "Vallée-Poussin, Charles-Jean de la", "Vallee-Poussin, Charles-Jean de la", "1866 – 1962", 1962,
    [
        {
            'title': "Recherches analytiques sur la théorie des nombres premiers",
            'english_title': "Analytical Researches on the Theory of Prime Numbers",
            'year': "1896",
            'notes': "Landmark memoir proving the Prime Number Theorem; published in Annales de la Société scientifique de Bruxelles.",
            'citations': [
                {
                    'ref': "Caput V, [^8]",
                    'loc_link': "caput-5/caput-5-en.md#fn-8",
                    'refers_to': "G. H. Hardy's reference to de la Vallée-Poussin's proof of the Prime Number Theorem.",
                    'supports_text': "Contrasts a long deductive proof (which compels belief through an intricate chain of syllogisms) with immediate intuitive arithmetic truths (such as 2 + 2 = 4)."
                }
            ]
        }
    ]
)

# ==============================================================
# 55. Jacques Hadamard (1865 – 1963)
# ==============================================================
add_author(
    "Hadamard, Jacques", "Hadamard, Jacques", "1865 – 1963", 1963,
    [
        {
            'title': "La géométrie (in Encyclopédie Française, Tome I)",
            'english_title': "Geometry (in French Encyclopedia, Vol. I: Mental Tools)",
            'year': "1937",
            'notes': "Survey essay on geometric intuition and displacement in Encyclopédie Française (Section I-52-10).",
            'citations': [
                {
                    'ref': "Caput IV, [^11] & [^22]",
                    'loc_link': "caput-4/caput-4-en.md#fn-11",
                    'refers_to': "Hadamard's observation that geometric displacement and motion cannot be eradicated from spatial understanding.",
                    'supports_text': "Confirms from a leading French mathematician that geometric congruence is fundamentally tied to spatial displacement."
                }
            ]
        }
    ]
)

# ==============================================================
# 56. Bertrand Russell (1872 – 1970)
# ==============================================================
add_author(
    "Russell, Bertrand", "Russell, Bertrand", "1872 – 1970", 1970,
    [
        {
            'title': "The Principles of Mathematics",
            'english_title': "The Principles of Mathematics",
            'year': "1903 (2nd ed. 1937)",
            'notes': "Russell's foundational logicist masterpiece (London: Allen & Unwin).",
            'citations': [
                {
                    'ref': "Caput IV, [^3], [^4], [^5] (nos. 390 ff., pp. 405–407)",
                    'loc_link': "caput-4/caput-4-en.md#fn-3",
                    'refers_to': "Russell's scathing critique of Euclid's superposition proof: 'It has no logical validity, and strikes every intelligent child as a juggle... to speak of motion implies that our triangles are not spatial but material.'",
                    'supports_text': "Hoenen uses Russell's objection to make a crucial distinction: physical superposition of material bodies indeed cannot prove geometric equality, but mental translation of figures within intelligible matter (materia intelligibilis) is an authentic intellectual operation that grounds congruence."
                },
                {
                    'ref': "Caput IV, [^28] (pp. 404 ff.)",
                    'loc_link': "caput-4/caput-4-en.md#fn-28",
                    'refers_to': "Russell's critique of empiricism: 'There is no evidence whatever that the circles which we are supposed to observe are true circles... geometry is not based upon observation of empirical shapes.'",
                    'supports_text': "Enlists Russell's logicist critique to demolish sensory empiricism: mathematical figures are never found in physical sensation, confirming their status as abstract intelligible entities."
                }
            ]
        }
    ]
)

# ==============================================================
# 57. Anneliese Maier (1905 – 1971)
# ==============================================================
add_author(
    "Maier, Anneliese", "Maier, Anneliese", "1905 – 1971", 1971,
    [
        {
            'title': "An der Grenze von Scholastik und Naturwissenschaft",
            'english_title': "On the Border of Scholasticism and Natural Science",
            'year': "1943",
            'notes': "Groundbreaking historical study of late medieval natural philosophy and 14th-century Parisian and Oxonian physics (Rome: Edizioni di Storia e Letteratura).",
            'citations': [
                {
                    'ref': "Appendix, [^33] (pp. 312 ff.)",
                    'loc_link': "appendix/appendix-en.md#fn-33",
                    'refers_to': "Maier's historical documentation of Nicole Oresme's doctrine of configurations of qualities and motions.",
                    'supports_text': "Hoenen utilizes Maier's scholarly findings while offering a philosophical correction: Maier treated Oresme's doctrine primarily as a mathematical precursor to coordinate geometry, whereas Hoenen shows that it represents a profound metaphysical insight into the qualitative configuration of fluent existential acts (esse fluens)."
                }
            ]
        }
    ]
)

# ==============================================================
# 58. Sir William David Ross (1877 – 1971)
# ==============================================================
add_author(
    "Ross, Sir William David", "Ross, Sir William David", "1877 – 1971", 1971.5,
    [
        {
            'title': "Aristotle's Metaphysics, Physics, and Analytics",
            'english_title': "Oxford Critical Editions and Commentaries on Aristotle",
            'year': "1924, 1936, 1949",
            'notes': "The premier 20th-century critical Greek texts and English commentaries on Aristotle's works (Oxford: Clarendon Press).",
            'citations': [
                {
                    'ref': "Caput I, [^3] & Caput IV, [^7]",
                    'loc_link': "caput-1/caput-1-en.md#fn-3",
                    'refers_to': "Ross's general monograph Aristotle (pp. 38–41, 54, 217) and critical edition of Physics IV.",
                    'supports_text': "Standard scholarly authority for peripatetic abstraction and natural philosophy."
                },
                {
                    'ref': "Appendix, [^3], [^5], [^13] (Metaphysics II, pp. 245, 264, 401)",
                    'loc_link': "appendix/appendix-en.md#fn-3",
                    'refers_to': "Ross's recension and English translation of Metaphysics IX, 3 ('The word actuality, which we connect with complete reality...'), and his textual reading of ἔστιν (estin, with paroxytone accent indicating existence).",
                    'supports_text': "Decisive philological support: reading ἔστιν confirms that Aristotle is treating actual existence in time rather than a mere copula, proving that the mover must already actually exist."
                }
            ]
        }
    ]
)

# ==============================================================
# 59. Gerhard Stammler (1898 – 1977)
# ==============================================================
add_author(
    "Stammler, Gerhard", "Stammler, Gerhard", "1898 – 1977", 1977,
    [
        {
            'title': "Begriff, Urteil, Schluss",
            'english_title': "Concept, Judgment, Inference",
            'year': "1928",
            'notes': "Epistemological investigation into the foundations of logic and judgment (Halle: Niemeyer).",
            'citations': [
                {
                    'ref': "Caput V, [^7] (pp. 229, 245)",
                    'loc_link': "caput-5/caput-5-en.md#fn-7",
                    'refers_to': "Stammler's demonstration that inference requires a synthetic apprehension of the relation between concepts.",
                    'supports_text': "Confirms that logical inference cannot be reduced to mechanical algorithmic manipulation without intellectual insight."
                }
            ]
        }
    ]
)

# ==============================================================
# 60. Étienne Gilson (1884 – 1978)
# ==============================================================
add_author(
    "Gilson, Étienne", "Gilson, Etienne", "1884 – 1978", 1978,
    [
        {
            'title': "L'être et l'essence & Being and Some Philosophers",
            'english_title': "Being and Essence (1948) & Being and Some Philosophers (1949)",
            'year': "1948, 1949",
            'notes': "Gilson's landmark treatises establishing existential Thomism and distinguishing it from essentialism (Paris: Vrin / Toronto: PIMS).",
            'citations': [
                {
                    'ref': "Appendix, § 7 and [^23], [^27] (L'être et l'essence, p. 248)",
                    'loc_link': "appendix/appendix-en.md#is-esse-conceptualizable",
                    'refers_to': "Gilson's thesis opposing 'existential' and 'essential' metaphysics, and his claim that esse itself is not conceptualizable ('un centre d'obscurité qu'il nous faut traverser pour atteindre l'existence').",
                    'supports_text': "Hoenen's pivotal critique: he praises Gilson for recovering the Thomistic primacy of esse, but demonstrates that Gilson goes too far in declaring esse completely unconceptualizable. Hoenen shows from St. Thomas that the intellect forms a true apprehensive concept of being (ratio essendi) following judgment, preserving the harmony between essence and existence."
                }
            ]
        }
    ]
)

# ==============================================================
# 61. Helmut Hasse (1898 – 1979)
# ==============================================================
add_author(
    "Hasse, Helmut", "Hasse, Helmut", "1898 – 1979", 1979,
    [
        {
            'title': "Die Grundlagenkrisis der griechischen Mathematik",
            'english_title': "The Foundational Crisis of Greek Mathematics",
            'year': "1928",
            'notes': "Historical-mathematical paper co-authored with Heinrich Scholz in Kantstudien (Vol. 33, pp. 4–34).",
            'citations': [
                {
                    'ref': "Caput I, [^6]",
                    'loc_link': "caput-1/caput-1-en.md#fn-6",
                    'refers_to': "Hasse and Scholz's analysis of the crisis caused by the discovery of incommensurable magnitudes in Pythagorean geometry.",
                    'supports_text': "Documents that the crisis of foundations in Greek geometry was resolved geometrically by Eudoxus rather than arithmetically."
                }
            ]
        }
    ]
)

# ==============================================================
# 62. Bernard Lonergan, S.J. (1904 – 1984)
# ==============================================================
add_author(
    "Lonergan, Bernard, S.J.", "Lonergan, Bernard, S.J.", "1904 – 1984", 1984,
    [
        {
            'title': "The Concept of Verbum in the Writings of St. Thomas Aquinas",
            'english_title': "The Concept of Verbum in the Writings of St. Thomas Aquinas",
            'year': "1946–1947",
            'notes': "Five seminal articles in Theological Studies (Vols. 7 & 8); later published as Verbum: Word and Idea in Aquinas (Notre Dame, 1967).",
            'citations': [
                {
                    'ref': "Appendix, § 7 and [^24] (Theological Studies 1946, pp. 349–392; 1947, pp. 35–79, 404–444; esp. Vol. I, p. 353)",
                    'loc_link': "appendix/appendix-en.md#is-esse-conceptualizable",
                    'refers_to': "Lonergan's demonstration that for St. Thomas, the term conceptio / conceptus is used not only for the definition produced in the first operation, but also for the interior word (verbum mentis) produced in judgment (the second operation).",
                    'supports_text': "Provides decisive contemporary Thomistic backing for Hoenen's thesis against Gilson: St. Thomas explicitly recognizes that judgment produces an interior conception, proving that esse is conceptualizable in the second operation of the intellect."
                }
            ]
        }
    ]
)

# ==============================================================
# 63. Hans Freudenthal (1905 – 1990)
# ==============================================================
add_author(
    "Freudenthal, Hans", "Freudenthal, Hans", "1905 – 1990", 1990,
    [
        {
            'title': "De fontibus geometriae",
            'english_title': "On the Sources of Geometry",
            'year': "1951",
            'notes': "Critical Latin article published in Gregorianum (Vol. 32, pp. 252–262) disputing Hoenen's scholastic philosophy of geometry.",
            'citations': [
                {
                    'ref': "Praefatio, [^1] & Caput V, [^2]",
                    'loc_link': "caput-5/caput-5-en.md#fn-2",
                    'refers_to': "The debate between Freudenthal and Hoenen regarding whether axiomatic geometry can be constituted independently of intuitive abstraction.",
                    'supports_text': "Serves as the vital contemporary sparring partner: Freudenthal defended modern formal axiomatics, prompting Hoenen to elaborate his 'semi-axiomatic' analysis and prove that axioms cannot function without semantic reference to intelligible matter."
                }
            ]
        }
    ]
)

# ==============================================================
# 64. José Alvarez Laso, C.M.F. (1910 – 1993)
# ==============================================================
add_author(
    "Alvarez Laso, José, C.M.F.", "Alvarez Laso, Jose, C.M.F.", "1910 – 1993", 1993,
    [
        {
            'title': "La Filosofía de las Matemáticas en Santo Tomás",
            'english_title': "The Philosophy of Mathematics in Saint Thomas",
            'year': "1952",
            'notes': "Monograph on Thomistic philosophy of mathematics (Mexico: Editorial Jus, pp. 2–6).",
            'citations': [
                {
                    'ref': "Caput VII, [^1]",
                    'loc_link': "caput-7/caput-7-en.md#fn-1",
                    'refers_to': "Alvarez Laso's exposition of Aquinas's commentary on Posterior Analytics I, 1 regarding triangle as subject vs. attribute.",
                    'supports_text': "Presents scholarly confirmation that St. Thomas's noetics of mathematics hinges on the intellectual activity that constructs figures in intelligible matter."
                }
            ]
        }
    ]
)

print(f"Total authors registered: {len(authors)}")

# Generate markdown document
header = """---
title: "Bibliography & Cited References (Bibliographia et Fontes)"
description: "Comprehensive critical bibliography and apparatus of cited sources for Petrus Hoenen's De Noetica Geometriae (1954), organized chronologically by death date with an alphabetical index."
---

> [Conspectus Totius Operis](index.md) | [Agent Chronicle](agent-chronicle.md) | [Historical Context: Fr. Peter Hoenen, S.J.](about/peter-hoenen.md)

---

# Bibliography & Cited References
## *Bibliographia et Apparatus Fontium*

This apparatus provides a comprehensive, critical reconstruction of all sources, classical treatises, mathematical works, and philosophical commentaries cited by **Father Peter Hoenen, S.J.** across *De Noetica Geometriae: Origine Theoriae Cognitionis* (Rome: Gregorian University, 1954).

Hoenen's citations reveal his unique intellectual position: trained in theoretical physics under Nobel laureate H. A. Lorentz at Leiden before teaching scholastic philosophy at the Gregorianum, he confronts the foundational crisis of modern mathematics (formalism, logicism, and non-Euclidean geometry) directly with the rigorous epistemology of Aristotle and St. Thomas Aquinas.

The bibliography is organized as follows:
1. **[Alphabetical Index of Authors](#alphabetical-index-of-authors)** — An A–Z directory of all 64 cited authors with direct links to their entries.
2. **[Chronological Bibliography](#chronological-bibliography-ordered-by-death-date)** — All authors arranged strictly chronologically by death date (earliest first), spanning 2,400 years from Eudoxus of Cnidus (c. 355 BC) to José Alvarez Laso (1993 AD).

Each entry consistently provides:
* **Author (Born–Died)**
  * **Book / Treatise Title** (*English Title*) Year
    *Scholarly notes on editions, co-authors, translators, and historical context*
    * **Citation**: Specific chapter and footnote in Hoenen's volume
      * *What Hoenen refers to*: The exact text, theorem, or doctrine cited
      * *How it supports the text*: How the citation functions within Hoenen's philosophical argumentation (problem of necessity, problem of exactitude, intuitive formal abstraction, intelligible matter, or the existential act)

---

## Alphabetical Index of Authors

"""

# Build Alphabetical Index
alpha_sorted = sorted(authors, key=lambda a: a['alpha_key'].lower())
current_letter = ""
alpha_toc_lines = []

for auth in alpha_sorted:
    letter = auth['alpha_key'][0].upper()
    if letter != current_letter:
        current_letter = letter
        alpha_toc_lines.append(f"\n### {current_letter}\n")
    anchor = slugify(auth['name'])
    alpha_toc_lines.append(f"* [{auth['name']} ({auth['born_died']})](#{anchor})")

alpha_toc_str = "\n".join(alpha_toc_lines) + "\n\n---\n\n## Chronological Bibliography (Ordered by Death Date)\n\n"

# Sort Chronologically by death_sort
chrono_sorted = sorted(authors, key=lambda a: a['death_sort'])

chrono_sections = []

for auth in chrono_sorted:
    anchor = slugify(auth['name'])
    sec = f'<a id="{anchor}"></a>\n\n'
    sec += f"### {auth['name']} ({auth['born_died']})\n\n"
    
    for work in auth['works']:
        sec += f"* **{work['title']}** (*{work['english_title']}*) {work['year']}\n"
        if work.get('notes'):
            sec += f"  *Notes*: {work['notes']}\n"
        for cit in work['citations']:
            sec += f"  * **Citation**: [{cit['ref']}]({cit['loc_link']})\n"
            sec += f"    * *What Hoenen refers to*: {cit['refers_to']}\n"
            sec += f"    * *How it supports the text*: {cit['supports_text']}\n"
        sec += "\n"
    
    sec += "---\n\n"
    chrono_sections.append(sec)

footer = """
## Summary Statistics

* **Total Authors Catalogued**: 64 authors spanning 24 centuries (c. 355 BC to 1993 AD).
* **Chronological Span**:
  * **Ancient Greek & Classical Foundations** (c. 355 BC – 560 AD): Eudoxus, Plato, Aristotle, Euclid, Alexander of Aphrodisias, Themistius, Proclus, Boethius, Simplicius.
  * **Medieval Scholastic Synthesis** (1274 – 1382 AD): St. Thomas Aquinas, St. Albert the Great, Nicole Oresme.
  * **Early Modern Epistemology** (1650 – 1804 AD): Descartes, Locke, Leibniz, Kant.
  * **19th-Century Mathematics, Logic, & Philology** (1864 – 1928 AD): Waitz, Möbius, Trendelenburg, Mill, Bonitz, Weierstrass, Hamelin, Poincaré, Couturat, Dedekind, Brentano, Cantor, Wellstein, Killing, Baeumker, Riehl, Klein, Hessenberg, Carteron, Burnet.
  * **20th-Century Axiomatics, Physics, & Neo-Scholasticism** (1930 – 1993 AD): Study, Pasch, Voss, Peano, Meyerson, Pirotta, Heath, Hausdorff, Hilbert, Enriques, Hardy, Geyser, Einstein, Weyl, Scholz, Amaldi, Hoenen, de la Vallée-Poussin, Hadamard, Russell, Maier, Ross, Stammler, Gilson, Hasse, Lonergan, Freudenthal, Alvarez Laso.
* **Footnote Census**: All 130 footnotes across the 9 sections of *De Noetica Geometriae* are cross-referenced to their respective author, work, and textual function.

---

> [Conspectus Totius Operis](index.md) | [Agent Chronicle](agent-chronicle.md) | [Historical Context: Fr. Peter Hoenen, S.J.](about/peter-hoenen.md)
"""

final_content = header + alpha_toc_str + "".join(chrono_sections) + footer

with open('docs/bibliography.md', 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"Generated docs/bibliography.md ({len(final_content)} bytes).")
