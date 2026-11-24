const theme = document.querySelector('#theme');
function applyTheme(value) {
  document.documentElement.dataset.theme = value;
  theme.value = value;
}
try {
  applyTheme(localStorage.getItem('wiki-theme') || 'system');
} catch {
  applyTheme('system');
}
theme.addEventListener('change', () => {
  applyTheme(theme.value);
  try { localStorage.setItem('wiki-theme', theme.value); } catch { /* Storage is optional. */ }
});

const menu = document.querySelector('#menu');
const sidebar = document.querySelector('#sidebar');
menu.addEventListener('click', () => {
  const expanded = sidebar.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(expanded));
  if (expanded) window.scrollTo(0, 0);
});
const query = document.querySelector('#query');
const tree = document.querySelector('#tree');
const results = document.querySelector('#results');
const list = results.querySelector('ul');
const statusLine = document.querySelector('#result-status');
const entries = Array.from(tree.querySelectorAll('a[href]'));
function filterNavigation() {
  const term = query.value.trim().toLowerCase();
  tree.hidden = Boolean(term);
  results.hidden = !term;
  list.replaceChildren();
  if (!term) return;
  const matches = entries.filter(link =>
    (link.textContent + ' ' + new URL(link.href).pathname).toLowerCase().includes(term)
  );
  for (const link of matches) {
    const item = document.createElement('li');
    item.append(link.cloneNode(true));
    list.append(item);
  }
  statusLine.textContent = matches.length ? '找到 ' + matches.length + ' 个条目' : '没有找到匹配的条目';
}
query.addEventListener('input', filterNavigation);
document.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    if (menu.offsetWidth && !sidebar.classList.contains('open')) menu.click();
    query.focus();
  } else if (event.key === 'Escape' && document.activeElement === query) {
    query.value = '';
    filterNavigation();
    query.blur();
  }
});
document.querySelector('#version').addEventListener('change', event => {
  if (event.target.value) window.location.assign(event.target.value);
});
