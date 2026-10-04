/* Run before styles load to avoid flashing the wrong theme. */
(() => {
  const read = (key) => { try { return localStorage.getItem(key); } catch { return null; } };
  const savedTheme = read('phat-theme');
  const savedLanguage = read('phat-language');
  const theme = ['light', 'dark', 'system'].includes(savedTheme) ? savedTheme : 'system';
  const language = ['th', 'en'].includes(savedLanguage) ? savedLanguage : (navigator.language?.startsWith('th') ? 'th' : 'en');
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  function applyTheme(value) {
    document.documentElement.dataset.theme = value === 'system' ? (system.matches ? 'dark' : 'light') : value;
    document.documentElement.dataset.themePreference = value;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = document.documentElement.dataset.theme === 'dark' ? '#141b18' : '#f7f8f2';
  }
  window.PHAT_PREFERENCES = {theme, language, applyTheme, save(key, value) {try { localStorage.setItem(key, value); } catch { /* Session controls still work when storage is unavailable. */ }}};
  document.documentElement.lang = language;
  applyTheme(theme);
  system.addEventListener('change', () => {if(window.PHAT_PREFERENCES.theme === 'system') applyTheme('system');});
})();
