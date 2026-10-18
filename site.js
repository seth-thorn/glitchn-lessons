/* Shared by the Glitch'n site pages (the home page, parts and printables, and pages to come):
   the language choice and switch, and the words in the top bar and footer.

   A page calls GL.start(T, render):
     T       its own words: { en: { key: '…' }, es: { key: '…' } }. Elements with data-t="key" get that text,
             and T[lang].title becomes the page title.
     render  optional; called with (lang, words) after every language change, for anything else the page draws.
   Links written as data-href="…" keep ?lang= when the address has it, the same way the lessons do. */
window.GL = (() => {
  const SITE = {
    en: {
      navLessons: 'Lessons', navNeed: 'What you need', langLabel: 'Language',
      who: "Glitch'n is a project of the School of Games, Arts, Media and Engineering at Arizona State University.",
      nsf: 'This material is based upon work supported by the U.S. National Science Foundation under Award No. 2432637 (Advancing Informal STEM Learning). Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.',
    },
    es: {
      navLessons: 'Lecciones', navNeed: 'Lo que necesitas', langLabel: 'Idioma',
      who: "Glitch'n es un proyecto de la School of Games, Arts, Media and Engineering de Arizona State University.",
      nsf: 'Este material se basa en trabajo financiado por la Fundación Nacional de Ciencias de EE. UU. (NSF) mediante la subvención n.º 2432637 (Advancing Informal STEM Learning). Las opiniones, hallazgos, conclusiones o recomendaciones expresadas en este material son de los autores y no reflejan necesariamente el punto de vista de la NSF.',
    },
  };

  /* language: ?lang= in the address, then the visitor's last choice, then the browser (same as the lessons) */
  const q = new URLSearchParams(location.search);
  const pick = () => {
    if (SITE[q.get('lang')]) return q.get('lang');
    try { const v = JSON.parse(localStorage.getItem('glitchn-lang')); if (SITE[v]) return v; } catch (e) {}
    return (navigator.languages || [navigator.language || '']).some((l) => /^es\b/i.test(l)) ? 'es' : 'en';
  };
  let LANG = pick();
  const keep = () => (q.get('lang') ? 'lang=' + LANG : '');
  const withLang = (h) => { const k = keep(); return k ? h + (h.includes('?') ? '&' : '?') + k : h; };

  function start(T, render) {
    const apply = () => {
      const t = Object.assign({}, SITE[LANG], (T || {})[LANG]);
      document.documentElement.lang = LANG;
      if (t.title) document.title = t.title;
      document.querySelectorAll('[data-t]').forEach((el) => { if (t[el.dataset.t] != null) el.textContent = t[el.dataset.t]; });
      document.querySelectorAll('[data-href]').forEach((a) => { a.href = withLang(a.dataset.href); });
      document.querySelectorAll('.lang').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.lang === LANG)));
      const langs = document.getElementById('langs'); if (langs) langs.setAttribute('aria-label', t.langLabel);
      const mt = document.getElementById('mt'); if (mt) mt.hidden = LANG !== 'es';
      if (render) render(LANG, t);
    };
    const langs = document.getElementById('langs');
    if (langs) langs.addEventListener('click', (e) => {
      const b = e.target.closest('.lang'); if (!b) return;
      LANG = b.dataset.lang;
      try { localStorage.setItem('glitchn-lang', JSON.stringify(LANG)); } catch (err) {}
      if (q.get('lang')) { q.set('lang', LANG); history.replaceState(null, '', '?' + q.toString() + location.hash); }
      apply();
    });
    apply();
  }
  return { start, withLang, get lang() { return LANG; } };
})();
