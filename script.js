const html = document.documentElement;

// —— Theme toggle (initial theme is set inline in <head>) ——
const themeBtn = document.getElementById('themeBtn');
const label = () => { themeBtn.textContent = html.dataset.theme === 'light' ? 'Dark' : 'Light'; };
label();
themeBtn.addEventListener('click', () => {
  html.dataset.theme = html.dataset.theme === 'light' ? 'dark' : 'light';
  label();
  try { localStorage.setItem('mh-theme', html.dataset.theme); } catch (e) {}
});

// —— Full-screen menu ——
const menuBtn = document.getElementById('menuBtn');
const menu = document.getElementById('menu');
const setMenu = open => {
  menu.hidden = !open;
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
