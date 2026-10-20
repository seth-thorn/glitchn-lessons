/* Glitch'n Radio: music from Audiobulb Records while you browse and build.
   A small "Radio" button in the corner of every page opens a player with three channels (tracks.js).
   The music streams through SoundCloud's embedded player (its widget API), credited and linked to the label;
   nothing loads from SoundCloud until someone opens the radio.
   Moving to another page: the player remembers the track and the spot, and picks up there on the next page.
   If the browser won't start sound by itself on the new page, the button offers "Resume" instead. */
(() => {
  if (window.__glitchnRadio) return;
  window.__glitchnRadio = true;
  const SRC = (document.currentScript && document.currentScript.src) || location.href;
  const HERE = new URL('./', SRC).href, ROOT = new URL('../', SRC).href;
  const VER = '202610201250';

  const WORDS = {
    en: { radio: 'Radio', title: "Glitch'n Radio", open: "Open Glitch'n Radio", close: 'Close', play: 'Play', pause: 'Pause', next: 'Next track',
      volume: 'Volume', channels: 'Channels', resume: 'Resume', resumeHint: 'Press play to keep listening.', learn: 'Learn how in {t}',
      from: 'Music from', label: 'Audiobulb Records', onSC: 'This track on SoundCloud', now: 'Now playing', notes: 'How it was made' },
    es: { radio: 'Radio', title: "Radio Glitch'n", open: "Abrir la Radio Glitch'n", close: 'Cerrar', play: 'Reproducir', pause: 'Pausa', next: 'Siguiente pista',
      volume: 'Volumen', channels: 'Canales', resume: 'Seguir', resumeHint: 'Pulsa reproducir para seguir escuchando.', learn: 'Aprende cómo en {t}',
      from: 'Música de', label: 'Audiobulb Records', onSC: 'Esta pista en SoundCloud', now: 'Sonando', notes: 'Cómo se hizo' },
  };
  const LESSONS = {
    'blink-to-drum-machine': { en: 'From Blink to Drum Machine', es: 'Del parpadeo a la caja de ritmos' },
    'radio-and-reset': { en: 'Two Oscillators, a Radio and a Reset', es: 'Dos osciladores, una radio y un reinicio' },
    'random-rhythms': { en: 'Random Rhythms with the 4021', es: 'Ritmos al azar con el 4021' },
    'stepping-sounds': { en: 'Stepping Through Sounds with the 4051', es: 'Recorrer sonidos con el 4051' },
    'three-oscillators': { en: 'Three Oscillators and Strange Things', es: 'Tres osciladores y cosas extrañas' },
  };

  /* ---------- small helpers ---------- */
  const lang = () => (/^es/i.test(document.documentElement.lang || '') ? 'es' : 'en');
  const w = (k, v) => String(WORDS[lang()][k]).replace(/\{(\w+)\}/g, (_, x) => (v && v[x] != null ? v[x] : ''));
  const loc = (o) => (o ? o[lang()] || o.en : '');
  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const ART = 'https://i1.sndcdn.com/';
  // Safari (and every browser on iPhone/iPad) only lets sound start straight from a tap. If the player starts any other
  // way it runs silently and stays silent, so there play() must happen inside the tap, and nothing starts by itself.
  const UA = navigator.userAgent;
  const STRICT = /iPad|iPhone|iPod/.test(UA) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1) ||
    (/AppleWebKit/.test(UA) && /Safari/.test(UA) && !/Chrome|Chromium|CriOS|FxiOS|Edg|OPR|Android/.test(UA));
  const calm = () => matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.dataset.style === 'clean';
  const local = { get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
  const session = { get(d) { try { const v = sessionStorage.getItem('glitchn-radio'); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(v) { try { sessionStorage.setItem('glitchn-radio', JSON.stringify(v)); } catch (e) {} } };
  const script = (src) => new Promise((ok, no) => { const s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = no; document.head.appendChild(s); });
  const ICON = {
    radio: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9.5h16v10H4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M7 9.5 17 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="15.5" cy="14.5" r="2.5" fill="currentColor"/><path d="M7 13h4M7 16h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>',
    pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6.5" y="5" width="4" height="14" rx="1" fill="currentColor"/><rect x="13.5" y="5" width="4" height="14" rx="1" fill="currentColor"/></svg>',
    next: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5.5v13l9-6.5z" fill="currentColor"/><rect x="16" y="5.5" width="3" height="13" rx="1" fill="currentColor"/></svg>',
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    wave: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 24h6l4-10 6 20 6-16 4 6h10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  };

  const link = document.createElement('link');
  link.rel = 'stylesheet'; link.href = HERE + 'radio.css?v=' + VER;
  document.head.appendChild(link);
  (window.GLITCHN_RADIO ? Promise.resolve() : script(HERE + 'tracks.js?v=' + VER)).then(build).catch(() => {});

  function build() {
    const DATA = window.GLITCHN_RADIO; if (!DATA) return;
    const CH = DATA.channels;
    const saved = session.get(null);
    const S = {
      ch: Math.max(0, CH.findIndex((c) => c.key === ((saved && saved.ch) || local.get('glitchn-radio-ch', 'listen')))),
      idx: (saved && saved.idx) || {},
      vol: local.get('glitchn-radio-vol', 80),
      playing: false, wanted: false, blocked: false, open: false, art: {}, widget: null, ready: null, live: false, loadedId: null, posMs: 0,
    };
    CH.forEach((c) => { if (S.idx[c.key] == null) S.idx[c.key] = Math.floor(Math.random() * c.tracks.length); });
    const chan = () => CH[S.ch], track = () => chan().tracks[S.idx[chan().key] % chan().tracks.length];
    const save = (extra) => session.set(Object.assign({ ch: chan().key, idx: S.idx, id: track().id, pos: S.posMs, playing: S.wanted, t: Date.now() }, extra || {}));

    /* ---------- the markup: the corner button, the pop-up card, the player ---------- */
    const root = document.createElement('div');
    root.className = 'gr' + (calm() ? ' gr-calm' : '');
    root.innerHTML =
      '<div class="gr-card" id="grCard" role="status" aria-live="polite" hidden></div>' +
      '<section class="gr-panel" id="grPanel" aria-labelledby="grTitle">' +
        '<div class="gr-head"><h2 id="grTitle"></h2><button type="button" class="gr-icon" id="grClose">' + ICON.close + '</button></div>' +
        '<div class="gr-tabs" role="tablist" id="grTabs"></div>' +
        '<p class="gr-blurb" id="grBlurb"></p>' +
        '<div class="gr-now"><div class="gr-art" id="grArt">' + ICON.wave + '</div><div class="gr-meta"><b id="grTrack"></b><span id="grArtist"></span></div></div>' +
        '<p class="gr-note" id="grNote"></p>' +
        '<a class="gr-lesson" id="grLesson" hidden></a>' +
        '<div class="gr-ctl"><button type="button" class="gr-play" id="grPlay"></button><button type="button" class="gr-icon" id="grNext">' + ICON.next + '</button>' +
          '<label class="gr-vol"><span class="gr-sr" id="grVolLabel"></span><input type="range" min="0" max="100" step="5" id="grVol"></label></div>' +
        '<div class="gr-foot"><span id="grFrom"></span> <a href="https://www.audiobulb.com" target="_blank" rel="noopener" id="grLabel"></a> · <a target="_blank" rel="noopener" id="grSC"></a></div>' +
        '<div class="gr-sc" id="grSCbox"></div>' +
      '</section>' +
      '<button type="button" class="gr-pill" id="grPill" aria-expanded="false" aria-controls="grPanel"><span class="gr-ic">' + ICON.radio + '</span><span id="grPillText"></span><span class="gr-eq" aria-hidden="true"><i></i><i></i><i></i></span></button>';
    document.body.appendChild(root);
    const $ = (id) => document.getElementById(id);

    /* ---------- drawing ---------- */
    function draw() {
      const t = track(), c = chan();
      root.classList.toggle('gr-calm', calm());
      root.classList.toggle('playing', S.playing);
      root.classList.toggle('blocked', S.blocked && !S.playing);
      $('grTitle').textContent = w('title');
      $('grClose').setAttribute('aria-label', w('close'));
      $('grNext').setAttribute('aria-label', w('next'));
      $('grTabs').setAttribute('aria-label', w('channels'));
      const tabs = $('grTabs');   // built once, then only updated, so focus stays put
      if (!tabs.children.length) tabs.innerHTML = CH.map((x, i) => '<button type="button" role="tab" data-i="' + i + '"></button>').join('');
      [...tabs.children].forEach((b, i) => { b.textContent = loc(CH[i].name); b.setAttribute('aria-selected', String(i === S.ch)); b.tabIndex = i === S.ch ? 0 : -1; });
      $('grBlurb').textContent = loc(c.blurb);
      $('grTrack').textContent = t.title;
      $('grArtist').textContent = t.artist;
      $('grNote').textContent = loc(t.note);
      const L = t.lesson && LESSONS[t.lesson];
      $('grLesson').hidden = !L;
      if (L) { $('grLesson').textContent = w('learn', { t: loc(L) }) + ' →'; $('grLesson').href = ROOT + 'lessons/' + t.lesson + '/index.html'; }
      const art = S.art[t.id] || (t.art ? ART + t.art : '');
      $('grArt').innerHTML = ICON.wave + (art ? '<img src="' + esc(art) + '" alt="" width="64" height="64" onerror="this.remove()">' : '');
      $('grPlay').innerHTML = (S.playing ? ICON.pause : ICON.play) + '<span>' + esc(S.playing ? w('pause') : (S.blocked ? w('resume') : w('play'))) + '</span>';
      $('grPlay').setAttribute('aria-pressed', String(S.playing));
      $('grPlay').disabled = STRICT && !!S.ready && !S.live;   // Safari: wait until the player is there, so the tap can start it
      $('grVolLabel').textContent = w('volume');
      $('grVol').value = S.vol;
      $('grFrom').textContent = w('from');
      $('grLabel').textContent = w('label');
      $('grSC').textContent = w('onSC');
      $('grSC').href = 'https://soundcloud.com/audiobulb/' + t.s;
      $('grPill').setAttribute('aria-label', S.blocked && !S.playing ? w('resume') + ': ' + w('title') : w('open'));
      $('grPillText').textContent = S.blocked && !S.playing ? w('resume') : w('radio');
      $('grPill').setAttribute('aria-expanded', String(S.open));
      $('grPanel').classList.toggle('open', S.open);
      $('grPanel').setAttribute('aria-hidden', String(!S.open));
      $('grPanel').inert = !S.open;
    }

    /* the card that pops up over the button when a new track starts and the player is closed */
    let cardTimer = 0;
    function card() {
      if (S.open) return;
      const t = track(), art = S.art[t.id] || (t.art ? ART + t.art : '');
      $('grCard').innerHTML = '<button type="button" class="gr-icon gr-x" aria-label="' + esc(w('close')) + '">' + ICON.close + '</button>' +
        '<span class="gr-kick">' + esc(w('now')) + ' · ' + esc(loc(chan().name)) + '</span>' +
        '<div class="gr-now">' + '<div class="gr-art">' + ICON.wave + (art ? '<img src="' + esc(art) + '" alt="" width="64" height="64" onerror="this.remove()">' : '') + '</div>' +
        '<div class="gr-meta"><b>' + esc(t.title) + '</b><span>' + esc(t.artist) + '</span></div></div>' +
        '<p class="gr-note">' + esc(loc(t.note)) + '</p>';
      $('grCard').hidden = false;
      clearTimeout(cardTimer); cardTimer = setTimeout(() => { $('grCard').hidden = true; }, 11000);
    }
    $('grCard').addEventListener('click', (e) => { $('grCard').hidden = true; if (!e.target.closest('.gr-x')) toggle(true); });

    /* ---------- SoundCloud: the widget loads on the first press of play ---------- */
    const url = (t) => 'https://api.soundcloud.com/tracks/' + t.id;
    function widget() {
      if (S.ready) return S.ready;
      S.ready = script('https://w.soundcloud.com/player/api.js').catch((e) => { S.ready = null; throw e; }).then(() => new Promise((ok) => {
        const f = document.createElement('iframe');
        f.title = 'SoundCloud'; f.allow = 'autoplay'; f.width = '100%'; f.height = '20'; f.scrolling = 'no'; f.frameBorder = 'no';
        f.src = 'https://w.soundcloud.com/player/?url=' + encodeURIComponent(url(track())) + '&color=%23fa6e79&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false&visual=false';
        $('grSCbox').appendChild(f);
        const W = window.SC.Widget(f); S.widget = W; S.loadedId = track().id;
        const E = window.SC.Widget.Events;
        W.bind(E.READY, () => { S.live = true; W.setVolume(S.vol); ok(W); draw(); });
        W.bind(E.PLAY, () => { S.playing = true; S.wanted = true; S.blocked = false; info(); save(); draw(); });
        W.bind(E.PAUSE, () => { if (leaving) return; S.playing = false; S.wanted = false; save(); draw(); });   // paused here or in SoundCloud's own bar
        W.bind(E.FINISH, () => { S.playing = false; next(true); });
        let last = 0;
        W.bind(E.PLAY_PROGRESS, (p) => { S.posMs = p.currentPosition; if (Date.now() - last > 2000) { last = Date.now(); save(); } });
      }));
      return S.ready;
    }
    function info() {
      if (!S.widget) return;
      S.widget.getCurrentSound((snd) => {
        if (!snd) return;
        const id = snd.id; const art = snd.artwork_url ? snd.artwork_url.replace('-large', '-t200x200') : '';
        if (art && S.art[id] !== art) { S.art[id] = art; draw(); }
      });
    }
    // start the current track (from a given spot), playing or not
    function start(play, fromMs, pop) {
      const t = track();
      S.wanted = play; S.posMs = fromMs || 0; save();
      return widget().then((W) => new Promise((ok) => {
        const go = () => { if (fromMs) W.seekTo(fromMs); W.setVolume(S.vol); if (play) W.play(); if (pop) card(); ok(); };
        if (S.loadedId === t.id) go();
        else { S.loadedId = t.id; W.load(url(t), { auto_play: false, show_user: true, visual: false, hide_related: true, show_comments: false, show_reposts: false, show_teaser: false, color: '#fa6e79', callback: go }); }
      }));
    }
    // load SoundCloud's player (paused) ahead of the first press of play
    function prime() { if (!S.ready) start(false, S.posMs).catch(() => {}); }   // offline or blocked: try again next time
    function next(auto) {
      const c = chan(); S.idx[c.key] = (S.idx[c.key] + 1) % c.tracks.length; S.posMs = 0; draw();
      const play = auto || S.playing || S.wanted;
      if (S.widget || play) start(play, 0, auto).catch(() => {}); else save();
    }
    function playPause() {
      if (S.playing) { S.wanted = false; S.widget.pause(); save(); return; }
      S.blocked = false;
      if (S.live && S.loadedId === track().id) {   // the usual case: the player is loaded, so start it right here, inside the tap
        S.wanted = true; save();
        S.widget.setVolume(S.vol); if (S.posMs) S.widget.seekTo(S.posMs); S.widget.play();
        return;
      }
      start(true, S.posMs).then(draw).catch(() => {});
    }
    function toggle(open) {
      S.open = open == null ? !S.open : open;
      if (S.open) { $('grCard').hidden = true; prime(); }
      draw();
      if (S.open) { const sel = $('grTabs').querySelector('[aria-selected="true"]'); if (sel) sel.focus(); } else $('grPill').focus({ preventScroll: true });
    }
    $('grPill').addEventListener('click', () => { if (S.blocked && !S.playing) { playPause(); return; } toggle(); });
    $('grClose').addEventListener('click', () => toggle(false));
    $('grPlay').addEventListener('click', playPause);
    $('grNext').addEventListener('click', () => next(false));
    $('grVol').addEventListener('input', (e) => { S.vol = +e.target.value; local.set('glitchn-radio-vol', S.vol); if (S.widget) S.widget.setVolume(S.vol); });
    $('grTabs').addEventListener('click', (e) => {
      const b = e.target.closest('[data-i]'); if (!b || +b.dataset.i === S.ch) return;
      const was = S.playing || S.wanted; S.ch = +b.dataset.i; S.posMs = 0; local.set('glitchn-radio-ch', chan().key); draw();
      $('grTabs').querySelector('[aria-selected="true"]').focus();
      if (was) start(true, 0).catch(() => {}); else save();
    });
    $('grTabs').addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const i = (S.ch + (e.key === 'ArrowRight' ? 1 : CH.length - 1)) % CH.length;
      $('grTabs').querySelectorAll('[data-i]')[i].click();
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && S.open) toggle(false); });
    document.addEventListener('click', (e) => { if (S.open && !e.composedPath().includes(root)) toggle(false); });   // a click anywhere else closes it
    let leaving = false;   // the page is going away: the sound stopping then isn't a pause
    addEventListener('beforeunload', () => { leaving = true; save(); });
    addEventListener('pagehide', () => { leaving = true; save(); });
    addEventListener('pageshow', (e) => { if (e.persisted) leaving = false; });
    // the page switched language: redraw
    new MutationObserver(draw).observe(document.documentElement, { attributes: true, attributeFilter: ['lang', 'data-style'] });

    draw();

    /* ---------- coming from another page while music was playing: pick up where it was ---------- */
    if (saved && saved.playing && Date.now() - saved.t < 30 * 60 * 1000) {
      if (STRICT) { S.blocked = true; S.posMs = saved.pos || 0; draw(); start(false, S.posMs).then(() => { S.wanted = true; save(); }).catch(() => {}); }   // one tap on Resume continues
      else start(true, saved.pos || 0).then(() => setTimeout(() => { if (!S.playing) { S.blocked = true; draw(); } }, 2500)).catch(() => { S.blocked = true; draw(); });
    }
  }
})();
