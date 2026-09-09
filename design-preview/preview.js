/* The pages remain readable and navigable without JavaScript. */
(() => {
  document.documentElement.classList.add('preview-interactive');
  if (new URLSearchParams(location.search).get('embed') === '1') {
    document.documentElement.classList.add('embedded-preview');
  }
  const studySelect = document.querySelector('.study-select');
  if (studySelect) {
    studySelect.addEventListener('change', () => {
      location.assign(studySelect.value);
    });
  }
  const thumbnails = document.querySelectorAll('.iframe-crop');
  if (thumbnails.length && 'ResizeObserver' in window) {
    const sizePreviews = new ResizeObserver(entries => {
      for (const entry of entries) {
        const frame = entry.target.querySelector('iframe');
        frame.style.transform = `scale(${entry.contentRect.width / 1100})`;
      }
    });
    thumbnails.forEach(thumbnail => sizePreviews.observe(thumbnail));
  }
  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;
  function setTheme(dark) {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    toggle.textContent = dark ? 'Light' : 'Dark';
    toggle.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} theme`);
    toggle.setAttribute('aria-pressed', String(dark));
  }
  try {
    if (!document.documentElement.classList.contains('embedded-preview')) {
      setTheme(localStorage.getItem('academic-preview-theme') === 'dark');
    }
  } catch { setTheme(false); }
  toggle.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    setTheme(dark);
    try { localStorage.setItem('academic-preview-theme', dark ? 'dark' : 'light'); } catch { /* Optional preference. */ }
  });
})();
