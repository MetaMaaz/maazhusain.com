const html = document.documentElement;

// —— Theme toggle (initial theme is set inline in <head>) ——
const themeBtn = document.getElementById('themeBtn');
const label = () => {
  const next = html.dataset.theme === 'light' ? 'Dark' : 'Light';
  themeBtn.textContent = next;
  themeBtn.setAttribute('aria-label', `${next} theme`);   // keeps the visible word in the name (WCAG 2.5.3)
};
label();
themeBtn.addEventListener('click', () => {
  html.dataset.theme = html.dataset.theme === 'light' ? 'dark' : 'light';
  label();
  try { localStorage.setItem('mh-theme', html.dataset.theme); } catch (e) {}
});

// —— Full-screen menu ——
const menuBtn = document.getElementById('menuBtn');
const menu = document.getElementById('menu');
const behind = document.querySelectorAll('main, .site-foot');
const setMenu = open => {
  menu.hidden = !open;
  behind.forEach(el => { el.inert = open; });   // keeps Tab and screen readers inside the open menu
  html.classList.toggle('menu-open', open);
  menuBtn.setAttribute('aria-expanded', open);
  menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
};
menuBtn.addEventListener('click', () => setMenu(menu.hidden));
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); menuBtn.focus(); } });

// —— Reveal on scroll ——
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
