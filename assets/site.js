(() => {
  'use strict';
  const sections = [...document.querySelectorAll('.page-section')];
  const navigation = document.querySelector('.primary-nav');
  const menu = document.querySelector('.menu-toggle');
  const tabs = [...document.querySelectorAll('[data-view]')];
  const baseTitle = 'Beixi Du (Chloe)';
  const aliases = { resume: 'cv', education: 'cv', skills: 'cv', experience: 'financial-engineering', 'coinbase-project': 'financial-engineering' };
  const titles = {about:'Cornell University', publications:'Publications', research:'Research', 'financial-engineering':'Financial Engineering', cats:'Life with Cats', cv:'Curriculum Vitae'};
  document.body.classList.add('enhanced');
  menu.hidden = false;
  document.querySelector('.subnav').hidden = false;
  document.querySelectorAll('.subpanel').forEach(panel => panel.setAttribute('role', 'tabpanel'));
  document.getElementById('year').textContent = new Date().getFullYear();

  function closeMenu() {
    navigation.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
  }
  function showPage({ focus = false } = {}) {
    const raw = location.hash.slice(1);
    const route = aliases[raw] || (Object.hasOwn(titles, raw) ? raw : 'about');
    const sectionId = route === 'research' ? 'publications' : route;
    sections.forEach(section => { section.hidden = section.id !== sectionId; });
    navigation.querySelectorAll('a').forEach(link => {
      if (link.hash === '#' + sectionId) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    const view = route === 'research' ? 'research' : 'papers';
    tabs.forEach(tab => {
      const selected = tab.dataset.view === view;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !selected;
    });
    document.title = `${baseTitle} | ${titles[route]}`;
    closeMenu();
    if (focus) {
      document.getElementById(sectionId).querySelector('.page-title').focus({ preventScroll: true });
      window.scrollTo({top: 0, behavior: 'instant'});
    }
  }
  function navigate(hash, { focus = true } = {}) {
    if (location.hash !== hash) history.pushState(null, '', hash);
    showPage({focus});
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const route = link.hash.slice(1);
    if (route === 'main') {
      event.preventDefault();
      document.getElementById('main').focus();
      return;
    }
    if (!Object.hasOwn(titles, route) && !Object.hasOwn(aliases, route)) return;
    event.preventDefault();
    navigate(link.hash);
  });
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && navigation.classList.contains('is-open')) { closeMenu(); menu.focus(); }
  });
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
      navigate(tab.dataset.view === 'research' ? '#research' : '#publications', { focus: false });
      tab.focus();
    });
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      tabs[next].click();
    });
  });
  window.addEventListener('popstate', () => showPage());
  window.addEventListener('hashchange', () => showPage());
  showPage();

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
