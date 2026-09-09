/* Theme preference is optional; all content and navigation work without JS. */
(() => {
  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;
  function setTheme(dark) {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    toggle.textContent = dark ? 'Light' : 'Dark';
    toggle.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} theme`);
    toggle.setAttribute('aria-pressed', String(dark));
  }
  try { setTheme(localStorage.getItem('academic-theme') === 'dark'); }
  catch { setTheme(false); }
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    setTheme(dark);
    try { localStorage.setItem('academic-theme', dark ? 'dark' : 'light'); }
    catch { /* The page works when browser storage is unavailable. */ }
  });
})();
