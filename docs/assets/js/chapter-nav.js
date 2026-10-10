/**
 * chapter-nav.js
 * 
 * 1. Generates an interactive, nested clickable Table of Contents (Conspectus Capitis)
 *    at the top of each chapter spanning two balanced columns.
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
    // 2. Generate Clickable Nested Chapter Table of Contents (TOC)
    // ------------------------------------------------------------------------
    // Never run chapter TOC on the site home page
    const normPath = window.location.pathname.replace(/\/+$/, '');
    if (normPath === '' || normPath === '/hoenen' || normPath.endsWith('/index.html') && (normPath === '/index.html' || normPath === '/hoenen/index.html')) {
      return;
    }

    // Find all headings within the article
    const allHeadings = Array.from(article.querySelectorAll('h2, h3, h4, h5'));
    
    // Filter out metadata, footnotes, apparatus footnotes
    const bodyHeadings = allHeadings.filter(h => {
      const text = h.textContent.trim().toLowerCase();
      if (text.includes('footnotes')) return false;
      if (text === 'scholarly apparatus' || text === 'scholarly notes') return false;
      return true;
    });

    if (bodyHeadings.length === 0) return;

    // Find where the actual section outline begins (first heading with §, numbered section, or Part)
    let startIndex = bodyHeadings.findIndex(h => {
      const text = h.textContent.trim();
      return text.includes('§') || /^\d+\.\s+/.test(text) || /^(PART|PARS)\s+[IVXLCDM]+/i.test(text);
    });

    // Only generate outline on chapters with explicit sections (§, numbered sections, or Part)
    if (startIndex === -1) return;

    const candidateHeadings = bodyHeadings.slice(startIndex);
    if (candidateHeadings.length < 2) return;

    // Build the hierarchical outline tree (parents and nested children)
    const tree = [];
    let currentParent = null;

    // Find the base heading level of major sections
    let minSectionLevel = 6;
    candidateHeadings.forEach(h => {
      const lvl = parseInt(h.tagName.substring(1), 10);
      const text = h.textContent.trim();
      if (text.includes('§') || /^(PART|PARS)\s+/i.test(text) || /^\d+\.\s+/.test(text)) {
        if (lvl < minSectionLevel) minSectionLevel = lvl;
      }
    });
    if (minSectionLevel === 6) minSectionLevel = 2;

    candidateHeadings.forEach((heading, idx) => {
      // Ensure heading has an anchor ID
      if (!heading.id) {
        heading.id = 'sec-' + (idx + 1) + '-' + heading.textContent
          .trim()
          .toLowerCase()
          .replace(/[^\w\s-]/g, '')
          .replace(/\s+/g, '-');
      }

      const lvl = parseInt(heading.tagName.substring(1), 10);
      const text = heading.textContent.trim();
      const isPart = /^(PART|PARS)\s+[IVXLCDM]+/i.test(text);
      const hasSectionMark = text.includes('§');
      const isTopLevel = isPart || hasSectionMark || (lvl <= minSectionLevel);

      if (isTopLevel) {
        currentParent = {
          heading: heading,
          isPart: isPart,
          children: []
        };
        tree.push(currentParent);
      } else if (currentParent) {
        currentParent.children.push(heading);
      } else {
        currentParent = {
          heading: heading,
          isPart: false,
          children: []
        };
        tree.push(currentParent);
      }
    });

    // Determine appropriate title and counts
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

    // Count total subsections if any
    let totalSubsections = 0;
    tree.forEach(p => { totalSubsections += p.children.length; });

    let badgeText = `${tree.length} ${countLabel}`;
    if (totalSubsections > 0) {
      badgeText = isEnglish 
        ? `${tree.length} sections (${totalSubsections} sub)` 
        : `${tree.length} sectiones (${totalSubsections} sub)`;
    }

    // Create TOC container
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
      <span class="chapter-toc-badge">${badgeText}</span>
    `;
    details.appendChild(summary);

    const list = document.createElement('ol');
    list.className = 'chapter-toc-list';

    tree.forEach(node => {
      const li = document.createElement('li');
      li.className = 'chapter-toc-item';
      if (node.isPart) li.classList.add('is-part-header');
      if (node.children.length > 0) li.classList.add('has-subsections');

      const a = document.createElement('a');
      a.href = '#' + node.heading.id;
      a.className = 'toc-parent-link';
      a.textContent = node.heading.textContent.trim().replace(/\s*\[\^\d+\]\s*/g, '');
      li.appendChild(a);

      // Render nested subsections
      if (node.children.length > 0) {
        const subList = document.createElement('ul');
        subList.className = 'chapter-toc-sublist';

        node.children.forEach(sub => {
          const subLi = document.createElement('li');
          subLi.className = 'chapter-toc-subitem';

          const subA = document.createElement('a');
          subA.href = '#' + sub.id;
          subA.className = 'toc-sub-link';
          subA.textContent = sub.textContent.trim().replace(/\s*\[\^\d+\]\s*/g, '');

          subLi.appendChild(subA);
          subList.appendChild(subLi);
        });

        li.appendChild(subList);
      }

      list.appendChild(li);
    });

    details.appendChild(list);
    nav.appendChild(details);

    // Insert TOC before the first section heading
    const firstSection = candidateHeadings[0];
    firstSection.parentNode.insertBefore(nav, firstSection);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChapterNavigation);
  } else {
    initChapterNavigation();
  }
})();
