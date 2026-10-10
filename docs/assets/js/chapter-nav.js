/**
 * chapter-nav.js
 * 
 * 1. Generates an interactive, clickable Table of Contents (Conspectus Capitis)
 *    at the top of each chapter from section headings (§ 1, § 2, etc.).
 * 2. Connects track-based [← Prev] and [Next →] links from the in-page menu bar
 *    into the sticky site header.
 */

(function() {
  'use strict';

  function initChapterNavigation() {
    const article = document.querySelector('article.manuscript');
    if (!article) return;

    // ------------------------------------------------------------------------
    // 1. Sync Prev / Next buttons to the Sticky Site Header
    // ------------------------------------------------------------------------
    const topBar = article.querySelector('blockquote:first-of-type');
    const headerPrev = document.getElementById('header-prev');
    const headerNext = document.getElementById('header-next');

    if (topBar && (headerPrev || headerNext)) {
      const links = topBar.querySelectorAll('a');
      links.forEach(link => {
        const text = link.textContent.trim();
        if (text.includes('←') && headerPrev) {
          const clone = link.cloneNode(true);
          clone.className = 'header-nav-btn header-nav-prev-btn';
          headerPrev.innerHTML = '';
          headerPrev.appendChild(clone);
        } else if (text.includes('→') && headerNext) {
          const clone = link.cloneNode(true);
          clone.className = 'header-nav-btn header-nav-next-btn';
          headerNext.innerHTML = '';
          headerNext.appendChild(clone);
        }
      });
    }

    // ------------------------------------------------------------------------
    // 2. Generate Clickable Chapter Table of Contents (TOC)
    // ------------------------------------------------------------------------
    // Find all section headings within the article
    const allHeadings = Array.from(article.querySelectorAll('h2, h3, h4'));
    
    // Filter for section headings (§ or numbered sections or Part divisions)
    const sectionHeadings = allHeadings.filter(h => {
      const text = h.textContent.trim();
      // Match § sections, e.g. "§ 1.", "§ 2"
      if (text.includes('§')) return true;
      // Match numbered sections, e.g. "1. Translation Criteria", "2. Critical Defect"
      if (/^\d+\.\s+/.test(text)) return true;
      // Match Part / Pars divisions
      if (/^(PART|PARS)\s+[IVXLCDM]+/i.test(text)) return true;
      return false;
    });

    if (sectionHeadings.length < 2) {
      return; // No TOC needed for pages without distinct sections
    }

    // Determine appropriate title based on language / context
    const path = window.location.pathname.toLowerCase();
    const isEnglish = path.includes('-en') || document.documentElement.lang === 'en';
    const isNotes = path.includes('notes') || path.includes('benchmark');
    const isSummary = path.includes('summary');

    let tocTitle = 'Conspectus Capitis';
    let countLabel = 'sectiones';
    if (isNotes) {
      tocTitle = isEnglish ? 'Apparatus & Section Index' : 'Index Argumentorum';
      countLabel = isEnglish ? 'sections' : 'sectiones';
    } else if (isSummary) {
      tocTitle = isEnglish ? 'Summary Outline' : 'Conspectus Argumentorum';
      countLabel = isEnglish ? 'sections' : 'sectiones';
    } else if (isEnglish) {
      tocTitle = 'Chapter Outline';
      countLabel = 'sections';
    }

    // Create TOC container element
    const nav = document.createElement('nav');
    nav.className = 'chapter-toc';
    nav.setAttribute('aria-label', tocTitle);

    const details = document.createElement('details');
    details.className = 'chapter-toc-details';
    details.open = true;

    const summary = document.createElement('summary');
    summary.className = 'chapter-toc-summary';
    summary.innerHTML = `
      <span class="chapter-toc-title">
        <span class="toc-icon">§</span>
        <span class="toc-text">${tocTitle}</span>
      </span>
      <span class="chapter-toc-badge">${sectionHeadings.length} ${countLabel}</span>
    `;
    details.appendChild(summary);

    const list = document.createElement('ol');
    list.className = 'chapter-toc-list';

    sectionHeadings.forEach((heading, idx) => {
      // Ensure heading has an ID
      if (!heading.id) {
        heading.id = 'section-' + (idx + 1) + '-' + heading.textContent
          .trim()
          .toLowerCase()
          .replace(/[^\w\s-]/g, '')
          .replace(/\s+/g, '-');
      }

      const li = document.createElement('li');
      li.className = 'chapter-toc-item';

      const a = document.createElement('a');
      a.href = '#' + heading.id;
      a.className = 'chapter-toc-link';
      
      // Clean display text (trim trailing notes marks or anchors)
      let cleanText = heading.textContent.trim().replace(/\s*\[\^\d+\]\s*/g, '');
      a.textContent = cleanText;

      li.appendChild(a);
      list.appendChild(li);
    });

    details.appendChild(list);
    nav.appendChild(details);

    // Place the TOC right before the first section heading
    const firstSection = sectionHeadings[0];
    firstSection.parentNode.insertBefore(nav, firstSection);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChapterNavigation);
  } else {
    initChapterNavigation();
  }
})();
