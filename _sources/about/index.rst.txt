:navigation: header
:order: 10
:nav_title: About

.. _about:
.. _about-index:

About
=====

.. rubric:: Extracting Historical Semantic Knowledge & Repurposing It for Exact Symbolic Reasoning

About This Edition
------------------

``geometor.hoenen`` is a digital critical edition, multi-track parallel translation, and semantic epistemological apparatus dedicated to Peter Hoenen, S.J.'s (1880–1961) masterwork, *De Noetica Geometriae: Origine Theoriae Cognitionis* (*Analecta Gregoriana*, Vol. LXIV, Romae: Apud Aedes Universitatis Gregorianae, 1954). Trained in theoretical physics under Nobel laureate H. A. Lorentz at Leiden before holding the chair of natural philosophy and epistemology at the Pontifical Gregorian University, Fr. Hoenen formulated a definitive defense of geometric intuition (*abstractio formalis intuitiva*), demonstrating that necessity in mathematics arises not from arbitrary logistical conventions but from direct intellectual apprehension within sensible presentations (*phantasmata* and *materia intelligibilis*).

This edition reconstructs Hoenen's treatise as an interactive multi-track **Book Codex** powered by ``photon-platform/publish``. Every chapter (Caput I–VII and Appendix) provides track-synchronized navigation across four parallel representations: *Editio Latina* (scrupulously transcribed and collated from the 1954 Rome editio princeps), *English Translation* (curated for philosophical accuracy and mathematical clarity), *Summaries* (succinct scholastic and epistemological abstracts), and *Translation Notes* (critical philological, historical, and mathematical apparatus). Interleaved throughout the text are structured semantic anchors linking directly to an exhaustive :doc:`Index Nominum </de_noetica_geometriae/people/index>`, a comprehensive :doc:`Bibliographia </de_noetica_geometriae/bibliography>`, and a technical Latin-Greek philosophical :ref:`Glossarium <glossary>`.

By formalizing Hoenen's dialogues with Euclid, Aristotle, Thomas Aquinas, Descartes, Kant, Poincaré, Hilbert, and Russell, ``geometor.hoenen`` bridges classical scholastic epistemology with modern mathematical axiomatics. It provides foundational philosophical grounding for sister GEOMETOR repositories—including ``geometor.elements``, ``geometor.model``, and ``geometor.klein``—clarifying how symbolic models and axiomatic formalisms remain rooted in intuitive geometric reality.

The GEOMETOR Mission
--------------------

The **GEOMETOR** initiative, conceived and directed by **phi ARCHITECT**, is dedicated to the systematic recovery, symbolic formalization, and creative re-articulation of humanity's geometric heritage. GEOMETOR unites classical synthesis with modern algebraic rigor across three core pillars:

Extracting Historical Semantic Knowledge
    Moving beyond passive page scans, static facsimile bitmaps, and flat optical character recognition (OCR), GEOMETOR recovers the living deductive architecture of 2,300+ years of geometric, axiomatic, and philosophical treatises. Primary sources—spanning Euclid, Apollonius, Archimedes, Pappus, Johannes Kepler, Felix Klein, and Clark Kimberling—are analyzed to elevate enunciations, deductive steps, synthetic justifications, marginal citations, primary-source folios (via ``publish folio``), and calibrated Ink-to-Vector ``.euclid-graphic`` diagrams into structured, machine-addressable semantic graphs.

Exact Symbolic Grounding (``geometor.model``)
    Geometric constructions must not depend on floating-point approximations or visual artifacts. GEOMETOR anchors geometric entities in 100% exact symbolic algebra via `SymPy <https://www.sympy.org/>`_ and the principles of Rational Trigonometry (quadrance, spread, cross-ratio). Points, lines, circles, and conic loci are evaluated over exact algebraic fields, ensuring that tangencies, incidences, harmonic conjugates, and collinearities represent absolute mathematical truths rather than numerical estimates.

Repurposing Knowledge Across Mediums
    Extracted semantic architectures and exact symbolic models are re-deployed across a unified digital ecosystem: synchronized multi-track **Book Codices** and EPUB 3 editions powered by ``photon-platform/publish``, computable deductive canons (``geometor.elements``, ``geometor.etc``, ``geometor.pappus``, ``geometor.divine``), interactive SVG exploration laboratories (``geometor.explorer``), ultra-high-definition visual broadcasts, and neuro-symbolic program synthesis (``geometor.seer``) across `geometor.com <https://geometor.com>`_.

Sources, Provenance & Methodology
---------------------------------

* **Archival Text**: Petrus H. J. Hoenen, S.J., *De Noetica Geometriae: Origine Theoriae Cognitionis*, *Analecta Gregoriana*, Vol. LXIV, Series Facultatis Philosophicae, Sectio A (n. 5), Romae: Apud Aedes Universitatis Gregorianae, 1954.
* **Institutional Provenance**: Pontifical Gregorian University (*Pontificia Universitas Gregoriana*), Rome.
* **Scan Processing & OCR Pipeline**: 600 DPI monochrome thresholded scans processed via customized OCR pipelines, manual scholastic Latin proofreading, and syntactic normalization as documented in the :ref:`PDF Parsing Guide <about-pdf-parsing-guide>`.
* **Digital Scriptorium Methodology**: Reconstructed and typeset by **phi ARCHITECT** using Sphinx, Python, and the ``photon-platform/publish`` Book Codex framework.

Historical & Editorial Monographs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`Fr. Peter Hoenen, S.J. (1880–1961) <about-peter-hoenen>` — Biography, academic training under Lorentz, and philosophical contributions.
* :ref:`Analecta Gregoriana <about-analecta-gregoriana>` — History and editorial scope of the Gregorian monograph series.
* :ref:`Pontifical Gregorian University <about-gregorian-university>` — Historical context of the Gregorian University in Rome.
* :ref:`PDF Parsing & Extraction Guide <about-pdf-parsing-guide>` — Reproduction guide for scan acquisition, chapter slicing, and OCR workflows.

.. toctree::
   :maxdepth: 1
   :hidden:

   peter-hoenen
   analecta-gregorian
   pontifical-gregorian-university
   pdf-parsing-guide
