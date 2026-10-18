/* Glitch'n part pictures: flat, top-down, in the colours the parts really have (viewBox 0 0 100 100).
   One small SVG per kit key (materials/kit.json, lessons/catalog.json). Used by the What you need page
   and by every lesson's parts list. GlitchnParts.picture(key) returns an <svg> string ('' for an unknown key). */
(function () {
  const LEG = '#A9ADB2';
  const legsDown = (xs, y1, y2, w = 2.2) => xs.map((x) => `<rect x="${x - w / 2}" y="${y1}" width="${w}" height="${y2 - y1}" rx="${w / 2}" fill="${LEG}"/>`).join('');
  const legsSide = (y, x1, x2) => `<rect x="${x1}" y="${y - 1.1}" width="${x2 - x1}" height="2.2" rx="1.1" fill="${LEG}"/>`;
  // A chip seen from above: pins/2 legs on each side (the 40106 has 14 pins, the 4040, 4021 and 4051 have 16).
  const chip = (num, pins) => {
    const n = pins / 2, x0 = 20, x1 = 80, step = (x1 - x0) / (n - 1);
    const xs = Array.from({ length: n }, (_, i) => x0 + i * step);
    const w = n > 7 ? 4.2 : 4.8;
    return `${xs.map((x) => `<rect x="${x - w / 2}" y="30" width="${w}" height="8" rx="1" fill="${LEG}"/><rect x="${x - w / 2}" y="62" width="${w}" height="8" rx="1" fill="${LEG}"/>`).join('')}
      <rect x="12" y="35" width="76" height="30" rx="3" fill="#26262A"/><path d="M12 44a6 6 0 0 1 0 12z" fill="#3E3E43"/>
      <rect x="27" y="39.5" width="56" height="21" fill="#FFF"/><text x="55" y="50.5" text-anchor="middle" dominant-baseline="middle" font-family="Manrope, sans-serif" font-weight="500" font-size="12.5" fill="#222">${num}</text>`;
  };
  const resistor = (bands) => `${legsSide(50, 6, 94)}<rect x="28" y="40" width="44" height="20" rx="9" fill="#E9D6AE"/>
      ${bands.map((c, i) => `<rect x="${36 + i * 8}" y="40" width="4.5" height="20" fill="${c}"/>`).join('')}`;
  const can = (w, h, color) => { const x = 50 - w / 2, y = 44 - h / 2;
    return `${legsDown([50 - w / 5, 50 + w / 5], y + h - 2, 92)}<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${w / 6}" fill="${color}"/>
      <rect x="${x + w * .66}" y="${y}" width="${w * .16}" height="${h}" fill="#C9CDD6" opacity=".75"/><ellipse cx="50" cy="${y + 3}" rx="${w / 2 - 2}" ry="2.2" fill="#000" opacity=".18"/>`; };
  const ART = {
    breadboard: () => { let d = ''; for (let r = 0; r < 5; r++) for (let c = 0; c < 12; c++) d += `<rect x="${17 + c * 6}" y="${36 + r * 6}" width="2.6" height="2.6" fill="#8C857C"/>`;
      return `<rect x="6" y="20" width="88" height="60" rx="4" fill="#FBF8F2"/><rect x="11" y="25" width="78" height="1.6" fill="#E25B5B"/><rect x="11" y="73.4" width="78" height="1.6" fill="#4C7BD9"/>${d}`; },
    jumpers: () => `<path d="M18 74V48a8 8 0 0 1 8-8h0a8 8 0 0 1 8 8v26" fill="none" stroke="#F08A24" stroke-width="5" stroke-linecap="round"/>
      <path d="M44 74V34a10 10 0 0 1 10-10h0a10 10 0 0 1 10 10v40" fill="none" stroke="#E34B4B" stroke-width="5" stroke-linecap="round"/>
      <path d="M72 74V58a6 6 0 0 1 12 0v16" fill="none" stroke="#F2C230" stroke-width="5" stroke-linecap="round"/>`,
    '40106': () => chip('40106', 14), '4040': () => chip('4040', 16), '4021': () => chip('4021', 16), '4051': () => chip('4051', 16),
    pot: () => `${legsDown([38, 50, 62], 70, 88)}<rect x="24" y="22" width="52" height="50" rx="6" fill="#2F64C9"/><circle cx="50" cy="47" r="18" fill="#4A80E8"/><rect x="47.5" y="32" width="5" height="17" rx="2.5" fill="#FFF"/>`,
    photocell: () => `${legsDown([44, 56], 62, 92)}<circle cx="50" cy="42" r="22" fill="#F1D7A3"/><path d="M36 36h24v5H40v5h20v5H36" fill="none" stroke="#B5523B" stroke-width="3" stroke-linejoin="round"/>`,
    button: () => `<rect x="22" y="22" width="56" height="56" rx="5" fill="#2B2B2E"/><circle cx="50" cy="50" r="16" fill="#55555B"/>
      ${[[18, 30], [18, 70], [82, 30], [82, 70]].map(([x, y]) => `<rect x="${x - 4}" y="${y - 2}" width="8" height="4" rx="2" fill="${LEG}"/>`).join('')}`,
    led: () => `${legsDown([44], 62, 94)}${legsDown([56], 62, 86)}<path d="M33 64V40a17 17 0 0 1 34 0v24z" fill="#F25C54"/><rect x="31" y="62" width="38" height="5" rx="2" fill="#E04A43"/><ellipse cx="44" cy="36" rx="4" ry="7" fill="#FFF" opacity=".45"/>`,
    diode: () => `${legsSide(50, 6, 94)}<rect x="32" y="42" width="36" height="16" rx="8" fill="#E58B5B"/><rect x="58" y="42" width="5" height="16" fill="#222"/>`,
    r_1k: () => resistor(['#7A4B2A', '#222', '#D8403A']),
    r_10k: () => resistor(['#7A4B2A', '#222', '#F08A24']),
    r_4k7: () => resistor(['#F2C230', '#7D4BC2', '#D8403A']),
    r_22k: () => resistor(['#D8403A', '#D8403A', '#F08A24']),
    r_other: () => resistor(['#9AA0A6', '#9AA0A6', '#9AA0A6']),
    c_0u1: () => `${legsDown([44, 56], 58, 92)}<ellipse cx="50" cy="44" rx="17" ry="15" fill="#E9B949"/>`,
    c_68p: () => `${legsDown([45, 55], 56, 92)}<circle cx="50" cy="44" r="13" fill="#D98B3A"/>`,
    c_1u: () => can(22, 30, '#2E3B8F'),
    c_10u: () => can(26, 36, '#2E3B8F'),
    c_100u: () => can(32, 44, '#26262A'),
    jack: () => `${legsDown([38, 50, 62], 70, 88)}<rect x="28" y="28" width="44" height="44" rx="4" fill="#26262A"/><circle cx="50" cy="44" r="9" fill="#8E9299"/><circle cx="50" cy="44" r="4.5" fill="#26262A"/>`,
    cable: () => `<path d="M22 70C22 40 78 60 78 30" fill="none" stroke="#2B2B2E" stroke-width="5" stroke-linecap="round"/>
      <rect x="16" y="68" width="12" height="16" rx="3" fill="#2B2B2E"/><rect x="20" y="84" width="4" height="10" rx="2" fill="${LEG}"/>
      <rect x="72" y="16" width="12" height="16" rx="3" fill="#2B2B2E"/><rect x="76" y="6" width="4" height="10" rx="2" fill="${LEG}"/>`,
    speaker: () => `<rect x="12" y="28" width="76" height="46" rx="20" fill="#FA6E79"/><circle cx="50" cy="51" r="15" fill="#E25562"/>
      ${[[-6, -6], [0, -6], [6, -6], [-6, 0], [0, 0], [6, 0], [-6, 6], [0, 6], [6, 6]].map(([x, y]) => `<circle cx="${50 + x}" cy="${51 + y}" r="1.6" fill="#FA6E79"/>`).join('')}`,
    battery: () => `<rect x="28" y="24" width="44" height="64" rx="5" fill="#2B2B2E"/><rect x="28" y="54" width="44" height="16" fill="#F2C230"/>
      <rect x="35" y="14" width="10" height="10" rx="2" fill="${LEG}"/><path d="M55 14h10v10H55z" fill="${LEG}"/><circle cx="60" cy="19" r="3" fill="#2B2B2E"/>`,
    'battery-clip': () => `<rect x="30" y="16" width="40" height="18" rx="4" fill="#2B2B2E"/>
      <path d="M42 34c0 20-14 26-14 48" fill="none" stroke="#E34B4B" stroke-width="4" stroke-linecap="round"/>
      <path d="M58 34c0 20 14 26 14 48" fill="none" stroke="#2B2B2E" stroke-width="4" stroke-linecap="round"/>`,
    alligator: () => `<path d="M14 62l34-10 2 7-34 9z" fill="#E34B4B"/><path d="M14 52l34 6-2 7-34-6z" fill="#E34B4B" opacity=".85"/>
      <path d="M50 58c14 0 18 18 34 18" fill="none" stroke="#E34B4B" stroke-width="4" stroke-linecap="round"/><rect x="82" y="72" width="10" height="8" rx="2" fill="${LEG}"/>`,
    radio: () => `<rect x="14" y="34" width="72" height="48" rx="8" fill="#9A4D76"/><circle cx="36" cy="58" r="12" fill="#B17491"/><rect x="56" y="48" width="22" height="6" rx="3" fill="#F6E8E0"/><rect x="56" y="60" width="22" height="6" rx="3" fill="#F6E8E0"/>
      <rect x="68" y="10" width="3" height="26" rx="1.5" fill="${LEG}" transform="rotate(20 70 34)"/>`,
  };
  window.GlitchnParts = {
    has: (k) => !!ART[k],
    picture: (k) => (ART[k] ? '<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">' + ART[k]() + '</svg>' : ''),
  };
})();
