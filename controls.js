'use strict';
(() => {
  const {translate, localize} = window.PHAT_I18N;
  const icons = {
    language: '<circle cx="10" cy="10" r="7.2"/><path d="M2.8 10h14.4M10 2.8c4 4 4 10.4 0 14.4-4-4-4-10.4 0-14.4Z"/>',
    system: '<rect x="2.5" y="3.5" width="15" height="10" rx="1.5"/><path d="M7 17h6m-3-3.5V17"/>',
    light: '<circle cx="10" cy="10" r="3.5"/><path d="M10 1.5v2m0 13v2m8.5-8.5h-2m-13 0h-2m14.5-6-1.4 1.4M5.4 14.6 4 16m12 0-1.4-1.4M5.4 5.4 4 4"/>',
    dark: '<path d="M16.7 12.2A7.2 7.2 0 0 1 7.8 3.3a7.2 7.2 0 1 0 8.9 8.9Z"/>',
    chevron: '<path d="m6 8 4 4 4-4"/>',
    check: '<path d="m4 10 4 4 8-8"/>',
    close: '<path d="m6 6 8 8m0-8-8 8"/>'
  };
  const icon = name => `<svg viewBox="0 0 20 20" fill="none" aria-hidden="true">${icons[name]}</svg>`;
  const controls = [];
  let openControl;

  // Keep the native select as the value source and no-JavaScript fallback.
  for (const select of document.querySelectorAll('.preferences select')) {
    const wrapper = select.parentElement;
    const isLanguage = select.id === 'language-select';
    const options = [...select.options];
    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'select-trigger';
    trigger.id = `${select.id}-trigger`;
    trigger.setAttribute('role', 'combobox');
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.setAttribute('aria-controls', `${select.id}-listbox`);
    trigger.setAttribute('aria-labelledby', `${isLanguage ? 'language' : 'theme'}-label ${select.id}-value`);
    trigger.innerHTML = `<span class="select-icon">${icon(isLanguage ? 'language' : select.value)}</span><span class="select-value" id="${select.id}-value"></span><span class="select-chevron">${icon('chevron')}</span>`;

    const listbox = document.createElement('div');
    listbox.className = 'select-listbox';
    listbox.id = `${select.id}-listbox`;
    listbox.setAttribute('role', 'listbox');
    listbox.setAttribute('aria-labelledby', `${isLanguage ? 'language' : 'theme'}-label`);
    listbox.hidden = true;
    const items = options.map((option, index) => {
      const item = document.createElement('div');
      item.className = 'select-option';
      item.id = `${select.id}-option-${option.value}`;
      item.setAttribute('role', 'option');
      item.innerHTML = `<span class="option-icon">${isLanguage ? `<span class="language-code" translate="no">${option.value.toUpperCase()}</span>` : icon(option.value)}</span><span class="option-label"></span><span class="option-check">${icon('check')}</span>`;
      item.addEventListener('pointermove', () => setActive(index));
      // Focus stays on the combobox; aria-activedescendant tracks the option.
      item.addEventListener('pointerdown', event => event.preventDefault());
      item.addEventListener('click', () => choose(index));
      listbox.append(item);
      return item;
    });
    let active = select.selectedIndex;
    let typeahead = '';
    let typedAt = 0;

    function setActive(index) {
      active = (index + options.length) % options.length;
      items.forEach((item, i) => item.classList.toggle('is-active', i === active));
      if (!listbox.hidden) trigger.setAttribute('aria-activedescendant', items[active].id);
    }
    function sync() {
      trigger.querySelector('.select-value').textContent = translate(options[select.selectedIndex].textContent);
      trigger.querySelector('.select-icon').innerHTML = icon(isLanguage ? 'language' : select.value);
      items.forEach((item, i) => {
        item.querySelector('.option-label').textContent = isLanguage && options[i].value === 'en' ? 'English' : translate(options[i].textContent);
        item.setAttribute('aria-selected', String(i === select.selectedIndex));
      });
    }
    function close() {
      listbox.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
      trigger.removeAttribute('aria-activedescendant');
      wrapper.classList.remove('is-open');
      typeahead = '';
      if (openControl === control) openControl = null;
    }
    function open(index = select.selectedIndex) {
      if (openControl && openControl !== control) openControl.close();
      listbox.hidden = false;
      trigger.setAttribute('aria-expanded', 'true');
      wrapper.classList.add('is-open');
      openControl = control;
      setActive(index);
    }
    function choose(index) {
      const changed = select.selectedIndex !== index;
      select.selectedIndex = index;
      close();
      if (changed) select.dispatchEvent(new Event('change', {bubbles:true}));
      sync();
      trigger.focus({preventScroll:true});
    }
    const control = {wrapper, close, sync};
    controls.push(control);
    trigger.addEventListener('click', () => listbox.hidden ? open() : close());
    trigger.addEventListener('keydown', event => {
      const {key} = event;
      if (key === 'Tab') {close(); return;}
      if (key === 'Escape') {
        if (!listbox.hidden) {event.preventDefault(); event.stopPropagation(); close();}
        return;
      }
      if (['ArrowDown', 'ArrowUp', 'Home', 'End', 'Enter', ' '].includes(key)) {
        event.preventDefault();
        event.stopPropagation();
        if (key === 'Enter' || key === ' ') {listbox.hidden ? open() : choose(active);}
        else if (key === 'Home' || key === 'End') {open(key === 'Home' ? 0 : options.length - 1);}
        else if (event.altKey && key === 'ArrowUp') {close();}
        else if (listbox.hidden) {open();}
        else {setActive(active + (key === 'ArrowDown' ? 1 : -1));}
        return;
      }
      if (key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
        event.preventDefault();
        // Prevent the page's '/' search shortcut while using the select.
        event.stopPropagation();
        const now = Date.now();
        typeahead = now - typedAt > 700 ? key : typeahead + key;
        typedAt = now;
        const query = typeahead.toLocaleLowerCase();
        const match = options.findIndex(option => translate(option.textContent).toLocaleLowerCase().startsWith(query) || option.value.startsWith(query));
        if (match >= 0) open(match);
      }
    });
    wrapper.addEventListener('focusout', event => {
      if (!wrapper.contains(event.relatedTarget)) close();
    });
    wrapper.classList.add('custom-select');
    wrapper.append(trigger, listbox);
    select.hidden = true;
    select.addEventListener('change', sync);
    sync();
  }
  document.addEventListener('pointerdown', event => {
    if (openControl && !openControl.wrapper.contains(event.target)) openControl.close();
  });
  document.addEventListener('change', event => {
    if (event.target.id === 'language-select') {
      controls.forEach(control => control.sync());
      localize();
    }
  });

  for (const input of document.querySelectorAll('.search-field input')) {
    const field = input.closest('.search-field');
    const clear = document.createElement('button');
    clear.type = 'button';
    clear.className = 'search-clear';
    clear.setAttribute('aria-label', 'Clear search');
    clear.innerHTML = icon('close');
    field.append(clear);
    input.setAttribute('autocomplete', 'off');
    input.setAttribute('spellcheck', 'false');
    const sync = () => {
      clear.hidden = !input.value;
      field.classList.toggle('has-value', Boolean(input.value));
    };
    const reset = () => {
      input.value = '';
      input.dispatchEvent(new Event('input', {bubbles:true}));
      input.focus({preventScroll:true});
    };
    clear.addEventListener('click', reset);
    input.addEventListener('input', sync);
    input.addEventListener('keydown', event => {
      if (event.key === 'Escape' && input.value) {event.preventDefault(); reset();}
    });
    sync();
  }
  localize();
})();
