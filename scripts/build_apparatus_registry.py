#!/usr/bin/env python3
"""Normalize :cite:, :term:, and :person: tags across all 287 Hoenen folios and build canonical apparatus registries."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path("/home/phi/PROJECTS/geometor/hoenen")
VOLUME_ROOT = ROOT / "resources" / "hoenen_1954" / "volume_I"
EDITION_ROOT = ROOT / "resources" / "hoenen_1954"

# Canonical normalization map for author:work prefixes
CITE_PREFIX_MAP: Dict[str, str] = {
    # Aquinas
    "aquinas:boeth-trin": "aquinas:de-trin",
    "aquinas:in-boet-de-trin": "aquinas:de-trin",
    "aquinas:in-boethii-de-trinitate": "aquinas:de-trin",
    "aquinas:in_de_trin": "aquinas:de-trin",
    "aquinas:in-de-anima": "aquinas:de-anima",
    "aquinas:in_deanima": "aquinas:de-anima",
    "aquinas:de-ver": "aquinas:de-veritate",
    "aquinas:dever": "aquinas:de-veritate",
    "aquinas:veritate": "aquinas:de-veritate",
    "aquinas:depot": "aquinas:de-potentia",
    "aquinas:in-de-caelo": "aquinas:de-caelo",
    "aquinas:in-metaphysicam": "aquinas:met",
    "aquinas:in_met": "aquinas:met",
    "aquinas:in_metaph": "aquinas:met",
    "aquinas:in-physica": "aquinas:phys",
    "aquinas:in-physicam": "aquinas:phys",
    "aquinas:in_phys": "aquinas:phys",
    "aquinas:in_periherm": "aquinas:periherm",
    "aquinas:in_sent": "aquinas:sent",
    "aquinas:sth": "aquinas:st",
    "aquinas:summa-theologiae": "aquinas:st",
    "aquinas:malo": "aquinas:de-malo",
    # Aristotle
    "aristotle:an_post": "aristotle:anal-post",
    "aristotle:analytica-posteriora": "aristotle:anal-post",
    "aristotle:apost": "aristotle:anal-post",
    "aristotle:an_pr": "aristotle:anal-prior",
    "aristotle:apri": "aristotle:anal-prior",
    "aristotle:physica": "aristotle:phys",
    "aristotle:metaphysica": "aristotle:met",
    "aristotle:ethica-nicomachea": "aristotle:eth-nic",
    # Euclid & Proclus
    "euclides:elementa": "euclid:elements",
    "euclid:elementa": "euclid:elements",
    "proclus:in-euclidem": "proclus:in-euclid",
    # Commentators & Scholastics
    "simplicius:in-physica": "simplicius:phys",
    "simplicius:in_phys": "simplicius:phys",
    "themistius:in_phys": "themistius:phys",
    "pseudo_thomas:summa_logicae": "pseudo-thomas:summa-totius-logicae",
    # Modern Philosophers & Mathematicians
    "leibniz:nouveaux_essais": "leibniz:nouveaux-essais",
    "hilbert:1930": "hilbert:grundlagen",
    "hilbert:grundlagen-1903": "hilbert:grundlagen",
    "poincare:1902": "poincare:science-hypothese",
    "poincare:1913": "poincare:dernieres-pensees",
    "poincare:valeur-de-la-science": "poincare:valeur-science",
    "whitehead_russell:1910": "whitehead-russell:principia",
    "weber-wellstein:1915": "weber-wellstein:enzyklopaedie",
    "weber-wellstein:1925": "weber-wellstein:enzyklopaedie",
    # Hoenen
    "hoenen:1945": "hoenen:cosmologia",
    "hoenen:1949:cosmologia": "hoenen:cosmologia",
    "hoenen:1946": "hoenen:theorie-du-jugement",
    "hoenen:th-d-j": "hoenen:theorie-du-jugement",
    "hoenen:1952": "hoenen:reality-and-judgment",
    "hoenen:filosofia": "hoenen:filosofia-natura",
}

AUTHOR_CATALOG: Dict[str, Dict[str, str]] = {
    "albertus": {
        "name": "Albert the Great, St., O.P. (c. 1200 – 1280)",
        "bib_anchor": "bib-albert-the-great-st-o-p",
        "work_default": "Commentaria in Analytica Priora",
    },
    "alexander": {
        "name": "Alexander of Aphrodisias (fl. c. 200 AD)",
        "bib_anchor": "bib-alexander-of-aphrodisias",
        "work_default": "In Aristotelis Metaphysica Commentaria",
    },
    "alvarez-laso": {
        "name": "Alvarez Laso, José, C.M.F. (1910 – 1993)",
        "bib_anchor": "bib-alvarez-laso-jose-c-m-f",
        "work_default": "La Filosofía de las Matemáticas en Santo Tomás (1952)",
    },
    "amaldi": {
        "name": "Amaldi, Ugo (1875 – 1957)",
        "bib_anchor": "bib-amaldi-ugo",
        "work_default": "Sui concetti di retta e di piano (Questioni riguardanti le matematiche elementari)",
    },
    "aquinas": {
        "name": "Thomas Aquinas, St., O.P. (1225 – 1274)",
        "bib_anchor": "bib-thomas-aquinas-st-o-p",
        "work_default": "Opera Omnia",
    },
    "aristotle": {
        "name": "Aristotle (384 – 322 BC)",
        "bib_anchor": "bib-aristotle",
        "work_default": "Corpus Aristotelicum (ed. Bekker)",
    },
    "baeumker": {
        "name": "Baeumker, Clemens (1853 – 1924)",
        "bib_anchor": "bib-baeumker-clemens",
        "work_default": "Das Problem der Materie in der griechischen Philosophie (1890)",
    },
    "becker": {
        "name": "Becker, Oskar (1889 – 1964)",
        "bib_anchor": "bib-becker-oskar",
        "work_default": "Beiträge zur phänomenologischen Begründung der Geometrie (1923)",
    },
    "bonitz": {
        "name": "Bonitz, Hermann (1814 – 1888)",
        "bib_anchor": "bib-bonitz-hermann",
        "work_default": "Aristotelis Metaphysica: Commentarius (1848–1849)",
    },
    "brouwer": {
        "name": "Brouwer, L. E. J. (1881 – 1966)",
        "bib_anchor": "bib-brouwer-luitzen-egbertus-jan",
        "work_default": "Over de grondslagen der wiskunde (1907)",
    },
    "brunschvicg": {
        "name": "Brunschvicg, Léon (1869 – 1944)",
        "bib_anchor": "bib-brunschvicg-leon",
        "work_default": "Les étapes de la philosophie mathématique (1912)",
    },
    "burnet": {
        "name": "Burnet, John (1863 – 1928)",
        "bib_anchor": "bib-burnet-john",
        "work_default": "Greek Philosophy: Thales to Plato (1914)",
    },
    "cajetan": {
        "name": "Cajetan, Thomas de Vio, O.P. (1469 – 1534)",
        "bib_anchor": "bib-thomas-de-vio-cajetan-cardinal-o-p",
        "work_default": "In De Ente et Essentia / In Summam Theologiae",
    },
    "cantor": {
        "name": "Cantor, Georg (1845 – 1918)",
        "bib_anchor": "bib-cantor-georg",
        "work_default": "Gesammelte Abhandlungen mathematischen und philosophischen Inhalts",
    },
    "carteron": {
        "name": "Carteron, Henri (1891 – 1927)",
        "bib_anchor": "bib-carteron-henri",
        "work_default": "Aristote: Physique (ed. Budé, 1926)",
    },
    "christ": {
        "name": "Christ, Wilhelm von (1831 – 1906)",
        "bib_anchor": "bib-christ-wilhelm-von",
        "work_default": "Aristotelis Metaphysica (ed. Teubner)",
    },
    "couturat": {
        "name": "Couturat, Louis (1868 – 1914)",
        "bib_anchor": "bib-couturat-louis",
        "work_default": "La philosophie des mathématiques de Kant (Revue de Métaphysique et de Morale, 1904)",
    },
    "dedekind": {
        "name": "Dedekind, Richard (1831 – 1916)",
        "bib_anchor": "bib-dedekind-richard",
        "work_default": "Stetigkeit und irrationale Zahlen (1872)",
    },
    "descartes": {
        "name": "Descartes, René (1596 – 1650)",
        "bib_anchor": "bib-descartes-rene",
        "work_default": "Œuvres de Descartes (ed. Adam & Tannery)",
    },
    "einstein": {
        "name": "Einstein, Albert (1879 – 1955)",
        "bib_anchor": "bib-einstein-albert",
        "work_default": "Geometrie und Erfahrung (1921)",
    },
    "enriques": {
        "name": "Enriques, Federigo (1871 – 1946)",
        "bib_anchor": "bib-enriques-federigo",
        "work_default": "Questioni riguardanti le matematiche elementari",
    },
    "euclid": {
        "name": "Euclid of Alexandria (fl. c. 300 BC)",
        "bib_anchor": "bib-euclid-of-alexandria",
        "work_default": "Elementa (ed. Heiberg)",
    },
    "freudenthal": {
        "name": "Freudenthal, Hans (1905 – 1990)",
        "bib_anchor": "bib-freudenthal-hans",
        "work_default": "De fontibus geometriae in intuitione et abstractione quaerendis (Gregorianum, 1951)",
    },
    "gauss": {
        "name": "Gauss, Carl Friedrich (1777 – 1855)",
        "bib_anchor": "bib-gauss-carl-friedrich",
        "work_default": "Werke",
    },
    "geyser": {
        "name": "Geyser, Joseph (1869 – 1948)",
        "bib_anchor": "bib-geyser-joseph",
        "work_default": "Die Erkenntnistheorie des Aristoteles (1917)",
    },
    "gilson": {
        "name": "Gilson, Étienne (1884 – 1978)",
        "bib_anchor": "bib-gilson-etienne",
        "work_default": "L'être et l'essence (1948) / Being and Some Philosophers (1949)",
    },
    "gonseth": {
        "name": "Gonseth, Ferdinand (1890 – 1975)",
        "bib_anchor": "bib-gonseth-ferdinand",
        "work_default": "Les fondements des mathématiques (1926)",
    },
    "gredt": {
        "name": "Gredt, Joseph, O.S.B. (1863 – 1940)",
        "bib_anchor": "bib-gredt-joseph-o-s-b",
        "work_default": "Elementa Philosophiae Aristotelico-Thomisticae",
    },
    "hadamard": {
        "name": "Hadamard, Jacques (1865 – 1963)",
        "bib_anchor": "bib-hadamard-jacques",
        "work_default": "Encyclopédie Française, Tome I: L'Outillage Mental (1937)",
    },
    "hamelin": {
        "name": "Hamelin, Octave (1856 – 1907)",
        "bib_anchor": "bib-hamelin-octave",
        "work_default": "Le Système d'Aristote (1920)",
    },
    "hardy": {
        "name": "Hardy, Godfrey Harold (1877 – 1947)",
        "bib_anchor": "bib-hardy-godfrey-harold",
        "work_default": "Mathematical Proof (Mind, 1929)",
    },
    "hasse-scholz": {
        "name": "Hasse, Helmut & Scholz, Heinrich",
        "bib_anchor": "bib-hasse-helmut",
        "work_default": "Die Grundlagenkrisis der griechischen Mathematik (Kant-Studien, 1928)",
    },
    "hausdorff": {
        "name": "Hausdorff, Felix (1868 – 1942)",
        "bib_anchor": "bib-hausdorff-felix",
        "work_default": "Das Raumproblem (Annalen der Naturphilosophie, 1904)",
    },
    "heath": {
        "name": "Heath, Sir Thomas Little (1861 – 1940)",
        "bib_anchor": "bib-heath-sir-thomas-little",
        "work_default": "The Thirteen Books of Euclid's Elements / A History of Greek Mathematics",
    },
    "hegel": {
        "name": "Hegel, Georg Wilhelm Friedrich (1770 – 1831)",
        "bib_anchor": "bib-hegel-georg-wilhelm-friedrich",
        "work_default": "Wissenschaft der Logik (Werke, 1834)",
    },
    "helmholtz": {
        "name": "Helmholtz, Hermann von (1821 – 1894)",
        "bib_anchor": "bib-helmholtz-hermann-von",
        "work_default": "Schriften zur Erkenntnistheorie (ed. Hertz & Schlick, 1921)",
    },
    "hessenberg": {
        "name": "Hessenberg, Gerhard (1874 – 1925)",
        "bib_anchor": "bib-hessenberg-gerhard",
        "work_default": "Kritik und System in Mathematik und Philosophie (1908)",
    },
    "hilbert": {
        "name": "Hilbert, David (1862 – 1943)",
        "bib_anchor": "bib-hilbert-david",
        "work_default": "Grundlagen der Geometrie (1899; 7th ed. 1930)",
    },
    "hoelder": {
        "name": "Hölder, Otto (1859 – 1937)",
        "bib_anchor": "bib-holder-otto",
        "work_default": "Die mathematische Methode (1924)",
    },
    "hoenen": {
        "name": "Hoenen, Petrus Hubertus Jacobus, S.J. (1880 – 1961)",
        "bib_anchor": "bib-hoenen-petrus-hubertus-jacobus-s-j",
        "work_default": "De Noetica Geometriae / La théorie du jugement / Cosmologia",
    },
    "hume": {
        "name": "Hume, David (1711 – 1776)",
        "bib_anchor": "bib-hume-david",
        "work_default": "A Treatise of Human Nature (1739)",
    },
    "kant": {
        "name": "Kant, Immanuel (1724 – 1804)",
        "bib_anchor": "bib-kant-immanuel",
        "work_default": "Kritik der reinen Vernunft (2nd ed., 1787) / Prolegomena (1783)",
    },
    "killing": {
        "name": "Killing, Wilhelm (1847 – 1923)",
        "bib_anchor": "bib-killing-wilhelm",
        "work_default": "Einführung in die Grundlagen der Geometrie (1893–1898)",
    },
    "klein": {
        "name": "Klein, Felix (1849 – 1925)",
        "bib_anchor": "bib-klein-felix",
        "work_default": "Anwendung der Differential- und Integralrechnung (1907) / Elementarmathematik (1925)",
    },
    "leibniz": {
        "name": "Leibniz, Gottfried Wilhelm (1646 – 1716)",
        "bib_anchor": "bib-leibniz-gottfried-wilhelm",
        "work_default": "Nouveaux Essais sur l'entendement humain (1704)",
    },
    "locke": {
        "name": "Locke, John (1632 – 1704)",
        "bib_anchor": "bib-locke-john",
        "work_default": "An Essay Concerning Human Understanding (1690)",
    },
    "lonergan": {
        "name": "Lonergan, Bernard, S.J. (1904 – 1984)",
        "bib_anchor": "bib-lonergan-bernard-s-j",
        "work_default": "The Concept of Verbum in the Writings of St. Thomas Aquinas (1946–1949)",
    },
    "maier": {
        "name": "Maier, Anneliese (1905 – 1971)",
        "bib_anchor": "bib-maier-anneliese",
        "work_default": "An der Grenze von Scholastik und Naturwissenschaft (1943)",
    },
    "maritain": {
        "name": "Maritain, Jacques (1882 – 1973)",
        "bib_anchor": "bib-maritain-jacques",
        "work_default": "Distinguish to Unite, or The Degrees of Knowledge (Les degrés du savoir, 1932)",
    },
    "mercier": {
        "name": "Mercier, Désiré-Joseph, Cardinal (1851 – 1926)",
        "bib_anchor": "bib-mercier-desire-joseph-cardinal",
        "work_default": "Critériologie générale (8th ed., 1923)",
    },
    "meyerson": {
        "name": "Meyerson, Émile (1859 – 1933)",
        "bib_anchor": "bib-meyerson-emile",
        "work_default": "Du cheminement de la pensée (1931)",
    },
    "mill": {
        "name": "Mill, John Stuart (1806 – 1873)",
        "bib_anchor": "bib-mill-john-stuart",
        "work_default": "A System of Logic (5th ed., 1862)",
    },
    "newton": {
        "name": "Newton, Sir Isaac (1642 – 1727)",
        "bib_anchor": "bib-newton-sir-isaac",
        "work_default": "Philosophiae Naturalis Principia Mathematica (1687)",
    },
    "pasch": {
        "name": "Pasch, Moritz (1843 – 1930)",
        "bib_anchor": "bib-pasch-moritz",
        "work_default": "Vorlesungen über neuere Geometrie (1882; 2nd ed. 1926)",
    },
    "philoponus": {
        "name": "John Philoponus (c. 490 – c. 570 AD)",
        "bib_anchor": "bib-john-philoponus",
        "work_default": "In Aristotelis Physicorum Libros Commentaria (ed. Vitelli)",
    },
    "plato": {
        "name": "Plato (428/427 – 348/347 BC)",
        "bib_anchor": "bib-plato",
        "work_default": "Respublica / Meno / Leges / Phaedo",
    },
    "poincare": {
        "name": "Poincaré, Henri (1854 – 1912)",
        "bib_anchor": "bib-poincare-henri",
        "work_default": "La Science et l'Hypothèse (1902) / La Valeur de la Science (1905) / Dernières Pensées (1913)",
    },
    "proclus": {
        "name": "Proclus Lycius Diadochus (412 – 485 AD)",
        "bib_anchor": "bib-proclus-lycius-diadochus",
        "work_default": "In Primum Euclidis Elementorum Librum Commentarii (ed. Friedlein, 1873)",
    },
    "pseudo-thomas": {
        "name": "Pseudo-Thomas Aquinas / Pseudo-Scotus",
        "bib_anchor": "bib-thomas-aquinas-st-o-p",
        "work_default": "Summa Totius Logicae Aristotelis",
    },
    "reichenbach": {
        "name": "Reichenbach, Hans (1891 – 1953)",
        "bib_anchor": "bib-reichenbach-hans",
        "work_default": "Philosophie der Raum-Zeit-Lehre (1928)",
    },
    "riehl": {
        "name": "Riehl, Alois (1844 – 1924)",
        "bib_anchor": "bib-riehl-alois",
        "work_default": "Logik und Erkenntnistheorie (Die Kultur der Gegenwart, 1921)",
    },
    "ross": {
        "name": "Ross, Sir William David (1877 – 1971)",
        "bib_anchor": "bib-ross-sir-william-david",
        "work_default": "Aristotle's Metaphysics (1924) / Aristotle's Physics (1936)",
    },
    "russell": {
        "name": "Russell, Bertrand (1872 – 1970)",
        "bib_anchor": "bib-russell-bertrand",
        "work_default": "The Principles of Mathematics (1903)",
    },
    "scholz": {
        "name": "Scholz, Heinrich (1884 – 1956)",
        "bib_anchor": "bib-scholz-heinrich",
        "work_default": "Warum haben die Griechen die Irrationalzahlen nicht aufgebaut? (1928)",
    },
    "simplicius": {
        "name": "Simplicius of Cilicia (c. 490 – c. 560 AD)",
        "bib_anchor": "bib-simplicius-of-cilicia",
        "work_default": "In Aristotelis Physicorum Libros Commentaria (ed. Diels)",
    },
    "stammler": {
        "name": "Stammler, Gerhard (1898 – 1977)",
        "bib_anchor": "bib-stammler-gerhard",
        "work_default": "Begriff, Urteil, Schluss (1928) / Der Zahlbegriff seit Gauss (1926)",
    },
    "study": {
        "name": "Study, Eduard (1862 – 1930)",
        "bib_anchor": "bib-study-eduard",
        "work_default": "Die realistische Weltansicht und die Lehre vom Raume (1914)",
    },
    "suarez": {
        "name": "Suárez, Francisco, S.J. (1548 – 1617)",
        "bib_anchor": "bib-suarez-francisco-s-j",
        "work_default": "Disputationes Metaphysicae (1597)",
    },
    "taylor": {
        "name": "Taylor, Alfred Edward (1869 – 1945)",
        "bib_anchor": "bib-taylor-alfred-edward",
        "work_default": "Plato: The Man and His Work (1927)",
    },
    "themistius": {
        "name": "Themistius (c. 317 – c. 388 AD)",
        "bib_anchor": "bib-themistius",
        "work_default": "In Aristotelis Physica Paraphrasis (ed. Schenkl)",
    },
    "voss": {
        "name": "Voss, Aurel (1845 – 1931)",
        "bib_anchor": "bib-voss-aurel",
        "work_default": "Über die mathematische Erkenntnis (Die Kultur der Gegenwart, 1914)",
    },
    "waitz": {
        "name": "Waitz, Theodor (1821 – 1864)",
        "bib_anchor": "bib-waitz-theodor",
        "work_default": "Aristotelis Organon Graece (1844–1846)",
    },
    "weber-wellstein": {
        "name": "Weber, Heinrich & Wellstein, Josef",
        "bib_anchor": "bib-weber-heinrich",
        "work_default": "Enzyklopädie der Elementarmathematik, Band II: Elemente der Geometrie (1915 / 1925)",
    },
    "weyl": {
        "name": "Weyl, Hermann (1885 – 1955)",
        "bib_anchor": "bib-weyl-hermann",
        "work_default": "Philosophie der Mathematik und Naturwissenschaft (1927)",
    },
    "whitehead-russell": {
        "name": "Whitehead, Alfred North & Russell, Bertrand",
        "bib_anchor": "bib-whitehead-alfred-north",
        "work_default": "Principia Mathematica (1910–1913)",
    },
}

WORK_TITLES: Dict[str, str] = {
    "aquinas:anal-post": "In Aristotelis Libros Posteriorum Analyticorum Expositio",
    "aquinas:de-trin": "Expositio super Librum Boethii De Trinitate",
    "aquinas:de-anima": "Sentencia Libri De Anima",
    "aquinas:de-veritate": "Quaestiones Disputatae de Veritate",
    "aquinas:de-potentia": "Quaestiones Disputatae de Potentia Dei",
    "aquinas:de-malo": "Quaestiones Disputatae de Malo",
    "aquinas:de-caelo": "In Libros Aristotelis De Caelo et Mundo Expositio",
    "aquinas:met": "Sententia super Metaphysicam",
    "aquinas:phys": "Commentaria in Octo Libros Physicorum Aristotelis",
    "aquinas:periherm": "Expositio Libri Peryermeneias",
    "aquinas:eth-nic": "Sententia Libri Ethicorum",
    "aquinas:sent": "Scriptum super Libros Sententiarum",
    "aquinas:scg": "Summa contra Gentiles",
    "aquinas:st": "Summa Theologiae",
    "aristotle:anal-post": "Analytica Posteriora (Posterior Analytics)",
    "aristotle:anal-prior": "Analytica Priora (Prior Analytics)",
    "aristotle:de-anima": "De Anima (On the Soul)",
    "aristotle:eth-nic": "Ethica Nicomachea (Nicomachean Ethics)",
    "aristotle:met": "Metaphysica (Metaphysics)",
    "aristotle:phys": "Physica (Physics)",
    "aristotle:periherm": "De Interpretatione (Peri Hermeneias)",
    "euclid:elements": "Elementa (The Thirteen Books of the Elements)",
    "hilbert:grundlagen": "Grundlagen der Geometrie (Foundations of Geometry, 1899 / 1930)",
    "hoenen:cosmologia": "Cosmologia (4th ed., Rome: Gregorian University, 1949)",
    "hoenen:theorie-du-jugement": "La théorie du jugement d'après St. Thomas d'Aquin (1946; 2nd ed. 1953)",
    "hoenen:reality-and-judgment": "Reality and Judgment According to St. Thomas (Chicago: Regnery, 1952)",
    "hoenen:filosofia-natura": "Filosofia della natura inorganica (Milan, 1949)",
    "hoenen:1933": "De origine primorum principiorum scientiae (Gregorianum XIV, 1933, pp. 153–184)",
    "hoenen:1937": "Le « Cogito ergo sum » comme intuition et comme mouvement de la pensée (1937)",
    "hoenen:1938": "De philosophia scholastica cognitionis geometricae (Gregorianum XIX, 1938, pp. 498–514)",
    "hoenen:1939": "De problemate necessitatis geometricae (Gregorianum XX, 1939, pp. 19–54)",
    "hoenen:1947": "Recherches de logique formelle (Rome: Gregorian University, 1947)",
    "hoenen:1948": "Gregorianum XXIX (1948), pp. 295–303",
    "hoenen:1949": "Pour une philosophie de la connaissance de l'étendu physique (Gregorianum XXX, 1949)",
    "hoenen:1951": "De noetica geometriae (Gregorianum XXXII, 1951, pp. 434–452)",
    "hoenen:1953": "De connexionibus necessariis inter actus existentiales (Gregorianum XXXIV, 1953)",
    "hoenen:1954": "De Noetica Geometriae: Origine Theoriae Cognitionis (1954 — Internal Cross-Reference)",
    "kant:krv": "Kritik der reinen Vernunft (Critique of Pure Reason, 2nd ed. 1787)",
    "kant:prolegomena": "Prolegomena zu einer jeden künftigen Metaphysik (1783)",
    "klein:1907": "Anwendung der Differential- und Integralrechnung auf Geometrie: Eine Revision der Prinzipien (2nd ed. 1907)",
    "klein:1925": "Elementarmathematik vom höheren Standpunkte aus, Band II: Geometrie (3rd ed. 1925)",
    "plato:rep": "Respublica (The Republic)",
    "plato:meno": "Meno",
    "plato:leges": "Leges (The Laws)",
    "poincare:science-hypothese": "La Science et l'Hypothèse (1902)",
    "poincare:valeur-science": "La Valeur de la Science (1905)",
    "poincare:science-methode": "Science et Méthode (1908)",
    "poincare:dernieres-pensees": "Dernières Pensées (1913)",
}

TERM_CATALOG: Dict[str, Dict[str, str]] = {
    "abstractio-formalis": {
        "headword": "abstractio formalis",
        "language": "Latin (Scholastic)",
        "translation": "Formal abstraction",
        "definition": "Abstraction of the intelligible form or mathematical nature (quantity/extension) from sensible matter.",
    },
    "abstractio-totalis": {
        "headword": "abstractio totalis",
        "language": "Latin (Scholastic)",
        "translation": "Total abstraction",
        "definition": "Abstraction of a universal whole (genus/species) from its individual particulars.",
    },
    "aitema": {
        "headword": "αἴτημα (αἰτήματα)",
        "language": "Greek",
        "translation": "Postulate (postulates)",
        "definition": "In Aristotle and Euclid, a demonstrable or constructible principle requested from the learner without proof within the science.",
    },
    "aiteo": {
        "headword": "αἰτεῖται",
        "language": "Greek",
        "translation": "He postulates / requests",
        "definition": "Aristotle's verb (Anal. Post. I 10, 76b28) for assuming a principle when the learner has no prior opinion or holds a contrary opinion.",
    },
    "anordnung": {
        "headword": "Anordnung",
        "language": "German",
        "translation": "Order / Arrangement",
        "definition": "Hilbert's second group of geometric axioms (Axioms of Order / Betweenness) in Grundlagen der Geometrie.",
    },
    "apotheosis-of-stupidity": {
        "headword": "the apotheosis of stupidity",
        "language": "English",
        "translation": "The apotheosis of stupidity",
        "definition": "G. H. Hardy's characterization (Mind, 1929) of reducing mathematical proof to purely mechanical, uncomprehending symbol manipulation.",
    },
    "approximationsmathematik": {
        "headword": "Approximationsmathematik",
        "language": "German",
        "translation": "Mathematics of approximation",
        "definition": "Felix Klein's term for empirical/applied mathematics bounded by a threshold of sensory accuracy (limen exactitudinis), contrasted with Präzisionsmathematik.",
    },
    "ars-epsilontica": {
        "headword": "ars epsilontica",
        "language": "Latin (Modern Mathematical)",
        "translation": "Epsilon-delta technique",
        "definition": "Weierstrassian rigorous limit and approximation analysis using arbitrary small quantities ε.",
    },
    "atomon": {
        "headword": "ἄτομον",
        "language": "Greek",
        "translation": "Indivisible",
        "definition": "An indivisible magnitude or unit lacking further division.",
    },
    "axioma": {
        "headword": "ἀξίωμα (ἀξιώματα)",
        "language": "Greek",
        "translation": "Axiom / Common dignity",
        "definition": "Self-evident first principle that every learner must possess to acquire scientific knowledge (Aristotle, Anal. Post. I 2 & I 10).",
    },
    "betweenness": {
        "headword": "betweenness",
        "language": "English",
        "translation": "Betweenness",
        "definition": "Fundamental order relation among collinear points (B lies between A and C), introduced by Pasch and formalized by Hilbert and Russell.",
    },
    "cheminement-de-la-pensee": {
        "headword": "le cheminement de la pensée",
        "language": "French",
        "translation": "The progression / pathway of thought",
        "definition": "Émile Meyerson's phrase (1931) for the actual cognitive movement of the mind in scientific discovery and deduction.",
    },
    "circulus-vitiosus": {
        "headword": "circulus vitiosus",
        "language": "Latin",
        "translation": "Vicious circle",
        "definition": "Circular reasoning or definition where the definiendum is presupposed in the definiens.",
    },
    "cogito-ergo-sum": {
        "headword": "cogito ergo sum",
        "language": "Latin",
        "translation": "I think, therefore I am",
        "definition": "Descartes' existential judgment; analyzed by Hoenen in Appendix as an intuitive perception of a necessary connection between an experienced act (cogito) and existence (sum).",
    },
    "cum-fundamento-in-re": {
        "headword": "cum fundamento in re",
        "language": "Latin (Scholastic)",
        "translation": "With a foundation in reality",
        "definition": "A conceptual being or idealized limit (ens rationis) grounded objectively in the real properties of extended bodies.",
    },
    "cum-grano-salis": {
        "headword": "cum grano salis",
        "language": "Latin",
        "translation": "With a grain of salt (with due qualification)",
        "definition": "Idiom indicating that a general formulation requires careful philosophical qualification.",
    },
    "dianoia": {
        "headword": "διάνοια",
        "language": "Greek",
        "translation": "Discursive mathematical understanding",
        "definition": "In Plato's Republic (VI 510–511), the cognitive faculty proper to geometry and arithmetic, intermediate between opinion (doxa) and pure noetic intellection (nous).",
    },
    "distinguo": {
        "headword": "distinguo",
        "language": "Latin (Scholastic)",
        "translation": "I distinguish",
        "definition": "Classic scholastic disputation operator separating the true and false senses of an ambiguous thesis.",
    },
    "doxa": {
        "headword": "δόξα",
        "language": "Greek",
        "translation": "Opinion (belief / appearance)",
        "definition": "Cognition of sensible, contingent things in Plato and Aristotle, contrasted with scientific knowledge (episteme).",
    },
    "dynamis": {
        "headword": "δύναμις (δυνάμει)",
        "language": "Greek",
        "translation": "Potency / In potentiality",
        "definition": "Aristotelian potentiality, contrasted with actuality (energeia / entelecheia).",
    },
    "eikasia": {
        "headword": "εἰκασία",
        "language": "Greek",
        "translation": "Imagination / Conjecture from shadows",
        "definition": "The lowest segment of Plato's Divided Line (Republic VI 509d–511e).",
    },
    "energeia": {
        "headword": "ἐνέργεια",
        "language": "Greek",
        "translation": "Act / Activity / Actuality",
        "definition": "Aristotle's core metaphysical term for actuality or operation, originally derived from local motion and extended to all existential and cognitive acts.",
    },
    "ens-rationis": {
        "headword": "ens rationis",
        "language": "Latin (Scholastic)",
        "translation": "Being of reason (conceptual entity)",
        "definition": "An object existing formally only in the intellect, though in mathematics grounded in real extension (cum fundamento in re).",
    },
    "ensemble": {
        "headword": "ensemble",
        "language": "French",
        "translation": "Set / Manifold",
        "definition": "Mathematical set or continuum of elements (equivalent to German Menge and Italian insieme).",
    },
    "entelecheia": {
        "headword": "ἐντελέχεια",
        "language": "Greek",
        "translation": "Complete actuality / Perfection (entelechy)",
        "definition": "Aristotle's term for realized form or act as holding its end/completeness within itself.",
    },
    "epharmozomenou-tou-trigonou": {
        "headword": "ἐφαρμοζομένου τοῦ τριγώνου",
        "language": "Greek",
        "translation": "The triangle being applied (superposed)",
        "definition": "Euclid's phrase in Elements I.4 for the superposition of one triangle upon another.",
    },
    "epipedos-epiphaneia-estin": {
        "headword": "ἐπίπεδος ἐπιφάνειά ἐστιν, ἥτις ἐξ ἴσου ταῖς ἐφ' ἑαυτῆς εὐθείαις κεῖται",
        "language": "Greek",
        "translation": "A plane surface is that which lies evenly with the straight lines on itself",
        "definition": "Euclid's Definition 7 of Book I (ed. Heiberg I, pp. 2–3).",
    },
    "episteme": {
        "headword": "ἐπιστήμη",
        "language": "Greek",
        "translation": "Scientific knowledge (apodictic science)",
        "definition": "Demonstrative knowledge through necessary causes and first principles.",
    },
    "eutheia-gramme-estin": {
        "headword": "εὐθεῖα γραμμή ἐστιν, ἥτις ἐξ ἴσου τοῖς ἐφ' ἑαυτῆς σημείοις κεῖται",
        "language": "Greek",
        "translation": "A straight line is a line which lies evenly with the points on itself",
        "definition": "Euclid's Definition 4 of Book I (ed. Heiberg I, pp. 2–3).",
    },
    "facio-ergo-materia-rei-factibilis-adest": {
        "headword": "facio ergo materia rei factibilis adest",
        "language": "Latin",
        "translation": "I make/act upon it, therefore the matter of the makeable thing is present",
        "definition": "Hoenen's formulation of the existential judgment of external material reality grounded in conscious bodily action upon matter.",
    },
    "folium-moebii": {
        "headword": "folium Moebii",
        "language": "Latin",
        "translation": "Möbius strip (one-sided surface)",
        "definition": "The non-orientable one-sided surface discovered by A. F. Möbius (1858), analyzed by Hoenen in Caput III § 2.4 to refute objections against defining surfaces as boundaries of bodies.",
    },
    "grenzprozess": {
        "headword": "Grenzprozess",
        "language": "German",
        "translation": "Limiting process",
        "definition": "Passage to the ideal mathematical limit from empirical approximations.",
    },
    "hoc-movetur-ergo-aliud-movens-existit": {
        "headword": "hoc movetur ergo aliud, movens, existit",
        "language": "Latin",
        "translation": "This moves, therefore another (a mover) exists",
        "definition": "Existential causal inference from perceived motion to an existing efficient cause.",
    },
    "hoc-movetur-ergo-locus-est": {
        "headword": "hoc movetur ergo locus est",
        "language": "Latin",
        "translation": "This moves locally, therefore place exists",
        "definition": "Existential inference from local motion (translation) to the reality of spatial location.",
    },
    "homologia": {
        "headword": "ὁμολογία",
        "language": "Greek",
        "translation": "Agreement / Admission",
        "definition": "Plato's term (Republic VII 533c) for unexamined hypotheses accepted merely by convention.",
    },
    "hyle-noete": {
        "headword": "ὕλη νοητή",
        "language": "Greek",
        "translation": "Intelligible matter (materia intelligibilis)",
        "definition": "Aristotle's term (Metaphysics VII 10, 1036a9; VIII 6, 1045a34) for pure spatial extension considered in the imagination apart from sensible qualities.",
    },
    "hyparchein": {
        "headword": "ὑπάρχειν",
        "language": "Greek",
        "translation": "To belong to / To exist / To inhere",
        "definition": "Aristotelian logical and ontological verb for predicate inherence or actual existence.",
    },
    "hypothesis": {
        "headword": "ὑπόθεσις (ὑποθέσεις)",
        "language": "Greek",
        "translation": "Hypothesis / Supposition",
        "definition": "In Aristotle (Anal. Post. I 2 & I 10), an assumed principle asserting that the subject exists or does not exist.",
    },
    "hypotithemai": {
        "headword": "ὑποτίθεται",
        "language": "Greek",
        "translation": "He supposes / assumes as a hypothesis",
        "definition": "Aristotle's verb (Anal. Post. I 10, 76b28) for assuming a demonstrable proposition that seems probable to the learner.",
    },
    "in-actu-exercito": {
        "headword": "in actu exercito",
        "language": "Latin (Scholastic)",
        "translation": "In the exercised act (implicitly in performance)",
        "definition": "Knowledge or principle grasped and used directly within the living act of thinking or perceiving, prior to explicit reflexive formulation (in actu signato).",
    },
    "in-actu-signato": {
        "headword": "in actu signato",
        "language": "Latin (Scholastic)",
        "translation": "In the signified act (explicitly formulated)",
        "definition": "Explicit, reflexively thematicized statement of a concept or principle previously grasped in actu exercito.",
    },
    "insieme": {
        "headword": "insieme",
        "language": "Italian",
        "translation": "Set / Continuum of numbers",
        "definition": "Mathematical set (used for the set/continuum of real numbers).",
    },
    "kinesis": {
        "headword": "κίνησις",
        "language": "Greek",
        "translation": "Motion / Change",
        "definition": "In Aristotle (Physics III 1), the actuality of what is in potentiality insofar as it is in potentiality.",
    },
    "oinai-ennoiai": {
        "headword": "κοιναὶ ἔννοιαι",
        "language": "Greek",
        "translation": "Common Notions (Axioms)",
        "definition": "Euclid's term for universal self-evident axioms (e.g., 'Things equal to the same thing are also equal to one another').",
    },
    "koinai-ennoiai": {
        "headword": "κοιναὶ ἔννοιαι",
        "language": "Greek",
        "translation": "Common Notions (Axioms)",
        "definition": "Euclid's term for universal self-evident axioms.",
    },
    "limen-exactitudinis": {
        "headword": "limen exactitudinis",
        "language": "Latin",
        "translation": "Threshold of exactitude (Schwellenwert der Genauigkeit)",
        "definition": "The finite limit of precision inherent in all external sensory perception and measurement (Felix Klein).",
    },
    "logica-docens": {
        "headword": "logica docens",
        "language": "Latin (Scholastic)",
        "translation": "Theoretical / Reflexive logic",
        "definition": "The explicit scientific theory of logical rules and syllogistic forms.",
    },
    "logica-utens": {
        "headword": "logica utens",
        "language": "Latin (Scholastic)",
        "translation": "Applied / Exercised logic",
        "definition": "Logic actively practiced by the mind in reasoning about objects (in actu exercito).",
    },
    "materia-intelligibilis": {
        "headword": "materia intelligibilis",
        "language": "Latin (Scholastic)",
        "translation": "Intelligible matter (ὕλη νοητή)",
        "definition": "Continuous spatial extension grasped in the phantasm apart from sensible qualities, serving as the principle of individuation and constructibility for geometric figures.",
    },
    "materia-sensibilis": {
        "headword": "materia sensibilis",
        "language": "Latin (Scholastic)",
        "translation": "Sensible matter (ὕλη αἰσθητή)",
        "definition": "Physical matter endowed with sensible qualities (color, heat, weight, hardness), abstracted from in mathematics.",
    },
    "menge": {
        "headword": "Menge",
        "language": "German",
        "translation": "Set",
        "definition": "Georg Cantor's term for a mathematical set or manifold.",
    },
    "minimum-imaginabile": {
        "headword": "minimum imaginabile",
        "language": "Latin",
        "translation": "Smallest imaginable magnitude",
        "definition": "Empiricist thesis (Berkeley, Hume) claiming imagination consists of finite indivisible minima.",
    },
    "minimum-visibile": {
        "headword": "minimum visibile",
        "language": "Latin",
        "translation": "Smallest visible spot",
        "definition": "The smallest angular or spatial extent discernible by the eye.",
    },
    "moveri-sequitur-esse": {
        "headword": "moveri sequitur esse",
        "language": "Latin",
        "translation": "Being moved follows upon existing",
        "definition": "Scholastic principle expressing the necessary existential connection between motion and actual existence.",
    },
    "movetur-ergo-est": {
        "headword": "movetur ergo est",
        "language": "Latin",
        "translation": "It moves, therefore it exists",
        "definition": "Hoenen's primary paradigm (Appendix § 1) of an intuitive existential judgment connecting perceived motion with actual existence.",
    },
    "noesis": {
        "headword": "νόησις",
        "language": "Greek",
        "translation": "Intellectual intuition / Noetic vision",
        "definition": "Direct intellectual apprehension of intelligible natures and first principles in the phantasm.",
    },
    "nous": {
        "headword": "νοῦς",
        "language": "Greek",
        "translation": "Intellect / Habit of first principles",
        "definition": "In Aristotle (Anal. Post. II 19), the intuitive intellectual faculty that grasps immediate first principles.",
    },
    "ou-meros-outhen": {
        "headword": "οὗ μέρος οὐθέν",
        "language": "Greek",
        "translation": "That of which there is no part",
        "definition": "Euclid's Definition 1 of a point (Σημεῖόν ἐστιν, οὗ μέρος οὐθέν).",
    },
    "peras": {
        "headword": "πέρας",
        "language": "Greek",
        "translation": "Boundary / Limit / Extremity",
        "definition": "Aristotle's and Euclid's ontological category for surfaces, lines, and points as indivisible boundaries of continua.",
    },
    "phantasma": {
        "headword": "φάντασμα (φαντάσματα)",
        "language": "Greek",
        "translation": "Phantasm (imaginative representation)",
        "definition": "Sensory/imaginative representation in which the intellect beholds universal mathematical and philosophical natures.",
    },
    "pistis": {
        "headword": "πίστις",
        "language": "Greek",
        "translation": "Belief / Sensory conviction",
        "definition": "The higher subdivision of opinion (doxa) in Plato's Divided Line, concerned with physical objects.",
    },
    "poiountes-gignoskousin": {
        "headword": "ποιοῦντες γιγνώσκουσιν",
        "language": "Greek",
        "translation": "By constructing/making, they know (facientes cognoscunt)",
        "definition": "Aristotle's dictum (Metaphysics IX 9, 1051a31) that geometric truths become manifest by actively drawing and dividing figures.",
    },
    "praezisionsmathematik": {
        "headword": "Präzisionsmathematik",
        "language": "German",
        "translation": "Mathematics of ideal precision",
        "definition": "Felix Klein's term for pure, exact mathematics operating with idealized limits, contrasted with Approximationsmathematik.",
    },
    "principium-individuationis": {
        "headword": "principium individuationis",
        "language": "Latin (Scholastic)",
        "translation": "Principle of individuation",
        "definition": "That whereby multiple individuals of the same species are numerically distinct (intelligible matter in geometry).",
    },
    "propositio-per-accidens": {
        "headword": "propositio per accidens",
        "language": "Latin (Scholastic)",
        "translation": "Accidental / Contingent proposition",
        "definition": "A judgment joining subject and predicate through contingent coexistence rather than essential necessity.",
    },
    "propositio-per-se": {
        "headword": "propositio per se",
        "language": "Latin (Scholastic)",
        "translation": "Essential / Self-grounded proposition (per se nota)",
        "definition": "A necessary proposition whose predicate belongs to the intelligible nature of the subject.",
    },
    "semeion": {
        "headword": "σημεῖον",
        "language": "Greek",
        "translation": "Point / Sign",
        "definition": "Geometric point (Euclid, Elements I Def. 1).",
    },
    "strecke": {
        "headword": "Strecke",
        "language": "German",
        "translation": "Line segment",
        "definition": "Hilbert's term in Grundlagen der Geometrie for a bounded straight segment AB defined as the system of two points.",
    },
    "ta-ex-aphaireseos": {
        "headword": "τὰ ἐξ ἀφαιρέσεως",
        "language": "Greek",
        "translation": "Things derived from abstraction (mathematical objects)",
        "definition": "Aristotle's standard technical designation for mathematical entities abstracted from sensible qualities.",
    },
    "telos": {
        "headword": "τέλος",
        "language": "Greek",
        "translation": "End / Final cause / Completion",
        "definition": "The goal or terminal perfection toward which an action or motion tends.",
    },
    "termini-transcendentes": {
        "headword": "termini transcendentes",
        "language": "Latin (Scholastic)",
        "translation": "Transcendental terms",
        "definition": "Terms such as ens (being), unum (one), res (thing), and aliquid (something) that transcend the ten Aristotelian categories.",
    },
    "ti-estin": {
        "headword": "τί ἐστιν",
        "language": "Greek",
        "translation": "What it is (quiddity / essence)",
        "definition": "Aristotle's question of essential definition, distinguished from whether a thing exists (εἰ ἔστιν).",
    },
    "tode": {
        "headword": "τόδε (τόδε τι)",
        "language": "Greek",
        "translation": "This something (concrete individual)",
        "definition": "Aristotle's expression for a determinate, demonstratively indicated individual entity.",
    },
    "verknuepfung": {
        "headword": "Verknüpfung",
        "language": "German",
        "translation": "Connection / Incidence",
        "definition": "Hilbert's first group of geometric axioms (Axiome der Verknüpfung / Axioms of Incidence) in Grundlagen der Geometrie.",
    },
}

PERSON_CATALOG: Dict[str, Dict[str, Any]] = {
    "albertus": {
        "name": "Albert the Great, St., O.P.",
        "dates": "c. 1200 – 1280",
        "role": "Scholastic Philosopher & Doctor of the Church",
        "bio": "Dominican friar, bishop, and teacher of Thomas Aquinas whose commentaries on Aristotle's Organon and Mathematics shaped medieval scholastic epistemology.",
        "works": ["Commentaria in Analytica Priora", "Commentaria in Analytica Posteriora", "Metaphysica"],
        "bib_anchor": "bib-albert-the-great-st-o-p",
    },
    "alexander": {
        "name": "Alexander of Aphrodisias",
        "dates": "fl. c. 200 AD",
        "role": "Peripatetic Commentator",
        "bio": "Foremost ancient Greek commentator on Aristotle, known in antiquity and the Middle Ages simply as 'The Commentator' before Averroes.",
        "works": ["In Aristotelis Metaphysica Commentaria", "In Aristotelis Analyticorum Priorum Librum I Commentarium"],
        "bib_anchor": "bib-alexander-of-aphrodisias",
    },
    "alvarez-laso": {
        "name": "José Alvarez Laso, C.M.F.",
        "dates": "1910 – 1993",
        "role": "Thomistic Philosopher of Mathematics",
        "bio": "Claretian scholar who authored a doctoral study under Hoenen on the philosophy of mathematics in St. Thomas Aquinas.",
        "works": ["La Filosofía de las Matemáticas en Santo Tomás (1952)"],
        "bib_anchor": "bib-alvarez-laso-jose-c-m-f",
    },
    "amaldi": {
        "name": "Ugo Amaldi",
        "dates": "1875 – 1957",
        "role": "Italian Mathematician",
        "bio": "Professor of mathematics in Rome and collaborator of Federigo Enriques on the foundations of elementary geometry and continuous transformation groups.",
        "works": ["Sui concetti di retta e di piano (Questioni riguardanti le matematiche elementari)"],
        "bib_anchor": "bib-amaldi-ugo",
    },
    "aquinas": {
        "name": "St. Thomas Aquinas, O.P.",
        "dates": "1225 – 1274",
        "role": "Scholastic Philosopher & Theologian (Doctor Angelicus)",
        "bio": "Dominican friar and Doctor of the Church whose synthesis of Aristotelian noetics—abstraction from phantasms, intelligible matter, and judgment by resolution to sensory principles—forms the central framework of Hoenen's treatise.",
        "works": [
            "Expositio super Librum Boethii De Trinitate",
            "In Aristotelis Libros Posteriorum Analyticorum Expositio",
            "Sententia super Metaphysicam",
            "Commentaria in Octo Libros Physicorum Aristotelis",
            "Summa Theologiae",
            "Quaestiones Disputatae de Veritate",
        ],
        "bib_anchor": "bib-thomas-aquinas-st-o-p",
    },
    "archimedes": {
        "name": "Archimedes of Syracuse",
        "dates": "c. 287 – c. 212 BC",
        "role": "Ancient Greek Mathematician & Physicist",
        "bio": "Greatest mathematician of antiquity, whose postulate on the comparison of magnitudes (the Archimedean Axiom) is central to modern continuity axioms.",
        "works": ["De Sphaera et Cylindro", "De Mensura Circuli", "Methodus"],
        "bib_anchor": "",
    },
    "aristotle": {
        "name": "Aristotle",
        "dates": "384 – 322 BC",
        "role": "Ancient Greek Philosopher (The Stagirite)",
        "bio": "Founder of the Peripatetic school and formal logic, whose theory of demonstrative science (Analytica Posteriora), abstraction (τὰ ἐξ ἀφαιρέσεως), and intelligible matter (ὕλη νοητή) originates classical geometric epistemology.",
        "works": [
            "Analytica Posteriora",
            "Analytica Priora",
            "Physica",
            "Metaphysica",
            "De Anima",
            "Ethica Nicomachea",
        ],
        "bib_anchor": "bib-aristotle",
    },
    "averroes": {
        "name": "Averroes (Ibn Rushd)",
        "dates": "1126 – 1198",
        "role": "Andalusian Philosopher & Aristotelian Commentator",
        "bio": "Islamic philosopher of Córdoba whose grand commentaries on Aristotle earned him the scholastic title 'The Commentator'.",
        "works": ["In Aristotelis Physica Commentaria", "In Aristotelis Metaphysica Commentaria"],
        "bib_anchor": "",
    },
    "avicenna": {
        "name": "Avicenna (Ibn Sīnā)",
        "dates": "c. 980 – 1037",
        "role": "Persian Polymath & Philosopher",
        "bio": "Author of the Book of Healing (Sufficientia), whose metaphysical doctrines on essence, existence, and abstraction deeply influenced Latin scholasticism.",
        "works": ["Liber de Philosophia Prima (Metaphysica)", "Sufficientia"],
        "bib_anchor": "",
    },
    "baeumker": {
        "name": "Clemens Baeumker",
        "dates": "1853 – 1924",
        "role": "Historian of Ancient & Medieval Philosophy",
        "bio": "German Neo-Scholastic historian of philosophy whose authoritative study on the problem of matter in Greek philosophy is cited by Hoenen on Plato and Aristotle.",
        "works": ["Das Problem der Materie in der griechischen Philosophie (1890)"],
        "bib_anchor": "bib-baeumker-clemens",
    },
    "becker": {
        "name": "Oskar Becker",
        "dates": "1889 – 1964",
        "role": "Phenomenologist & Historian of Ancient Mathematics",
        "bio": "German philosopher and student of Husserl who wrote extensively on the phenomenological foundations of geometry and Eudoxian proportion theory.",
        "works": ["Beiträge zur phänomenologischen Begründung der Geometrie (1923)", "Eudoxos-Studien (1933–1936)"],
        "bib_anchor": "bib-becker-oskar",
    },
    "bekker": {
        "name": "Immanuel Bekker",
        "dates": "1785 – 1871",
        "role": "Classical Philologist",
        "bio": "Prussian philologist who edited the monumental Berlin Academy edition of Aristotle (1831), establishing the standard Bekker pagination.",
        "works": ["Aristotelis Opera (ed. Academia Regia Borussica, 1831)"],
        "bib_anchor": "bib-aristotle",
    },
    "beltrami": {
        "name": "Eugenio Beltrami",
        "dates": "1835 – 1900",
        "role": "Italian Mathematician",
        "bio": "Pioneer of differential geometry who constructed the first concrete Euclidean models (pseudosphere) proving the relative consistency of non-Euclidean geometry.",
        "works": ["Saggio di interpretazione della geometria non-euclidea (1868)"],
        "bib_anchor": "",
    },
    "berkeley": {
        "name": "George Berkeley",
        "dates": "1685 – 1753",
        "role": "Anglo-Irish Empiricist Philosopher",
        "bio": "Bishop of Cloyne whose critique of abstract ideas and theory of sensory minima (minimum visibile) prepared Hume's radical empiricism.",
        "works": ["A Treatise Concerning the Principles of Human Knowledge (1710)", "An Essay Towards a New Theory of Vision (1709)"],
        "bib_anchor": "",
    },
    "boethius": {
        "name": "Anicius Manlius Severinus Boethius",
        "dates": "c. 477 – 524 AD",
        "role": "Roman Christian Philosopher & Translator",
        "bio": "Late antique philosopher whose treatise De Trinitate occasioned Thomas Aquinas's celebrated commentary on the division and methods of the speculative sciences.",
        "works": ["De Trinitate", "De Institutione Arithmetica", "De Consolatione Philosophiae"],
        "bib_anchor": "bib-thomas-aquinas-st-o-p",
    },
    "bolyai": {
        "name": "János Bolyai",
        "dates": "1802 – 1860",
        "role": "Hungarian Mathematician",
        "bio": "Co-discoverer, independently of Lobachevsky and Gauss, of hyperbolic non-Euclidean geometry.",
        "works": ["Appendix scientiam spatii absolute veram exhibens (1832)"],
        "bib_anchor": "",
    },
    "bonitz": {
        "name": "Hermann Bonitz",
        "dates": "1814 – 1888",
        "role": "Classical Philologist & Aristotle Scholar",
        "bio": "German philologist and author of the indispensable Index Aristotelicus and commentary on Aristotle's Metaphysics.",
        "works": ["Aristotelis Metaphysica: Commentarius (1848–1849)", "Index Aristotelicus (1870)"],
        "bib_anchor": "bib-bonitz-hermann",
    },
    "borel": {
        "name": "Émile Borel",
        "dates": "1871 – 1956",
        "role": "French Mathematician",
        "bio": "Pioneer of measure theory and real analysis whose discussions on set theory and mathematical continuum are referenced in modern foundational debates.",
        "works": ["Leçons sur la théorie des fonctions (1898)"],
        "bib_anchor": "",
    },
    "boyer": {
        "name": "Charles Boyer, S.J.",
        "dates": "1884 – 1980",
        "role": "Jesuit Philosopher & Theologian",
        "bio": "Professor at the Pontifical Gregorian University in Rome and colleague of Hoenen, renowned for his studies on Augustine and St. Thomas's theory of knowledge.",
        "works": ["L'idée de vérité dans la philosophie de saint Augustin (1920)", "Cursus Philosophiae (1937)"],
        "bib_anchor": "",
    },
    "brouwer": {
        "name": "Luitzen Egbertus Jan Brouwer",
        "dates": "1881 – 1966",
        "role": "Dutch Mathematician & Founder of Intuitionism",
        "bio": "Topologist and philosopher of mathematics who founded mathematical intuitionism, grounding mathematics in the primordial intuition of time rather than formalist axioms.",
        "works": ["Over de grondslagen der wiskunde (1907)", "Intuitionisme en formalisme (1912)"],
        "bib_anchor": "bib-brouwer-luitzen-egbertus-jan",
    },
    "brunschvicg": {
        "name": "Léon Brunschvicg",
        "dates": "1869 – 1944",
        "role": "French Idealist Philosopher & Historian of Mathematics",
        "bio": "Co-founder of the Revue de Métaphysique et de Morale whose historical-critical study of mathematical philosophy is frequently examined by Hoenen.",
        "works": ["Les étapes de la philosophie mathématique (1912)"],
        "bib_anchor": "bib-brunschvicg-leon",
    },
    "burnet": {
        "name": "John Burnet",
        "dates": "1863 – 1928",
        "role": "Scottish Classical Scholar",
        "bio": "Professor of Greek at St Andrews whose editions of Plato and histories of early Greek philosophy shaped twentieth-century scholarship on Platonic hypotheses.",
        "works": ["Greek Philosophy: Thales to Plato (1914)", "Early Greek Philosophy (1892)"],
        "bib_anchor": "bib-burnet-john",
    },
    "cajetan": {
        "name": "Thomas de Vio Cajetan, Cardinal, O.P.",
        "dates": "1469 – 1534",
        "role": "Renaissance Thomistic Commentator",
        "bio": "Master General of the Dominicans and classic commentator on the Summa Theologiae, who systematized the distinction between abstractio formalis and abstractio totalis.",
        "works": ["In De Ente et Essentia Commentaria (1495)", "Commentaria in Summam Theologiae"],
        "bib_anchor": "bib-thomas-de-vio-cajetan-cardinal-o-p",
    },
    "cantor": {
        "name": "Georg Cantor",
        "dates": "1845 – 1918",
        "role": "German Mathematician & Creator of Set Theory",
        "bio": "Founder of transfinite set theory (Mengenlehre) and the arithmetic of the continuum, whose definitions of point-sets and continuity transformed modern analysis.",
        "works": ["Grundlagen einer allgemeinen Mannigfaltigkeitslehre (1883)", "Gesammelte Abhandlungen (1932)"],
        "bib_anchor": "bib-cantor-georg",
    },
    "carteron": {
        "name": "Henri Carteron",
        "dates": "1891 – 1927",
        "role": "French Historian of Ancient Philosophy",
        "bio": "Editor and translator of the Budé edition of Aristotle's Physics and author of a study on Aristotle's concept of force and motion.",
        "works": ["Aristote: Physique (ed. Budé, 1926)", "La notion de force dans le système d'Aristote (1923)"],
        "bib_anchor": "bib-carteron-henri",
    },
    "cayley": {
        "name": "Arthur Cayley",
        "dates": "1821 – 1895",
        "role": "British Mathematician",
        "bio": "Demonstrated that Euclidean and non-Euclidean metric geometries can be subordinated as special cases within projective geometry via the absolute conic.",
        "works": ["A Sixth Memoir upon Quantics (1859)"],
        "bib_anchor": "",
    },
    "christ": {
        "name": "Wilhelm von Christ",
        "dates": "1831 – 1906",
        "role": "German Classical Philologist",
        "bio": "Editor of the Teubner critical edition of Aristotle's Metaphysics.",
        "works": ["Aristotelis Metaphysica (ed. Teubner, 1886)"],
        "bib_anchor": "bib-christ-wilhelm-von",
    },
    "couturat": {
        "name": "Louis Couturat",
        "dates": "1868 – 1914",
        "role": "French Logician & Philosopher of Mathematics",
        "bio": "Champion of symbolic logic and Russellian logicism in France, editor of Leibniz's unpublished logical manuscripts, and critic of Kantian mathematical intuition.",
        "works": ["La philosophie des mathématiques de Kant (1904)", "Les Principes des Mathématiques (1905)", "La Logique de Leibniz (1901)"],
        "bib_anchor": "bib-couturat-louis",
    },
    "dedekind": {
        "name": "Richard Dedekind",
        "dates": "1831 – 1916",
        "role": "German Mathematician",
        "bio": "Formulated the rigorous arithmetic characterization of continuity and irrational numbers via Dedekind cuts (Schnitte).",
        "works": ["Stetigkeit und irrationale Zahlen (1872)", "Was sind und was sollen die Zahlen? (1888)"],
        "bib_anchor": "bib-dedekind-richard",
    },
    "democritus": {
        "name": "Democritus of Abdera",
        "dates": "c. 460 – c. 370 BC",
        "role": "Pre-Socratic Atomist Philosopher & Geometer",
        "bio": "Co-founder of ancient atomism whose views on indivisible magnitudes and sensory appearances were criticized by Plato and Aristotle.",
        "works": ["Fragments (Diels-Kranz)"],
        "bib_anchor": "",
    },
    "descartes": {
        "name": "René Descartes",
        "dates": "1596 – 1650",
        "role": "French Philosopher & Mathematician",
        "bio": "Founder of analytic geometry and modern rationalism; Hoenen critically examines both his coordinate reduction of extension and the intuitive nature of his Cogito ergo sum.",
        "works": ["La Géométrie (1637)", "Discours de la méthode (1637)", "Meditationes de prima philosophia (1641)", "Regulae ad directionem ingenii"],
        "bib_anchor": "bib-descartes-rene",
    },
    "diels": {
        "name": "Hermann Alexander Diels",
        "dates": "1848 – 1922",
        "role": "German Classical Philologist",
        "bio": "Chief editor of the Commentaria in Aristotelem Graeca (including Simplicius on the Physics) and Die Fragmente der Vorsokratiker.",
        "works": ["Simplicii in Aristotelis Physicorum Libros Quattuor Priores Commentaria (1882)", "Die Fragmente der Vorsokratiker (1903)"],
        "bib_anchor": "bib-simplicius-of-cilicia",
    },
    "duhem": {
        "name": "Pierre Duhem",
        "dates": "1861 – 1916",
        "role": "French Physicist, Philosopher & Historian of Science",
        "bio": "Pioneering historian of medieval science and philosopher of physical theory who contrasted abstract symbolic models with concrete qualitative perception.",
        "works": ["La théorie physique: son objet et sa structure (1906)", "Le Système du Monde (1913–1959)"],
        "bib_anchor": "",
    },
    "einstein": {
        "name": "Albert Einstein",
        "dates": "1879 – 1955",
        "role": "Theoretical Physicist",
        "bio": "Creator of special and general relativity; his 1921 lecture 'Geometrie und Erfahrung' famously distinguished purely axiomatic geometry from practical physical geometry.",
        "works": ["Geometrie und Erfahrung (1921)", "Die Grundlage der allgemeinen Relativitätstheorie (1916)"],
        "bib_anchor": "bib-einstein-albert",
    },
    "enriques": {
        "name": "Federigo Enriques",
        "dates": "1871 – 1946",
        "role": "Italian Geometer & Philosopher of Science",
        "bio": "Leader of the Italian school of algebraic geometry and editor of Questioni riguardanti le matematiche elementari, who analyzed the psychological and sensory origins of geometric concepts.",
        "works": ["Questioni riguardanti le matematiche elementari (1912 / 1924)", "Problemi della scienza (1906)"],
        "bib_anchor": "bib-enriques-federigo",
    },
    "euclid": {
        "name": "Euclid of Alexandria",
        "dates": "fl. c. 300 BC",
        "role": "Ancient Greek Geometer",
        "bio": "Author of the Elements, whose tripartite division of first principles into Definitions (ὅροι), Postulates (αἰτήματα), and Common Notions (κοιναὶ ἔννοιαι) embodies the Aristotelian demonstrative ideal.",
        "works": ["Elementa (The Thirteen Books of the Elements)"],
        "bib_anchor": "bib-euclid-of-alexandria",
    },
    "eudoxus": {
        "name": "Eudoxus of Cnidus",
        "dates": "c. 408 – c. 355 BC",
        "role": "Ancient Greek Mathematician & Astronomer",
        "bio": "Member of Plato's Academy who created the general theory of proportions (Elements Book V) and the method of exhaustion (Book XII) to resolve the crisis of incommensurables.",
        "works": ["Theory of Proportions (preserved in Euclid, Elements V)"],
        "bib_anchor": "",
    },
    "euler": {
        "name": "Leonhard Euler",
        "dates": "1707 – 1783",
        "role": "Swiss Mathematician & Physicist",
        "bio": "Pioneered analysis, mechanics, and topology (analysis situs), including the polyhedral formula and early topological problems.",
        "works": ["Introductio in analysin infinitorum (1748)"],
        "bib_anchor": "",
    },
    "fraenkel": {
        "name": "Abraham Adolf Fraenkel",
        "dates": "1891 – 1965",
        "role": "German-Israeli Mathematician & Set Theorist",
        "bio": "Co-developer of Zermelo-Fraenkel set theory (ZFC) and author of standard treatises on the foundations of set theory.",
        "works": ["Einleitung in die Mengenlehre (1919)"],
        "bib_anchor": "",
    },
    "frege": {
        "name": "Gottlob Frege",
        "dates": "1848 – 1925",
        "role": "German Mathematician, Logician & Philosopher",
        "bio": "Founder of modern predicate logic and logicism in arithmetic, who defended the objective truth and intuitive geometric grounding of Euclidean axioms in his correspondence with Hilbert.",
        "works": ["Die Grundlagen der Arithmetik (1884)", "Über die Grundlagen der Geometrie (1903–1906)"],
        "bib_anchor": "",
    },
    "freudenthal": {
        "name": "Hans Freudenthal",
        "dates": "1905 – 1990",
        "role": "German-Dutch Mathematician",
        "bio": "Topologist and historian of mathematics who engaged directly with Hoenen in Gregorianum on the roles of intuition and abstraction in the foundations of geometry.",
        "works": ["De fontibus geometriae in intuitione et abstractione quaerendis (Gregorianum, 1951)"],
        "bib_anchor": "bib-freudenthal-hans",
    },
    "friedlein": {
        "name": "Gottfried Friedlein",
        "dates": "1828 – 1875",
        "role": "German Historian of Mathematics & Philologist",
        "bio": "Editor of the standard Teubner critical text of Proclus's Commentary on Book I of Euclid's Elements (1873).",
        "works": ["Procli Diadochi in Primum Euclidis Elementorum Librum Commentarii (1873)"],
        "bib_anchor": "bib-proclus-lycius-diadochus",
    },
    "galileo": {
        "name": "Galileo Galilei",
        "dates": "1564 – 1642",
        "role": "Italian Natural Philosopher, Astronomer & Mathematician",
        "bio": "Pioneer of mathematical physics and kinematics whose distinction between primary quantitative properties and secondary sensible qualities shaped modern science.",
        "works": ["Il Saggiatore (1623)", "Discorsi e dimostrazioni matematiche intorno a due nuove scienze (1638)"],
        "bib_anchor": "",
    },
    "gauss": {
        "name": "Carl Friedrich Gauss",
        "dates": "1777 – 1855",
        "role": "German Mathematician & Physicist (Princeps Mathematicorum)",
        "bio": "Developed the intrinsic differential geometry of curved surfaces and privately discovered non-Euclidean geometry, questioning the a priori necessity of Euclidean space.",
        "works": ["Disquisitiones generales circa superficies curvas (1827)", "Werke"],
        "bib_anchor": "bib-gauss-carl-friedrich",
    },
    "geyser": {
        "name": "Joseph Geyser",
        "dates": "1869 – 1948",
        "role": "German Neo-Scholastic Philosopher",
        "bio": "Professor of philosophy at Münster, Freiburg, and Munich, known for his studies on Aristotelian epistemology and critical realism.",
        "works": ["Die Erkenntnistheorie des Aristoteles (1917)", "Grundlegung der Logik und Erkenntnistheorie (1919)"],
        "bib_anchor": "bib-geyser-joseph",
    },
    "gilson": {
        "name": "Étienne Gilson",
        "dates": "1884 – 1978",
        "role": "French Thomistic Philosopher & Historian of Medieval Philosophy",
        "bio": "Leading twentieth-century historian of medieval philosophy and proponent of existential Thomism, whose works on being, essence, and existential judgment Hoenen discusses in the Appendix.",
        "works": ["L'être et l'essence (1948)", "Being and Some Philosophers (1949)", "Le Thomisme"],
        "bib_anchor": "bib-gilson-etienne",
    },
    "gonseth": {
        "name": "Ferdinand Gonseth",
        "dates": "1890 – 1975",
        "role": "Swiss Mathematician & Philosopher of Science",
        "bio": "Professor at ETH Zürich who characterized mathematical objects as idealized 'schematic physics' (physique de l'objet quelconque) abstracted from experimental reality.",
        "works": ["Les fondements des mathématiques (1926)", "Les mathématiques et la réalité (1936)"],
        "bib_anchor": "bib-gonseth-ferdinand",
    },
    "gredt": {
        "name": "Joseph Gredt, O.S.B.",
        "dates": "1863 – 1940",
        "role": "Benedictine Thomistic Philosopher",
        "bio": "Professor at the Pontifical Athenaeum of Sant'Anselmo in Rome and author of a widely used manual of Aristotelian-Thomistic philosophy.",
        "works": ["Elementa Philosophiae Aristotelico-Thomisticae (7th ed., 1937)"],
        "bib_anchor": "bib-gredt-joseph-o-s-b",
    },
    "hadamard": {
        "name": "Jacques Hadamard",
        "dates": "1865 – 1963",
        "role": "French Mathematician",
        "bio": "Leading French analyst and geometer who investigated the psychology of mathematical invention and directed the mathematical volume of the Encyclopédie Française.",
        "works": ["Leçons de géométrie élémentaire (1898)", "Encyclopédie Française, Tome I: L'Outillage Mental (1937)"],
        "bib_anchor": "bib-hadamard-jacques",
    },
    "hamelin": {
        "name": "Octave Hamelin",
        "dates": "1856 – 1907",
        "role": "French Philosopher & Aristotle Scholar",
        "bio": "French idealist philosopher and historian of ancient philosophy whose posthumous lectures on the system of Aristotle are cited by Hoenen.",
        "works": ["Le Système d'Aristote (1920)"],
        "bib_anchor": "bib-hamelin-octave",
    },
    "hardy": {
        "name": "Godfrey Harold Hardy",
        "dates": "1877 – 1947",
        "role": "British Mathematician",
        "bio": "Leading Cambridge analyst and number theorist whose 1929 essay 'Mathematical Proof' defended genuine intellectual insight against purely formalist symbol-games.",
        "works": ["Mathematical Proof (Mind, 1929)", "A Course of Pure Mathematics (1908)"],
        "bib_anchor": "bib-hardy-godfrey-harold",
    },
    "hasse": {
        "name": "Helmut Hasse",
        "dates": "1898 – 1979",
        "role": "German Mathematician",
        "bio": "Algebraist and number theorist who co-authored with Heinrich Scholz a celebrated treatise on the foundational crisis of Greek mathematics triggered by incommensurability.",
        "works": ["Die Grundlagenkrisis der griechischen Mathematik (with H. Scholz, 1928)"],
        "bib_anchor": "bib-hasse-helmut",
    },
    "hausdorff": {
        "name": "Felix Hausdorff",
        "dates": "1868 – 1942",
        "role": "German Mathematician & Founder of General Topology",
        "bio": "Creator of the theory of topological and metric spaces (Hausdorff spaces) and author of philosophical essays on the problem of physical and geometric space.",
        "works": ["Das Raumproblem (Annalen der Naturphilosophie, 1904)", "Grundzüge der Mengenlehre (1914)"],
        "bib_anchor": "bib-hausdorff-felix",
    },
    "heath": {
        "name": "Sir Thomas Little Heath",
        "dates": "1861 – 1940",
        "role": "British Historian of Ancient Greek Mathematics",
        "bio": "Foremost English translator and commentator of Euclid, Archimedes, and Apollonius, whose monumental commentary on Euclid's Elements is a primary source for Hoenen.",
        "works": ["The Thirteen Books of Euclid's Elements (1908; 2nd ed. 1926)", "A History of Greek Mathematics (1921)", "Mathematics in Aristotle (1949)"],
        "bib_anchor": "bib-heath-sir-thomas-little",
    },
    "hegel": {
        "name": "Georg Wilhelm Friedrich Hegel",
        "dates": "1770 – 1831",
        "role": "German Idealist Philosopher",
        "bio": "Architect of absolute idealism whose remarks on Euclid's definitions and postulates in the Wissenschaft der Logik are examined by Hoenen.",
        "works": ["Wissenschaft der Logik (1812–1816)"],
        "bib_anchor": "bib-hegel-georg-wilhelm-friedrich",
    },
    "heiberg": {
        "name": "Johan Ludvig Heiberg",
        "dates": "1854 – 1928",
        "role": "Danish Classical Philologist & Historian of Mathematics",
        "bio": "Editor of the definitive critical Greek editions of Euclid's Elements, Archimedes, Apollonius, and Ptolemy.",
        "works": ["Euclidis Elementa (ed. Teubner, 1883–1888)"],
        "bib_anchor": "bib-euclid-of-alexandria",
    },
    "helmholtz": {
        "name": "Hermann von Helmholtz",
        "dates": "1821 – 1894",
        "role": "German Physicist, Physiologist & Philosopher of Science",
        "bio": "Investigated the physiological optics of spatial perception and characterized physical geometry through the free mobility of rigid bodies (Riemann-Helmholtz space problem).",
        "works": ["Über die Tatsachen, die der Geometrie zum Grunde liegen (1868)", "Über den Ursprung und die Bedeutung der geometrischen Axiome (1870)", "Schriften zur Erkenntnistheorie (1921)"],
        "bib_anchor": "bib-helmholtz-hermann-von",
    },
    "heraclitus": {
        "name": "Heraclitus of Ephesus",
        "dates": "c. 535 – c. 475 BC",
        "role": "Pre-Socratic Philosopher",
        "bio": "Philosopher of universal flux (πάντα ῥεῖ), whose denial of stable sensible being prompted Plato's separation of eternal Ideas from sensible phenomena.",
        "works": ["Fragments (Diels-Kranz)"],
        "bib_anchor": "",
    },
    "heron": {
        "name": "Hero of Alexandria",
        "dates": "c. 10 – c. 70 AD",
        "role": "Graeco-Roman Mathematician & Engineer",
        "bio": "Geometer and author of commentaries and definitions on Euclidean geometry preserved in Proclus and Arabic translations.",
        "works": ["Definitiones", "Metrica"],
        "bib_anchor": "",
    },
    "hertz": {
        "name": "Paul Hertz",
        "dates": "1881 – 1940",
        "role": "German Physicist & Philosopher of Science",
        "bio": "Co-edited Helmholtz's epistemological writings with Moritz Schlick, contributing detailed critical annotations on geometry and perception.",
        "works": ["Hermann v. Helmholtz: Schriften zur Erkenntnistheorie (ed. with M. Schlick, 1921)"],
        "bib_anchor": "bib-helmholtz-hermann-von",
    },
    "hessenberg": {
        "name": "Gerhard Hessenberg",
        "dates": "1874 – 1925",
        "role": "German Mathematician & Neo-Friesian Philosopher",
        "bio": "Geometer and foundational theorist known for his work on projective geometry (Desargues's and Pascal's theorems) and philosophical critique of mathematical axiomatics.",
        "works": ["Kritik und System in Mathematik und Philosophie (1908)", "Grundlagen der Geometrie (1930)"],
        "bib_anchor": "bib-hessenberg-gerhard",
    },
    "hilbert": {
        "name": "David Hilbert",
        "dates": "1862 – 1943",
        "role": "German Mathematician & Leader of Formalism",
        "bio": "Author of Grundlagen der Geometrie (1899), which replaced intuitive definitions with implicit axiomatic characterization of incidence, order, congruence, parallels, and continuity.",
        "works": ["Grundlagen der Geometrie (1899; 7th ed. 1930)", "Grundzüge der theoretischen Logik (1928)"],
        "bib_anchor": "bib-hilbert-david",
    },
    "hippocrates": {
        "name": "Hippocrates of Chios",
        "dates": "c. 470 – c. 410 BC",
        "role": "Ancient Greek Geometer",
        "bio": "Composed the earliest known Elements of Geometry and squared the lune, pioneering the method of geometric reduction (ἀπαγωγή).",
        "works": ["Elementa (lost; reported by Proclus and Simplicius)"],
        "bib_anchor": "",
    },
    "hoelder": {
        "name": "Otto Hölder",
        "dates": "1859 – 1937",
        "role": "German Mathematician",
        "bio": "Group theorist and analyst who authored a major philosophical treatise on the mathematical method, axiomatic deduction, and genetic construction.",
        "works": ["Die mathematische Methode (1924)", "Anschauung und Denken in der Geometrie (1900)"],
        "bib_anchor": "bib-holder-otto",
    },
    "hoenen": {
        "name": "Petrus Hubertus Jacobus Hoenen, S.J.",
        "dates": "1880 – 1961",
        "role": "Jesuit Philosopher of Science & Mathematics",
        "bio": "Professor of Cosmology and Philosophy of Mathematics at the Pontifical Gregorian University in Rome; author of De Noetica Geometriae and La théorie du jugement d'après St. Thomas d'Aquin.",
        "works": [
            "De Noetica Geometriae: Origine Theoriae Cognitionis (1954)",
            "La théorie du jugement d'après St. Thomas d'Aquin (1946; 2nd ed. 1953)",
            "Reality and Judgment According to St. Thomas (1952)",
            "Cosmologia (4th ed. 1949)",
            "Filosofia della natura inorganica (1949)",
        ],
        "bib_anchor": "bib-hoenen-petrus-hubertus-jacobus-s-j",
    },
    "hume": {
        "name": "David Hume",
        "dates": "1711 – 1776",
        "role": "Scottish Empiricist Philosopher",
        "bio": "Radical empiricist who attacked the exactness of Euclidean geometry in the Treatise by reducing space to discrete sensory minima (minimum visibile) incapable of infinite divisibility.",
        "works": ["A Treatise of Human Nature (1739–1740)", "An Enquiry Concerning Human Understanding (1748)"],
        "bib_anchor": "bib-hume-david",
    },
    "husserl": {
        "name": "Edmund Husserl",
        "dates": "1859 – 1938",
        "role": "German Philosopher & Founder of Phenomenology",
        "bio": "Trained as a mathematician under Weierstrass; founded phenomenology and developed the theory of eidetic intuition (Wesensschau) and exact vs. morphological essences.",
        "works": ["Philosophie der Arithmetik (1891)", "Logische Untersuchungen (1900–1901)", "Ideen I (1913)"],
        "bib_anchor": "",
    },
    "johannes-a-sancto-thoma": {
        "name": "John of St. Thomas (João Poinsot, O.P.)",
        "dates": "1589 – 1644",
        "role": "Baroque Thomistic Logician & Philosopher",
        "bio": "Dominican professor at Alcalá whose Cursus Philosophicus Thomisticus (Ars Logica) provided the classic late-scholastic synthesis of formal logic, abstraction, and the degrees of science.",
        "works": ["Cursus Philosophicus Thomisticus: Ars Logica (1631–1632)"],
        "bib_anchor": "",
    },
    "jordan": {
        "name": "Camille Jordan",
        "dates": "1838 – 1922",
        "role": "French Mathematician",
        "bio": "Group theorist and analyst who formulated the rigorous definition of a continuous curve (Jordan curve) and proved the Jordan Curve Theorem separating a plane into interior and exterior regions.",
        "works": ["Cours d'analyse de l'École Polytechnique (1882–1887)"],
        "bib_anchor": "",
    },
    "kant": {
        "name": "Immanuel Kant",
        "dates": "1724 – 1804",
        "role": "German Critical Philosopher",
        "bio": "Characterized geometric propositions as synthetic a priori judgments grounded in pure intuition of space as an a priori form of sensibility—a doctrine Hoenen contrasts with Aristotelian abstraction from sensible phantasms.",
        "works": ["Kritik der reinen Vernunft (1781 / 1787)", "Prolegomena zu einer jeden künftigen Metaphysik (1783)"],
        "bib_anchor": "bib-kant-immanuel",
    },
    "killing": {
        "name": "Wilhelm Killing",
        "dates": "1847 – 1923",
        "role": "German Mathematician",
        "bio": "Co-discoverer of Lie algebras (Killing form) and professor at Münster who wrote a comprehensive two-volume treatise on the foundations of Euclidean and non-Euclidean geometry.",
        "works": ["Einführung in die Grundlagen der Geometrie (1893–1898)"],
        "bib_anchor": "bib-killing-wilhelm",
    },
    "klein": {
        "name": "Felix Klein",
        "dates": "1849 – 1925",
        "role": "German Mathematician",
        "bio": "Author of the Erlangen Program classifying geometries by transformation groups, and originator of the philosophical distinction between Approximationsmathematik (empirical perception bounded by a threshold) and Präzisionsmathematik (idealized limits).",
        "works": [
            "Vergleichende Betrachtungen über neuere geometrische Forschungen (Erlanger Programm, 1872)",
            "Anwendung der Differential- und Integralrechnung auf Geometrie: Eine Revision der Prinzipien (1902; 2nd ed. 1907)",
            "Elementarmathematik vom höheren Standpunkte aus (3rd ed. 1925)",
        ],
        "bib_anchor": "bib-klein-felix",
    },
    "kronecker": {
        "name": "Leopold Kronecker",
        "dates": "1823 – 1891",
        "role": "German Mathematician",
        "bio": "Number theorist and algebraist who advocated strict arithmetization and constructivism based on the natural numbers.",
        "works": ["Über den Zahlbegriff (1887)"],
        "bib_anchor": "",
    },
    "lambert": {
        "name": "Johann Heinrich Lambert",
        "dates": "1728 – 1777",
        "role": "Swiss Polymath, Mathematician & Philosopher",
        "bio": "Proved the irrationality of π and investigated the parallel postulate via the 'Lambert quadrilateral', anticipating non-Euclidean geometry.",
        "works": ["Die Theorie der Parallellinien (1766 / 1786)"],
        "bib_anchor": "",
    },
    "leibniz": {
        "name": "Gottfried Wilhelm Leibniz",
        "dates": "1646 – 1716",
        "role": "German Polymath, Philosopher & Mathematician",
        "bio": "Co-inventor of the infinitesimal calculus and pioneer of symbolic logic (characteristica universalis) and analysis situs, who sought to reduce all mathematical truths to identities demonstrable via definitions.",
        "works": ["Nouveaux Essais sur l'entendement humain (1704)", "Mathematische Schriften (ed. Gerhardt)"],
        "bib_anchor": "bib-leibniz-gottfried-wilhelm",
    },
    "lobachevsky": {
        "name": "Nikolai Ivanovich Lobachevsky",
        "dates": "1792 – 1856",
        "role": "Russian Mathematician",
        "bio": "Published the first systematic development of hyperbolic non-Euclidean ('imaginary') geometry by replacing Euclid's Fifth Postulate.",
        "works": ["Geometrische Untersuchungen zur Theorie der Parallellinien (1840)"],
        "bib_anchor": "",
    },
    "locke": {
        "name": "John Locke",
        "dates": "1632 – 1704",
        "role": "English Empiricist Philosopher",
        "bio": "Author of An Essay Concerning Human Understanding, whose conceptualist account of abstract general ideas was critiqued by Berkeley, Hume, and Leibniz.",
        "works": ["An Essay Concerning Human Understanding (1690)"],
        "bib_anchor": "bib-locke-john",
    },
    "lonergan": {
        "name": "Bernard Lonergan, S.J.",
        "dates": "1904 – 1984",
        "role": "Jesuit Philosopher & Theologian",
        "bio": "Studied under Hoenen at the Gregorian University; his Verbum articles (1946–1949) and Insight (1957) developed Hoenen's discovery of Aquinas's doctrine of intellectual insight into phantasms.",
        "works": ["The Concept of Verbum in the Writings of St. Thomas Aquinas (1946–1949)", "Insight: A Study of Human Understanding (1957)"],
        "bib_anchor": "bib-lonergan-bernard-s-j",
    },
    "mach": {
        "name": "Ernst Mach",
        "dates": "1838 – 1916",
        "role": "Austrian Physicist & Empiricist Philosopher of Science",
        "bio": "Phenomenalist philosopher who traced geometric concepts to empirical experiences of physiological space in comparison with tactile and visual space.",
        "works": ["Erkenntnis und Irrtum (1905)", "Die Mechanik in ihrer Entwicklung (1883)"],
        "bib_anchor": "",
    },
    "maier": {
        "name": "Anneliese Maier",
        "dates": "1905 – 1971",
        "role": "German Historian of Late Medieval Science & Philosophy",
        "bio": "Archival scholar at the Vatican Library whose groundbreaking studies illuminated fourteenth-century Scholastic natural philosophy and mathematics.",
        "works": ["An der Grenze von Scholastik und Naturwissenschaft (1943)", "Die Vorläufer Galileis im 14. Jahrhundert (1949)"],
        "bib_anchor": "bib-maier-anneliese",
    },
    "maritain": {
        "name": "Jacques Maritain",
        "dates": "1882 – 1973",
        "role": "French Thomistic Philosopher",
        "bio": "Prominent Neo-Thomist whose analysis of the three degrees of abstraction and the epistemology of mathematics and physico-mathematical science is engaged by Hoenen.",
        "works": ["Distinguish to Unite, or The Degrees of Knowledge (Les degrés du savoir, 1932)", "Sept leçons sur l'être (1934)"],
        "bib_anchor": "bib-maritain-jacques",
    },
    "mercier": {
        "name": "Désiré-Joseph Cardinal Mercier",
        "dates": "1851 – 1926",
        "role": "Belgian Neo-Scholastic Philosopher & Founder of the Louvain Institute",
        "bio": "Founder of the Higher Institute of Philosophy at Louvain; Hoenen critiques Mercier's purely conceptualist ('analytic') interpretation of necessary judgments.",
        "works": ["Critériologie générale (8th ed., 1923)", "Logique"],
        "bib_anchor": "bib-mercier-desire-joseph-cardinal",
    },
    "meyerson": {
        "name": "Émile Meyerson",
        "dates": "1859 – 1933",
        "role": "Polish-born French Philosopher of Science & Epistemologist",
        "bio": "Analyzed the actual progression of scientific and mathematical thought (le cheminement de la pensée) as a tension between rational identification and the resistance of the real.",
        "works": ["Du cheminement de la pensée (1931)", "Identité et réalité (1908)"],
        "bib_anchor": "bib-meyerson-emile",
    },
    "mill": {
        "name": "John Stuart Mill",
        "dates": "1806 – 1873",
        "role": "British Empiricist Philosopher",
        "bio": "Argued in A System of Logic that geometric definitions describe non-existent idealizations and that axioms are merely inductive generalizations from sensory experience.",
        "works": ["A System of Logic, Ratiocinative and Inductive (1843; 5th ed. 1862)"],
        "bib_anchor": "bib-mill-john-stuart",
    },
    "moebius": {
        "name": "August Ferdinand Möbius",
        "dates": "1790 – 1868",
        "role": "German Mathematician & Astronomer",
        "bio": "Pioneer of projective geometry and topology; discovered the non-orientable one-sided surface (folium Moebii / Möbius strip), which Hoenen analyzes in detail in Caput III.",
        "works": ["Der barycentrische Calcul (1827)", "Über die Bestimmung des Inhaltes eines Polyëders (1865)"],
        "bib_anchor": "",
    },
    "newton": {
        "name": "Sir Isaac Newton",
        "dates": "1642 – 1727",
        "role": "English Mathematician & Natural Philosopher",
        "bio": "Author of the Principia Mathematica and co-founder of the calculus (method of fluxions); defended absolute space and time and the kinematic generation of geometric magnitudes.",
        "works": ["Philosophiae Naturalis Principia Mathematica (1687)", "Tractatus de Quadratura Curvarum (1704)"],
        "bib_anchor": "bib-newton-sir-isaac",
    },
    "nicomachus": {
        "name": "Nicomachus of Gerasa",
        "dates": "c. 60 – c. 120 AD",
        "role": "Neopythagorean Mathematician",
        "bio": "Author of the Introductio Arithmetica, which transmitted Neopythagorean number theory to Boethius and the Latin Middle Ages.",
        "works": ["Introductio Arithmetica"],
        "bib_anchor": "",
    },
    "parmenides": {
        "name": "Parmenides of Elea",
        "dates": "fl. early 5th century BC",
        "role": "Pre-Socratic Eleatic Philosopher",
        "bio": "Founder of the Eleatic school who affirmed the unity and immutability of Being and denied the reality of motion and division.",
        "works": ["On Nature (Fragments)"],
        "bib_anchor": "",
    },
    "pascal": {
        "name": "Blaise Pascal",
        "dates": "1623 – 1662",
        "role": "French Mathematician, Physicist & Philosopher",
        "bio": "Proved Pascal's Theorem in projective geometry and authored De l'Esprit géométrique, distinguishing primitive undefined terms and self-evident axioms grasped by the 'cœur' from demonstrated propositions.",
        "works": ["De l'Esprit géométrique (c. 1657)", "Essai pour les coniques (1640)", "Pensées"],
        "bib_anchor": "",
    },
    "pasch": {
        "name": "Moritz Pasch",
        "dates": "1843 – 1930",
        "role": "German Mathematician",
        "bio": "Pioneered the rigorous axiomatization of projective and order geometry (Pasch's Axiom), insisting that geometric deduction must proceed independently of intuitive diagrams once nuclear axioms (Kern-Sätze) are abstracted from experience.",
        "works": ["Vorlesungen über neuere Geometrie (1882; 2nd ed. 1926)", "Mathematik und Logik (1919)"],
        "bib_anchor": "bib-pasch-moritz",
    },
    "peano": {
        "name": "Giuseppe Peano",
        "dates": "1858 – 1932",
        "role": "Italian Mathematician & Logician",
        "bio": "Formulated the Peano axioms for arithmetic, symbolic mathematical logic, and the space-filling Peano curve (1890) challenging naive intuitions of dimension.",
        "works": ["Arithmetices principia, nova methodo exposita (1889)", "I principii di geometria logicamente esposti (1889)", "Sur une courbe, qui remplit toute une aire plane (1890)"],
        "bib_anchor": "",
    },
    "philoponus": {
        "name": "John Philoponus",
        "dates": "c. 490 – c. 570 AD",
        "role": "Alexandrian Christian Philosopher & Aristotelian Commentator",
        "bio": "Late antique commentator on Aristotle's Physics and Posterior Analytics who developed the theory of three-dimensional spatial extension (διάστημα) and impetus.",
        "works": ["In Aristotelis Physicorum Libros Commentaria", "In Aristotelis Analytica Posteriora Commentaria"],
        "bib_anchor": "bib-john-philoponus",
    },
    "plato": {
        "name": "Plato",
        "dates": "428/427 – 348/347 BC",
        "role": "Ancient Greek Philosopher",
        "bio": "Founder of the Athenian Academy; his Divided Line (Republic VI) assigned mathematical objects to discursive understanding (διάνοια) proceeding from hypotheses with the aid of visible diagrams.",
        "works": ["Respublica", "Meno", "Phaedo", "Theaetetus", "Timaeus", "Leges"],
        "bib_anchor": "bib-plato",
    },
    "poincare": {
        "name": "Henri Poincaré",
        "dates": "1854 – 1912",
        "role": "French Mathematician, Physicist & Philosopher of Science",
        "bio": "Universal mathematician and creator of algebraic topology (analysis situs) who argued that geometric axioms are neither synthetic a priori judgments nor experimental facts, but conventions (disguised definitions) guided by experience.",
        "works": ["La Science et l'Hypothèse (1902)", "La Valeur de la Science (1905)", "Science et Méthode (1908)", "Dernières Pensées (1913)"],
        "bib_anchor": "bib-poincare-henri",
    },
    "poncelet": {
        "name": "Jean-Victor Poncelet",
        "dates": "1788 – 1867",
        "role": "French Mathematician & Engineer",
        "bio": "Revived synthetic projective geometry through the principle of continuity and the theory of poles, polars, and points at infinity.",
        "works": ["Traité des propriétés projectives des figures (1822)"],
        "bib_anchor": "",
    },
    "proclus": {
        "name": "Proclus Lycius Diadochus",
        "dates": "412 – 485 AD",
        "role": "Neoplatonic Philosopher & Commentator on Euclid",
        "bio": "Head of the Athenian Neoplatonic Academy whose Commentary on Book I of Euclid's Elements is the primary ancient source on the history and philosophy of Greek geometry and imagination (φαντασία) as passive intellect.",
        "works": ["In Primum Euclidis Elementorum Librum Commentarii"],
        "bib_anchor": "bib-proclus-lycius-diadochus",
    },
    "protagoras": {
        "name": "Protagoras of Abdera",
        "dates": "c. 490 – c. 420 BC",
        "role": "Greek Sophist",
        "bio": "Sophist who argued against geometers that sensible circles and rulers touch at more than a single indivisible point (reported by Aristotle, Metaphysics III 2, 997b35).",
        "works": ["Fragments (Diels-Kranz)"],
        "bib_anchor": "",
    },
    "ptolemy": {
        "name": "Claudius Ptolemy",
        "dates": "c. 100 – c. 170 AD",
        "role": "Graeco-Roman Astronomer, Mathematician & Geographer",
        "bio": "Author of the Almagest and a lost treatise on the three-dimensionality of space and the proof of Euclid's Fifth Postulate (preserved by Proclus and Simplicius).",
        "works": ["Syntaxis Mathematica (Almagest)", "On Distance / Dimension"],
        "bib_anchor": "",
    },
    "pythagoras": {
        "name": "Pythagoras of Samos",
        "dates": "c. 570 – c. 495 BC",
        "role": "Ancient Greek Philosopher & Geometer",
        "bio": "Founder of the Pythagorean brotherhood, which discovered the mathematical ratios of musical harmony, the Pythagorean theorem, and the incommensurability of the diagonal with the side.",
        "works": ["Pythagorean Tradition"],
        "bib_anchor": "",
    },
    "reichenbach": {
        "name": "Hans Reichenbach",
        "dates": "1891 – 1953",
        "role": "German Philosopher of Science & Logical Empiricist",
        "bio": "Founder of the Berlin Circle who analyzed relativistic spacetime geometry via 'coordinative definitions' (Zuordnungsdefinitionen) and critiqued geometric visualization.",
        "works": ["Philosophie der Raum-Zeit-Lehre (1928)"],
        "bib_anchor": "bib-reichenbach-hans",
    },
    "riehl": {
        "name": "Alois Riehl",
        "dates": "1844 – 1924",
        "role": "Austrian-German Neo-Kantian Philosopher",
        "bio": "Representative of critical realism within Neo-Kantianism whose essays on logic and epistemology are cited by Hoenen.",
        "works": ["Der philosophische Kritizismus (1876–1887)", "Logik und Erkenntnistheorie (1921)"],
        "bib_anchor": "bib-riehl-alois",
    },
    "riemann": {
        "name": "Bernhard Riemann",
        "dates": "1826 – 1866",
        "role": "German Mathematician",
        "bio": "Revolutionized differential geometry in his 1854 Habilitationsschrift by introducing n-dimensional Riemannian manifolds with arbitrary curvature metrics.",
        "works": ["Über die Hypothesen, welche der Geometrie zu Grunde liegen (1854 / 1867)"],
        "bib_anchor": "",
    },
    "ross": {
        "name": "Sir William David Ross",
        "dates": "1877 – 1971",
        "role": "Scottish Philosopher & Aristotle Scholar",
        "bio": "Provost of Oriel College, Oxford, and general editor of the Oxford Translation of Aristotle; his critical editions and commentaries on Aristotle's Metaphysics, Physics, and Analytics are frequently cited by Hoenen.",
        "works": ["Aristotle's Metaphysics (1924)", "Aristotle's Physics (1936)", "Aristotle's Prior and Posterior Analytics (1949)"],
        "bib_anchor": "bib-ross-sir-william-david",
    },
    "russell": {
        "name": "Bertrand Russell",
        "dates": "1872 – 1970",
        "role": "British Philosopher, Logician & Mathematician",
        "bio": "Co-author of Principia Mathematica and leading proponent of logicism, who defined pure mathematics as the class of all formal implications 'p implies q' containing only logical constants and variables.",
        "works": ["An Essay on the Foundations of Geometry (1897)", "The Principles of Mathematics (1903)", "Principia Mathematica (with A. N. Whitehead, 1910–1913)"],
        "bib_anchor": "bib-russell-bertrand",
    },
    "saccheri": {
        "name": "Girolamo Saccheri, S.J.",
        "dates": "1667 – 1733",
        "role": "Italian Jesuit Mathematician & Logician",
        "bio": "Professor at Pavia who investigated the consequences of denying Euclid's Fifth Postulate via the acute and obtuse angle hypotheses, unwittingly discovering many theorems of non-Euclidean geometry.",
        "works": ["Euclides ab omni naevo vindicatus (1733)", "Logica demonstrativa (1697)"],
        "bib_anchor": "",
    },
    "schlick": {
        "name": "Moritz Schlick",
        "dates": "1882 – 1936",
        "role": "German Philosopher & Founder of the Vienna Circle",
        "bio": "Leader of logical positivism who popularized Hilbert's concept of 'implicit definitions' in general epistemology and co-edited Helmholtz's epistemological writings.",
        "works": ["Allgemeine Erkenntnislehre (1918)", "Hermann v. Helmholtz: Schriften zur Erkenntnistheorie (ed. with P. Hertz, 1921)"],
        "bib_anchor": "bib-helmholtz-hermann-von",
    },
    "scholz": {
        "name": "Heinrich Scholz",
        "dates": "1884 – 1956",
        "role": "German Logician, Philosopher & Historian of Mathematics",
        "bio": "Founder of the Münster school of mathematical logic; co-authored with Helmut Hasse the study on the foundational crisis of Greek mathematics.",
        "works": ["Die Grundlagenkrisis der griechischen Mathematik (with H. Hasse, 1928)", "Warum haben die Griechen die Irrationalzahlen nicht aufgebaut? (1928)", "Geschichte der Logik (1931)"],
        "bib_anchor": "bib-scholz-heinrich",
    },
    "scotus": {
        "name": "John Duns Scotus, Bl., O.F.M.",
        "dates": "c. 1265 – 1308",
        "role": "Franciscan Scholastic Philosopher & Theologian (Doctor Subtilis)",
        "bio": "Major Scholastic thinker whose doctrines on intuitive cognition, formal distinction, and the univocity of being contrasted with the Thomistic school.",
        "works": ["Ordinatio (Opus Oxoniense)", "Quaestiones super Libros Metaphysicorum Aristotelis"],
        "bib_anchor": "",
    },
    "simplicius": {
        "name": "Simplicius of Cilicia",
        "dates": "c. 490 – c. 560 AD",
        "role": "Neoplatonic Commentator on Aristotle",
        "bio": "Student of Ammonius and Damascius whose encyclopedic commentaries on Aristotle's Physics and De Caelo preserve crucial fragments of Eudemus, Hippocrates of Chios, and ancient geometry.",
        "works": ["In Aristotelis Physicorum Libros Commentaria", "In Aristotelis De Caelo Commentaria"],
        "bib_anchor": "bib-simplicius-of-cilicia",
    },
    "socrates": {
        "name": "Socrates",
        "dates": "c. 470 – 399 BC",
        "role": "Athenian Philosopher",
        "bio": "Teacher of Plato who initiated the philosophical search for universal definitions (τί ἐστιν) and guided the slave boy's geometric discovery in Plato's Meno.",
        "works": ["Platonic Dialogues"],
        "bib_anchor": "",
    },
    "spinoza": {
        "name": "Baruch Spinoza",
        "dates": "1632 – 1677",
        "role": "Dutch Rationalist Philosopher",
        "bio": "Constructed his metaphysical system in the Ethica 'more geometrico' (in geometric fashion) from definitions and axioms, and insisted on genetic (causal) definitions of geometric figures.",
        "works": ["Ethica, ordine geometrico demonstrata (1677)", "Tractatus de intellectus emendatione"],
        "bib_anchor": "",
    },
    "stammler": {
        "name": "Gerhard Stammler",
        "dates": "1898 – 1977",
        "role": "German Philosopher of Mathematics & Logic",
        "bio": "Neo-Kantian philosopher at Halle who analyzed the history of the number concept since Gauss and the logical theory of concepts, judgments, and inferences.",
        "works": ["Der Zahlbegriff seit Gauss (1926)", "Begriff, Urteil, Schluss (1928)"],
        "bib_anchor": "bib-stammler-gerhard",
    },
    "staudt": {
        "name": "Karl Georg Christian von Staudt",
        "dates": "1798 – 1867",
        "role": "German Geometer",
        "bio": "Freed projective geometry from metric concepts by defining the cross-ratio and projective coordinates purely through harmonic constructions (Wurf-Rechnung).",
        "works": ["Geometrie der Lage (1847)", "Beiträge zur Geometrie der Lage (1856–1860)"],
        "bib_anchor": "",
    },
    "steiner": {
        "name": " Jakob Steiner",
        "dates": "1796 – 1863",
        "role": "Swiss Mathematician",
        "bio": "Great synthetic geometer who developed projective geometry through the systematic generation of higher figures from simpler projective forms.",
        "works": ["Systematische Entwickelung der Abhängigkeit geometrischer Gestalten von einander (1832)"],
        "bib_anchor": "",
    },
    "study": {
        "name": "Eduard Study",
        "dates": "1862 – 1930",
        "role": "German Mathematician",
        "bio": "Differential and algebraic geometer at Bonn who defended scientific realism in geometry against positivism and conventionalism.",
        "works": ["Die realistische Weltansicht und die Lehre vom Raume (1914)"],
        "bib_anchor": "bib-study-eduard",
    },
    "suarez": {
        "name": "Francisco Suárez, S.J.",
        "dates": "1548 – 1617",
        "role": "Spanish Jesuit Philosopher & Theologian (Doctor Eximius)",
        "bio": "Author of the Disputationes Metaphysicae, whose influential late-Scholastic metaphysics and theory of abstraction bridged medieval philosophy and early modern thought.",
        "works": ["Disputationes Metaphysicae (1597)"],
        "bib_anchor": "bib-suarez-francisco-s-j",
    },
    "taylor": {
        "name": "Alfred Edward Taylor",
        "dates": "1869 – 1945",
        "role": "British Idealist Philosopher & Plato Scholar",
        "bio": "Professor of Moral Philosophy at St Andrews and Edinburgh, renowned for his commentary on Plato's Timaeus and comprehensive study of Plato's dialogues.",
        "works": ["Plato: The Man and His Work (1926)", "A Commentary on Plato's Timaeus (1928)"],
        "bib_anchor": "bib-taylor-alfred-edward",
    },
    "thales": {
        "name": "Thales of Miletus",
        "dates": "c. 624 – c. 546 BC",
        "role": "Pre-Socratic Philosopher & Geometer",
        "bio": "Traditional founder of Greek philosophy and deductive geometry, credited by Proclus and Eudemus with the earliest geometric theorems.",
        "works": ["Fragments (Diels-Kranz)"],
        "bib_anchor": "",
    },
    "theaetetus": {
        "name": "Theaetetus of Athens",
        "dates": "c. 417 – c. 369 BC",
        "role": "Ancient Greek Mathematician",
        "bio": "Associate of Plato's Academy who classified quadratic irrationals (Euclid, Elements Book X) and completed the construction of the five regular polyhedra (Book XIII).",
        "works": ["Theory of Irrationals & Regular Solids (in Euclid, Elements X & XIII)"],
        "bib_anchor": "",
    },
    "themistius": {
        "name": "Themistius",
        "dates": "c. 317 – c. 388 AD",
        "role": "Late Antique Rhetorician & Aristotelian Commentator",
        "bio": "Composed lucid paraphrases of Aristotle's Posterior Analytics, Physics, and De Anima that were widely studied by Arabic and Latin Scholastics.",
        "works": ["In Aristotelis Physica Paraphrasis", "In Aristotelis Analyticorum Posteriorum Paraphrasis"],
        "bib_anchor": "bib-themistius",
    },
    "theodorus": {
        "name": "Theodorus of Cyrene",
        "dates": "c. 465 – c. 398 BC",
        "role": "Ancient Greek Mathematician",
        "bio": "Teacher of Plato and Theaetetus who proved the irrationality of the square roots of non-square integers from 3 up to 17.",
        "works": ["Reported in Plato, Theaetetus 147d"],
        "bib_anchor": "",
    },
    "trendelenburg": {
        "name": "Friedrich Adolf Trendelenburg",
        "dates": "1802 – 1872",
        "role": "German Philosopher & Aristotle Scholar",
        "bio": "Leader of the nineteenth-century Aristotelian revival in Germany, editor of De Anima, and critic of Hegelian dialectic and Kantian subjectivity.",
        "works": ["Logische Untersuchungen (1840)", "Elementa logices Aristoteleae (1836)"],
        "bib_anchor": "",
    },
    "vallee-poussin": {
        "name": "Charles-Jean de la Vallée Poussin",
        "dates": "1866 – 1962",
        "role": "Belgian Mathematician",
        "bio": "Professor at Louvain who proved the Prime Number Theorem independently of Hadamard and authored the classic Cours d'Analyse Infinitésimale.",
        "works": ["Cours d'Analyse Infinitésimale (1903)"],
        "bib_anchor": "",
    },
    "veronese": {
        "name": "Giuseppe Veronese",
        "dates": "1854 – 1917",
        "role": "Italian Geometer",
        "bio": "Pioneer of higher-dimensional projective geometry and constructed the first rigorous non-Archimedean geometry containing actual infinitesimals.",
        "works": ["Fondamenti di geometria a più dimensioni (1891)"],
        "bib_anchor": "",
    },
    "voss": {
        "name": "Aurel Voss",
        "dates": "1845 – 1931",
        "role": "German Mathematician",
        "bio": "Differential geometer at Munich who authored influential philosophical surveys on the nature of mathematical knowledge.",
        "works": ["Über das Wesen der Mathematik (1908)", "Über die mathematische Erkenntnis (1914)"],
        "bib_anchor": "bib-voss-aurel",
    },
    "waitz": {
        "name": "Theodor Waitz",
        "dates": "1821 – 1864",
        "role": "German Philosopher, Psychologist & Philologist",
        "bio": "Edited the standard nineteenth-century critical Greek edition and Latin commentary of Aristotle's Organon.",
        "works": ["Aristotelis Organon Graece (1844–1846)"],
        "bib_anchor": "bib-waitz-theodor",
    },
    "weber": {
        "name": "Heinrich Martin Weber",
        "dates": "1842 – 1913",
        "role": "German Mathematician",
        "bio": "Algebraist and co-editor with Josef Wellstein of the Enzyklopädie der Elementarmathematik.",
        "works": ["Enzyklopädie der Elementarmathematik (with J. Wellstein, 1903–1915)", "Lehrbuch der Algebra (1895)"],
        "bib_anchor": "bib-weber-heinrich",
    },
    "weierstrass": {
        "name": "Karl Weierstrass",
        "dates": "1815 – 1897",
        "role": "German Mathematician (Father of Modern Analysis)",
        "bio": "Established the rigorous epsilon-delta ('ars epsilontica') foundations of calculus and constructed a continuous nowhere-differentiable curve, exposing the limits of naive visual intuition.",
        "works": ["Mathematische Werke"],
        "bib_anchor": "",
    },
    "wellstein": {
        "name": "Josef Wellstein",
        "dates": "1869 – 1919",
        "role": "German Mathematician",
        "bio": "Professor at Strasbourg and co-author with Heinrich Weber of the Enzyklopädie der Elementarmathematik, whose chapters on the foundations of geometry are extensively analyzed by Hoenen.",
        "works": ["Grundlagen der Geometrie (in Weber-Wellstein, Enzyklopädie der Elementarmathematik II, 1915 / 1925)"],
        "bib_anchor": "bib-weber-heinrich",
    },
    "weyl": {
        "name": "Hermann Weyl",
        "dates": "1885 – 1955",
        "role": "German Mathematician & Mathematical Physicist",
        "bio": "Student of Hilbert who contributed fundamentally to group representations, differential geometry, gauge theory, and the philosophy of the mathematical continuum.",
        "works": ["Das Kontinuum (1918)", "Raum, Zeit, Materie (1918)", "Philosophie der Mathematik und Naturwissenschaft (1927)"],
        "bib_anchor": "bib-weyl-hermann",
    },
    "whitehead": {
        "name": "Alfred North Whitehead",
        "dates": "1861 – 1947",
        "role": "British Mathematician & Process Philosopher",
        "bio": "Co-author with Bertrand Russell of Principia Mathematica and creator of the method of extensive abstraction for deriving geometric points and instants from overlapping physical events.",
        "works": ["Principia Mathematica (with B. Russell, 1910–1913)", "A Treatise on Universal Algebra (1898)", "An Enquiry Concerning the Principles of Natural Knowledge (1919)"],
        "bib_anchor": "bib-whitehead-alfred-north",
    },
    "wolff": {
        "name": "Christian Wolff",
        "dates": "1679 – 1754",
        "role": "German Enlightenment Rationalist Philosopher",
        "bio": "Systematized Leibnizian rationalism and Scholastic terminology into the German Enlightenment handbooks against which Kant reacted.",
        "works": ["Elementa matheseos universae (1713–1715)", "Philosophia prima sive Ontologia (1730)"],
        "bib_anchor": "",
    },
    "zeller": {
        "name": "Eduard Zeller",
        "dates": "1814 – 1908",
        "role": "German Historian of Ancient Philosophy",
        "bio": "Author of the monumental Die Philosophie der Grichen in ihrer geschichtlichen Entwicklung.",
        "works": ["Die Philosophie der Griechen in ihrer geschichtlichen Entwicklung"],
        "bib_anchor": "",
    },
    "zeno": {
        "name": "Zeno of Elea",
        "dates": "c. 495 – c. 430 BC",
        "role": "Pre-Socratic Eleatic Philosopher",
        "bio": "Disciple of Parmenides whose paradoxes of motion and plurality (Achilles, Dichotomy, Arrow, Stadium) catalyzed Greek and Scholastic analyses of the continuum.",
        "works": ["Paradoxes of Motion and Plurality (Aristotle, Physics VI 9)"],
        "bib_anchor": "",
    },
    "zermelo": {
        "name": "Ernst Zermelo",
        "dates": "1871 – 1953",
        "role": "German Mathematician & Logician",
        "bio": "Formulated the Axiom of Choice (1904) and the first axiomatization of set theory (1908) to avoid Russell's paradox.",
        "works": ["Untersuchungen über die Grundlagen der Mengenlehre I (1908)"],
        "bib_anchor": "",
    },
}

# Ordered regex patterns for tagging person mentions in Latin/vernacular prose.
# Multi-word and titled patterns come before single-word patterns.
PERSON_PATTERNS: List[Tuple[str, str]] = [
    (
        "aquinas",
        r"(?:D\.|S\.|St\.|Sancti|Sanctus|Sancto|Sanctum|Divi|Divus|Divo|Divum)\s+"
        r"(?:Thomae\s+de\s+Aquino|Thomas\s+de\s+Aquino|Thoma\s+de\s+Aquino|"
        r"Thomae\s+Aquinatis|Thomas\s+Aquinas|Thomae|Thomas|Thoma|Thomam)"
        r"|Thomae\s+de\s+Aquino|Thomas\s+de\s+Aquino|Thoma\s+de\s+Aquino"
        r"|Thomae\s+Aquinatis|Thomas\s+Aquinas|Aquinatis|Aquinate|Aquinatem|Aquinas"
        r"|Doctoris\s+Angelici|Doctor\s+Angelicus|Doctore\s+Angelico|Doctori\s+Angelico"
        r"|Thomae|Thomam",
    ),
    (
        "albertus",
        r"(?:S\.|B\.|D\.)?\s*Albert(?:us|i|o|um)\s+Magn(?:us|i|o|um)|Albert(?:us|i|o|um)\s+Magn(?:us|i|o|um)",
    ),
    (
        "cajetan",
        r"Card\.\s*Cajetan(?:us|i|o|um)|Cajetan(?:us|i|o|um)|Caietan(?:us|i|o|um)",
    ),
    (
        "johannes-a-sancto-thoma",
        r"(?:Ioann(?:es|is|i|em)|Joann(?:es|is|i|em))\s+a\s+(?:S\.|Sancto)\s+Thoma",
    ),
    (
        "scotus",
        r"Duns\s+Scot(?:us|i|o|um)|(?:Ps\.-|Pseudo-)Scot(?:us|i|o|um)|Scot(?:us|i|o|um)",
    ),
    (
        "suarez",
        r"Suarez(?:ii|io|ium|ius)?|Suárez",
    ),
    (
        "aristotle",
        r"Aristotel(?:es|is|i|em|e)|Stagirit(?:a|ae|am)|Philosoph(?:us|i|o|um)",
    ),
    (
        "plato",
        r"Platon(?:is|i|em|e)|Plato",
    ),
    (
        "socrates",
        r"Socrat(?:es|is|i|em|e)",
    ),
    (
        "euclid",
        r"Euclid(?:es|is|i|em|e)",
    ),
    (
        "proclus",
        r"Procl(?:us|i|o|um)",
    ),
    (
        "simplicius",
        r"Simplici(?:us|i|o|um)",
    ),
    (
        "philoponus",
        r"(?:Ioann(?:es|is|i|em)|Joann(?:es|is|i|em))\s+Philopon(?:us|i|o|um)|Philopon(?:us|i|o|um)",
    ),
    (
        "themistius",
        r"Themisti(?:us|i|o|um)",
    ),
    (
        "alexander",
        r"Alexandr(?:i|o|um)\s+Aphrodisiens(?:is|i|em|e)|Alexander\s+Aphrodisiensis|Alexandr(?:o|i)\s+in\s+Met",
    ),
    (
        "averroes",
        r"Averro(?:ës|es|is|i|em|e)|Commentator(?:is|i|em|e)",
    ),
    (
        "avicenna",
        r"Avicenn(?:a|ae|am)",
    ),
    (
        "boethius",
        r"Boëthi(?:us|i|o|um)|Boethi(?:us|i|o|um)",
    ),
    (
        "pythagoras",
        r"Pythagor(?:as|ae|am|a)|Pythagor(?:ei|eorum|eis|eos)",
    ),
    (
        "archimedes",
        r"Archimed(?:es|is|i|em|e)",
    ),
    (
        "eudoxus",
        r"Eudox(?:us|i|o|um)",
    ),
    (
        "theaetetus",
        r"Theaetet(?:us|i|o|um)",
    ),
    (
        "theodorus",
        r"Theodor(?:us|i|o|um)\s+Cyren(?:aeus|aei)",
    ),
    (
        "hippocrates",
        r"Hippocrat(?:es|is|i|em|e)(?:\s+Chi(?:us|i|o))?",
    ),
    (
        "democritus",
        r"Democrit(?:us|i|o|um)",
    ),
    (
        "protagoras",
        r"Protagor(?:as|ae|am|a)",
    ),
    (
        "zeno",
        r"Zenon(?:is|i|em|e)|Zeno",
    ),
    (
        "parmenides",
        r"Parmenid(?:es|is|i|em|e)",
    ),
    (
        "heraclitus",
        r"Heraclit(?:us|i|o|um)",
    ),
    (
        "thales",
        r"Thal(?:es|etis|eti|etem|ete)",
    ),
    (
        "ptolemy",
        r"Ptolemae(?:us|i|o|um)",
    ),
    (
        "heron",
        r"Heron(?:is|i|em|e)\s+Alexandrin(?:i|o|um)|Heron(?:is|i|em|e)",
    ),
    (
        "nicomachus",
        r"Nicomach(?:us|i|o|um)",
    ),
    (
        "descartes",
        r"Renat(?:us|i|o|um)\s+Cartesi(?:us|i|o|um)|Cartesi(?:us|i|o|um)|Descartes",
    ),
    (
        "spinoza",
        r"Spinoz(?:a|ae|am)",
    ),
    (
        "leibniz",
        r"G\.\s*W\.\s*Leibniz|Leibniti(?:us|i|o|um)|Leibniz(?:ii|io|ium|ius)?",
    ),
    (
        "newton",
        r"Isaac(?:us|i|o|um)\s+Newton(?:us|i|o|um)?|Newton(?:us|i|o|um)?",
    ),
    (
        "galileo",
        r"Galilae(?:us|i|o|um)|Galilei|Galileo",
    ),
    (
        "pascal",
        r"B\.\s*Pascal|Pascal(?:is|i|em)?",
    ),
    (
        "saccheri",
        r"H\.\s*Saccheri|G\.\s*Saccheri|Saccheri(?:us|i|o|um)?",
    ),
    (
        "locke",
        r"J\.\s*Locke|Lock(?:ius|ii|io|ium|e)",
    ),
    (
        "berkeley",
        r"G\.\s*Berkeley|Berkeley",
    ),
    (
        "hume",
        r"D\.\s*Hume|David\s+Hume|Humi(?:us|i|o|um)|Hume",
    ),
    (
        "kant",
        r"Imm\.\s*Kant|I\.\s*Kant|Kanti(?:us|i|o|um)|Kant",
    ),
    (
        "hegel",
        r"G\.\s*W\.\s*F\.\s*Hegel|Hegel(?:ii|io|ium|ius)?",
    ),
    (
        "wolff",
        r"Chr\.\s*Wolff|Christian(?:us|i|o)\s+Wolff(?:ius|ii|io)?|Wolff(?:ius|ii|io|ium)?",
    ),
    (
        "mill",
        r"J\.\s*St\.\s*Mill|Stuart\s+Mill|Mill(?:ius|ii|io)?",
    ),
    (
        "gauss",
        r"C\.\s*Fr\.\s*Gauss|C\.\s*F\.\s*Gauss|Gauss(?:ius|ii|io|ium)?",
    ),
    (
        "riemann",
        r"B\.\s*Riemann|Riemann(?:us|i|o|um)?",
    ),
    (
        "lobachevsky",
        r"Lobatschefsk(?:ij|y|i)|Lobachevsk(?:y|i)",
    ),
    (
        "bolyai",
        r"J\.\s*Bolyai|Bolyai",
    ),
    (
        "beltrami",
        r"E\.\s*Beltrami|Beltrami",
    ),
    (
        "helmholtz",
        r"H\.\s*v(?:on|\.)\s*Helmholtz|v(?:on|\.)\s*Helmholtz|Helmholtz(?:ii|io|ium)?",
    ),
    (
        "klein",
        r"F(?:elix|\.)\s+Klein|Klein(?:ii|io|ium)?",
    ),
    (
        "hilbert",
        r"D(?:avid|\.)\s+Hilbert|Hilbert(?:us|i|o|um)?",
    ),
    (
        "poincare",
        r"H(?:enri|\.)\s+Poincaré|Poincaré|Poincare",
    ),
    (
        "russell",
        r"B(?:ertrand|\.)\s+Russell|Russell(?:ius|ii|io)?",
    ),
    (
        "whitehead",
        r"A\.\s*N\.\s*Whitehead|Whitehead",
    ),
    (
        "frege",
        r"G\.\s*Frege|Frege",
    ),
    (
        "peano",
        r"G\.\s*Peano|Peano",
    ),
    (
        "pasch",
        r"M(?:oritz|\.)\s+Pasch|Pasch(?:ii|io)?",
    ),
    (
        "cantor",
        r"G(?:eorg|\.)\s+Cantor|Cantor(?:is|i|em)?",
    ),
    (
        "dedekind",
        r"R(?:ichard|\.)\s+Dedekind|Dedekind",
    ),
    (
        "weierstrass",
        r"K\.\s*Weierstrass|Weierstrass",
    ),
    (
        "kronecker",
        r"L\.\s*Kronecker|Kronecker",
    ),
    (
        "jordan",
        r"C(?:amille|\.)\s+Jordan|Jordan",
    ),
    (
        "moebius",
        r"A\.\s*F\.\s*Möbius|Möbius|Moebi(?:us|i|o|um)",
    ),
    (
        "veronese",
        r"G\.\s*Veronese|Veronese",
    ),
    (
        "enriques",
        r"F(?:ederigo|\.)\s+Enriques|Enriques",
    ),
    (
        "amaldi",
        r"U(?:go|\.)\s+Amaldi|Amaldi",
    ),
    (
        "brouwer",
        r"L\.\s*E\.\s*J\.\s*Brouwer|Brouwer",
    ),
    (
        "weyl",
        r"H(?:ermann|\.)\s+Weyl|Weyl",
    ),
    (
        "einstein",
        r"A(?:lbert|\.)\s+Einstein|Einstein(?:ii|io)?",
    ),
    (
        "gonseth",
        r"F(?:erdinand|\.)\s+Gonseth|Gonseth",
    ),
    (
        "brunschvicg",
        r"L(?:éon|\.)\s+Brunschvicg|Brunschvicg",
    ),
    (
        "meyerson",
        r"[ÉE](?:mile|\.)\s+Meyerson|Meyerson",
    ),
    (
        "couturat",
        r"L(?:ouis|\.)\s+Couturat|Couturat",
    ),
    (
        "hadamard",
        r"J(?:acques|\.)\s+Hadamard|Hadamard",
    ),
    (
        "hardy",
        r"G\.\s*H\.\s*Hardy|Hardy",
    ),
    (
        "hoelder",
        r"O(?:tto|\.)\s+Hölder|Hölder|Hoelder",
    ),
    (
        "killing",
        r"W(?:ilhelm|\.)\s+Killing|Killing",
    ),
    (
        "study",
        r"E(?:duard|\.)\s+Study|Study",
    ),
    (
        "voss",
        r"A(?:urel|\.)\s+Voss|Voss",
    ),
    (
        "wellstein",
        r"J(?:osef|\.)\s+Wellstein|Wellstein",
    ),
    (
        "weber",
        r"H(?:einrich|\.)\s+Weber|Weber",
    ),
    (
        "hessenberg",
        r"G(?:erhard|\.)\s+Hessenberg|Hessenberg",
    ),
    (
        "hausdorff",
        r"F(?:elix|\.)\s+Hausdorff|Hausdorff",
    ),
    (
        "reichenbach",
        r"H(?:ans|\.)\s+Reichenbach|Reichenbach",
    ),
    (
        "schlick",
        r"M(?:oritz|\.)\s+Schlick|Schlick",
    ),
    (
        "hertz",
        r"P(?:aul|\.)\s+Hertz|Hertz",
    ),
    (
        "husserl",
        r"E(?:dmund|\.)\s+Husserl|Husserl",
    ),
    (
        "becker",
        r"O(?:skar|\.)\s+Becker|Becker",
    ),
    (
        "scholz",
        r"H(?:einrich|\.)\s+Scholz|Scholz",
    ),
    (
        "hasse",
        r"H(?:elmut|\.)\s+Hasse|Hasse",
    ),
    (
        "stammler",
        r"G(?:erhard|\.)\s+Stammler|Stammler",
    ),
    (
        "riehl",
        r"A(?:lois|\.)\s+Riehl|Riehl",
    ),
    (
        "geyser",
        r"J(?:oseph|\.)\s+Geyser|Geyser",
    ),
    (
        "baeumker",
        r"Cl(?:emens|\.)\s+Baeumker|Baeumker",
    ),
    (
        "maier",
        r"A(?:nneliese|\.)\s+Maier|Maier",
    ),
    (
        "mercier",
        r"Card\.\s*Mercier|D\.\s*Mercier|Mercier",
    ),
    (
        "maritain",
        r"J(?:acques|\.)\s+Maritain|Maritain",
    ),
    (
        "gilson",
        r"[ÉE](?:tienne|\.)\s+Gilson|Gilson",
    ),
    (
        "gredt",
        r"J(?:oseph|\.)\s+Gredt|Gredt",
    ),
    (
        "boyer",
        r"C(?:harles|\.)\s+Boyer|Boyer",
    ),
    (
        "lonergan",
        r"B(?:ernard|\.)\s+Lonergan|Lonergan",
    ),
    (
        "alvarez-laso",
        r"J(?:osé|\.)\s+Alvarez\s+Laso|Alvarez\s+Laso",
    ),
    (
        "freudenthal",
        r"H(?:ans|\.)\s+Freudenthal|Freudenthal",
    ),
    (
        "hoenen",
        r"P\.\s*Hoenen|Hoenen",
    ),
    (
        "ross",
        r"W\.\s*D\.\s*Ross|D\.\s*Ross|Ross",
    ),
    (
        "heath",
        r"T(?:homas|\.)\s*L\.\s*Heath|T\.\s*Heath|Heath",
    ),
    (
        "taylor",
        r"A\.\s*E\.\s*Taylor|Taylor",
    ),
    (
        "burnet",
        r"J(?:ohn|\.)\s+Burnet|Burnet",
    ),
    (
        "bonitz",
        r"H(?:ermann|\.)\s+Bonitz|Bonitz",
    ),
    (
        "waitz",
        r"Th(?:eodor|\.)\s+Waitz|Waitz",
    ),
    (
        "christ",
        r"W\.\s*Christ|Christ",
    ),
    (
        "heiberg",
        r"J\.\s*L\.\s*Heiberg|Heiberg",
    ),
    (
        "friedlein",
        r"G\.\s*Friedlein|Friedlein",
    ),
    (
        "diels",
        r"H\.\s*Diels|Diels",
    ),
    (
        "bekker",
        r"I\.\s*Bekker|Bekker",
    ),
    (
        "carteron",
        r"H(?:enri|\.)\s+Carteron|Carteron",
    ),
    (
        "hamelin",
        r"O(?:ctave|\.)\s+Hamelin|Hamelin",
    ),
    (
        "zeller",
        r"E(?:duard|\.)\s+Zeller|Zeller",
    ),
    (
        "trendelenburg",
        r"A\.\s*Trendelenburg|Trendelenburg",
    ),
    (
        "duhem",
        r"P(?:ierre|\.)\s+Duhem|Duhem",
    ),
    (
        "mach",
        r"E(?:rnst|\.)\s+Mach|Mach",
    ),
    (
        "poncelet",
        r"J\.\s*V\.\s*Poncelet|Poncelet",
    ),
    (
        "steiner",
        r"J(?:akob|\.)\s+Steiner|Steiner",
    ),
    (
        "staudt",
        r"Ch\.\s*v(?:on|\.)\s*Staudt|v(?:on|\.)\s*Staudt|Staudt",
    ),
    (
        "cayley",
        r"A(?:rthur|\.)\s+Cayley|Cayley",
    ),
    (
        "lambert",
        r"J\.\s*H\.\s*Lambert|Lambert",
    ),
    (
        "euler",
        r"L(?:eonhard|\.)\s+Euler|Euler",
    ),
    (
        "borel",
        r"[ÉE](?:mile|\.)\s+Borel|Borel",
    ),
    (
        "vallee-poussin",
        r"de\s+la\s+Vallée-Poussin's|de\s+la\s+Vallée-Poussin|Vallée-Poussin",
    ),
    (
        "zermelo",
        r"E(?:rnst|\.)\s+Zermelo|Zermelo",
    ),
    (
        "fraenkel",
        r"A\.\s*Fraenkel|Fraenkel",
    ),
]

GROUP_TO_SLUG = {f"p_{i}": slug for i, (slug, _) in enumerate(PERSON_PATTERNS)}
MASTER_PERSON_RE = re.compile(
    r"(?<![A-Za-z0-9_äöüÄÖÜéèêàáíóú*`'-])(?:"
    + "|".join(f"(?P<p_{i}>{pat})" for i, (_, pat) in enumerate(PERSON_PATTERNS))
    + r")(?![A-Za-z0-9_äöüÄÖÜéèêàáíóú*`'-])"
)

# Regex splitting lines into unprotected prose (even indices) and protected inline markup (odd indices)
PROTECTED_SPAN_RE = re.compile(
    r"(:(?:cite|term|person|g|just|line|ref):`[^`]+`|``[^`]+``|`[^`]+`|\*\*[^*\n]+\*\*|\*[^*\n]+\*|\[\#f[0-9]+\]_|\.\.\s+\[\#f[0-9]+\])"
)

# Map composite citation author keys to individual person slugs
CITE_AUTHOR_TO_PERSONS: Dict[str, List[str]] = {
    "weber-wellstein": ["weber", "wellstein"],
    "whitehead-russell": ["whitehead", "russell"],
    "hasse-scholz": ["hasse", "scholz"],
    "pseudo-thomas": ["aquinas"],
}


def normalize_cite_target(target: str) -> str:
    """Normalize a citation target to canonical ``author:work[:locus]`` form."""
    t = target.strip()
    if t == "aquinas":
        return "aquinas:anal-post"
    parts = t.split(":")
    if len(parts) >= 3:
        prefix3 = f"{parts[0]}:{parts[1]}:{parts[2]}"
        if prefix3 in CITE_PREFIX_MAP:
            mapped = CITE_PREFIX_MAP[prefix3]
            rest = ":".join(parts[3:])
            return f"{mapped}:{rest}" if rest else mapped
    if len(parts) >= 2:
        prefix = f"{parts[0]}:{parts[1]}"
        if prefix in CITE_PREFIX_MAP:
            mapped = CITE_PREFIX_MAP[prefix]
            rest = ":".join(parts[2:])
            return f"{mapped}:{rest}" if rest else mapped
    if t in CITE_PREFIX_MAP:
        return CITE_PREFIX_MAP[t]
    return t


def normalize_term_slug(slug: str) -> str:
    """Normalize a glossary term slug."""
    s = slug.strip().lower()
    if s == "oinai-ennoiai":
        return "koinai-ennoiai"
    return s


def normalize_person_slug(slug: str) -> str:
    """Normalize a person slug."""
    return slug.strip().lower()


def infer_language(headword: str, slug: str) -> str:
    """Infer the source language of a glossary term."""
    if slug in TERM_CATALOG:
        return TERM_CATALOG[slug]["language"]
    if any("\u0370" <= ch <= "\u03ff" or "\u1f00" <= ch <= "\u1fff" for ch in headword):
        return "Greek"
    if any(
        w in slug
        for w in (
            "mathematik",
            "kurven",
            "gedachte",
            "punkte",
            "gesetze",
            "weise",
            "prozess",
            "utopie",
            "zusammenhang",
            "umgekehrt",
            "einerseits",
            "andererseits",
            "erklaerungen",
            "beschaffenheit",
        )
    ):
        return "German"
    if any(w in slug for w in ("pensee", "prealable", "rigueur", "ensemble")):
        return "French"
    if slug == "insieme":
        return "Italian"
    if slug in ("betweenness", "apotheosis-of-stupidity"):
        return "English"
    return "Latin (Scholastic)"


def tag_persons_in_rst(text: str) -> str:
    """Tag unprotected person mentions in body prose and footnotes with :person:`Display <slug>`."""
    lines = text.splitlines()
    # Skip top metadata block
    body_start = 0
    while body_start < len(lines) and lines[body_start].strip():
        body_start += 1

    new_lines = list(lines[:body_start])
    for idx in range(body_start, len(lines)):
        line = lines[idx]
        s = line.strip()
        if not s:
            new_lines.append(line)
            continue

        # Skip section underline lines
        if re.match(r"^[=\-~^+\"']{3,}$", s):
            new_lines.append(line)
            continue

        # Skip heading lines (followed by a section underline line)
        if idx + 1 < len(lines):
            next_s = lines[idx + 1].strip()
            if len(next_s) >= 3 and re.match(r"^[=\-~^+\"']{3,}$", next_s):
                new_lines.append(line)
                continue

        # Skip directive/comment lines except footnote definitions .. [#fN]
        if s.startswith("..") and not re.match(r"^\.\.\s+\[\#f[0-9]+\]\s+", s):
            new_lines.append(line)
            continue

        # Skip field list lines
        if re.match(r"^:[A-Za-z0-9_.-]+:\s*", s):
            new_lines.append(line)
            continue

        segments = PROTECTED_SPAN_RE.split(line)
        rebuilt_segments: List[str] = []
        for seg_idx, seg in enumerate(segments):
            if seg_idx % 2 == 1:
                rebuilt_segments.append(seg)
            else:
                def _repl_person(m: re.Match) -> str:
                    slug = GROUP_TO_SLUG[m.lastgroup]
                    disp = m.group(0)
                    return f":person:`{disp} <{slug}>`"

                rebuilt_segments.append(MASTER_PERSON_RE.sub(_repl_person, seg))

        new_lines.append("".join(rebuilt_segments))

    res = "\n".join(new_lines)
    if text.endswith("\n"):
        res += "\n"
    return res


def main() -> None:
    rst_files = sorted([p for p in VOLUME_ROOT.rglob("*.rst") if not p.name.endswith(".notes.rst")])

    citations_registry: Dict[str, Dict[str, Any]] = {}
    glossary_registry: Dict[str, Dict[str, Any]] = {}
    persons_registry: Dict[str, Dict[str, Any]] = {}
    normalized_files = 0

    total_cite_tags = 0
    total_term_tags = 0
    total_person_tags = 0

    for p in rst_files:
        text = p.read_text(encoding="utf-8")
        orig_text = text

        # Extract metadata
        meta: Dict[str, str] = {}
        for line in text.splitlines():
            if not line.strip():
                break
            m = re.match(r"^:([A-Za-z0-9_.-]+):\s*(.*)$", line)
            if m:
                meta[m.group(1)] = m.group(2).strip()

        folio = meta.get("folio", p.stem)
        page = meta.get("page", str(int(folio)) if folio.isdigit() else folio)
        book = meta.get("book", "")
        section = meta.get("section", p.parent.name)

        # Normalize :cite:`...` in text
        def _replace_cite(match: re.Match) -> str:
            content = match.group(1)
            cm = re.match(r"^(.*?)\s*<([^>]+)>$", content)
            if cm:
                disp, raw_target = cm.group(1).strip(), cm.group(2).strip()
            else:
                disp, raw_target = content.strip(), content.strip().lower()
            norm_target = normalize_cite_target(raw_target)
            return f":cite:`{disp} <{norm_target}>`"

        text = re.sub(r":cite:`([^`]+)`", _replace_cite, text)

        # Normalize :term:`...` in text
        def _replace_term(match: re.Match) -> str:
            content = match.group(1)
            tm = re.match(r"^(.*?)\s*<([^>]+)>$", content)
            if tm:
                disp, raw_slug = tm.group(1).strip(), tm.group(2).strip()
            else:
                disp, raw_slug = content.strip(), content.strip().lower()
            norm_slug = normalize_term_slug(raw_slug)
            return f":term:`{disp} <{norm_slug}>`"

        text = re.sub(r":term:`([^`]+)`", _replace_term, text)

        # Normalize existing :person:`...` in text
        def _replace_existing_person(match: re.Match) -> str:
            content = match.group(1)
            pm = re.match(r"^(.*?)\s*<([^>]+)>$", content)
            if pm:
                disp, raw_slug = pm.group(1).strip(), pm.group(2).strip()
            else:
                disp, raw_slug = content.strip(), content.strip().lower()
            norm_slug = normalize_person_slug(raw_slug)
            return f":person:`{disp} <{norm_slug}>`"

        text = re.sub(r":person:`([^`]+)`", _replace_existing_person, text)

        # Tag unprotected person mentions in body & footnotes
        text = tag_persons_in_rst(text)

        if text != orig_text:
            p.write_text(text, encoding="utf-8")
            normalized_files += 1

        # Collect occurrences from body
        lines = text.splitlines()
        idx = 0
        while idx < len(lines) and lines[idx].strip():
            idx += 1
        body = "\n".join(lines[idx:])

        for m in re.finditer(r":cite:`([^`]+)`", body):
            total_cite_tags += 1
            c = m.group(1)
            cm = re.match(r"^(.*?)\s*<([^>]+)>$", c)
            if not cm:
                continue
            disp, target = cm.group(1).strip(), cm.group(2).strip()
            parts = target.split(":")
            author_key = parts[0]
            work_prefix = ":".join(parts[:2]) if len(parts) >= 2 else author_key
            locus = ":".join(parts[2:]) if len(parts) > 2 else ""

            author_info = AUTHOR_CATALOG.get(
                author_key,
                {
                    "name": author_key.replace("-", " ").title(),
                    "bib_anchor": f"bib-{author_key}",
                    "work_default": work_prefix,
                },
            )
            work_title = WORK_TITLES.get(work_prefix, author_info["work_default"])

            entry = citations_registry.setdefault(
                target,
                {
                    "key": target,
                    "author_key": author_key,
                    "work_key": work_prefix,
                    "locus": locus,
                    "author": author_info["name"],
                    "bib_anchor": author_info["bib_anchor"],
                    "work": work_title,
                    "occurrences": [],
                },
            )
            clean_disp = re.sub(r"\*([^*]+)\*", r"\1", disp)
            entry["occurrences"].append(
                {
                    "volume": "volume_I",
                    "folio": folio,
                    "page": page,
                    "book": book,
                    "section": section,
                    "display": clean_disp,
                }
            )

        for m in re.finditer(r":term:`([^`]+)`", body):
            total_term_tags += 1
            c = m.group(1)
            tm = re.match(r"^(.*?)\s*<([^>]+)>$", c)
            if not tm:
                continue
            disp, slug = tm.group(1).strip(), tm.group(2).strip()
            clean_disp = re.sub(r"\*([^*]+)\*", r"\1", disp)
            cat = TERM_CATALOG.get(slug, {})
            headword = cat.get("headword", clean_disp)
            lang = infer_language(headword, slug)
            translation = cat.get("translation", clean_disp)
            definition = cat.get(
                "definition",
                f"Technical philosophical/mathematical term in Hoenen's De Noetica Geometriae ({lang}).",
            )

            t_entry = glossary_registry.setdefault(
                slug,
                {
                    "slug": slug,
                    "headword": headword,
                    "language": lang,
                    "translation": translation,
                    "definition": definition,
                    "occurrences": [],
                },
            )
            t_entry["occurrences"].append(
                {
                    "volume": "volume_I",
                    "folio": folio,
                    "page": page,
                    "book": book,
                    "section": section,
                    "display": clean_disp,
                }
            )

        for m in re.finditer(r":person:`([^`]+)`", body):
            total_person_tags += 1
            c = m.group(1)
            pm = re.match(r"^(.*?)\s*<([^>]+)>$", c)
            if not pm:
                continue
            disp, slug = pm.group(1).strip(), pm.group(2).strip()
            clean_disp = re.sub(r"\*([^*]+)\*", r"\1", disp)
            p_cat = PERSON_CATALOG.get(
                slug,
                {
                    "name": slug.replace("-", " ").title(),
                    "dates": "",
                    "role": "Philosopher / Mathematician",
                    "bio": "",
                    "works": [],
                    "bib_anchor": f"bib-{slug}",
                },
            )
            p_entry = persons_registry.setdefault(
                slug,
                {
                    "slug": slug,
                    "name": p_cat["name"],
                    "dates": p_cat["dates"],
                    "role": p_cat["role"],
                    "bio": p_cat["bio"],
                    "works": p_cat["works"],
                    "bib_anchor": p_cat["bib_anchor"],
                    "occurrences": [],
                },
            )
            p_entry["occurrences"].append(
                {
                    "volume": "volume_I",
                    "folio": folio,
                    "page": page,
                    "book": book,
                    "section": section,
                    "display": clean_disp,
                }
            )

    # Also merge citation-derived author occurrences into persons_registry so authors cited inside :cite:`...`
    # are represented in persons.json with their cited folios if not already recorded on that folio.
    for target, c_entry in citations_registry.items():
        ak = c_entry["author_key"]
        p_slugs = CITE_AUTHOR_TO_PERSONS.get(ak, [ak] if ak in PERSON_CATALOG else [])
        for slug in p_slugs:
            p_cat = PERSON_CATALOG[slug]
            p_entry = persons_registry.setdefault(
                slug,
                {
                    "slug": slug,
                    "name": p_cat["name"],
                    "dates": p_cat["dates"],
                    "role": p_cat["role"],
                    "bio": p_cat["bio"],
                    "works": p_cat["works"],
                    "bib_anchor": p_cat["bib_anchor"],
                    "occurrences": [],
                },
            )
            existing_folios = {o["folio"] for o in p_entry["occurrences"]}
            for occ in c_entry["occurrences"]:
                if occ["folio"] not in existing_folios:
                    p_entry["occurrences"].append(
                        {
                            "volume": occ.get("volume", "volume_I"),
                            "folio": occ["folio"],
                            "page": occ["page"],
                            "book": occ["book"],
                            "section": occ["section"],
                            "display": occ["display"],
                        }
                    )
                    existing_folios.add(occ["folio"])

    # Sort each person's occurrences by folio number
    for slug, p_entry in persons_registry.items():
        p_entry["occurrences"].sort(key=lambda o: o["folio"])

    # Also compute work-level sibling folios so clicking any locus of a work shows all folios citing that work
    work_folios: Dict[str, List[Dict[str, str]]] = {}
    for target, entry in citations_registry.items():
        wk = entry["work_key"]
        seen = {o["folio"] for o in work_folios.get(wk, [])}
        for occ in entry["occurrences"]:
            if occ["folio"] not in seen:
                work_folios.setdefault(wk, []).append(occ)
                seen.add(occ["folio"])

    for target, entry in citations_registry.items():
        entry["work_occurrences"] = work_folios.get(entry["work_key"], entry["occurrences"])

    # Sort dictionaries by key for deterministic output
    citations_sorted = dict(sorted(citations_registry.items()))
    glossary_sorted = dict(sorted(glossary_registry.items()))
    persons_sorted = dict(sorted(persons_registry.items()))

    # Write citations.json, glossary.json, and persons.json to resources/hoenen_1954/
    (EDITION_ROOT / "citations.json").write_text(
        json.dumps(citations_sorted, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (EDITION_ROOT / "glossary.json").write_text(
        json.dumps(glossary_sorted, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (EDITION_ROOT / "persons.json").write_text(
        json.dumps(persons_sorted, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Updated {normalized_files} folio RST files.")
    print(f"Total :cite: tags: {total_cite_tags} across {len(citations_sorted)} canonical citation keys -> {EDITION_ROOT / 'citations.json'}")
    print(f"Total :term: tags: {total_term_tags} across {len(glossary_sorted)} glossary terms -> {EDITION_ROOT / 'glossary.json'}")
    print(f"Total :person: tags: {total_person_tags} across {len(persons_sorted)} prosopographical entries -> {EDITION_ROOT / 'persons.json'}")


if __name__ == "__main__":
    main()
