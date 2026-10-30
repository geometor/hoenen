:navigation: header
:order: 20

=====
usage
=====

``geometor.hoenen`` implements a 4-stage pipeline to transform the 299-page 1954 archival scan of *De Noetica Geometriae* into a synchronized bilingual Book Codex.

Pipeline Scripts
----------------

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
