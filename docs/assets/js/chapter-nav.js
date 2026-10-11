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
    // 1. Build Header Navigation from Centralized JSON Data
    // ------------------------------------------------------------------------
    const siteHeader = document.querySelector('.site-header');
    const headerDocRow = document.getElementById('header-doc-row');
    const headerDocTitle = document.getElementById('header-doc-title');
    const headerPrev = document.getElementById('header-prev');
    const headerNext = document.getElementById('header-next');
    const headerTracks = document.getElementById('header-tracks');

    function updateHeaderOffset() {
      if (siteHeader) {
        const h = Math.round(siteHeader.getBoundingClientRect().height);
        document.documentElement.style.setProperty('--header-height', h + 'px');
      }
    }

    // Load navigation data from embedded script or fallback to fetch
    let navData = null;
    const navScript = document.getElementById('nav-data');
    if (navScript && navScript.textContent.trim()) {
      try {
        navData = JSON.parse(navScript.textContent);
      } catch (e) {
        console.warn('Could not parse embedded nav data:', e);
      }
    }

    function renderHeaderNav(data) {
      if (!data || !data.chapters || !headerDocRow || !headerDocTitle) {
        updateHeaderOffset();
        return;
      }

      const baseUrl = window.HOENEN_BASE_URL !== undefined 
        ? window.HOENEN_BASE_URL 
        : (window.location.pathname.startsWith('/hoenen') ? '/hoenen' : '');

      let currentPath = window.location.pathname;
      if (baseUrl && currentPath.startsWith(baseUrl)) {
        currentPath = currentPath.slice(baseUrl.length);
      }
      currentPath = currentPath.replace(/^\/+|\/+$/g, '').replace(/\.(html|md)$/, '');

      let currentChapter = null;
      let currentIndex = -1;
      let currentTrack = null;

      for (let i = 0; i < data.chapters.length; i++) {
        const ch = data.chapters[i];
        for (const [tKey, tData] of Object.entries(ch.tracks)) {
          const p = (tData.path || '').replace(/^\/+|\/+$/g, '').replace(/\.(html|md)$/, '');
          const s = (tData.src || '').replace(/^\/+|\/+$/g, '').replace(/\.(html|md)$/, '');
          if (currentPath === p || currentPath === s || currentPath.endsWith(p) || currentPath.endsWith(s)) {
            currentChapter = ch;
            currentIndex = i;
            currentTrack = tKey;
            break;
          }
        }
        if (currentChapter) break;
      }

      if (!currentChapter) {
        // Standalone or index page: keep Level 2 & 3 hidden
        headerDocRow.style.display = 'none';
        if (headerTracks) headerTracks.style.display = 'none';
        updateHeaderOffset();
        return;
      }

      // Display Level 2 (Sequence Row) and Level 3 (Tracks Submenu)
      headerDocRow.style.display = 'grid';
      if (headerTracks) headerTracks.style.display = 'flex';

      // 1. Current Document Title
      const docTitle = currentTrack === 'latin' ? currentChapter.title_la : currentChapter.title;
      headerDocTitle.textContent = docTitle;

      // 2. Previous Button
      let prevCh = null;
      for (let i = currentIndex - 1; i >= 0; i--) {
        if (data.chapters[i].tracks[currentTrack]) {
          prevCh = data.chapters[i];
          break;
        }
      }
      if (prevCh && prevCh.tracks[currentTrack]) {
        const prevLabel = currentTrack === 'latin' ? prevCh.title_la : prevCh.title;
        const prevPath = prevCh.tracks[currentTrack].path;
        headerPrev.innerHTML = `
          <a href="${baseUrl}/${prevPath}" class="header-nav-btn header-nav-prev-btn" title="Previous: ${prevLabel}">
            <span class="nav-arrow">←</span>
            <span class="nav-label">${prevLabel}</span>
          </a>
        `.trim();
      } else {
        headerPrev.innerHTML = '';
      }

      // 3. Next Button
      let nextCh = null;
      for (let i = currentIndex + 1; i < data.chapters.length; i++) {
        if (data.chapters[i].tracks[currentTrack]) {
          nextCh = data.chapters[i];
          break;
        }
      }
      if (nextCh && nextCh.tracks[currentTrack]) {
        const nextLabel = currentTrack === 'latin' ? nextCh.title_la : nextCh.title;
        const nextPath = nextCh.tracks[currentTrack].path;
        headerNext.innerHTML = `
          <a href="${baseUrl}/${nextPath}" class="header-nav-btn header-nav-next-btn" title="Next: ${nextLabel}">
            <span class="nav-label">${nextLabel}</span>
            <span class="nav-arrow">→</span>
          </a>
        `.trim();
      } else {
        headerNext.innerHTML = '';
      }

      // 4. Submenu Tracks
      if (headerTracks) {
        const trackOrder = data.track_order || ['latin', 'english', 'summary', 'notes'];
        const items = [];
        for (const tKey of trackOrder) {
          if (currentChapter.tracks[tKey]) {
            const tData = currentChapter.tracks[tKey];
            if (tKey === currentTrack) {
              items.push(`<span class="header-track-item is-active" aria-current="page">${tData.label}</span>`);
            } else {
              items.push(`<a href="${baseUrl}/${tData.path}" class="header-track-item">${tData.label}</a>`);
            }
          }
        }
        headerTracks.innerHTML = items.join('<span class="header-track-sep">·</span>');
      }

      // Clean any residual in-page navigation blockquotes
      const topBar = article.querySelector('blockquote:first-of-type');
      if (topBar && (
        topBar.textContent.includes('Latin') ||
        topBar.textContent.includes('English') ||
        topBar.textContent.includes('Summary') ||
        topBar.textContent.includes('Notes')
      )) {
        const nextEl = topBar.nextElementSibling;
        if (nextEl && nextEl.tagName === 'HR') nextEl.remove();
        topBar.remove();
      }

      updateHeaderOffset();
      window.addEventListener('resize', updateHeaderOffset);
      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(updateHeaderOffset);
      }
    }

    if (navData) {
      renderHeaderNav(navData);
    } else {
      const baseUrl = window.HOENEN_BASE_URL !== undefined 
        ? window.HOENEN_BASE_URL 
        : (window.location.pathname.startsWith('/hoenen') ? '/hoenen' : '');
      fetch(`${baseUrl}/assets/data/navigation.json`)
        .then(res => res.json())
        .then(renderHeaderNav)
        .catch(err => {
          console.warn('Could not fetch navigation data:', err);
          updateHeaderOffset();
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
