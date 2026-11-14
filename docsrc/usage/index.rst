:navigation: header
:order: 20
:nav_title: Usage

Using This Edition
==================

.. rubric:: Reader's Guide to the Digital Bilingual Edition of *De Noetica Geometriae*

This critical digital edition of Father Peter Hoenen, S.J.'s *De Noetica Geometriae: Origine Theoriae Cognitionis* (Analecta Gregoriana, Vol. LXIII, Rome: Gregorian University, 1954) provides interactive scholarly apparatus, parallel Latin–English reading tracks, and complete bibliographic cross-references.

Reader Features
---------------

1. Synchronized Reading Tracks
   Switch seamlessly between reading tracks using the book codex header:
   
   * **Editio Latina (1954)**: Complete transcription of the original Latin text with Hoenen's scholastic terminology, mathematical symbols, and Greek citations.
   * **English Translation**: Modern scholarly English translation preserving technical distinctions (:term:`abstractio formalis <abstractio-formalis>`, :term:`materia intelligibilis <materia-intelligibilis>`, *esse in potentia*).
   * **Unit Summaries & Notes**: Detailed philosophical summaries and philological translation notes analyzing Hoenen's engagement with classical and modern thinkers.

2. Primary-Source Folio Milestones
   Marginal page markers (such as ``[p. 1]`` through ``[p. 299]``) mark exact page breaks corresponding to the 1954 *Analecta Gregoriana* edition. Clicking header **Folio** badges or marginal markers links directly to archival scans.

3. Interactive Diagrams & Deductive Links
   All geometrical and philosophical arguments (including the problem of indivisibles, the triangle bridge, and axiomatic configurations) are cross-referenced across chapters, notes, and the analytical index.

4. Full-Text Search with In-Page Highlighting
   Use the search bar in the sidebar or top header to search across both the Latin text and English translation. Results automatically open the target page with query terms highlighted in context.

5. Faceted Navigation & Collection Views
   Browse chapters, topics, and editorial logs via the sidebar taxonomy. The analytical index and logs support **Cards**, **Banners**, and **List** view toggles.

6. People, Bibliography & Glossary Tooltips
   Hovering over any historical person (:person:`Peter Hoenen <hoenen>`, :person:`Aristotle <aristotle>`, :person:`Thomas Aquinas <aquinas>`, :person:`David Hilbert <hilbert>`, :person:`Bertrand Russell <russell>`), citation (:cite:`Aristotle's Posterior Analytics <aristotle-anal-post>`, :cite:`Hoenen (1937) <hoenen-1937>`), or scholastic term (:term:`abstractio formalis <abstractio-formalis>`, :term:`materia intelligibilis <materia-intelligibilis>`, :term:`phantasma <phantasma>`) surfaces rich tooltip cards.

----

Archival Processing Pipeline
----------------------------

The digital edition is assembled from archival scans via a multi-stage Python pipeline:

.. code-block:: bash

   # 1. Extract and normalize archival page images (p001.png - p299.png)
   python3 src/geometor/hoenen/extract_pages.py

   # 2. Transcribe Latin & Greek text with structural RST markup
   python3 src/geometor/hoenen/transcribe_pages.py

   # 3. Generate scholarly English translations per page
   python3 src/geometor/hoenen/translate_pages.py

   # 4. Assemble the de-paginated bilingual Book Codex & apparatus
   python3 src/geometor/hoenen/build_book_codex.py

   # 5. Build the HTML documentation into docs/
   publish build
