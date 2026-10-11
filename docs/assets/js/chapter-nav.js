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
    // 1. Process Menu Bars & Sync Prev / Next buttons to Site Header
    // ------------------------------------------------------------------------
    const headerPrev = document.getElementById('header-prev');
    const headerNext = document.getElementById('header-next');
    const siteHeader = document.querySelector('.site-header');

    function updateHeaderOffset() {
      if (siteHeader) {
        if (window.innerWidth <= 640) {
          document.documentElement.style.setProperty('--header-height', '0px');
        } else {
          const rect = siteHeader.getBoundingClientRect();
          const h = Math.round(rect.height);
          document.documentElement.style.setProperty('--header-height', h + 'px');
        }
      }
    }

    const topBar = article.querySelector('blockquote:first-of-type');
    if (topBar) {
      topBar.classList.add('chapter-edition-bar');
    }

    function removeNavFromMenu(link) {
      const td = link.closest('td');
      if (td) {
        td.remove();
        return;
      }

      const parent = link.parentNode;

      // Clean trailing separator: e.g. " | "
      let next = link.nextSibling;
      while (next && next.nodeType === Node.TEXT_NODE && !next.textContent.trim()) {
        const toRemove = next;
        next = next.nextSibling;
        toRemove.remove();
      }
      if (next && next.nodeType === Node.TEXT_NODE) {
        next.textContent = next.textContent.replace(/^\s*\|\s*/, '');
        if (!next.textContent.trim()) {
          next.remove();
        }
      }

      // Clean leading separator: e.g. " | "
      let prev = link.previousSibling;
      while (prev && prev.nodeType === Node.TEXT_NODE && !prev.textContent.trim()) {
        const toRemove = prev;
        prev = prev.previousSibling;
        toRemove.remove();
      }
      if (prev && prev.nodeType === Node.TEXT_NODE) {
        prev.textContent = prev.textContent.replace(/\s*\|\s*$/, '');
        if (!prev.textContent.trim()) {
          prev.remove();
        }
      }

      link.remove();

      // Clean dangling pipes or whitespace at container edges
      if (parent) {
        if (parent.firstChild && parent.firstChild.nodeType === Node.TEXT_NODE) {
          parent.firstChild.textContent = parent.firstChild.textContent.replace(/^\s*\|\s*/, '');
          if (!parent.firstChild.textContent.trim()) {
            parent.firstChild.remove();
          }
        }
        if (parent.lastChild && parent.lastChild.nodeType === Node.TEXT_NODE) {
          parent.lastChild.textContent = parent.lastChild.textContent.replace(/\s*\|\s*$/, '');
          if (!parent.lastChild.textContent.trim()) {
            parent.lastChild.remove();
          }
        }
      }
    }

    // Remove any redundant bottom menu bar since top menu bar is sticky
    const allBlockquotes = Array.from(article.querySelectorAll('blockquote'));
    if (allBlockquotes.length > 1) {
      const bottomBar = allBlockquotes[allBlockquotes.length - 1];
      const hasNav = bottomBar.querySelector('a') && (
        bottomBar.textContent.includes('←') ||
        bottomBar.textContent.includes('→') ||
        bottomBar.textContent.includes('Latin') ||
        bottomBar.textContent.includes('English') ||
        bottomBar.textContent.includes('Summary') ||
        bottomBar.textContent.includes('Notes') ||
        bottomBar.textContent.includes('Model')
      );
      if (hasNav) {
        if (headerPrev && !headerPrev.hasChildNodes()) {
          const prevLink = Array.from(bottomBar.querySelectorAll('a')).find(a => a.textContent.includes('←'));
          if (prevLink) {
            const clone = prevLink.cloneNode(true);
            clone.className = 'header-nav-btn header-nav-prev-btn';
            headerPrev.innerHTML = '';
            headerPrev.appendChild(clone);
          }
        }
        if (headerNext && !headerNext.hasChildNodes()) {
          const nextLink = Array.from(bottomBar.querySelectorAll('a')).find(a => a.textContent.includes('→'));
          if (nextLink) {
            const clone = nextLink.cloneNode(true);
            clone.className = 'header-nav-btn header-nav-next-btn';
            headerNext.innerHTML = '';
            headerNext.appendChild(clone);
          }
        }

        const prevEl = bottomBar.previousElementSibling;
        if (prevEl && prevEl.tagName === 'HR') {
          prevEl.remove();
        }
        bottomBar.remove();
      }
    }

    if (topBar && (headerPrev || headerNext)) {
      const links = Array.from(topBar.querySelectorAll('a'));
      links.forEach(link => {
        const text = link.textContent.trim();
        if (text.includes('←')) {
          if (headerPrev && !headerPrev.hasChildNodes()) {
            const clone = link.cloneNode(true);
            clone.className = 'header-nav-btn header-nav-prev-btn';
            headerPrev.innerHTML = '';
            headerPrev.appendChild(clone);
          }
          removeNavFromMenu(link);
        } else if (text.includes('→')) {
          if (headerNext && !headerNext.hasChildNodes()) {
            const clone = link.cloneNode(true);
            clone.className = 'header-nav-btn header-nav-next-btn';
            headerNext.innerHTML = '';
            headerNext.appendChild(clone);
          }
          removeNavFromMenu(link);
        }
      });

      if (!topBar.textContent.trim()) {
        topBar.remove();
      }
    }

    updateHeaderOffset();
    window.addEventListener('resize', updateHeaderOffset);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(updateHeaderOffset);
    }

    // ------------------------------------------------------------------------
    // 2. Generate Clickable Nested Chapter Table of Contents (TOC)
    // ------------------------------------------------------------------------
    // Never run chapter TOC on the site home page
    const normPath = window.location.pathname.replace(/\/+$/, '');
    if (normPath === '' || normPath === '/hoenen' || normPath.endsWith('/index.html') && (normPath === '/index.html' || normPath === '/hoenen/index.html')) {
      return;
    }

    // Determine appropriate title, counts, and page type
    const path = window.location.pathname.toLowerCase();
    const isSummary = path.includes('summary') || Boolean(article.querySelector('h1')?.textContent.includes('AI SUMMARY'));
    const isNotes = path.includes('notes') || path.includes('benchmark') || Boolean(article.querySelector('h1')?.textContent.includes('TRANSLATION NOTES'));
    const isEnglish = path.includes('-en') || document.documentElement.lang === 'en' || isSummary || isNotes;

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

    let candidateHeadings = [];
    if (isSummary) {
      // On summary pages, the hierarchy begins at Executive Summary
      let startIndex = bodyHeadings.findIndex(h => /^executive\s+summary/i.test(h.textContent.trim()));
      if (startIndex === -1) startIndex = 0;
      candidateHeadings = bodyHeadings.slice(startIndex);
    } else if (isNotes) {
      // On translation notes, the hierarchy begins at the first numbered section
      let startIndex = bodyHeadings.findIndex(h => /^\d+\.\s+/.test(h.textContent.trim()));
      if (startIndex === -1) startIndex = 0;
      candidateHeadings = bodyHeadings.slice(startIndex);
    } else {
      // On chapter pages, find where the section outline begins
      let startIndex = bodyHeadings.findIndex(h => {
        const text = h.textContent.trim();
        return text.includes('§') || /^\d+\.\s+/.test(text) || /^(PART|PARS)\s+[IVXLCDM]+/i.test(text);
      });
      if (startIndex === -1) return;
      candidateHeadings = bodyHeadings.slice(startIndex);
    }

    if (candidateHeadings.length < 2) return;

    // Build the hierarchical outline tree (parents and nested children)
    const tree = [];
    let currentParent = null;

    if (isSummary || isNotes) {
      // On summaries and notes, H2 headings form top-level items, and H3/H4 form nested children
      candidateHeadings.forEach((heading, idx) => {
        if (!heading.id) {
          heading.id = 'sec-' + (idx + 1) + '-' + heading.textContent
            .trim()
            .toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-');
        }

        const lvl = parseInt(heading.tagName.substring(1), 10);
        if (lvl === 2) {
          currentParent = {
            heading: heading,
            isPart: false,
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
    } else {
      // On chapter pages, find base heading level of major sections
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
    }

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
          const subLvl = parseInt(sub.tagName.substring(1), 10);
          if (subLvl >= 4) subLi.classList.add('is-level-4');

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

    // Locate insertion point:
    // 1. On summary pages: place TOC outline before Executive Summary
    // 2. On other pages: place TOC outline right after the manuscript title block
    function findTitleEndElement() {
      const firstH1 = article.querySelector('h1');
      if (!firstH1) return null;

      let lastTitleElem = firstH1;
      let next = firstH1.nextElementSibling;

      while (next) {
        if (next.tagName === 'H1') {
          lastTitleElem = next;
          next = next.nextElementSibling;
          continue;
        }

        if (next.tagName === 'H2') {
          const text = next.textContent.trim();
          const isContentSection = text.includes('§') || 
                                   /^\d+\.\s+/.test(text) || 
                                   /^(PART|PARS)\s+[IVXLCDM]+/i.test(text) ||
                                   /^executive\s+summary/i.test(text) ||
                                   /^detailed\s+/i.test(text) ||
                                   /^analytical\s+/i.test(text) ||
                                   /^thematic\s+/i.test(text) ||
                                   /^conceptual\s+/i.test(text) ||
                                   /^scholarly\s+/i.test(text);
          if (!isContentSection) {
            lastTitleElem = next;
            next = next.nextElementSibling;
            continue;
          }
        }

        break;
      }

      return lastTitleElem;
    }

    if (isSummary) {
      const execHeading = bodyHeadings.find(h => /^executive\s+summary/i.test(h.textContent.trim()));
      if (execHeading && execHeading.parentNode) {
        execHeading.parentNode.insertBefore(nav, execHeading);
      } else {
        const lastTitle = findTitleEndElement();
        if (lastTitle && lastTitle.parentNode) {
          lastTitle.parentNode.insertBefore(nav, lastTitle.nextSibling);
        } else {
          candidateHeadings[0].parentNode.insertBefore(nav, candidateHeadings[0]);
        }
      }
    } else {
      const lastTitle = findTitleEndElement();
      if (lastTitle && lastTitle.parentNode) {
        lastTitle.parentNode.insertBefore(nav, lastTitle.nextSibling);
      } else {
        const firstSection = candidateHeadings[0];
        firstSection.parentNode.insertBefore(nav, firstSection);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChapterNavigation);
  } else {
    initChapterNavigation();
  }
})();
