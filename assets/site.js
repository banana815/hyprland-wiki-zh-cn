// Keep navigation and all article content usable without JavaScript.
const theme = document.querySelector('#theme');
try {
  theme.value = localStorage.getItem('wiki-theme') || 'system';
} catch { /* Browser storage is optional. */ }
document.documentElement.dataset.theme = theme.value;
theme.addEventListener('change', () => {
  document.documentElement.dataset.theme = theme.value;
  try { localStorage.setItem('wiki-theme', theme.value); } catch { /* Optional. */ }
});

const menu = document.querySelector('#menu');
const sidebar = document.querySelector('#sidebar');
menu.addEventListener('click', () => {
  const expanded = sidebar.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(expanded));
  if (expanded) window.scrollTo(0, 0);
});

const root = new URL(document.body.dataset.root, document.baseURI);
const query = document.querySelector('#query');
const tree = document.querySelector('#tree');
const results = document.querySelector('#results');
const statusLine = document.querySelector('#result-status');
const list = results.querySelector('ul');
// Titles can be searched immediately, even if the full-text index is unavailable.
let entries = Array.from(tree.querySelectorAll('a'), link => ({
  title: link.textContent,
  path: new URL(link.href).pathname.slice(root.pathname.length),
  text: ''
}));
let loadPromise;
function loadIndex() {
  loadPromise ??= fetch(new URL('assets/search.json', root))
    .then(response => {
      if (!response.ok) throw new Error(response.statusText);
      return response.json();
    })
    .then(data => { entries = data; filter(); })
    .catch(() => { loadPromise = undefined; });
}
function filter() {
  const term = query.value.trim().toLowerCase();
  tree.hidden = Boolean(term);
  results.hidden = !term;
  list.replaceChildren();
  if (!term) return;
  const matches = entries.map(entry => {
    const index = entry.text.toLowerCase().indexOf(term);
    const titleHit = (entry.title + ' ' + entry.path).toLowerCase().includes(term);
    return { entry, index, rank: titleHit ? 0 : index < 0 ? 2 : 1 };
  }).filter(hit => hit.rank < 2).sort((a,b) => a.rank - b.rank);
  for (const {entry, index} of matches) {
    const row = document.createElement('li');
    const link = document.createElement('a');
    link.href = new URL(entry.path || './', root);
    link.textContent = entry.title;
    row.append(link);
    if (index >= 0) {
      const snippet = document.createElement('small');
      const start = Math.max(0, index - 14);
      snippet.textContent = (start ? '…' : '') + entry.text.slice(start, index + term.length + 28) + '…';
      row.append(snippet);
    }
    list.append(row);
  }
  statusLine.textContent = matches.length ? '找到 ' + matches.length + ' 篇文档' : '没有匹配的文档';
}
query.addEventListener('focus', loadIndex);
query.addEventListener('input', () => { filter(); loadIndex(); });
document.addEventListener('keydown', event => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    if (menu.offsetWidth && !sidebar.classList.contains('open')) menu.click();
    query.focus();
  } else if (event.key === 'Escape' && document.activeElement === query) {
    query.value = '';
    filter();
    query.blur();
  }
});

for (const tabs of document.querySelectorAll('.tabs')) {
  const panels = Array.from(tabs.querySelectorAll(':scope > .tab-panel'));
  if (!panels.length) continue;
  const buttons = document.createElement('div');
  buttons.className = 'tab-controls';
  buttons.setAttribute('aria-label', '选择示例');
  const controls = panels.map((panel, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = panel.dataset.tab;
    button.addEventListener('click', () => select(index));
    panel.querySelector('.tab-label').hidden = true;
    buttons.append(button);
    return button;
  });
  function select(active) {
    panels.forEach((panel, index) => {
      panel.hidden = index !== active;
      controls[index].classList.toggle('active', index === active);
      controls[index].setAttribute('aria-pressed', String(index === active));
    });
  }
  tabs.prepend(buttons);
  select(0);
}
