/* Glitch'n lesson player. One copy serves every lesson.
   A lesson page is a small HTML file with <div id="glitchn-player"></div> and this script.
   Optional settings: window.GLITCHN_PLAYER = { lesson, index, home, lessonHref } (see the defaults below). */
(() => {
  const $ = (id) => document.getElementById(id);
  // A lesson page sets nothing and gets these defaults: lesson.json beside the page,
  // the lesson index one folder up, and the home page two folders up.
  const C = window.GLITCHN_PLAYER || {};
  const LESSON_URL = C.lesson || 'lesson.json';
  const INDEX_URL = C.index || '../index.json';
  const HOME_URL = C.home || '../../index.html';
  const lessonHref = (slug) => (C.lessonHref || '../{slug}/index.html').replace('{slug}', slug);
  /* ---------- language ----------
     Interface wording lives in UI below. Lesson text comes from lesson.json (English) and, for other
     languages, from lesson.<lang>.json beside it: a list of English lines and their translations.
     A line with no translation simply shows in English. Choice order: ?lang= in the address,
     then the visitor's last choice, then the browser's language. */
  const LANGS = { en: 'English', es: 'Español' };
  const UI = {
    en: {
      style: 'Style', style_tv: 'TV', style_rams: 'Rams', allLessons: '← All lessons', lessonEyebrow: "Glitch'n lesson", draft: 'Draft', draftTitle: 'Step text and links are drafts for the team to review',
      loading: 'Loading…', skin: 'Skin', skinGroup: 'Colour skin', language: 'Language',
      skin_navy: 'Navy skin', skin_sky: 'Sky skin', skin_coral: 'Coral skin', skin_green: 'Green skin', skin_yellow: 'Yellow skin', skin_red: 'Red skin',
      tutorialVideo: 'Tutorial video', play: 'Play', pause: 'Pause', mute: 'Mute', unmute: 'Unmute', speed: 'Playback speed', fullScreen: 'Full screen', seek: 'Seek through the lesson',
      instructions: 'Instructions', buildSteps: 'Build steps', follow: 'Follow video', followTitle: 'Scroll the list to follow the video',
      closeups: 'Close-up stills', hint: 'Point at the board to magnify', hintTouch: 'Touch and drag to magnify', zoomLess: 'Less magnification', zoomMore: 'More magnification',
      prevStill: 'Previous still', nextStill: 'Next still', backToVideo: "Back to the video's step", stillsForStep: 'Stills for this step', showStill: 'Show still {n}',
      progress: 'Progress', whatsNext: "What's next?", mapLabel: 'Lessons connected to this one', ready: 'Ready', coming: 'Coming', comingSmall: 'coming', comingLater: ', coming later',
      keyPlay: 'play / pause', keySeconds: '5 seconds', keySub: 'previous / next sub-step', keyMute: 'mute',
      startingPoint: 'Starting point', finishedResult: 'Finished result of {n}', beforeStep: 'Before step {n}: ', boardAt: 'Breadboard at {n}: {t}',
      done: 'done ✓', watched: 'Watched {x} of {y} sub-steps', stepOf: 'Step <b>{n}</b> of {m} · {t}', goToStep: 'Go to step {n}: {t}', of: '{a} of {b}',
      startHere: 'Start here', moreSoon: 'More soon', youAreHere: 'You’re in this lesson.', notReady: '“{t}” isn’t ready yet.',
      noFullScreen: 'Full screen is not available here.', videoError: 'This video could not load. Check that {f} is next to the page.',
      notFound: 'Lesson not found', notFoundBody: '<b>The lesson file did not load.</b> Each lesson folder needs a lesson.json beside its page.',
      untranslated: '', machine: '',
      kind_variation: 'variation', kind_related: 'related', 'kind_next day': 'next day', kind_revisited: 'revisited'
    },
    es: {
      style: 'Estilo', style_tv: 'Tele', style_rams: 'Rams', allLessons: '← Todas las lecciones', lessonEyebrow: 'Lección de Glitch’n', draft: 'Borrador', draftTitle: 'El texto de los pasos y los enlaces son un borrador',
      loading: 'Cargando…', skin: 'Color', skinGroup: 'Color de la interfaz', language: 'Idioma',
      skin_navy: 'Azul marino', skin_sky: 'Celeste', skin_coral: 'Coral', skin_green: 'Verde', skin_yellow: 'Amarillo', skin_red: 'Rojo',
      tutorialVideo: 'Video de la lección', play: 'Reproducir', pause: 'Pausar', mute: 'Silenciar', unmute: 'Activar sonido', speed: 'Velocidad de reproducción', fullScreen: 'Pantalla completa', seek: 'Avanzar o retroceder en la lección',
      instructions: 'Instrucciones', buildSteps: 'Pasos de armado', follow: 'Seguir el video', followTitle: 'Desplazar la lista para seguir el video',
      closeups: 'Fotos de cerca', hint: 'Señala la protoboard para ampliar', hintTouch: 'Toca y arrastra para ampliar', zoomLess: 'Menos aumento', zoomMore: 'Más aumento',
      prevStill: 'Foto anterior', nextStill: 'Foto siguiente', backToVideo: 'Volver al paso del video', stillsForStep: 'Fotos de este paso', showStill: 'Mostrar la foto {n}',
      progress: 'Progreso', whatsNext: '¿Qué sigue?', mapLabel: 'Lecciones conectadas con esta', ready: 'Lista', coming: 'Próximamente', comingSmall: 'próximamente', comingLater: ', disponible más adelante',
      keyPlay: 'reproducir / pausar', keySeconds: '5 segundos', keySub: 'subpaso anterior / siguiente', keyMute: 'silenciar',
      startingPoint: 'Punto de partida', finishedResult: 'Resultado terminado de {n}', beforeStep: 'Antes del paso {n}: ', boardAt: 'Protoboard en {n}: {t}',
      done: 'listo ✓', watched: 'Viste {x} de {y} subpasos', stepOf: 'Paso <b>{n}</b> de {m} · {t}', goToStep: 'Ir al paso {n}: {t}', of: '{a} de {b}',
      startHere: 'Empieza aquí', moreSoon: 'Pronto habrá más', youAreHere: 'Ya estás en esta lección.', notReady: '“{t}” todavía no está lista.',
      noFullScreen: 'La pantalla completa no está disponible aquí.', videoError: 'Este video no se pudo cargar ({f}).',
      notFound: 'No se encontró la lección', notFoundBody: '<b>No se pudo cargar el archivo de la lección.</b> Cada carpeta de lección necesita un lesson.json junto a su página.',
      untranslated: 'Esta lección todavía no está traducida. Se muestra en inglés.', machine: 'Traducción automática',
      kind_variation: 'variación', kind_related: 'relacionada', 'kind_next day': 'día siguiente', kind_revisited: 'repaso'
    }
  };
  function pickLang() {
    const q = new URLSearchParams(location.search).get('lang');
    if (q && LANGS[q]) return q;
    try { const v = JSON.parse(localStorage.getItem('glitchn-lang')); if (v && LANGS[v]) return v; } catch (e) {}
    return (navigator.languages || [navigator.language || '']).some((l) => /^es\b/i.test(l)) ? 'es' : 'en';
  }
  const LANG = pickLang();
  document.documentElement.lang = LANG;
  const t = (k, v) => String(UI[LANG][k] ?? UI.en[k] ?? k).replace(/\{(\w+)\}/g, (_, n) => (v && v[n] != null ? v[n] : ''));
  /* ---------- styles: whole looks for the page (colours, type, shapes, the TV itself) ----------
     Each style is CSS in player.css under :root[data-style="…"]. Choice order: ?style= in the address,
     then the visitor's last choice, then TV. Add a style by adding it here and writing its CSS block. */
  const STYLES = ['tv', 'rams'];
  function pickStyle() {
    const q = new URLSearchParams(location.search).get('style'); if (q && STYLES.includes(q)) return q;
    try { const v = JSON.parse(localStorage.getItem('glitchn-style')); if (STYLES.includes(v)) return v; } catch (e) {}
    return 'tv';
  }
  let STYLE = pickStyle();
  document.documentElement.dataset.style = STYLE;
  const kindLabel = (k) => t('kind_' + k) === 'kind_' + k ? k : t('kind_' + k);
  const mount = document.getElementById('glitchn-player') || document.body.appendChild(document.createElement('div'));
  mount.innerHTML = `<div class="app" id="app">
  <header class="top">
    <div>
      <div class="eyebrow"><a class="home-link" id="homeLink" href="../../index.html">${t('allLessons')}</a><span>${t('lessonEyebrow')}</span><span class="draft-chip" id="draftChip" title="${t('draftTitle')}" hidden>${t('draft')}</span><span class="draft-chip lang-note" id="langNote" hidden></span></div>
      <h1 id="title">${t('loading')}</h1>
    </div>
    <div class="top-tools">
    <label class="style-pick"><span>${t('style')}</span><select id="styleSel">${STYLES.map((k) => '<option value="' + k + '"' + (k === STYLE ? ' selected' : '') + '>' + t('style_' + k) + '</option>').join('')}</select></label>
    <div class="langs" role="group" aria-label="${t('language')}">${Object.entries(LANGS).map(([k, n]) => '<button class="lang" data-lang="' + k + '" lang="' + k + '" aria-pressed="' + (k === LANG) + '">' + n + '</button>').join('')}</div>
    <div class="skins" role="group" aria-label="${t('skinGroup')}">
      <span>${t('skin')}</span>
      <button class="skin" data-skin="navy" style="--c:#4259A8" aria-label="${t('skin_navy')}" aria-pressed="false"></button>
      <button class="skin" data-skin="sky" style="--c:#57BEE4" aria-label="${t('skin_sky')}" aria-pressed="false"></button>
      <button class="skin" data-skin="coral" style="--c:#EE6668" aria-label="${t('skin_coral')}" aria-pressed="true"></button>
      <button class="skin" data-skin="green" style="--c:#66C26A" aria-label="${t('skin_green')}" aria-pressed="false"></button>
      <button class="skin" data-skin="yellow" style="--c:#F5CF42" aria-label="${t('skin_yellow')}" aria-pressed="false"></button>
      <button class="skin" data-skin="red" style="--c:#E8493F" aria-label="${t('skin_red')}" aria-pressed="false"></button>
    </div>
    </div>
  </header>

  <div class="grid">
    <section class="tv-wrap" aria-label="${t('tutorialVideo')}">
      <div class="tv panel" id="tv">
        <span class="ant" aria-hidden="true"><i class="rod l"></i><i class="rod r"></i><i class="base"></i></span>
        <div class="screen idle" id="screen">
          <video id="vA" class="on" playsinline preload="auto"></video>
          <video id="vB" playsinline preload="auto"></video>
          <span class="glass" aria-hidden="true"></span>
          <div class="now-chip" id="nowChip"></div>
          <button class="big-play" id="bigPlay" aria-label="${t('play')}"><span><svg viewBox="0 0 24 24"><path d="M6 3.5v17l14-8.5z" fill="currentColor"/></svg></span></button>
        </div>
        <div class="scrub" id="scrub">
          <div class="ticks" id="ticks"></div>
          <div class="track" id="track"><div class="fill" id="fill"></div></div>
          <div class="knob" id="knob"></div>
          <input type="range" id="seek" min="0" max="100" step="0.1" value="0" aria-label="${t('seek')}">
          <div class="hover-tip" id="tip" hidden></div>
        </div>
        <div class="controls">
          <button class="ctl" id="playBtn" aria-label="${t('play')}"><svg viewBox="0 0 24 24" id="playIcon"><path d="M6 3.5v17l14-8.5z" fill="currentColor"/></svg></button>
          <span class="divider" aria-hidden="true"></span>
          <button class="ctl dial" id="rateBtn" aria-label="${t('speed')}"><span class="dial-face" aria-hidden="true"><span class="dial-mark"></span></span><span class="dial-label" id="rateLabel">1.0x</span></button>
          <span class="divider" aria-hidden="true"></span>
          <button class="ctl" id="muteBtn" aria-label="${t('mute')}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" id="volIcon"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor" stroke="none"/><path d="M15.5 9a4.2 4.2 0 0 1 0 6M18.3 6.5a8 8 0 0 1 0 11"/></svg></button>
          <span class="time" id="time">0:00 / 0:00</span>
          <span class="grow grille" aria-hidden="true"></span>
          <button class="ctl" id="fsBtn" aria-label="${t('fullScreen')}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg></button>
        </div>
        <span class="feet" aria-hidden="true"><i></i><i></i></span>
      </div>
    </section>

    <section class="steps-cell" aria-label="${t('instructions')}">
      <div class="steps panel">
        <div class="steps-head">
          <h2 class="panel-title">${t('buildSteps')}</h2>
          <button class="follow" id="followBtn" aria-pressed="true" title="${t('followTitle')}"><i></i>${t('follow')}</button>
        </div>
        <ol class="step-list" id="stepList"></ol>
      </div>
    </section>

    <section class="stills-cell" aria-label="${t('closeups')}">
      <div class="stills panel">
        <div class="viewport" id="viewport">
          <img id="stillImg" alt="">
          <div class="lens" id="lens"></div>
          <div class="hint" id="hint">${t('hint')}</div>
          <div class="zoom" id="zoomBox">
            <button id="zoomOut" aria-label="${t('zoomLess')}">−</button>
            <output id="zoomOut2">2.5×</output>
            <button id="zoomIn" aria-label="${t('zoomMore')}">+</button>
          </div>
        </div>
        <button class="arrow prev" id="prevStill" aria-label="${t('prevStill')}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M15 4l-8 8 8 8"/></svg></button>
        <button class="arrow next" id="nextStill" aria-label="${t('nextStill')}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M9 4l8 8-8 8"/></svg></button>
        <div class="caption-row">
          <div class="caption" id="caption"></div>
          <button class="back-btn" id="backBtn" hidden>${t('backToVideo')}</button>
        </div>
        <div class="film" id="film" aria-label="${t('stillsForStep')}"></div>
      </div>
    </section>

    <div class="side">
      <section class="progress panel" aria-label="${t('progress')}">
        <div class="prog-head"><h2 class="panel-title">${t('progress')}</h2><span class="prog-pct" id="progPct">0%</span></div>
        <div class="prog-bar" id="progBar"></div>
        <div class="prog-note"><span id="progStep"></span><span id="progWatched"></span></div>
      </section>
      <section class="mapbox panel" aria-label="${t('whatsNext')}">
        <div class="map-inner">
          <h2 class="panel-title">${t('whatsNext')}</h2>
          <svg class="map-svg" id="map" viewBox="0 0 440 290" role="group" aria-label="${t('mapLabel')}"></svg>
          <div class="map-legend"><span><i></i>${t('ready')}</span><span><i class="dash"></i>${t('coming')}</span></div>
        </div>
      </section>
    </div>
  </div>

  <div class="keys"><span><kbd>Space</kbd>${t('keyPlay')}</span><span><kbd>←</kbd><kbd>→</kbd>${t('keySeconds')}</span><span><kbd>[</kbd><kbd>]</kbd>${t('keySub')}</span><span><kbd>M</kbd>${t('keyMute')}</span></div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>

`;
  const RATES = [0.5, 0.75, 1, 1.25, 1.5, 2];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  const fmt = (s) => { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  let toastTimer;
  function toast(msg) { const t = $('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 2600); }

  /* ---------- skins ---------- */
  function setSkin(name) {
    if (name === 'coral') delete document.documentElement.dataset.skin; else document.documentElement.dataset.skin = name;
    document.querySelectorAll('.skin').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.skin === name)));
    store.set('glitchn-skin', name);
  }
  document.querySelectorAll('.skin').forEach((b) => b.addEventListener('click', () => setSkin(b.dataset.skin)));
  setSkin(store.get('glitchn-skin', 'coral'));
  $('styleSel').addEventListener('change', (e) => { STYLE = e.target.value; document.documentElement.dataset.style = STYLE; store.set('glitchn-style', STYLE); });

  const homeUrl = new URL(HOME_URL, location.href); if (new URLSearchParams(location.search).get('lang')) homeUrl.searchParams.set('lang', LANG);
  $('homeLink').href = homeUrl.href;
  const lessonAbs = new URL(LESSON_URL, location.href);
  // Switching language reloads the page in that language and returns to the same moment in the video.
  let currentTime = () => 0;
  document.querySelectorAll('.lang').forEach((b) => b.addEventListener('click', () => {
    if (b.dataset.lang === LANG) return;
    store.set('glitchn-lang', b.dataset.lang);
    try { sessionStorage.setItem('glitchn-resume', JSON.stringify({ path: location.pathname, t: currentTime() })); } catch (e) {}
    const u = new URL(location.href); u.searchParams.set('lang', b.dataset.lang); location.href = u.href;
  }));
  const translationUrl = new URL(lessonAbs.pathname.replace(/lesson\.json$/, 'lesson.' + LANG + '.json') + lessonAbs.search, lessonAbs).href;
  Promise.all([
    fetch(LESSON_URL).then((r) => { if (!r.ok) throw new Error(r.status + ' ' + LESSON_URL); return r.json(); }),
    fetch(INDEX_URL).then((r) => r.json()).catch(() => null),
    LANG === 'en' ? Promise.resolve(null) : fetch(translationUrl).then((r) => (r.ok ? r.json() : null)).catch(() => null)
  ])
    .then(([lesson, idx, tr]) => start(translate(lesson, tr), idx))
    .catch((e) => { $('title').textContent = t('notFound'); $('app').insertAdjacentHTML('beforeend', '<div class="err">' + t('notFoundBody') + ' (' + esc(e.message) + ')</div>'); });

  // Replace each English line with its translation when one exists.
  function translate(L, tr) {
    if (LANG === 'en') return L;
    const note = $('langNote');
    if (!tr || !tr.strings) { note.textContent = t('untranslated'); note.hidden = false; return L; }
    const d = tr.strings, tx = (s) => (s && d[s]) || s;
    L.title = tx(L.title); L.summary = tx(L.summary);
    L.steps.forEach((st) => { st.title = tx(st.title); st.subs.forEach((sb) => { sb.text = tx(sb.text); }); });
    if (tr.machine && !tr.reviewed) { note.textContent = t('machine'); note.title = tr.note || ''; note.hidden = false; }
    return L;
  }

  function start(L, IDX) {
    /* ---------- media paths are relative to lesson.json ---------- */
    const abs = (p) => (p ? new URL(p, lessonAbs).href : p);
    L.segments.forEach((s) => { s.src = abs(s.src); });
    L.steps.forEach((st) => { st.startStill = abs(st.startStill); st.subs.forEach((sb) => { sb.still = abs(sb.still); }); });
    const slug = L.slug || L.id;
    /* ---------- timeline ---------- */
    const segs = L.segments;
    const offsets = []; let total = 0;
    segs.forEach((s) => { offsets.push(total); total += s.duration; });
    const flat = []; // every sub-step on the global timeline
    const stills = []; // every still the viewer can show, in order
    L.steps.forEach((step, si) => {
      step.subStillIdx = [];
      step.firstStill = stills.length;
      stills.push({ si, ui: -1, src: step.startStill, label: (si + 1) + '.0', tag: t('startingPoint'), text: step.title });
      step.subs.forEach((sub, ui) => {
        const g = offsets[step.segment] + sub.t;
        flat.push({ si, ui, g, text: sub.text, label: (si + 1) + '.' + (ui + 1) });
        step.subStillIdx.push(stills.length);
        stills.push({ si, ui, src: sub.still, label: (si + 1) + '.' + (ui + 1), tag: t('finishedResult', { n: (si + 1) + '.' + (ui + 1) }), text: sub.text, fi: flat.length - 1 });
      });
      step.g0 = offsets[step.segment];
      step.g1 = offsets[step.segment] + segs[step.segment].duration;
    });
    flat.forEach((f, i) => { f.end = i + 1 < flat.length ? flat[i + 1].g : total; f.key = L.steps[f.si].id + '/' + f.ui; });
    const thumb = (src) => src.replace(/\/stills\/([^/]+)$/, '/thumbs/$1');

    $('title').innerHTML = esc(L.title) + ((L.summary || L.subtitle) ? '<span class="sub">' + esc(L.summary || L.subtitle) + '</span>' : '');
    document.title = L.title + " · Glitch'n";
    $('draftChip').hidden = L.status !== 'draft';

    /* ---------- state ---------- */
    const watchKey = 'glitchn-watched-' + slug;
    const watched = new Set(store.get(watchKey, []));
    const S = { cur: -1, follow: true, userScrollUntil: 0, pinned: -1, still: -1, zoom: 2.5, rate: 1, muted: false, playing: false, act: 0, seg: 0, switching: false, token: 0, lastT: 0 };
    const vids = [$('vA'), $('vB')];

    /* ---------- build step list ---------- */
    const list = $('stepList');
    const check = '<svg viewBox="0 0 12 12" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 6.3l2.3 2.3 4.7-5"/></svg>';
    list.innerHTML = L.steps.map((st, si) => (
      '<li class="step" id="step-' + si + '">' +
        '<button class="step-btn" data-step="' + si + '"><span class="step-num">' + (si + 1) + '.</span><span class="step-title">' + esc(st.title) + '</span><span class="step-meta" id="meta-' + si + '"></span></button>' +
        '<ol class="subs">' + st.subs.map((sub, ui) => {
          const fi = flat.findIndex((f) => f.si === si && f.ui === ui);
          return '<li><button class="sub" id="sub-' + fi + '" data-fi="' + fi + '"><span class="chk">' + check + '</span><span class="ts">' + fmt(flat[fi].g - offsets[st.segment]) + '</span><span>' + esc(sub.text) + '</span></button></li>';
        }).join('') + '</ol>' +
      '</li>')).join('');
    list.addEventListener('click', (e) => {
      const sb = e.target.closest('.sub'); const stb = e.target.closest('.step-btn');
      if (sb) { seek(flat[+sb.dataset.fi].g + 0.01); unpin(); }
      else if (stb) { seek(L.steps[+stb.dataset.step].g0 + 0.01); unpin(); }
    });
    ['wheel', 'touchstart', 'pointerdown'].forEach((ev) => list.addEventListener(ev, () => { S.userScrollUntil = performance.now() + 6000; }, { passive: true }));
    function updateMeta() {
      L.steps.forEach((st, si) => {
        const n = st.subs.length;
        let w = 0; st.subs.forEach((_, ui) => { if (watched.has(st.id + '/' + ui)) w++; });
        $('meta-' + si).innerHTML = w === n ? '<span class="ok">' + t('done') + '</span>' : fmt(st.g1 - st.g0) + (w ? ' · ' + w + '/' + n : '');
      });
      flat.forEach((f, i) => $('sub-' + i).classList.toggle('watched', watched.has(f.key)));
      $('progWatched').textContent = t('watched', { x: flat.filter((f) => watched.has(f.key)).length, y: flat.length });
    }
    $('followBtn').addEventListener('click', () => {
      S.follow = !S.follow; $('followBtn').setAttribute('aria-pressed', String(S.follow));
      if (S.follow) { S.userScrollUntil = 0; scrollToCurrent(); }
    });

    /* ---------- scrubber ---------- */
    const seekEl = $('seek');
    seekEl.max = total.toFixed(2);
    const track = $('track');
    L.steps.forEach((st, si) => { if (si) track.insertAdjacentHTML('beforeend', '<span class="sep" style="left:' + (st.g0 / total * 100) + '%"></span>'); });
    $('ticks').innerHTML = flat.filter((f) => f.ui > 0).map((f) => '<i style="left:' + (f.g / total * 100) + '%"></i>').join('');
    let scrubbing = false;
    seekEl.addEventListener('input', () => { scrubbing = true; seek(+seekEl.value); });
    seekEl.addEventListener('change', () => { scrubbing = false; });
    const scrub = $('scrub'), tip = $('tip');
    scrub.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      const r = scrub.getBoundingClientRect(); const x = Math.min(Math.max(e.clientX - r.left, 0), r.width);
      const g = x / r.width * total; const f = flat[findFlat(g)];
      tip.hidden = false; tip.innerHTML = '<b>' + f.label + '</b>' + esc(f.text);
      const half = Math.min(130, r.width / 2); tip.style.left = Math.min(Math.max(x, half), r.width - half) + 'px';
    });
    scrub.addEventListener('pointerleave', () => { tip.hidden = true; });

    /* ---------- progress bar ---------- */
    $('progBar').innerHTML = L.steps.map((st, si) => '<button class="prog-seg" style="--w:' + (st.g1 - st.g0).toFixed(1) + '" data-step="' + si + '" aria-label="' + esc(t('goToStep', { n: si + 1, t: st.title })) + '"><span class="f" id="pf-' + si + '"></span></button>').join('');
    $('progBar').addEventListener('click', (e) => { const b = e.target.closest('.prog-seg'); if (b) { seek(L.steps[+b.dataset.step].g0 + 0.01); unpin(); } });

    /* ---------- video engine: one timeline across several clips ---------- */
    function segIndex(g) { let i = 0; while (i + 1 < segs.length && g >= offsets[i + 1]) i++; return i; }
    function setSrc(el, i) { if (el.dataset.seg !== String(i)) { el.dataset.seg = String(i); el.src = segs[i].src; el.load(); } }
    const active = () => vids[S.act];
    const now = () => offsets[S.seg] + (active().currentTime || 0);
    function applyAV(el) { el.playbackRate = S.rate; el.muted = S.muted; }
    function preloadNext() { const other = vids[1 - S.act]; if (S.seg + 1 < segs.length) setSrc(other, S.seg + 1); }
    function switchTo(i, local, play) {
      const old = active(), nx = vids[1 - S.act], token = ++S.token;
      S.switching = true; setSrc(nx, i); applyAV(nx);
      let done = false;
      const finish = () => {
        if (done || token !== S.token) return; done = true;
        old.pause(); old.classList.remove('on'); nx.classList.add('on');
        S.act = 1 - S.act; S.seg = i; S.switching = false;
        if (play) nx.play().catch(() => {});
        preloadNext(); render(true);
      };
      const doSeek = () => { if (token !== S.token) return; nx.addEventListener('seeked', finish, { once: true }); setTimeout(finish, 700); nx.currentTime = Math.max(0, local); };
      if (nx.readyState >= 1) doSeek(); else nx.addEventListener('loadedmetadata', doSeek, { once: true });
    }
    function seek(g, play = S.playing) {
      g = Math.min(Math.max(g, 0), total - 0.05);
      const i = segIndex(g), local = g - offsets[i];
      if (i === S.seg && !S.switching) { active().currentTime = local; if (play) active().play().catch(() => {}); render(true); }
      else switchTo(i, local, play);
    }
    function play() {
      if (now() >= total - 0.1) { seek(0, true); }
      S.playing = true; applyAV(active()); active().play().catch(() => { S.playing = false; renderButtons(); });
      unpin(); renderButtons();
    }
    function pause() { S.playing = false; active().pause(); renderButtons(); }
    vids.forEach((v) => {
      v.addEventListener('ended', () => {
        if (v !== active()) return;
        if (S.cur >= 0) markWatched(S.cur);
        if (S.seg + 1 < segs.length) switchTo(S.seg + 1, 0, S.playing);
        else { S.playing = false; renderButtons(); }
      });
      v.addEventListener('error', () => { if (v.getAttribute('src')) toast(t('videoError', { f: segs[+v.dataset.seg].src.split('/').pop() })); });
      v.addEventListener('pause', () => { if (v === active() && !S.switching && !v.ended && S.playing && !document.hidden) { S.playing = false; renderButtons(); } });
    });
    setSrc(vids[0], 0); preloadNext();

    /* ---------- controls ---------- */
    const PLAY = '<path d="M6 3.5v17l14-8.5z" fill="currentColor"/>';
    const PAUSE = '<rect x="5" y="4" width="5" height="16" rx="1.2" fill="currentColor"/><rect x="14" y="4" width="5" height="16" rx="1.2" fill="currentColor"/>';
    function renderButtons() {
      $('playIcon').innerHTML = S.playing ? PAUSE : PLAY;
      $('playBtn').setAttribute('aria-label', S.playing ? t('pause') : t('play'));
      $('bigPlay').hidden = S.playing || S.everPlayed;
      $('screen').classList.toggle('idle', !S.everPlayed);
    }
    $('playBtn').addEventListener('click', () => { S.everPlayed = true; S.playing ? pause() : play(); });
    $('bigPlay').addEventListener('click', () => { S.everPlayed = true; play(); });
    $('screen').addEventListener('click', (e) => { if (e.target.closest('.big-play')) return; S.everPlayed = true; S.playing ? pause() : play(); });
    $('rateBtn').addEventListener('click', () => {
      S.rate = RATES[(RATES.indexOf(S.rate) + 1) % RATES.length]; vids.forEach(applyAV);
      $('rateLabel').textContent = (S.rate % 1 ? S.rate : S.rate.toFixed(1)) + 'x';
      $('rateBtn').style.setProperty('--rot', ((RATES.indexOf(S.rate) - 2) * 40) + 'deg'); // the dial turns with the speed
    });
    function toggleMute() {
      S.muted = !S.muted; vids.forEach(applyAV);
      $('volIcon').innerHTML = S.muted ? '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor" stroke="none"/><path d="M16 9.5l5 5M21 9.5l-5 5"/>' : '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor" stroke="none"/><path d="M15.5 9a4.2 4.2 0 0 1 0 6M18.3 6.5a8 8 0 0 1 0 11"/>';
      $('muteBtn').setAttribute('aria-label', S.muted ? t('unmute') : t('mute'));
    }
    $('muteBtn').addEventListener('click', toggleMute);
    $('fsBtn').addEventListener('click', () => {
      const tv = $('tv');
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
      else if (tv.requestFullscreen) tv.requestFullscreen().catch(() => toast(t('noFullScreen')));
      else toast(t('noFullScreen'));
    });
    document.addEventListener('keydown', (e) => {
      if (e.target.closest('input, textarea, select') || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === ' ' || e.key === 'k') { if (e.target.closest('button') && e.key === ' ') return; e.preventDefault(); S.everPlayed = true; S.playing ? pause() : play(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); seek(now() - 5); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); seek(now() + 5); }
      else if (e.key === '[') { const i = findFlat(now()); const f = flat[i]; seek((now() - f.g > 1.5 || i === 0) ? f.g + 0.01 : flat[i - 1].g + 0.01); unpin(); }
      else if (e.key === ']') { const i = findFlat(now()); if (i + 1 < flat.length) { seek(flat[i + 1].g + 0.01); unpin(); } }
      else if (e.key === 'm' || e.key === 'M') toggleMute();
    });

    /* ---------- active sub-step ---------- */
    function findFlat(g) { let lo = 0, hi = flat.length - 1; while (lo < hi) { const m = (lo + hi + 1) >> 1; if (flat[m].g <= g + 0.02) lo = m; else hi = m - 1; } return lo; }
    function markWatched(i) { if (!watched.has(flat[i].key)) { watched.add(flat[i].key); store.set(watchKey, [...watched]); updateMeta(); } }
    function scrollToCurrent() {
      if (S.cur < 0) return;
      const el = $('sub-' + S.cur); const r = el.getBoundingClientRect(), lr = list.getBoundingClientRect();
      const top = r.top - lr.top + list.scrollTop - list.clientHeight * 0.28;
      list.scrollTo({ top: Math.max(0, top), behavior: reduceMotion ? 'auto' : 'smooth' });
    }
    function setCurrent(i) {
      if (i === S.cur) return;
      const prev = S.cur; S.cur = i;
      if (prev >= 0 && S.playing && i === prev + 1) markWatched(prev);
      const f = flat[i];
      document.querySelectorAll('.step.active').forEach((el) => { if (el.id !== 'step-' + f.si) el.classList.remove('active'); });
      $('step-' + f.si).classList.add('active');
      document.querySelectorAll('.sub.current').forEach((el) => el.classList.remove('current'));
      $('sub-' + i).classList.add('current');
      $('nowChip').innerHTML = '<b>' + f.label + '</b>' + esc(f.text);
      document.querySelectorAll('.prog-seg.cur').forEach((el) => el.classList.remove('cur'));
      document.querySelector('.prog-seg[data-step="' + f.si + '"]').classList.add('cur');
      $('progStep').innerHTML = t('stepOf', { n: f.si + 1, m: L.steps.length, t: esc(L.steps[f.si].title) });
      if (S.follow && performance.now() > S.userScrollUntil) requestAnimationFrame(scrollToCurrent);
      if (S.pinned < 0) showStill(L.steps[f.si].subStillIdx[f.ui]);
    }

    /* ---------- render loop ---------- */
    function render(force) {
      const tm = S.switching ? S.lastT : now();
      S.lastT = tm;
      if (!scrubbing) seekEl.value = tm.toFixed(2);
      const pct = tm / total * 100;
      $('fill').style.width = pct + '%';
      $('knob').style.left = pct + '%';
      $('time').textContent = fmt(tm) + ' / ' + fmt(total);
      seekEl.setAttribute('aria-valuetext', t('of', { a: fmt(tm), b: fmt(total) }));
      $('progPct').textContent = Math.round(pct) + '%';
      L.steps.forEach((st, si) => { $('pf-' + si).style.width = Math.min(100, Math.max(0, (tm - st.g0) / (st.g1 - st.g0) * 100)) + '%'; });
      setCurrent(findFlat(tm));
    }

    /* ---------- stills + magnifier ---------- */
    const vp = $('viewport'), img = $('stillImg'), lens = $('lens');
    if (matchMedia('(pointer: coarse)').matches) $('hint').textContent = t('hintTouch');
    const cache = {};
    function preload(src) { if (src && !cache[src]) { const im = new Image(); im.src = src; cache[src] = im; } }
    function showStill(k) {
      if (k === S.still) return;
      S.still = k; const s = stills[k];
      img.src = s.src; img.alt = t('boardAt', { n: s.label, t: s.text });
      lens.style.backgroundImage = 'url("' + s.src + '")';
      $('caption').innerHTML = '<span class="tag">' + esc(s.tag) + '</span>' + esc(s.ui < 0 ? t('beforeStep', { n: s.si + 1 }) + s.text : s.text);
      preload((stills[k + 1] || {}).src); preload((stills[k - 1] || {}).src);
      const st = L.steps[s.si];
      const film = $('film');
      if (film.dataset.step !== String(s.si)) {
        film.dataset.step = String(s.si);
        const ids = [st.firstStill, ...st.subStillIdx];
        film.innerHTML = ids.map((id) => '<button data-k="' + id + '" aria-label="' + esc(t('showStill', { n: stills[id].label })) + '"><img src="' + thumb(stills[id].src) + '" alt=""><span>' + stills[id].label + '</span></button>').join('');
      }
      film.querySelectorAll('button').forEach((b) => b.setAttribute('aria-current', String(+b.dataset.k === k)));
      const curBtn = film.querySelector('[aria-current="true"]');
      if (curBtn) film.scrollTo({ left: curBtn.offsetLeft - film.clientWidth / 2 + curBtn.clientWidth / 2, behavior: reduceMotion ? 'auto' : 'smooth' });
    }
    function pin(k) { S.pinned = k; showStill(k); $('backBtn').hidden = false; }
    function unpin() { S.pinned = -1; $('backBtn').hidden = true; if (S.cur >= 0) { const f = flat[S.cur]; showStill(L.steps[f.si].subStillIdx[f.ui]); } }
    $('backBtn').addEventListener('click', unpin);
    $('prevStill').addEventListener('click', () => pin(Math.max(0, S.still - 1)));
    $('nextStill').addEventListener('click', () => pin(Math.min(stills.length - 1, S.still + 1)));
    $('film').addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) pin(+b.dataset.k); });

    function setZoom(z) { S.zoom = Math.min(6, Math.max(1.5, Math.round(z * 2) / 2)); $('zoomOut2').textContent = S.zoom + '×'; }
    $('zoomIn').addEventListener('click', (e) => { e.stopPropagation(); setZoom(S.zoom + 0.5); });
    $('zoomOut').addEventListener('click', (e) => { e.stopPropagation(); setZoom(S.zoom - 0.5); });
    function moveLens(e) {
      if (e.target.closest('.zoom')) { vp.classList.remove('lensing'); return; }
      const r = vp.getBoundingClientRect();
      const x = e.clientX - r.left, y = e.clientY - r.top;
      const lx = x, ly = e.pointerType === 'mouse' ? y : y - 95; // keep the lens above a finger
      const size = lens.offsetWidth || 190, z = S.zoom;
      lens.style.left = lx + 'px'; lens.style.top = ly + 'px';
      lens.style.backgroundSize = (r.width * z) + 'px ' + (r.height * z) + 'px';
      lens.style.backgroundPosition = (-(x * z - size / 2)) + 'px ' + (-(y * z - size / 2)) + 'px';
      vp.classList.add('lensing');
    }
    vp.addEventListener('pointermove', moveLens);
    vp.addEventListener('pointerdown', (e) => { if (e.target.closest('.zoom')) return; if (e.pointerType !== 'mouse') vp.setPointerCapture(e.pointerId); moveLens(e); });
    vp.addEventListener('pointerup', (e) => { if (e.pointerType !== 'mouse') vp.classList.remove('lensing'); });
    vp.addEventListener('pointerleave', () => vp.classList.remove('lensing'));
    vp.addEventListener('pointercancel', () => vp.classList.remove('lensing'));

    /* ---------- what's next map: this lesson and the lessons linked to it ---------- */
    // Nodes come from the lesson index (lessons/index.json); each lesson lists its own outgoing links.
    const nodes = {};
    const all = IDX ? [...(IDX.lessons || []), ...(IDX.planned || [])] : [];
    all.forEach((n) => { nodes[n.slug] = Object.assign({}, n, { title: (n.i18n && n.i18n[LANG] && n.i18n[LANG].title) || n.title }); });
    nodes[slug] = Object.assign({}, nodes[slug] || {}, { slug, title: L.title, status: L.status === 'planned' ? 'planned' : 'ready', links: L.links || (nodes[slug] || {}).links });
    const edges = [];
    Object.values(nodes).forEach((n) => (n.links || []).forEach((l) => {
      if (nodes[l.to] && !edges.some((e) => e.from === n.slug && e.to === l.to)) edges.push({ from: n.slug, to: l.to, kind: l.kind || 'next' });
    }));
    const svg = $('map');
    function wrap(text, max) {
      const words = String(text).split(/\s+/); const lines = []; let line = '';
      words.forEach((w) => { if ((line + ' ' + w).trim().length > max && line) { lines.push(line); line = w; } else line = (line + ' ' + w).trim(); });
      if (line) lines.push(line); return lines;
    }
    function nodeSvg(n, x, y, r, cls) {
      const planned = n.status === 'planned';
      const fs = r >= 50 ? 13.5 : r >= 40 ? 11.5 : 10;
      const lines = wrap(n.title, r >= 50 ? 13 : r >= 40 ? 11 : 9).slice(0, 4);
      const lh = fs * 1.12; const y0 = y - (lines.length - 1) * lh / 2 + (planned && r >= 40 ? -5 : 0);
      let lbl = lines.map((l, i) => '<text x="' + x + '" y="' + (y0 + i * lh) + '" font-size="' + fs + '">' + esc(l) + '</text>').join('');
      if (planned && r >= 40) lbl += '<text class="day" x="' + x + '" y="' + (y0 + lines.length * lh + 1) + '" font-size="10">' + esc(t('comingSmall')) + '</text>';
      return '<g class="node ' + cls + (planned ? ' later' : '') + '" tabindex="0" role="button" data-id="' + esc(n.slug) + '" aria-label="' + esc(n.title) + (planned ? esc(t('comingLater')) : '') + '"><circle cx="' + x + '" cy="' + y + '" r="' + r + '"/>' + lbl + '</g>';
    }
    function spread(n, cy, gap) { return Array.from({ length: n }, (_, i) => cy + (i - (n - 1) / 2) * gap); }
    function drawMap(id) {
      const cx = 200, cy = 145;
      const ins = edges.filter((e) => e.to === id).map((e) => ({ e, n: nodes[e.from] }));
      const outs = edges.filter((e) => e.from === id).map((e) => ({ e, n: nodes[e.to] }));
      const seen = new Set([id, ...ins.map((o) => o.n.slug), ...outs.map((o) => o.n.slug)]);
      const far = [];
      outs.forEach((o) => edges.filter((e) => e.from === o.n.slug && !seen.has(e.to)).forEach((e) => { seen.add(e.to); far.push({ e, n: nodes[e.to], parent: o.n.slug }); }));
      const pos = { [id]: [cx, cy, 56] };
      const insShown = ins.slice(0, 3), outsShown = outs.slice(0, 3), farShown = far.slice(0, 3);
      spread(insShown.length, cy, 100).forEach((y, i) => { pos[insShown[i].n.slug] = [62, y, 44]; });
      spread(outsShown.length, cy, 104).forEach((y, i) => { pos[outsShown[i].n.slug] = [318, y, 44]; });
      spread(farShown.length, cy, 84).forEach((y, i) => { pos[farShown[i].n.slug] = [404, y, 31]; });
      const link = (a, b, kind, soft) => {
        const [x1, y1, r1] = pos[a], [x2, y2, r2] = pos[b];
        const dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy) || 1;
        const sx = x1 + dx / d * r1, sy = y1 + dy / d * r1, ex = x2 - dx / d * (r2 + 5), ey = y2 - dy / d * (r2 + 5);
        let s = '<path class="edge' + (soft ? ' soft' : '') + '" d="M' + sx + ' ' + sy + 'L' + ex + ' ' + ey + '" marker-end="url(#arr)"/>';
        if (kind && kind !== 'next') {
          const kl = kindLabel(kind), mx = (sx + ex) / 2, my = (sy + ey) / 2, w = kl.length * 6.8 + 12;
          s += '<g class="elabel"><rect x="' + (mx - w / 2) + '" y="' + (my - 9) + '" width="' + w + '" height="18" rx="9"/><text x="' + mx + '" y="' + (my + 0.5) + '">' + esc(kl) + '</text></g>';
        }
        return s;
      };
      let out = '<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs><g>';
      insShown.forEach((o) => { out += link(o.n.slug, id, o.e.kind, false); });
      outsShown.forEach((o) => { out += link(id, o.n.slug, o.e.kind, o.n.status === 'planned'); });
      farShown.forEach((o) => { out += link(o.parent, o.n.slug, o.e.kind, true); });
      out += '</g>';
      insShown.forEach((o) => { const p = pos[o.n.slug]; out += nodeSvg(o.n, p[0], p[1], p[2], ''); });
      outsShown.forEach((o) => { const p = pos[o.n.slug]; out += nodeSvg(o.n, p[0], p[1], p[2], ''); });
      farShown.forEach((o) => { const p = pos[o.n.slug]; out += nodeSvg(o.n, p[0], p[1], p[2], 'far'); });
      out += nodeSvg(nodes[id], cx, cy, 56, 'center');
      if (!ins.length) out += '<text class="map-note" x="62" y="' + cy + '">' + esc(t('startHere')) + '</text>';
      if (!outs.length) out += '<text class="map-note" x="318" y="' + cy + '">' + esc(t('moreSoon')) + '</text>';
      svg.innerHTML = out;
    }
    function openNode(nid) {
      const n = nodes[nid]; if (!n) return;
      if (nid === slug) toast(t('youAreHere'));
      else if (n.status === 'planned') toast(t('notReady', { t: n.title }));
      else { const u = new URL(lessonHref(nid), location.href); if (new URLSearchParams(location.search).get('lang')) u.searchParams.set('lang', LANG); location.href = u.href; }
    }
    svg.addEventListener('click', (e) => { const g = e.target.closest('.node'); if (g) openNode(g.dataset.id); });
    svg.addEventListener('keydown', (e) => { const g = e.target.closest('.node'); if (g && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openNode(g.dataset.id); } });

    /* ---------- go ---------- */
    updateMeta(); renderButtons();
    const h = (location.hash || '').match(/^#step-?(\d+)$/);
    const startStep = h ? Math.min(L.steps.length, Math.max(1, +h[1])) - 1 : 0;
    if (startStep) seek(L.steps[startStep].g0 + 0.01, false);
    currentTime = () => now();
    try {
      const r = JSON.parse(sessionStorage.getItem('glitchn-resume') || 'null'); sessionStorage.removeItem('glitchn-resume');
      if (r && r.path === location.pathname && r.t > 0.5) seek(r.t, false);
    } catch (e) {}
    render(true);
    drawMap(slug);
    (function loop() { render(); requestAnimationFrame(loop); })();
  }
})();
