// —— Theme toggle ——
const themeBtn = document.getElementById('themeBtn');
const html = document.documentElement;
let dark = true;
const saved = localStorage.getItem('mh-theme');
if (saved === 'light') { dark = false; html.dataset.theme = 'light'; themeBtn.textContent = '☀ dark'; }

themeBtn.addEventListener('click', () => {
  dark = !dark;
  html.dataset.theme = dark ? 'dark' : 'light';
  themeBtn.textContent = dark ? '☀ light' : '☀ dark';
  localStorage.setItem('mh-theme', dark ? 'dark' : 'light');
});

// —— Hamburger ——
const hamburger = document.getElementById('hamburgerBtn');
const navLinks = document.getElementById('navLinks');
hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  hamburger.textContent = navLinks.classList.contains('open') ? '✕' : '☰';
});
navLinks.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => { navLinks.classList.remove('open'); hamburger.textContent = '☰'; });
});

// —— Reveal on scroll ——
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// —— Tweaks ——
window.addEventListener('message', e => {
  if (e.data?.type === '__activate_edit_mode') document.getElementById('tweaks-panel').classList.add('open');
  if (e.data?.type === '__deactivate_edit_mode') document.getElementById('tweaks-panel').classList.remove('open');
});
window.parent.postMessage({ type: '__edit_mode_available' }, '*');

document.getElementById('tweak-accent').addEventListener('input', e => {
  document.documentElement.style.setProperty('--accent', e.target.value);
  window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { accent: e.target.value } }, '*');
});
document.getElementById('tweak-role').addEventListener('change', e => {
  document.querySelector('.hero-eyebrow').textContent = e.target.value;
});
document.getElementById('tweak-serif').addEventListener('change', e => {
  document.documentElement.style.setProperty('--serif', e.target.value);
});
