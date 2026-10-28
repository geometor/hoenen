#!/usr/bin/env python3
"""Enrich apparatus JSON registries and generate persons.rst, glossary.rst, and enriched bibliography.rst."""

from __future__ import annotations

import json
import re
from pathlib import Path

HOENEN_ROOT = Path("/home/phi/PROJECTS/geometor/hoenen")
RES_DIR = HOENEN_ROOT / "resources" / "de_noetica_geometriae"
DOCSRC_BOOK = HOENEN_ROOT / "docsrc" / "de_noetica_geometriae"


def apparatus_slug(key: str) -> str:
    """Deterministic HTML anchor slug for a citation, work, person, or term key."""
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


# Rich scholarly definitions for the 37 glossary terms that previously had generic placeholders
GLOSSARY_ENRICHMENTS: dict[str, tuple[str, str, str, str]] = {
    "abstractio-intuitiva": (
        "abstractio intuitiva formalis",
        "Latin (Scholastic)",
        "Intuitive formal abstraction",
        "Hoenen's technical designation for the intellectual operation in which the mind directly intuits universal, necessary formal relationships (such as spatial continuity and geometric properties) within the concrete sensible phantasm.",
    ),
    "agere-sequitur-esse": (
        "agere sequitur ad esse in actu",
        "Latin (Scholastic)",
        "Action follows upon actual being",
        "Classical Thomistic metaphysical axiom affirming that no causal agency or operation can proceed except from an entity that already possesses actual existence (esse in actu).",
    ),
    "aisthema": (
        "αἴσθημα (pl. αἰσθήματα)",
        "Greek",
        "Sense-impression / perceptual datum",
        "In Aristotle's De Anima (III, c. 8, 432a), the content of sensory perception from which the imagination forms phantasms and the intellect abstracts intelligible species.",
    ),
    "anairei": (
        "ἀναιρεῖ (ἀναιρεῖν)",
        "Greek",
        "Destroys / sublates (hypotheses)",
        "Plato's term in Republic VII (533c) for the dialectical method, which 'destroys' or transcends the provisional hypotheses of the mathematical sciences in order to ascend to the unhypothetical first principle.",
    ),
    "andererseits": (
        "andererseits",
        "German",
        "On the other hand",
        "Correlative discourse marker used in German mathematical exposition (paired with einerseits) when contrasting dual axiomatic or geometric aspects.",
    ),
    "arche": (
        "ἀρχή (acc. ἀρχήν)",
        "Greek",
        "First principle / starting point / origin",
        "In Aristotle and Plato, the foundational starting point of being, demonstration, or cognition (such as the unhypothetical principle in Republic VI–VII or the immediate premises of science in Posterior Analytics).",
    ),
    "beschaffenheit": (
        "Beschaffenheit",
        "German",
        "Constitution / qualitative nature / character",
        "Term used by German mathematicians (such as Killing and Klein) to denote the intrinsic spatial or structural character of geometric figures and manifolds.",
    ),
    "bezeichnungsweise": (
        "Bezeichnungsweise",
        "German",
        "Mode of designation / system of notation",
        "In modern axiomatics and mathematical formalism, a symbolic notation or convention for designating geometric objects and relations.",
    ),
    "das-gedachte": (
        "das Gedachte (des Gedachten)",
        "German",
        "That which is thought / the object of thought",
        "In Gerhard Stammler's epistemology of logic, the objective conceptual content grasped by the mind in judgment and inference, as opposed to mere psychological acts.",
    ),
    "das-system-beider-punkte": (
        "das System beider Punkte",
        "German",
        "The system of both points",
        "David Hilbert's phrase in Grundlagen der Geometrie (§ 1) designating a pair of points as determining a straight line in his axiomatic incidence relations.",
    ),
    "denkgesetze": (
        "Denkgesetze",
        "German",
        "Laws of thought",
        "In 19th- and early 20th-century German logic and epistemology, the fundamental normative principles governing valid conceptual thought and inference.",
    ),
    "dispositio-rei": (
        "dispositio rei",
        "Latin (Scholastic)",
        "Disposition / objective arrangement of the thing",
        "In St. Thomas Aquinas (Metaphysics IX, lect. 11), the real ontological arrangement of a state of affairs to which the intellect's composition or division must correspond for truth.",
    ),
    "doctrine-prealable": (
        "la doctrine préalable",
        "French",
        "The preliminary / prior doctrine",
        "Ferdinand Gonseth's epistemological term for the pre-axiomatic intuitive body of knowledge that necessarily precedes and guides formal axiomatization.",
    ),
    "einerseits": (
        "einerseits",
        "German",
        "On the one hand",
        "Correlative German expression used in mathematical analysis to distinguish complementary aspects of a geometric definition or postulate.",
    ),
    "elektron": (
        "ἤλεκτρον",
        "Greek",
        "Amber (and by extension, the electron)",
        "Classical Greek term for amber, cited by Aristotle in Meteorology IV (388b) as a homogeneous natural substance and contrasted with modern microphysical particles.",
    ),
    "ere-de-la-rigueur-de-weierstrass": (
        "l'ère de la rigueur de Weierstrass",
        "French",
        "The era of Weierstrassian rigor",
        "Henri Poincaré's characterization of late 19th-century mathematical analysis, in which Karl Weierstrass replaced naive spatial intuition of continuous curves with rigorous epsilon-delta arithmetic definitions.",
    ),
    "erklaerungen": (
        "Erklärungen",
        "German",
        "Explanations / preliminary definitions",
        "David Hilbert's heading at the opening of Grundlagen der Geometrie introducing the primitive undefined domains of points, straight lines, and planes.",
    ),
    "ho-to-poson-gignosketai": (
        "ᾧ τὸ ποσὸν γιγνώσκεται",
        "Greek",
        "That by which quantity is known",
        "Aristotle's definition of the unit or measure in Metaphysics X (c. 1, 1052b20): the primary measure by which quantitative magnitude or multitude is cognized.",
    ),
    "kritzelige-kurven": (
        "kritzelige Kurven",
        "German",
        "Scribbly / crinkly curves",
        "Felix Klein's vivid description (in Elementarmathematik vom höheren Standpunkte) of rough, imprecise empirical curves drawn by hand, contrasted with idealized analytic curves.",
    ),
    "omne-agens-agit-propter-finem": (
        "Omne agens agit propter finem",
        "Latin (Scholastic)",
        "Every agent acts for an end",
        "Foundational Aristotelian-Thomistic principle of finality, cited by Hoenen as an existential synthetic judgment connecting causal action with teleological determination.",
    ),
    "physis": (
        "φύσις (dat. φύσει)",
        "Greek",
        "Nature / by nature",
        "In Aristotle's Posterior Analytics and Metaphysics, that which is prior or more intelligible 'by nature' (φύσει / secundum naturam) as opposed to what is prior 'to us' (πρὸς ἡμᾶς / quoad nos).",
    ),
    "pos-estin": (
        "πῶς ἔστιν",
        "Greek",
        "How it is / the mode of its being",
        "Aristotle's question in Physics IV regarding the ontological mode of existence of entities such as place, time, and the mathematical continuum.",
    ),
    "pragma": (
        "πρᾶγμα (pl. πράγματα)",
        "Greek",
        "Thing / objective reality / state of affairs",
        "In Aristotle's logic and metaphysics, the extramental reality or objective state of affairs that grounds the truth of spoken and mental propositions.",
    ),
    "prealable": (
        "préalable",
        "French",
        "Prior / preliminary / antecedent",
        "In French philosophy of mathematics (Gonseth, Poincaré), designating the intuitive cognition that must precede formal axiomatic construction.",
    ),
    "prouparchein": (
        "προϋπάρχειν",
        "Greek",
        "To pre-exist / exist beforehand",
        "Technical peripatetic verb (used by Aristotle, Themistius, and Simplicius) signifying that the moving cause, mobile subject, or first principles must actually exist prior to motion or demonstration.",
    ),
    "psyche": (
        "ψυχή (dat. ψυχῇ)",
        "Greek",
        "Soul / mind",
        "In Plato and Aristotle, the vital and cognitive principle whose intellectual faculty (νοῦς) beholds mathematical and metaphysical truths.",
    ),
    "rhysin-tou-semeiou": (
        "ῥύσις τοῦ σημείου (acc. ῥύσιν τοῦ σημείου)",
        "Greek",
        "Flow / fluxion of the point",
        "Ancient Greek kinematic conception (reported by Aristotle in De Anima I, 4 and Proclus) according to which the motion or flowing of a point generates a line.",
    ),
    "rigueur": (
        "rigueur",
        "French",
        "Mathematical rigor",
        "Logical and deductive exactness in mathematical demonstration, central to the debate between Poincaré, Klein, and the formalist/logicist schools.",
    ),
    "sachverhalt": (
        "Sachverhalt",
        "German",
        "State of affairs / objective complex",
        "In German phenomenology and epistemology (Brentano, Geyser, Stammler), the objective relational structure in reality corresponding to a true judgment.",
    ),
    "syngenes": (
        "συγγενές (pl. συγγενῆ)",
        "Greek",
        "Kindred / connatural / of the same genus",
        "In Plato's Republic VII and Aristotle's Posterior Analytics, the affinity and structural kinship of the mathematical sciences and their principles.",
    ),
    "termini-significativi": (
        "termini significativi",
        "Latin (Scholastic)",
        "Significant / semantically meaningful terms",
        "Terms possessing real intensional meaning and reference to intelligible objects, contrasted by Hoenen with the empty uninterpreted symbols of pure formalism.",
    ),
    "thesei": (
        "θέσει",
        "Greek",
        "By position / having position",
        "In Aristotle's distinction between arithmetic and geometry: whereas the arithmetic unit is without position (ἄθετος), the geometric point is an indivisible having position (θέσιν ἔχον / θέσει).",
    ),
    "thesis": (
        "θέσις (acc. θέσιν)",
        "Greek",
        "Position / positing",
        "In Aristotle's Posterior Analytics (I, c. 2, 72a14), an immediate principle of demonstration that cannot be proved but is not indispensable for learning everything (divided into hypotheses and definitions); in geometry, spatial position.",
    ),
    "tithemenou-tou-semeiou": (
        "τιθεμένου τοῦ σημείου",
        "Greek",
        "The point being posited / placed",
        "Greek genitive absolute describing the constructive positing of a geometric point in spatial intuition.",
    ),
    "umgekehrt": (
        "umgekehrt (die umgekehrte)",
        "German",
        "Conversely / the converse",
        "Mathematical and logical term designating the converse of a proposition or geometric relation.",
    ),
    "utopie": (
        "eine Utopie",
        "German",
        "A utopia / an unattainable ideal",
        "Felix Klein's characterization of the claim that pure formal logic can generate mathematical science without any appeal to spatial intuition.",
    ),
    "zusammenhang": (
        "Zusammenhang",
        "German",
        "Connection / nexus / structural coherence",
        "In German philosophy of mathematics (Hilbert, Klein, Stammler), the necessary structural interconnection linking axioms, concepts, and geometric configurations.",
    ),
}


# Additional author entries to add to bibliography.rst so every author in citations.json has a #bib-... section
ADDITIONAL_BIB_AUTHORS = [
    (
        "bib-john-philoponus",
        "John Philoponus (c. 490 – c. 570 AD)",
        "In Aristotelis Analytica Posteriora & Physica Commentaria (*Commentaries on Aristotle's Posterior Analytics and Physics*) c. 520–530 AD",
        "Alexandrian Neoplatonic and Christian commentator on Aristotle; edited by M. Wallies and H. Vitelli in Commentaria in Aristotelem Graeca (CAG Vols. XIII, XVI–XVII, Berlin: Reimer, 1887–1909).",
        "Philoponus's commentary on Aristotle's Posterior Analytics and Physics regarding the nature of mathematical abstraction, spatial extension, and the pre-existence of moving causes.",
        "Provides late-antique Greek textual witness confirming the peripatetic understanding of mathematical abstraction and existential prerequisites of motion.",
    ),
    (
        "bib-newton-sir-isaac",
        "Newton, Sir Isaac (1642 – 1727)",
        "Philosophiae Naturalis Principia Mathematica & Tractatus de Quadratura Curvarum (*Mathematical Principles of Natural Philosophy & Treatise on the Quadrature of Curves*) 1687, 1704",
        "Foundational treatises of classical mechanics and the method of fluxions, conceiving continuous geometric magnitudes as generated by continuous motion.",
        "Newton's cinematic generation of lines and surfaces by the local motion of points and lines (fluxions), following the classical geometric tradition commented on by St. Thomas in In I De Caelo.",
        "Demonstrates that the generation of continuous figures through imagined motion in intelligible extension belongs to the perennial mainstream of mathematical thought.",
    ),
    (
        "bib-hegel-georg-wilhelm-friedrich",
        "Hegel, Georg Wilhelm Friedrich (1770 – 1831)",
        "Wissenschaft der Logik & Enzyklopädie der philosophischen Wissenschaften (*Science of Logic & Encyclopedia of the Philosophical Sciences*) 1812–1817",
        "Foundational treatises of German absolute idealism analyzing quantity, the mathematical infinite, and the philosophy of nature.",
        "Hegel's critique of the Cartesian Cogito and his dialectical treatment of quantity and mathematical demonstration.",
        "Contrasted by Hoenen with the realistic Aristotelian-Thomistic intuition of existential acts and continuous quantity.",
    ),
    (
        "bib-gauss-carl-friedrich",
        "Gauss, Carl Friedrich (1777 – 1855)",
        "Disquisitiones generales circa superficies curvas & Briefwechsel (*General Investigations of Curved Surfaces & Mathematical Correspondence*) 1827",
        "Landmark differential-geometric memoir and foundational correspondence on non-Euclidean geometry and the concept of number.",
        "Gauss's investigations into intrinsic surface curvature, non-Euclidean parallel theory, and the foundations of number and continuous magnitude (as analyzed by Gerhard Stammler).",
        "Marks the historical turning point toward non-Euclidean geometry and the modern critical examination of Euclid's Fifth Postulate.",
    ),
    (
        "bib-helmholtz-hermann-von",
        "Helmholtz, Hermann von (1821 – 1894)",
        "Über die Tatsachen, die der Geometrie zum Grunde liegen (*On the Facts Underlying Geometry*) 1868",
        "Seminal memoir in Nachrichten von der Königlichen Gesellschaft der Wissenschaften zu Göttingen grounding Riemannian metrics in the free mobility of rigid bodies.",
        "Helmholtz's analysis of congruence and spatial measurement through the transport and superposition of rigid bodies.",
        "Hoenen examines Helmholtz's empiricist appeal to physical rigid bodies to distinguish physical mechanics from the pure intellectual translation of figures in intelligible matter.",
    ),
    (
        "bib-christ-wilhelm-von",
        "Christ, Wilhelm von (1831 – 1906)",
        "Aristotelis Metaphysica (*Critical Teubner Edition of Aristotle's Metaphysics*) 1886 (rev. ed. 1895)",
        "Standard critical Greek edition of Aristotle's Metaphysics published by B. G. Teubner (Leipzig).",
        "Christ's critical apparatus and textual readings in Metaphysics V and IX alongside Bonitz and Ross.",
        "Provides philological verification of Aristotle's Greek text on actuality (energeia) and metaphysical diversity.",
    ),
    (
        "bib-mercier-desire-joseph-cardinal",
        "Mercier, Désiré-Joseph, Cardinal (1851 – 1926)",
        "Critériologie générale ou Théorie générale de la certitude (*General Criteriology or General Theory of Certitude*) 1899 (8th ed. 1923)",
        "Foundational Louvain neo-scholastic treatise on epistemology and the criterion of truth (Louvain: Institut Supérieur de Philosophie).",
        "Mercier's Louvain criteriology separating purely ideal judgments (connecting abstract concepts) from existential judgments of reality.",
        "Critiqued in the Appendix: Hoenen shows that necessary synthetic connections exist not only between abstract quidditative concepts, but directly between concrete existential acts.",
    ),
    (
        "bib-holder-otto",
        "Hölder, Otto (1859 – 1937)",
        "Die mathematische Methode & Anschauung und Denken in der Geometrie (*The Mathematical Method & Intuition and Thought in Geometry*) 1900, 1924",
        "Influential epistemological studies on geometric intuition, axiomatic deduction, and measurement (Leipzig: Teubner).",
        "Hölder's analysis of the interplay between spatial intuition (Anschauung) and deductive logical thought in geometric proofs.",
        "Supports Hoenen's thesis that deductive chains in geometry continuously rely on the structural intuition of spatial configurations.",
    ),
    (
        "bib-brunschvicg-leon",
        "Brunschvicg, Léon (1869 – 1944)",
        "Les étapes de la philosophie mathématique (*The Stages of Mathematical Philosophy*) 1912",
        "Comprehensive historical and critical study of the philosophy of mathematics from Greek antiquity to modern logicism (Paris: Alcan).",
        "Brunschvicg's historical interpretation of Aristotelian syllogistics, Cartesian analytic geometry, and modern mathematical idealism.",
        "Engaged by Hoenen to defend the authentic realist meaning of Aristotelian and Thomistic mathematical abstraction against idealist reconstructions.",
    ),
    (
        "bib-taylor-alfred-edward",
        "Taylor, Alfred Edward (1869 – 1945)",
        "A Commentary on Plato's Timaeus & Plato: The Man and His Work (*Commentary on Plato's Timaeus & Plato*) 1928",
        "Monumental British philological and philosophical studies on Plato and Pythagorean mathematics (Oxford: Clarendon Press).",
        "Taylor's analysis of Platonic mathematical intermediates, Pythagorean geometry, and the divided line in the Republic.",
        "Clarifies the historical divergence between Platonic mathematical idealism and Aristotle's doctrine of abstraction from sensible phantasms.",
    ),
    (
        "bib-reichenbach-hans",
        "Reichenbach, Hans (1891 – 1953)",
        "Philosophie der Raum-Zeit-Lehre (*The Philosophy of Space and Time*) 1928",
        "Logical empiricist treatise on the epistemology of geometry, coordinative definitions, and general relativity (Berlin: Walter de Gruyter).",
        "Reichenbach's positivist critique of spatial intuition and his claim that geometric visualization is merely subjective and conventional.",
        "Refuted by Hoenen through the distinction between variable sensory images and the universal formal relations intuited by the intellect in intelligible matter.",
    ),
    (
        "bib-becker-oskar",
        "Becker, Oskar (1889 – 1964)",
        "Mathematische Existenz & Grundlagen der Mathematik in geschichtlicher Entwicklung (*Mathematical Existence & Foundations of Mathematics in Historical Development*) 1927, 1954",
        "Phenomenological and historical investigations into Greek mathematics, Eudoxian proportion theory, and intuitionism (Halle: Niemeyer).",
        "Becker's studies on the ontology of mathematical objects and the Greek theory of incommensurables.",
        "Corroborates the irreducible role of intuitive construction in both ancient Greek geometry and modern foundational research.",
    ),
    (
        "bib-brouwer-luitzen-egbertus-jan",
        "Brouwer, L. E. J. (1881 – 1966)",
        "Intuitionism and Formalism & Begründung der Mengenlehre unabhängig vom logischen Satz vom ausgeschlossenen Dritten (*Foundational Papers on Mathematical Intuitionism*) 1912, 1918",
        "Seminal Dutch mathematical treatises founding intuitionistic mathematics in opposition to Hilbertian formalism.",
        "Brouwer's insistence on primordial mathematical intuition over uninterpreted formalist symbol manipulation.",
        "Hoenen notes that while modern intuitionism rightly rejects empty formalism, it must be grounded in realistic Thomistic abstraction of continuous extension rather than Kantian subjective time-intuition.",
    ),
]


CHAPTER_META = [
    ("preface", "preface.rst", "preface-en.rst", "Praefatio", "Preface"),
    ("caput-1", "caput-1.rst", "caput-1-en.rst", "Caput I", "Chapter I"),
    ("caput-2", "caput-2.rst", "caput-2-en.rst", "Caput II", "Chapter II"),
    ("caput-3", "caput-3.rst", "caput-3-en.rst", "Caput III", "Chapter III"),
    ("caput-4", "caput-4.rst", "caput-4-en.rst", "Caput IV", "Chapter IV"),
    ("caput-5", "caput-5.rst", "caput-5-en.rst", "Caput V", "Chapter V"),
    ("caput-6", "caput-6.rst", "caput-6-en.rst", "Caput VI", "Chapter VI"),
    ("caput-7", "caput-7.rst", "caput-7-en.rst", "Caput VII", "Chapter VII"),
    ("appendix", "appendix.rst", "appendix-en.rst", "Appendix", "Appendix"),
]


def enrich_glossary_json() -> dict:
    glossary_path = RES_DIR / "glossary.json"
    glossary = json.loads(glossary_path.read_text(encoding="utf-8"))
    for slug, (headword, lang, trans, defn) in GLOSSARY_ENRICHMENTS.items():
        if slug in glossary:
            glossary[slug]["headword"] = headword
            glossary[slug]["language"] = lang
            glossary[slug]["translation"] = trans
            glossary[slug]["definition"] = defn
    glossary_path.write_text(json.dumps(glossary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Enriched {len(GLOSSARY_ENRICHMENTS)} glossary definitions in {glossary_path}")
    return glossary


def scan_chapter_occurrences() -> tuple[dict, dict, dict]:
    """Scan all Latin and English chapter RST files to map every role occurrence to its exact anchor and context."""
    cite_occs: dict[str, list[dict]] = {}
    person_occs: dict[str, list[dict]] = {}
    term_occs: dict[str, list[dict]] = {}

    for folder, la_file, en_file, la_title, en_title in CHAPTER_META:
        la_path = DOCSRC_BOOK / folder / la_file
        en_path = DOCSRC_BOOK / folder / en_file

        def extract_file_occs(rst_path: Path, lang: str) -> dict[tuple[str, str], list[dict]]:
            res: dict[tuple[str, str], list[dict]] = {}
            lines = rst_path.read_text(encoding="utf-8").splitlines()
            current_sec_label = f"{folder}-{lang}"
            current_sec_title = la_title if lang == "la" else en_title
            in_fn: str | None = None
            role_counts: dict[tuple[str, str], int] = {}

            for idx, line in enumerate(lines):
                s = line.strip()
                m_lbl = re.match(r"^\.\.\s+_([A-Za-z0-9_-]+):\s*$", s)
                if m_lbl:
                    current_sec_label = m_lbl.group(1)
                    in_fn = None
                    # Look ahead for heading
                    for j in range(idx + 1, min(idx + 5, len(lines))):
                        cand = lines[j].strip()
                        if cand and not cand.startswith("..") and not all(c in "=-~^\"'" for c in cand):
                            current_sec_title = re.sub(r"\*([^*]+)\*", r"\1", cand)
                            break
                    continue

                m_fn = re.match(r"^\.\.\s+\[#(f\d+)\]\s*(.+)$", s)
                if m_fn:
                    in_fn = m_fn.group(1)
                elif s and not line.startswith("   ") and not s.startswith(".. [#f"):
                    if in_fn is not None:
                        in_fn = None

                for role_name in ("cite", "person", "term"):
                    for m in re.finditer(rf":{role_name}:`([^`]+)`", line):
                        body = m.group(1).strip()
                        tm = re.match(r"^(.*?)\s*<([^>]+)>$", body)
                        disp, target = (tm.group(1).strip(), tm.group(2).strip()) if tm else (body, body)
                        key_tuple = (role_name, target)
                        role_counts[key_tuple] = role_counts.get(key_tuple, 0) + 1
                        occ_num = role_counts[key_tuple]
                        occ_id = f"occ-{role_name}-{apparatus_slug(target)}-{occ_num}"
                        short_sec = current_sec_title
                        m_sec_num = re.match(r"^(§\s*\d+\.|[0-9]+\.|[A-Z]\))", short_sec)
                        if m_sec_num:
                            short_sec = m_sec_num.group(1)
                        elif len(short_sec) > 28:
                            short_sec = short_sec[:25].rstrip() + "…"
                        loc_label = f"n. {in_fn[1:]}" if in_fn else short_sec
                        res.setdefault(key_tuple, []).append(
                            {
                                "folder": folder,
                                "html_file": f"{folder}/{rst_path.stem}.html",
                                "occ_id": occ_id,
                                "sec_label": current_sec_label,
                                "fn_id": in_fn,
                                "loc_label": loc_label,
                                "display": re.sub(r"\*([^*]+)\*", r"\1", disp),
                            }
                        )
            return res

        la_map = extract_file_occs(la_path, "la")
        en_map = extract_file_occs(en_path, "en")

        all_keys = sorted(set(la_map.keys()) | set(en_map.keys()))
        for role_name, target in all_keys:
            la_list = la_map.get((role_name, target), [])
            en_list = en_map.get((role_name, target), [])
            max_len = max(len(la_list), len(en_list))
            paired = []
            for k_idx in range(max_len):
                la_item = la_list[k_idx] if k_idx < len(la_list) else None
                en_item = en_list[k_idx] if k_idx < len(en_list) else None
                paired.append(
                    {
                        "chapter_la": la_title,
                        "chapter_en": en_title,
                        "la": la_item,
                        "en": en_item,
                    }
                )
            if role_name == "cite":
                cite_occs.setdefault(target, []).extend(paired)
            elif role_name == "person":
                person_occs.setdefault(target, []).extend(paired)
            elif role_name == "term":
                term_occs.setdefault(target, []).extend(paired)

    return cite_occs, person_occs, term_occs


def format_occ_links_rst(paired_list: list[dict]) -> str:
    """Format paired Latin/English occurrence links using custom :occ: role or clean inline markup."""
    # Group by chapter
    by_chap: dict[str, list[dict]] = {}
    for item in paired_list:
        by_chap.setdefault(item["chapter_la"], []).append(item)

    chap_parts = []
    for chap_la, items in by_chap.items():
        loci = []
        for it in items:
            la = it["la"]
            en = it["en"]
            loc_lbl = (la or en)["loc_label"]
            if la and en:
                loci.append(
                    f"{loc_lbl} (`LA <{la['html_file']}#{la['occ_id']}>`__ · `EN <{en['html_file']}#{en['occ_id']}>`__)"
                )
            elif la:
                loci.append(f"{loc_lbl} (`LA <{la['html_file']}#{la['occ_id']}>`__)")
            elif en:
                loci.append(f"{loc_lbl} (`EN <{en['html_file']}#{en['occ_id']}>`__)")
        chap_parts.append(f"**{chap_la}**: " + ", ".join(loci))
    return " | ".join(chap_parts)


def generate_persons_rst(persons: dict, citations: dict, person_occs: dict) -> None:
    """Generate docsrc/de_noetica_geometriae/persons.rst."""
    lines = [
        ":title: Index Nominum — Biographical Register of Persons",
        ":description: Comprehensive biographical register and concordance of all 83 philosophers, mathematicians, and commentators in Petrus Hoenen's De Noetica Geometriae (1954).",
        ":layout: book",
        "",
        ".. _persons:",
        ".. _index-nominum:",
        "",
        "Index Nominum (Biographical Register)",
        "=====================================",
        "",
        ".. rubric:: * Catalogus Auctorum, Philosophorum et Mathematicorum *",
        "",
        "This biographical register catalogues all **83 philosophers, mathematicians, physicists, and classical commentators** referenced across **Father Peter Hoenen, S.J.**'s *De Noetica Geometriae: Origine Theoriae Cognitionis* (1954). Every ``:person:`` reference in both the Latin and English editions links directly to its entry below, and each entry provides biographical context, cited works linked to the :ref:`Systematic Bibliography <bibliography>`, and exact back-links (`LA` · `EN`) to every occurrence in the text.",
        "",
    ]

    # Sort persons alphabetically by name
    sorted_items = sorted(persons.items(), key=lambda kv: kv[1].get("name", kv[0]).lower())

    # Group by initial letter for A-Z index
    by_letter: dict[str, list[tuple[str, dict]]] = {}
    for slug, pdata in sorted_items:
        first_char = pdata.get("name", slug)[0].upper()
        if first_char == "É":
            first_char = "E"
        elif first_char == "Ö":
            first_char = "O"
        by_letter.setdefault(first_char, []).append((slug, pdata))

    lines.extend(
        [
            "----",
            "",
            ".. _persons-alphabetical-index:",
            "",
            "Alphabetical Directory",
            "----------------------",
            "",
        ]
    )

    for letter in sorted(by_letter.keys()):
        lines.append(f"{letter}")
        lines.append("~" * max(4, len(letter)))
        lines.append("")
        for slug, pdata in by_letter[letter]:
            name = pdata.get("name", slug)
            dates = pdata.get("dates", "")
            role = pdata.get("role", "")
            date_str = f" ({dates})" if dates else ""
            role_str = f" — *{role}*" if role else ""
            lines.append(f"* :ref:`{name}{date_str} <person-{apparatus_slug(slug)}>`{role_str}")
        lines.append("")

    lines.extend(
        [
            "----",
            "",
            ".. _persons-biographical-entries:",
            "",
            "Biographical Entries & Textual Concordance",
            "------------------------------------------",
            "",
        ]
    )

    # Map author_key -> list of (work_key, work_title) from citations.json
    author_works: dict[str, dict[str, str]] = {}
    for ckey, cdata in citations.items():
        ak = cdata.get("author_key", "")
        wk = cdata.get("work_key", "")
        wt = cdata.get("work", "")
        if ak and wk and wt:
            author_works.setdefault(ak, {})[wk] = wt

    for slug, pdata in sorted_items:
        p_id = f"person-{apparatus_slug(slug)}"
        name = pdata.get("name", slug)
        dates = pdata.get("dates", "")
        role = pdata.get("role", "")
        bio = pdata.get("bio", "")
        works = pdata.get("works", [])
        bib_anchor = pdata.get("bib_anchor", "")
        heading = f"{name} ({dates})" if dates else name

        lines.append(f".. _{p_id}:")
        lines.append("")
        lines.append(heading)
        lines.append("~" * max(4, len(heading)))
        lines.append("")
        if role:
            lines.append(f"* **Role**: *{role}*")
        if bio:
            lines.append(f"* **Biographical & Philosophical Note**: {bio}")
        if bib_anchor:
            # Handle proclus / wellstein alias
            lines.append(f"* **Bibliographic Apparatus**: :ref:`View Full Entry in Systematic Bibliography <{bib_anchor}>`")

        # Works
        if slug in author_works:
            w_links = []
            for wk, wt in sorted(author_works[slug].items()):
                w_slug = f"work-{apparatus_slug(wk)}"
                w_links.append(f"`{wt} <bibliography.html#{w_slug}>`__")
            lines.append(f"* **Cited Works**: " + " · ".join(w_links))
        elif works:
            lines.append("* **Principal Works**: " + " · ".join(f"*{w}*" for w in works))

        occs = person_occs.get(slug, [])
        if occs:
            occ_str = format_occ_links_rst(occs)
            lines.append(f"* **Occurrences in De Noetica Geometriae ({len(occs)})**: {occ_str}")
        else:
            # Fallback to folio occurrences from persons.json if mentioned in apparatus/index
            f_occs = pdata.get("occurrences", [])
            if f_occs:
                pages = sorted({str(o.get("page", "")) for o in f_occs if o.get("page")})
                lines.append(f"* **Edition Pages**: pp. {', '.join(pages)}")

        lines.append("")
        lines.append("----")
        lines.append("")

    target_path = DOCSRC_BOOK / "persons.rst"
    target_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {target_path} ({len(lines)} lines)")


def generate_glossary_rst(glossary: dict, term_occs: dict) -> None:
    """Generate docsrc/de_noetica_geometriae/glossary.rst."""
    lines = [
        ":title: Glossarium Technicum — Greek & Scholastic Technical Glossary",
        ":description: Comprehensive technical glossary of 99 Greek, Scholastic Latin, German, and French philosophical and mathematical terms in Petrus Hoenen's De Noetica Geometriae (1954).",
        ":layout: book",
        "",
        ".. _glossary:",
        ".. _glossarium-technicum:",
        "",
        "Glossarium Technicum (Technical Glossary)",
        "=========================================",
        "",
        ".. rubric:: * Lexicon Terminorum Graecorum, Scholasticorum et Mathematicorum *",
        "",
        "This technical glossary defines all **99 Greek, Scholastic Latin, German, and French philosophical and mathematical terms** tagged with ``:term:`` across **Father Peter Hoenen, S.J.**'s *De Noetica Geometriae* (1954). Every inline ``:term:`` in the Latin and English editions links directly to its entry below, and each entry provides the original headword, language tradition, English translation, philosophical explanation, and direct back-links (`LA` · `EN`) to every occurrence in the text.",
        "",
        "----",
        "",
        ".. _glossary-alphabetical-index:",
        "",
        "Alphabetical Index of Technical Terms",
        "-------------------------------------",
        "",
    ]

    sorted_terms = sorted(glossary.items(), key=lambda kv: kv[0].lower())
    by_letter: dict[str, list[tuple[str, dict]]] = {}
    for slug, tdata in sorted_terms:
        letter = slug[0].upper()
        by_letter.setdefault(letter, []).append((slug, tdata))

    for letter in sorted(by_letter.keys()):
        lines.append(f"{letter}")
        lines.append("~" * max(4, len(letter)))
        lines.append("")
        for slug, tdata in by_letter[letter]:
            hw = tdata.get("headword", slug)
            trans = tdata.get("translation", "")
            lang = tdata.get("language", "")
            lines.append(f"* :ref:`{hw} <term-{apparatus_slug(slug)}>` — *{trans}* ({lang})")
        lines.append("")

    lines.extend(
        [
            "----",
            "",
            ".. _glossary-entries:",
            "",
            "Glossary Entries & Textual Concordance",
            "--------------------------------------",
            "",
        ]
    )

    for slug, tdata in sorted_terms:
        t_id = f"term-{apparatus_slug(slug)}"
        hw = tdata.get("headword", slug)
        lang = tdata.get("language", "")
        trans = tdata.get("translation", "")
        defn = tdata.get("definition", "")
        heading = f"{hw} — {trans}" if trans and trans.lower() != hw.lower() else hw

        lines.append(f".. _{t_id}:")
        lines.append("")
        lines.append(heading)
        lines.append("~" * max(4, len(heading)))
        lines.append("")
        lines.append(f"* **Headword**: *{hw}* (``{slug}``)")
        lines.append(f"* **Language Tradition**: {lang}")
        if trans:
            lines.append(f"* **English Translation**: *{trans}*")
        if defn:
            lines.append(f"* **Noetic & Mathematical Definition**: {defn}")

        occs = term_occs.get(slug, [])
        if occs:
            occ_str = format_occ_links_rst(occs)
            lines.append(f"* **Occurrences in De Noetica Geometriae ({len(occs)})**: {occ_str}")
        else:
            f_occs = tdata.get("occurrences", [])
            if f_occs:
                pages = sorted({str(o.get("page", "")) for o in f_occs if o.get("page")})
                lines.append(f"* **Edition Pages**: pp. {', '.join(pages)}")

        lines.append("")
        lines.append("----")
        lines.append("")

    target_path = DOCSRC_BOOK / "glossary.rst"
    target_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {target_path} ({len(lines)} lines)")


def enrich_bibliography_rst(citations: dict, persons: dict, cite_occs: dict) -> None:
    """Enrich bibliography.rst with all missing authors and exact #cite-<slug> and #work-<slug> anchors."""
    bib_path = DOCSRC_BOOK / "bibliography.rst"
    orig_text = bib_path.read_text(encoding="utf-8")

    # Strip any previously appended Locus Concordance section so this function is idempotent
    marker = "\n.. _bib-additional-cited-authors:"
    if marker in orig_text:
        orig_text = orig_text[: orig_text.index(marker)]

    # Ensure :layout: book is present in top field list
    if ":layout: book" not in orig_text[:300]:
        orig_text = orig_text.replace(
            ":title: Bibliography & Cited References (Bibliographia et Fontes)\n",
            ":title: Bibliography & Cited References (Bibliographia et Fontes)\n:layout: book\n",
            1,
        )

    # Remove any legacy .. container:: track-nav from bibliography.rst
    orig_text = re.sub(
        r"\n*\.\.\s+container::\s+track-nav\n+(?:[ \t]+[^\n]+\n?)+",
        "\n\n",
        orig_text,
    )

    # Add alias labels where citations.json uses slightly different bib_anchor names
    if ".. _bib-proclus-lycius-diadochus:" not in orig_text:
        orig_text = orig_text.replace(
            ".. _bib-proclus-diadochus:\n",
            ".. _bib-proclus-diadochus:\n.. _bib-proclus-lycius-diadochus:\n",
        )
    if ".. _bib-weber-heinrich:" not in orig_text:
        orig_text = orig_text.replace(
            ".. _bib-wellstein-josef:\n",
            ".. _bib-wellstein-josef:\n.. _bib-weber-heinrich:\n",
        )
    if ".. _bib-whitehead-alfred-north:" not in orig_text:
        orig_text = orig_text.replace(
            ".. _bib-russell-bertrand:\n",
            ".. _bib-russell-bertrand:\n.. _bib-whitehead-alfred-north:\n",
        )

    # Build the Additional Cited Authors section + Complete Locus Concordance of all 412 :cite: keys
    extra_lines = [
        "",
        ".. _bib-additional-cited-authors:",
        "",
        "Additional Cited Authors & Commentators",
        "---------------------------------------",
        "",
    ]

    for bib_id, author_heading, work_line, notes_line, refers_line, supports_line in ADDITIONAL_BIB_AUTHORS:
        extra_lines.extend(
            [
                f".. _{bib_id}:",
                "",
                author_heading,
                "~" * max(4, len(author_heading)),
                "",
                f"* **{work_line}**",
                "",
                f"  *Notes*: {notes_line}",
                "",
                f"  * *What Hoenen refers to*: {refers_line}",
                f"  * *How it supports the text*: {supports_line}",
                "",
                "----",
                "",
            ]
        )

    # Now build the complete, deterministic Locus Concordance (412 citations across 115 works)
    # grouped by author -> work -> locus, with exact .. _work-<slug>: and .. _cite-<slug>: anchors!
    extra_lines.extend(
        [
            ".. _bib-locus-concordance:",
            "",
            "Complete Concordance of Cited Loci (412 Citations)",
            "--------------------------------------------------",
            "",
            "Every inline ``:cite:`` reference across the Latin and English editions of *De Noetica Geometriae* resolves directly to its canonical locus entry below. Each entry links upward to the author's main bibliographic commentary, to their biographical entry in the :ref:`Index Nominum <persons>`, and directly back (`LA` · `EN`) to every occurrence in the text.",
            "",
        ]
    )

    # Group citations by author_key -> work_key -> list of (ckey, cdata)
    by_author: dict[str, list[tuple[str, dict]]] = {}
    for ckey, cdata in sorted(citations.items()):
        ak = cdata.get("author_key", "other")
        by_author.setdefault(ak, []).append((ckey, cdata))

    for ak in sorted(by_author.keys(), key=lambda k: by_author[k][0][1].get("author", k).lower()):
        entries = by_author[ak]
        author_name = entries[0][1].get("author", ak)
        bib_anchor = entries[0][1].get("bib_anchor", "")
        person_slug = f"person-{apparatus_slug(ak)}"

        by_work: dict[str, list[tuple[str, dict]]] = {}
        for ckey, cdata in entries:
            wk = cdata.get("work_key", f"{ak}:work")
            by_work.setdefault(wk, []).append((ckey, cdata))

        for wk, w_entries in sorted(by_work.items()):
            w_title = w_entries[0][1].get("work", wk)
            w_anchor = f"work-{apparatus_slug(wk)}"
            heading = f"{author_name} — {w_title}"
            extra_lines.append(f".. _{w_anchor}:")
            extra_lines.append("")
            extra_lines.append(heading)
            extra_lines.append("~" * max(4, len(heading)))
            extra_lines.append("")

            nav_bits = []
            if bib_anchor:
                nav_bits.append(f":ref:`Author Commentary <{bib_anchor}>`")
            if ak in persons:
                nav_bits.append(f":ref:`Biographical Entry ({persons[ak].get('name', ak)}) <{person_slug}>`")
            if nav_bits:
                extra_lines.append("* **Apparatus Links**: " + " · ".join(nav_bits))
                extra_lines.append("")

            for ckey, cdata in w_entries:
                c_anchor = f"cite-{apparatus_slug(ckey)}"
                locus = cdata.get("locus", ckey)
                occs = cite_occs.get(ckey, [])
                sample_disp = ""
                if occs:
                    first_occ = occs[0]["la"] or occs[0]["en"]
                    if first_occ:
                        sample_disp = first_occ.get("display", "")
                elif cdata.get("occurrences"):
                    sample_disp = cdata["occurrences"][0].get("display", "")

                occ_str = format_occ_links_rst(occs) if occs else ""
                disp_part = f" — *« {sample_disp} »*" if sample_disp and sample_disp != locus else ""
                loc_part = f" — {occ_str}" if occ_str else ""
                extra_lines.append(f".. _{c_anchor}:")
                extra_lines.append("")
                extra_lines.append(f"* **{locus}** (``{ckey}``){disp_part}{loc_part}")
                extra_lines.append("")

            extra_lines.append("----")
            extra_lines.append("")

    full_bib = orig_text.rstrip() + "\n" + "\n".join(extra_lines)
    bib_path.write_text(full_bib, encoding="utf-8")
    print(f"Enriched {bib_path} ({len(full_bib.splitlines())} lines)")


def update_book_index_rst() -> None:
    """Update docsrc/de_noetica_geometriae/index.rst to include Index Nominum (persons) and Glossarium Technicum (glossary)."""
    idx_path = DOCSRC_BOOK / "index.rst"
    txt = idx_path.read_text(encoding="utf-8")

    old_block = """Bibliographia et Fontes *(Bibliography & References)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`Systematic Bibliography & Annotated Footnote Concordance <bibliography>`

----

Apparatus & Editorial Documentation
-----------------------------------

* :ref:`Bibliography & Cited References (Bibliographia et Fontes) <bibliography>`
* :ref:`The Transcription Chronicle: An AI Agent's First-Person Memoir <agent-chronicle>`
* :ref:`Scan Inventory & Problem Page Log <scan-inventory>`"""

    new_block = """Apparatus Criticus: Bibliographia, Index Nominum et Glossarium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Bibliographia et Fontes — Systematic Bibliography & Cited Loci (412 Citations) <bibliography>`
* :ref:`Index Nominum — Biographical Register of Philosophers & Mathematicians (83 Persons) <persons>`
* :ref:`Glossarium Technicum — Greek, Scholastic & Mathematical Glossary (99 Terms) <glossary>`

----

Apparatus & Editorial Documentation
-----------------------------------

* :ref:`Bibliography & Cited References (Bibliographia et Fontes) <bibliography>`
* :ref:`Biographical Register of Persons (Index Nominum) <persons>`
* :ref:`Technical Glossary of Terms (Glossarium Technicum) <glossary>`
* :ref:`The Transcription Chronicle: An AI Agent's First-Person Memoir <agent-chronicle>`
* :ref:`Scan Inventory & Problem Page Log <scan-inventory>`"""

    if old_block in txt:
        txt = txt.replace(old_block, new_block, 1)

    old_toc = """.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Apparatus & Editorial

   bibliography
   agent-chronicle
   scan-inventory"""

    new_toc = """.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Apparatus & Editorial

   bibliography
   persons
   glossary
   agent-chronicle
   scan-inventory"""

    if old_toc in txt:
        txt = txt.replace(old_toc, new_toc, 1)

    idx_path.write_text(txt, encoding="utf-8")
    print(f"Updated {idx_path}")


def main() -> None:
    glossary = enrich_glossary_json()
    persons = json.loads((RES_DIR / "persons.json").read_text(encoding="utf-8"))
    citations = json.loads((RES_DIR / "citations.json").read_text(encoding="utf-8"))
    cite_occs, person_occs, term_occs = scan_chapter_occurrences()
    print(
        f"Scanned occurrences: {len(cite_occs)} cite keys, {len(person_occs)} person keys, {len(term_occs)} term keys"
    )
    generate_persons_rst(persons, citations, person_occs)
    generate_glossary_rst(glossary, term_occs)
    enrich_bibliography_rst(citations, persons, cite_occs)
    update_book_index_rst()


if __name__ == "__main__":
    main()
