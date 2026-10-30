# GEOMETOR • hoenen

## *De Noetica Geometriae: Origine Theoriae Cognitionis*
*(On the Noetics of Geometry: Origin of the Theory of Knowledge)*

**Petrus Hubertus Jacobus Hoenen, S.J. (1880–1961)**  
*Analecta Gregoriana*, Vol. LXIII  
Romae: Apud Aedes Universitatis Gregorianae, 1954.

---

> ### 🌐 [Read the Full Book Codex & English Translation at geometor.github.io/hoenen](https://geometor.github.io/hoenen)
>
> The complete Latin text, facing English translations, chapter summaries, scholarly notes, and analytical apparatus are available online in the **Book Codex** edition powered by [`photon-platform/publish`](https://github.com/photon-platform/publish):  
> 👉 **[Visit the Project Website: geometor.github.io/hoenen](https://geometor.github.io/hoenen)**

---

## What Is This Book About?

Father Peter Hoenen, S.J. (1880–1961) was a Dutch Jesuit philosopher who taught at the Pontifical Gregorian University in Rome. Before studying scholastic philosophy, he was trained in theoretical physics under Nobel laureate H. A. Lorentz at Leiden University.

In *De Noetica Geometriae*, Hoenen tackled a question that had thrown 20th-century mathematics and philosophy into turmoil: **Where does our knowledge of geometry actually come from?**

### The Foundational Crisis
When Albert Einstein formulated general relativity and mathematicians developed non-Euclidean geometries, traditional assumptions about space collapsed:
* **Empiricists** argued that geometry is just physics—an approximate guess based on measuring physical space.
* **Formalists** (such as David Hilbert) argued that geometry is an uninterpreted game of symbols—you pick arbitrary axioms, and the deductions need not refer to anything real.

Hoenen argued that both views miss the essential nature of human mathematical cognition by ignoring two fundamental problems:

1. **The Problem of Necessity (*Problema Necessitatis*)**:  
   When we recognize that $7 + 5 = 12$, or that two points uniquely determine a straight line, we do not treat it as an experimental hypothesis subject to empirical falsification. We perceive an intrinsic, immutable necessity. Where does that certainty come from?
2. **The Problem of Exactitude (*Problema Exactitudinis*)**:  
   No human eye has ever seen a true mathematical point (zero dimensions) or a true line (zero breadth). Physical reality presents only blurred thresholds and finite grain. How does the mind attain exact geometric concepts if our senses only experience imperfect physical objects?

### Hoenen's Answer: Intuitive Formal Abstraction
Drawing on Aristotle and Thomas Aquinas, Hoenen showed that mathematical knowledge is neither an empirical generalization nor an arbitrary formal game.

Through **intuitive formal abstraction** (*abstractio formalis intuitiva*), the intellect perceives necessary relationships directly within the imaginative sensible presentation (*phantasma* and *materia intelligibilis*, or intelligible matter). You cannot divide a continuous line without generating an indivisible point of division; you cannot close a curve on a plane without bounding an interior from an exterior.

For Hoenen, geometry is not an isolated specialty, but the true foundation and starting point of all general theory of knowledge (*origo noeticae generalis*).

---

## Process, Pipeline & Coordination with `publish`

Published in Rome in 1954, *De Noetica Geometriae* was never reprinted, never translated into English, and published without a Table of Contents. Recovering the 293-page monograph from a physical copy preserved at **Mount Angel Abbey** followed a four-stage pipeline integrated with [`photon-platform/publish`](https://github.com/photon-platform/publish):

1. **Archival Spread Splitting & Folio Calibration (`resources/de_noetica_geometriae/`)**:
   Two-page spreads were split into individual page PNGs (`0001.png`–`0297.png`) and paired with page-level RST transcriptions reviewed in `publish folio`.
2. **Direct Multimodal Transcription (Zero-OCR)**:
   Bypassing conventional OCR—which fails on polyglot scholastic Latin, polytonic Greek citations, French, German, and mathematical notation—every page was transcribed directly from the folio images, preserving footnotes and marginal pagination (`.. folio::`).
3. **Multi-Track Book Codex Compilation (`scripts/build_docsrc.py`)**:
   Assembled into `docsrc/de_noetica_geometriae/` using `:layout: book` in `photon-platform/publish`:
   - **English Track (`_en.rst`)**: Complete English translation of the Praefatio, Chapters I–IX, Appendices, and Analytical Index.
   - **Latin Track (`_la.rst`)**: Diplomatic 1954 Latin text synchronized section-by-section with the English track.
   - **Summary & Notes Tracks (`_notes.rst`)**: Philosophical commentary and chapter syntheses.
4. **Scholarly Apparatus (`:cite:`, `:person:`, `:term:`)**:
   - Interactive prosopographical (`resources/persons.json`), bibliographic (`resources/citations.json`), and scholastic/mathematical glossary (`resources/glossary.json`) registries rendered with hover cards and compiled into standalone apparatus indices.

---

## Usage

```bash
# Launch the interactive Folio Reviewer on resources/de_noetica_geometriae/
publish folio

# Build and serve the multi-track Book Codex locally
publish test
```

## Related Projects

* **[GEOMETOR • euclid](https://github.com/geometor/euclid)** & **[GEOMETOR • elements](https://github.com/geometor/elements)**: Digital reconstruction of Euclid's *Elements* and the symbolic G-Index.
* **[GEOMETOR • pacioli](https://github.com/geometor/pacioli)**: Fra Luca Pacioli's *De Divina Proportione* (1509 / 1889).
* **[PHOTON • publish](https://github.com/photon-platform/publish)**: Sphinx Book Codex publishing engine and theme.
