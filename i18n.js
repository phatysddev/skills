'use strict';
(() => {
  const preferences = window.PHAT_PREFERENCES;
  const dictionary = new Map();
  for (const [en, th] of window.PHAT_TRANSLATIONS) {
    dictionary.set(en, {en, th});
    dictionary.set(th, {en, th});
  }
  for (const [source, translations] of Object.entries(window.PHAT_TRANSLATION_ALIASES)) {dictionary.set(source, translations); dictionary.set(translations.en, translations); dictionary.set(translations.th, translations);}
  const records = new WeakMap();
  function translate(value) {
    const leading = value.match(/^\s*/)[0];
    const trailing = value.match(/\s*$/)[0];
    const key = value.trim();
    if (!key) return value;
    if (key.endsWith(' · Phat Skills')) return translate(key.slice(0, -14)) + ' · Phat Skills';
    const found = dictionary.get(key);
    if (found) return leading + found[preferences.language] + trailing;
    if (value.includes('\n')) return value.split('\n').map(translate).join('\n');
    if (/^พบ \d+ skills$/.test(key)) return preferences.language === 'en' ? `${key.match(/\d+/)[0]} skills found` : value;
    if (key.startsWith('คัดลอก ')) return translate('Copy') + ' ' + translate(key.slice('คัดลอก '.length));
    if (/^Open .+\/SKILL.md ↗$/.test(key)) return preferences.language === 'th' ? key.replace('Open ', 'เปิด ') : value;
    return value;
  }
  function remember(node, key, value) {
    let record = records.get(node);
    if (!record) {record = new Map(); records.set(node, record);}
    let entry = record.get(key);
    if (!entry || entry.output !== value) entry = {source:value};
    entry.output = translate(entry.source);
    record.set(key, entry);
    return entry.output;
  }
  function localize(root = document.body) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.parentElement.closest('script,style,noscript,[translate="no"]')) continue;
      const output = remember(node, 'text', node.nodeValue);
      if (output !== node.nodeValue) node.nodeValue = output;
    }
    for (const node of root.querySelectorAll('[aria-label],[placeholder],[title],[data-copy]')) {
      for (const attribute of ['aria-label','placeholder','title','data-copy']) {
        if (node.hasAttribute(attribute)) node.setAttribute(attribute, remember(node, attribute, node.getAttribute(attribute)));
      }
    }
    document.title = remember(document.documentElement, 'title', document.title);
  }
  window.PHAT_I18N = {translate, localize, searchText(value) {const entry = dictionary.get(value); return entry ? `${entry.en} ${entry.th}` : value;}};
  const languageSelect = document.querySelector('#language-select');
  const themeSelect = document.querySelector('#theme-select');
  languageSelect.value = preferences.language;
  themeSelect.value = preferences.theme;
  languageSelect.addEventListener('change', () => {
    preferences.language = languageSelect.value;
    preferences.save('phat-language', preferences.language);
    document.documentElement.lang = preferences.language;
    localize();
    // Search matches both languages; rerender it to keep results and live counts current.
    document.querySelector('#skill-search')?.dispatchEvent(new Event('input'));
    document.querySelector('#docs-search')?.dispatchEvent(new Event('input'));
  });
  themeSelect.addEventListener('change', () => {
    preferences.theme = themeSelect.value;
    preferences.save('phat-theme', preferences.theme);
    preferences.applyTheme(preferences.theme);
  });
})();
