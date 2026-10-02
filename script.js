const body = document.body;
const progress = document.querySelector('.scroll-progress span');
const menuToggle = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('.mobile-menu');
const toast = document.querySelector('.toast');

window.addEventListener('load', () => {
  body.classList.add('page-loaded');
  document.querySelectorAll('.hero .reveal').forEach((element, index) => {
    window.setTimeout(() => element.classList.add('is-visible'), 120 + index * 140);
  });
});

const updateProgress = () => {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const percentage = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
  progress.style.width = `${percentage}%`;
};

window.addEventListener('scroll', updateProgress, { passive: true });
updateProgress();

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.13 });

document.querySelectorAll('.reveal:not(.hero .reveal)').forEach((element) => observer.observe(element));

const closeMenu = () => {
  body.classList.remove('menu-open');
  menuToggle?.setAttribute('aria-expanded', 'false');
};

menuToggle?.addEventListener('click', () => {
  const isOpen = body.classList.toggle('menu-open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
});

mobileMenu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));

const showToast = () => {
  toast.classList.add('is-visible');
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => toast.classList.remove('is-visible'), 2400);
};

document.querySelectorAll('.copy-command').forEach((button) => {
  button.addEventListener('click', async () => {
    const value = button.dataset.copy;
    try {
      await navigator.clipboard.writeText(value);
    } catch {
      const input = document.createElement('textarea');
      input.value = value;
      document.body.appendChild(input);
      input.select();
      document.execCommand('copy');
      input.remove();
    }
    const label = button.querySelector('.copy-label');
    if (label) {
      const original = label.textContent;
      label.textContent = 'Copied';
      window.setTimeout(() => { label.textContent = original; }, 1800);
    }
    showToast();
  });
});

const receiptTabs = document.querySelectorAll('.receipt-tab');
const receipts = document.querySelectorAll('.receipt');

receiptTabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    const target = tab.dataset.receipt;
    receiptTabs.forEach((item) => {
      const active = item === tab;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-selected', String(active));
    });
    receipts.forEach((receipt) => {
      const active = receipt.id === `receipt-${target}`;
      receipt.hidden = !active;
      receipt.classList.toggle('is-hidden', !active);
    });
  });
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenu();
});
