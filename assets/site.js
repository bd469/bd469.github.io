(() => {
  'use strict';
  document.getElementById('year').textContent = new Date().getFullYear();

  // Keep old inbound links working without replacing native page navigation.
  const aliases = {
    resume: 'cv', education: 'cv', skills: 'cv',
    experience: 'industry-experience', 'financial-engineering': 'industry-experience',
    research: 'publications', 'papers-panel': 'publications', 'research-panel': 'publications'
  };
  function revealHashTarget() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(aliases[id] || id);
    if (!target) return;
    let ancestor = target.parentElement;
    let expanded = false;
    while (ancestor) {
      if (ancestor.tagName === 'DETAILS' && !ancestor.open) {
        ancestor.open = true;
        expanded = true;
      }
      ancestor = ancestor.parentElement;
    }
    if (aliases[id] || expanded) target.scrollIntoView({ block: 'start' });
  }
  window.addEventListener('hashchange', revealHashTarget);
  revealHashTarget();

  const dialog = document.getElementById('cat-dialog');
  const photos = [...document.querySelectorAll('.cat-photo')];
  const dialogImage = document.getElementById('cat-dialog-image');
  let currentCat = 0;
  function displayCat(index) {
    currentCat = (index + photos.length) % photos.length;
    const photo = photos[currentCat];
    dialogImage.src = photo.href;
    dialogImage.alt = photo.querySelector('img').alt;
    document.getElementById('cat-dialog-title').textContent = photo.dataset.caption;
    document.getElementById('cat-dialog-number').textContent = `${currentCat + 1} / ${photos.length}`;
  }
  if (typeof dialog.showModal === 'function') {
    photos.forEach((photo, index) => photo.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      displayCat(index);
      dialog.showModal();
    }));
    dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
    document.getElementById('previous-cat').addEventListener('click', () => displayCat(currentCat - 1));
    document.getElementById('next-cat').addEventListener('click', () => displayCat(currentCat + 1));
    dialog.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        displayCat(currentCat + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    dialog.addEventListener('click', event => {
      const r = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) dialog.close();
    });
  }
})();
