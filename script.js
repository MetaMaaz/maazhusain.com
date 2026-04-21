// ── Theme toggle ──
const btn = document.getElementById('themeBtn');
const html = document.documentElement;
let dark = false;

const saved = localStorage.getItem('mh-theme');
if (saved === 'dark') { dark = true; html.dataset.theme = 'dark'; btn.textContent = '☀ light'; }

btn.addEventListener('click', () => {
  dark = !dark;
  html.dataset.theme = dark ? 'dark' : 'light';
  btn.textContent = dark ? '☀ light' : '☀ dark';
  localStorage.setItem('mh-theme', dark ? 'dark' : 'light');
});

// ── Scroll reveals ──
const revealEls = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); }
  });
}, { threshold: 0.12 });

revealEls.forEach(el => observer.observe(el));

// ── Tweaks panel ──
window.addEventListener('message', e => {
  if (e.data?.type === '__activate_edit_mode') document.getElementById('tweaks-panel').classList.add('open');
  if (e.data?.type === '__deactivate_edit_mode') document.getElementById('tweaks-panel').classList.remove('open');
});
window.parent.postMessage({ type: '__edit_mode_available' }, '*');

document.getElementById('tweak-accent').addEventListener('input', e => {
  document.documentElement.style.setProperty('--accent', e.target.value);
  window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { accent: e.target.value } }, '*');
});

document.getElementById('tweak-font').addEventListener('change', e => {
  document.body.style.fontSize = e.target.value;
});

document.getElementById('tweak-title').addEventListener('change', e => {
  document.querySelector('.hero-label').textContent = e.target.value;
});
