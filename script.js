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

// —— In-page links: scroll without adding #section to the address bar ——
// Runs after the menu link's own handler (which closes the menu and un-inerts the page).
// Without JS the links still work as plain #anchors.
document.addEventListener('click', e => {
  const a = e.target.closest('a[href^="#"]');
  if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  const target = document.getElementById(a.getAttribute('href').slice(1));
  if (!target) return;
  e.preventDefault();
  target.scrollIntoView();                                  // follows CSS scroll-behavior, so reduced motion is respected
  if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
  target.focus({ preventScroll: true });                    // keyboard and screen-reader users continue from the section
  if (location.hash) history.replaceState(null, '', location.pathname + location.search);
});

// —— Reveal on scroll ——
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
