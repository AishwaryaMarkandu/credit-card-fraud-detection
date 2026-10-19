/* Charts and interactions for the fraud-detection report. No dependencies: plain SVG driven by results/metrics.json. */
(function () {
'use strict';
var D = window.DATA, T = window.I18N, P = window.PAGE, LANG = P.lang;
var NS = 'http://www.w3.org/2000/svg';

/* ---------- helpers ---------- */
function nf(n, o) { return new Intl.NumberFormat(LANG, o).format(n); }
function fix(n, d) { d = d || 0; return nf(n, { minimumFractionDigits: d, maximumFractionDigits: d }); }
function pct(x, d) { return fix(x * 100, d == null ? 1 : d) + (LANG === 'fr' ? ' %' : '%'); }
function eur(x, d) { d = d || 0; return LANG === 'fr' ? fix(x, d) + ' €' : '€' + fix(x, d); }
function amt(v) { /* compact euro labels for axes */
  var s = v >= 1000 ? fix(v / 1000) + 'k' : fix(v);
  return LANG === 'fr' ? s + ' €' : '€' + s;
}
function $(s, r) { return (r || document).querySelector(s); }
function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
function S(tag, attrs, parent) {
  var e = document.createElementNS(NS, tag);
  for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function T_(parent, x, y, str, cls, anchor) {
  var t = S('text', { x: x, y: y, 'text-anchor': anchor || 'start', 'class': cls || '' }, parent);
  t.textContent = str; return t;
}
function lin(d0, d1, r0, r1) {
  var f = function (v) { return r0 + (v - d0) / (d1 - d0) * (r1 - r0); };
  f.inv = function (p) { return d0 + (p - r0) / (r1 - r0) * (d1 - d0); };
  return f;
}
function niceTicks(max, n) {
  var raw = max / n, mag = Math.pow(10, Math.floor(Math.log10(raw))), r = raw / mag;
  var step = (r < 1.5 ? 1 : r < 3.5 ? 2 : r < 7.5 ? 5 : 10) * mag, out = [];
  for (var v = 0; v <= max + step * 0.001; v += step) out.push(+v.toFixed(10));
  return out;
}
function el(tag, cls, html, parent) {
  var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html;
  if (parent) parent.appendChild(e); return e;
}
function rbar(x, y, w, h, r, dir) { /* bar with a rounded data-end and square baseline. dir: 'up' | 'right' | 'left' */
  r = Math.min(r, Math.abs(dir === 'up' ? h : w) / 2);
  if (dir === 'up') return 'M' + x + ',' + (y + h) + 'V' + (y + r) + 'Q' + x + ',' + y + ' ' + (x + r) + ',' + y + 'H' + (x + w - r) + 'Q' + (x + w) + ',' + y + ' ' + (x + w) + ',' + (y + r) + 'V' + (y + h) + 'Z';
  if (dir === 'right') return 'M' + x + ',' + y + 'H' + (x + w - r) + 'Q' + (x + w) + ',' + y + ' ' + (x + w) + ',' + (y + r) + 'V' + (y + h - r) + 'Q' + (x + w) + ',' + (y + h) + ' ' + (x + w - r) + ',' + (y + h) + 'H' + x + 'Z';
  return 'M' + (x + w) + ',' + y + 'H' + (x + r) + 'Q' + x + ',' + y + ' ' + x + ',' + (y + r) + 'V' + (y + h - r) + 'Q' + x + ',' + (y + h) + ' ' + (x + r) + ',' + (y + h) + 'H' + (x + w) + 'Z';
}
function ft(t) { return fix(t, t < 0.01 ? 3 : 2); }
function fname(f) { return f === 'log_amount' ? T.js_amount_log + ' (log)' : f === 'hour' ? T.js_hour : f; }
var MODEL_CLASS = { logreg: 'blue', rf: 'orange', xgb: 'aqua' };

/* ---------- tooltip ---------- */
var tip = $('#tip');
function showTip(html, ev) {
  tip.innerHTML = html; tip.style.opacity = 1; tip.setAttribute('aria-hidden', 'false');
  var r = tip.getBoundingClientRect(), x = ev.clientX + 14, y = ev.clientY + 14;
  if (x + r.width > innerWidth - 8) x = ev.clientX - r.width - 14;
  if (y + r.height > innerHeight - 8) y = ev.clientY - r.height - 14;
  tip.style.transform = 'translate(' + Math.max(8, x) + 'px,' + Math.max(8, y) + 'px)';
}
function hideTip() { tip.style.opacity = 0; tip.setAttribute('aria-hidden', 'true'); tip.style.transform = 'translate(-9999px,-9999px)'; }
function bindHover(target, onMove) {
  target.addEventListener('pointermove', onMove); target.addEventListener('pointerdown', onMove);
  target.addEventListener('pointerleave', function () { hideTip(); if (target._leave) target._leave(); });
}
function localX(ev, svg) { var r = svg.getBoundingClientRect(); return (ev.clientX - r.left) * (svg.viewBox.baseVal.width / r.width); }

/* ---------- chart registry (re-render on resize) ---------- */
var REG = {};
function chart(id, draw) {
  var root = $('#' + id + ' .plot'); if (!root) return;
  var c = REG[id] = { root: root, draw: draw, w: 0, first: true };
  c.run = function () { var w = Math.floor(root.clientWidth); if (w < 160) return; c.w = w; root.innerHTML = ''; draw(root, w, c.first); c.first = false; };
  new ResizeObserver(function () { var w = Math.floor(root.clientWidth); if (w >= 160 && w !== c.w) c.run(); }).observe(root);
}
function redraw(id) { if (REG[id]) REG[id].run(); }
function frame(root, w, h, label) {
  var svg = S('svg', { viewBox: '0 0 ' + w + ' ' + h, width: w, height: h, role: 'img', 'aria-label': label || '' });
  root.appendChild(svg); return svg;
}
function legend(sel, items) {
  $$(sel).forEach(function (n) {
    n.innerHTML = items.map(function (i) { return '<span><i class="' + (i.sq ? 'sq ' : '') + 'bg-' + i.c + '"></i>' + i.t + '</span>'; }).join('');
  });
}
function addTable(id, headers, rows) {
  var host = $('#' + id + ' .tbl'); if (!host) return;
  host.innerHTML = '<details><summary>' + T.table_view + '</summary><div class="tw"><table><thead><tr>' +
    headers.map(function (h) { return '<th>' + h + '</th>'; }).join('') + '</tr></thead><tbody>' +
    rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div></details>';
}
function yGrid(g, y, ticks, x0, x1, fmt) {
  ticks.forEach(function (v) {
    var gy = S('g', { 'class': 'grid' }, g); S('line', { x1: x0, x2: x1, y1: y(v), y2: y(v) }, gy);
    T_(g, x0 - 8, y(v) + 4, fmt(v), '', 'end');
  });
}

/* ---------- 1. waffle ---------- */
(function () {
  var w = $('#waffle'); if (!w) return;
  var n = P.one_in, fraudAt = Math.round(n * 0.58), html = '';
  w.style.gridTemplateColumns = 'repeat(30, 1fr)';
  for (var i = 0; i < n; i++) html += '<i' + (i === fraudAt ? ' class="f"' : '') + '></i>';
  w.innerHTML = html;
})();

/* ---------- 2. amount distribution ---------- */
(function () {
  var A = D.eda.amount_hist, e = A.edges_log, nb = A.legit.length;
  legend('[data-legend=classes]', [{ c: 'legit', t: T.js_legit }, { c: 'fraud', t: T.js_fraud }]);
  var ticksV = [0, 1, 10, 100, 1000, 10000];
  var mids = []; for (var q = 0; q < nb; q++) mids.push((e[q] + e[q + 1]) / 2);
  chart('ch-amount', function (root, w, first) {
    var H = Math.round(Math.min(300, Math.max(220, w * 0.58))), m = { t: 14, r: 12, b: 34, l: 46 };
    var svg = frame(root, w, H, T.js_share_class);
    var ymax = Math.max.apply(null, A.legit.concat(A.fraud)) * 1.12;
    var x = lin(0, 10.5, m.l, w - m.r), y = lin(0, ymax, H - m.b, m.t);
    var g = S('g', {}, svg);
    yGrid(g, y, niceTicks(ymax, 4), m.l, w - m.r, function (v) { return pct(v, 0); });
    S('line', { x1: m.l, x2: w - m.r, y1: H - m.b, y2: H - m.b, 'class': 'axis', stroke: 'var(--axis)' }, g);
    ticksV.forEach(function (v) { T_(g, x(Math.log1p(v)), H - m.b + 18, amt(v), '', 'middle'); });
    [['legit', A.legit], ['fraud', A.fraud]].forEach(function (s) {
      var pts = mids.map(function (mm, i) { return x(mm) + ',' + y(s[1][i]); });
      S('path', { d: 'M' + x(mids[0]) + ',' + y(0) + 'L' + pts.join('L') + 'L' + x(mids[nb - 1]) + ',' + y(0) + 'Z', 'class': 'f-' + s[0], opacity: .12 }, g);
      var ln = S('path', { d: 'M' + pts.join('L'), fill: 'none', 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', 'class': 's-' + s[0] + (first ? ' draw' : '') }, g);
      ln.style.setProperty('--len', 2000);
      var pk = 0, best = -1; s[1].forEach(function (vv, ii) { if ((s[0] === 'fraud' || mids[ii] > Math.log1p(4)) && vv > best) { best = vv; pk = ii; } });
      T_(g, x(mids[pk]) + (s[0] === 'fraud' ? 8 : 0), y(s[1][pk]) - 8, s[0] === 'fraud' ? T.js_fraud : T.js_legit, 'lbl', s[0] === 'fraud' ? 'start' : 'middle');
    });
    var hl = S('line', { 'class': 'hover-line', y1: m.t, y2: H - m.b, opacity: 0 }, g);
    var hit = S('rect', { x: m.l, y: m.t, width: w - m.l - m.r, height: H - m.t - m.b, 'class': 'hit' }, svg);
    bindHover(hit, function (ev) {
      var px = localX(ev, svg), v = x.inv(px), i = Math.max(0, Math.min(nb - 1, Math.floor((v - e[0]) / (e[1] - e[0]))));
      hl.setAttribute('x1', x(mids[i])); hl.setAttribute('x2', x(mids[i])); hl.setAttribute('opacity', 1);
      var lo = Math.expm1(e[i]), hi = Math.expm1(e[i + 1]);
      showTip('<b>' + eur(lo, lo < 10 ? 1 : 0) + ' – ' + eur(hi, hi < 10 ? 1 : 0) + '</b>' +
        '<div class="row"><span class="sw bg-legit"></span>' + T.js_legit + ': ' + pct(A.legit[i], 1) + '</div>' +
        '<div class="row"><span class="sw bg-fraud"></span>' + T.js_fraud + ': ' + pct(A.fraud[i], 1) + '</div>', ev);
    });
    hit._leave = function () { hl.setAttribute('opacity', 0); };
  });
  addTable('ch-amount', [T.js_tbl_bin, T.js_tbl_legit, T.js_tbl_fraudshare], mids.map(function (mm, i) {
    return [eur(Math.expm1(e[i]), 1) + ' – ' + eur(Math.expm1(e[i + 1]), 1), pct(A.legit[i], 1), pct(A.fraud[i], 1)];
  }));
})();

/* ---------- 3. hourly ---------- */
(function () {
  var H24 = D.eda.hourly, tot = H24.reduce(function (a, r) { return a + r.n; }, 0);
  chart('ch-hourly', function (root, w) {
    var m = { l: 46, r: 8, t: 22, b: 28 }, hA = 92, hB = 118, gap = 46, H = m.t + hA + gap + hB + m.b;
    var svg = frame(root, w, H, T.eda2_chart_a + ' / ' + T.eda2_chart_b), g = S('g', {}, svg);
    var band = (w - m.l - m.r) / 24, bw = Math.min(20, band * 0.72);
    var shareMax = Math.max.apply(null, H24.map(function (r) { return r.n / tot; })) * 1.1;
    var rateMax = Math.max.apply(null, H24.map(function (r) { return r.rate_per_10k; })) * 1.15;
    var yA = lin(0, shareMax, m.t + hA, m.t), yB = lin(0, rateMax, m.t + hA + gap + hB, m.t + hA + gap);
    T_(g, m.l - 40, 12, T.eda2_chart_a, 'ttl'); T_(g, m.l - 40, m.t + hA + gap - 16, T.eda2_chart_b, 'ttl');
    yGrid(g, yA, niceTicks(shareMax, 2), m.l, w - m.r, function (v) { return pct(v, 0); });
    yGrid(g, yB, niceTicks(rateMax, 3), m.l, w - m.r, function (v) { return fix(v); });
    var order = H24.map(function (r) { return r.rate_per_10k; }).slice().sort(function (a, b) { return b - a; });
    H24.forEach(function (r, i) {
      var cx = m.l + band * (i + .5), a = yA(r.n / tot), b = yB(r.rate_per_10k);
      S('path', { d: rbar(cx - bw / 2, a, bw, m.t + hA - a, 4, 'up'), 'class': 'f-legit' }, g);
      var top2 = r.rate_per_10k >= order[1];
      S('path', { d: rbar(cx - bw / 2, b, bw, m.t + hA + gap + hB - b, 4, 'up'), 'class': 'f-fraud', opacity: top2 ? 1 : .6 }, g);
      if (top2) T_(g, cx, b - 5, fix(r.rate_per_10k), 'val', 'middle');
      if (i % 3 === 0) T_(g, cx, H - 8, r.hour + 'h', '', 'middle');
    });
    var hl = S('rect', { y: m.t - 4, height: H - m.t - m.b + 4, width: band, fill: 'var(--ink)', opacity: 0, 'pointer-events': 'none' }, g);
    var hit = S('rect', { x: m.l, y: 0, width: w - m.l - m.r, height: H, 'class': 'hit' }, svg);
    bindHover(hit, function (ev) {
      var i = Math.max(0, Math.min(23, Math.floor((localX(ev, svg) - m.l) / band))), r = H24[i];
      hl.setAttribute('x', m.l + band * i); hl.setAttribute('opacity', .06);
      showTip('<b>' + r.hour + 'h</b><div>' + T.js_tbl_tx + ': ' + fix(r.n) + ' (' + pct(r.n / tot, 1) + ')</div><div>' + T.js_tbl_fraud + ': ' + fix(r.fraud) + '</div><div>' + fix(r.rate_per_10k, 1) + ' ' + T.js_rate + '</div>', ev);
    });
    hit._leave = function () { hl.setAttribute('opacity', 0); };
  });
  addTable('ch-hourly', [T.js_tbl_hour, T.js_tbl_tx, T.js_tbl_fraud, T.js_tbl_rate], H24.map(function (r) { return [r.hour, fix(r.n), fix(r.fraud), fix(r.rate_per_10k, 1)]; }));
})();

/* ---------- 4. correlations ---------- */
(function () {
  var C = D.eda.corr;
  chart('ch-corr', function (root, w) {
    var rowH = 26, m = { t: 8, r: 16, b: 34, l: 54 }, H = m.t + C.length * rowH + m.b;
    var svg = frame(root, w, H, T.eda3_chart), g = S('g', {}, svg);
    var rs = C.map(function (c) { return c.r; }), lo = Math.min(0, Math.min.apply(null, rs)) * 1.2, hi = Math.max(0, Math.max.apply(null, rs)) * 1.25;
    var x = lin(lo, hi, m.l + 30, w - m.r - 30), x0 = x(0);
    niceTicks(Math.max(-lo, hi), 3).forEach(function (v) { [v, -v].forEach(function (t, k) { if (k && !v) return; if (t < lo || t > hi) return;
      var gg = S('g', { 'class': 'grid' }, g); S('line', { x1: x(t), x2: x(t), y1: m.t, y2: H - m.b }, gg); T_(g, x(t), H - m.b + 16, fix(t, 1), '', 'middle'); }); });
    S('line', { x1: x0, x2: x0, y1: m.t, y2: H - m.b, stroke: 'var(--axis)' }, g);
    C.forEach(function (c, i) {
      var y = m.t + i * rowH + (rowH - 14) / 2, pos = c.r > 0, bw = Math.abs(x(c.r) - x0);
      S('path', { d: rbar(pos ? x0 : x(c.r), y, bw, 14, 4, pos ? 'right' : 'left'), 'class': pos ? 'f-pos' : 'f-neg' }, g);
      T_(g, m.l - 10, y + 11, fname(c.feature), 'lbl', 'end');
      T_(g, pos ? x(c.r) + 6 : x(c.r) - 6, y + 11, fix(c.r, 2), 'val', pos ? 'start' : 'end');
    });
  });
  var lg = $('#ch-corr .plot'); /* polarity key */
  var key = el('div', 'legend', '<span><i class="sq" style="background:var(--neg)"></i>' + T.js_neg_corr + '</span><span><i class="sq" style="background:var(--pos)"></i>' + T.js_pos_corr + '</span>');
  lg.parentNode.insertBefore(key, lg);
  addTable('ch-corr', [T.js_tbl_feature, T.js_corr], C.map(function (c) { return [c.feature, fix(c.r, 3)]; }));
})();

/* ---------- 5. class separation (small multiples) ---------- */
(function () {
  var Ds = D.eda.dists;
  chart('ch-dists', function (root, w) {
    var cols = w > 560 ? 2 : 1, gap = 18, pw = (w - gap * (cols - 1)) / cols, ph = 128, rows = Math.ceil(Ds.length / cols);
    var H = rows * (ph + 40), svg = frame(root, w, H, T.eda4_chart);
    Ds.forEach(function (d, k) {
      var ox = (k % cols) * (pw + gap), oy = Math.floor(k / cols) * (ph + 40) + 18, nb = d.legit.length, e = d.edges;
      var g = S('g', { transform: 'translate(' + ox + ',' + oy + ')' }, svg);
      var x = lin(e[0], e[nb], 4, pw - 4), ymax = Math.max.apply(null, d.legit.concat(d.fraud)) * 1.1, y = lin(0, ymax, ph, 4);
      T_(g, 0, -6, d.feature, 'ttl');
      S('line', { x1: 0, x2: pw, y1: ph, y2: ph, stroke: 'var(--axis)' }, g);
      var mids = []; for (var i = 0; i < nb; i++) mids.push((e[i] + e[i + 1]) / 2);
      [['legit', d.legit], ['fraud', d.fraud]].forEach(function (s) {
        var pts = mids.map(function (mm, i) { return x(mm) + ',' + y(s[1][i]); });
        S('path', { d: 'M' + x(mids[0]) + ',' + y(0) + 'L' + pts.join('L') + 'L' + x(mids[nb - 1]) + ',' + y(0) + 'Z', 'class': 'f-' + s[0], opacity: .12 }, g);
        S('path', { d: 'M' + pts.join('L'), fill: 'none', 'stroke-width': 2, 'stroke-linejoin': 'round', 'class': 's-' + s[0] }, g);
      });
      [e[0], (e[0] + e[nb]) / 2, e[nb]].forEach(function (v, j) { T_(g, x(v), ph + 16, fix(v, 1), '', j === 0 ? 'start' : j === 2 ? 'end' : 'middle'); });
      var hl = S('line', { 'class': 'hover-line', y1: 0, y2: ph, opacity: 0 }, g);
      var hit = S('rect', { x: 0, y: 0, width: pw, height: ph, 'class': 'hit' }, g);
      bindHover(hit, function (ev) {
        var px = localX(ev, svg) - ox, i = Math.max(0, Math.min(nb - 1, Math.floor((x.inv(px) - e[0]) / (e[1] - e[0]))));
        hl.setAttribute('x1', x(mids[i])); hl.setAttribute('x2', x(mids[i])); hl.setAttribute('opacity', 1);
        showTip('<b>' + d.feature + ' ' + fix(e[i], 2) + ' → ' + fix(e[i + 1], 2) + '</b><div class="row"><span class="sw bg-legit"></span>' + T.js_legit + ': ' + pct(d.legit[i], 1) +
          '</div><div class="row"><span class="sw bg-fraud"></span>' + T.js_fraud + ': ' + pct(d.fraud[i], 1) + '</div>', ev);
      });
      hit._leave = function () { hl.setAttribute('opacity', 0); };
    });
  });
})();

/* ---------- 6. precision-recall curves ---------- */
(function () {
  var keys = ['logreg', 'rf', 'xgb'], FIN = D.final.key;
  legend('[data-legend=models]', keys.map(function (k) { return { c: MODEL_CLASS[k], t: T.js_models[k] + (k === FIN ? ' ★' : '') }; })
    .concat([{ c: 'base', t: T.js_baseline + ' (' + pct(D.prevalence_test, 2) + ')' }]));
  var curves = {};
  keys.forEach(function (k) { /* ascending recall + suffix-max precision (standard interpolated PR) */
    var r = D.pr_curves[k].recall.slice().reverse(), p = D.pr_curves[k].precision.slice().reverse(), sm = p.slice();
    for (var i = sm.length - 2; i >= 0; i--) sm[i] = Math.max(sm[i], sm[i + 1]);
    curves[k] = { r: r, p: p, sm: sm };
  });
  function precAt(k, rr) { var c = curves[k]; for (var i = 0; i < c.r.length; i++) if (c.r[i] >= rr - 1e-9) return c.sm[i]; return 0; }
  chart('ch-pr', function (root, w, first) {
    var H = Math.round(Math.min(430, Math.max(280, w * 0.78))), m = { t: 30, r: 14, b: 44, l: 50 };
    var svg = frame(root, w, H, T.pr_h), g = S('g', {}, svg), x = lin(0, 1, m.l, w - m.r), y = lin(0, 1.02, H - m.b, m.t);
    yGrid(g, y, [0, .25, .5, .75, 1], m.l, w - m.r, function (v) { return pct(v, 0); });
    S('line', { x1: m.l, x2: w - m.r, y1: H - m.b, y2: H - m.b, stroke: 'var(--axis)' }, g);
    [0, .25, .5, .75, 1].forEach(function (v) { T_(g, x(v), H - m.b + 16, pct(v, 0), '', 'middle'); });
    T_(g, (m.l + w - m.r) / 2, H - 6, T.js_recall, 'ttl', 'middle');
    T_(g, 4, 12, T.js_precision, 'ttl');
    S('line', { x1: x(0), x2: x(1), y1: y(D.prevalence_test), y2: y(D.prevalence_test), stroke: 'var(--muted)', 'stroke-width': 1.5, 'stroke-dasharray': '5 4' }, g);
    keys.forEach(function (k) {
      var c = curves[k], d = 'M' + c.r.map(function (r, i) { return x(r) + ',' + y(c.p[i]); }).join('L');
      var ln = S('path', { d: d, fill: 'none', 'stroke-width': k === FIN ? 3 : 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', 'class': 's-' + MODEL_CLASS[k] + (first ? ' draw' : '') }, g);
      ln.style.setProperty('--len', 4000);
    });
    var dots = keys.map(function (k) { return S('circle', { r: 5, 'class': 'f-' + MODEL_CLASS[k], stroke: 'var(--surface)', 'stroke-width': 2, opacity: 0 }, g); });
    var hl = S('line', { 'class': 'hover-line', y1: m.t, y2: H - m.b, opacity: 0 }, g);
    var hit = S('rect', { x: m.l, y: m.t, width: w - m.l - m.r, height: H - m.t - m.b, 'class': 'hit' }, svg);
    bindHover(hit, function (ev) {
      var rr = Math.max(0, Math.min(1, x.inv(localX(ev, svg))));
      hl.setAttribute('x1', x(rr)); hl.setAttribute('x2', x(rr)); hl.setAttribute('opacity', 1);
      var rows = '';
      keys.forEach(function (k, i) { var pp = precAt(k, rr); dots[i].setAttribute('cx', x(rr)); dots[i].setAttribute('cy', y(pp)); dots[i].setAttribute('opacity', 1);
        rows += '<div class="row"><span class="sw bg-' + MODEL_CLASS[k] + '"></span>' + T.js_models[k] + ': ' + pct(pp, 1) + '</div>'; });
      showTip('<b>' + T.js_tbl_recall + ' ' + pct(rr, 0) + '</b>' + rows, ev);
    });
    hit._leave = function () { hl.setAttribute('opacity', 0); dots.forEach(function (d) { d.setAttribute('opacity', 0); }); };
  });
})();

/* ---------- 7. threshold explorer ---------- */
(function () {
  var SW = D.sweep, G = SW.grid, n = G.length, nTest = SW.n_test, fraudTest = SW.fraud_test, noModel = SW.fraud_amount_test;
  var thr = D.final.thresholds, st = { c: P.fa_cost };
  var COLORS = { default: 'base', f1: 'orange', cost: 'aqua' };
  function idx(t) { var b = 0; for (var i = 0; i < n; i++) if (Math.abs(G[i] - t) < 1e-9) return i; return b; }
  function costBest(c) { /* same rule as the notebook: lowest OOF cost, middle of the plateau */
    var best = Infinity, v = [], i;
    for (i = 0; i < n; i++) { v.push(SW.oof.missed[i] + c * SW.oof.fp[i]); if (v[i] < best) best = v[i]; }
    var ok = []; for (i = 0; i < n; i++) if (Math.abs(v[i] - best) <= 1e-9 * Math.max(1, Math.abs(best))) ok.push(i);
    return ok[Math.floor(ok.length / 2)];
  }
  function op(i, c) {
    var tp = SW.test.tp[i], fp = SW.test.fp[i], fn = SW.test.fn[i], miss = SW.test.missed[i];
    return { i: i, t: G[i], tp: tp, fp: fp, fn: fn, tn: nTest - fraudTest - fp, missed: miss, alerts: (tp + fp) / nTest * 1e5, total: miss + c * fp };
  }
  function ops() { return { default: op(idx(thr.default), st.c), f1: op(idx(thr.f1), st.c), cost: op(costBest(st.c), st.c) }; }

  var slider = $('#fa-slider'), out = $('#fa-out'), chips = $('#fa-chips');
  [1, 5, 25, 100].forEach(function (v) {
    var b = el('button', 'chip', eur(v), chips); b.type = 'button'; b.setAttribute('aria-pressed', v === st.c);
    b.addEventListener('click', function () { slider.value = v; update(); });
  });
  function update() {
    st.c = +slider.value; out.textContent = eur(st.c);
    $$('.chip', chips).forEach(function (b, i) { b.setAttribute('aria-pressed', [1, 5, 25, 100][i] === st.c); });
    var o = ops().cost;
    $('#thr-live').innerHTML = T.thr_live.replace('{c}', eur(st.c)).replace('{t}', ft(o.t)).replace('{tp}', o.tp).replace('{fp}', o.fp).replace('{fa_word}', o.fp === 1 ? T.js_fa_one : T.js_fa_many)
      .replace('{cost}', eur(o.total)).replace('{nomodel}', eur(noModel));
    renderOps(); redraw('ch-cost');
  }
  function renderOps() {
    var O = ops(), box = $('#ops'), best = 'default';
    var same = O.f1.tp === O.default.tp && O.f1.fp === O.default.fp && O.cost.tp === O.default.tp && O.cost.fp === O.default.fp;
    $('#ops-note').textContent = same ? T.thr_same : '';
    ['f1', 'cost'].forEach(function (k) { if (O[k].total < O[best].total - 1e-9) best = k; });
    if (same) best = null;
    box.innerHTML = ['default', 'f1', 'cost'].map(function (k) {
      var o = O[k];
      return '<div class="op' + (k === best ? ' best' : '') + '"><h4><span class="dot bg-' + COLORS[k] + '"></span>' + T['op_' + k] +
        (k === best ? '<span class="badge">' + T.op_best + '</span>' : '') + '</h4><div class="t">' + ft(o.t) + '</div>' +
        '<div class="cm"><div class="h"></div><div class="h">' + T.cm_legit + '</div><div class="h">' + T.cm_fraud + '</div>' +
        '<div class="h">' + T.cm_legit + '</div><div class="c">' + fix(o.tn) + '</div><div class="c bad">' + fix(o.fp) + '</div>' +
        '<div class="h">' + T.cm_fraud + '</div><div class="c bad">' + fix(o.fn) + '</div><div class="c tp">' + fix(o.tp) + '</div></div>' +
        '<dl><dt>' + T.op_caught + '</dt><dd>' + o.tp + ' / ' + fraudTest + ' (' + pct(o.tp / fraudTest, 0) + ')</dd>' +
        '<dt>' + T.op_fp + '</dt><dd>' + fix(o.fp) + '</dd><dt>' + T.op_alerts + '</dt><dd>' + fix(o.alerts) + '</dd>' +
        '<dt>' + T.op_missed + '</dt><dd>' + eur(o.missed) + '</dd><dt>' + T.op_total + '</dt><dd>' + eur(o.total) + '</dd></dl></div>';
    }).join('');
  }
  chart('ch-cost', function (root, w, first) {
    var O = ops(), H = Math.round(Math.min(380, Math.max(260, w * 0.62))), m = { t: 52, r: 16, b: 42, l: 56 };
    var svg = frame(root, w, H, T.thr_chart_h), g = S('g', {}, svg);
    var ymax = noModel * 1.3, x = lin(0, 1, m.l, w - m.r), y = lin(0, ymax, H - m.b, m.t);
    var cost = function (i) { return SW.test.missed[i] + st.c * SW.test.fp[i]; };
    yGrid(g, y, niceTicks(ymax, 4), m.l, w - m.r, function (v) { return amt(v); });
    S('line', { x1: m.l, x2: w - m.r, y1: H - m.b, y2: H - m.b, stroke: 'var(--axis)' }, g);
    [0, .25, .5, .75, 1].forEach(function (v) { T_(g, x(v), H - m.b + 16, fix(v, 2), '', 'middle'); });
    T_(g, (m.l + w - m.r) / 2, H - 6, T.js_threshold, 'ttl', 'middle');
    var cp = S('clipPath', { id: 'costclip' }, g); S('rect', { x: m.l, y: m.t - 4, width: w - m.l - m.r, height: H - m.b - m.t + 4 }, cp);
    S('line', { x1: m.l, x2: w - m.r, y1: y(noModel), y2: y(noModel), stroke: 'var(--muted)', 'stroke-width': 1.5, 'stroke-dasharray': '5 4' }, g);
    T_(g, w - m.r - 4, y(noModel) - 6, T.js_no_model + ' · ' + eur(noModel), 'lbl', 'end');
    var d = 'M' + G.map(function (t, i) { return x(t) + ',' + y(cost(i)); }).join('L');
    var ln = S('path', { d: d, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2, 'stroke-linejoin': 'round', 'clip-path': 'url(#costclip)', 'class': first ? 'draw' : '' }, g);
    ln.style.setProperty('--len', 3000);
    /* markers, staggered labels so close thresholds do not collide */
    var mk = ['default', 'f1', 'cost'].map(function (k) { return { k: k, o: O[k] }; }).sort(function (a, b) { return a.o.t - b.o.t; });
    mk.forEach(function (q, j) {
      var cx = x(q.o.t), cy = Math.min(y(cost(q.o.i)), H - m.b), row = j % 3, ly = 14 + row * 14;
      S('line', { x1: cx, x2: cx, y1: ly + 4, y2: H - m.b, stroke: 'var(--' + (q.k === 'default' ? 'muted' : q.k === 'f1' ? 'orange' : 'aqua') + ')', 'stroke-width': 1.5, 'stroke-dasharray': q.k === 'default' ? '3 3' : '0' }, g);
      S('circle', { cx: cx, cy: cy, r: 5.5, fill: 'var(--' + (q.k === 'default' ? 'muted' : q.k === 'f1' ? 'orange' : 'aqua') + ')', stroke: 'var(--surface)', 'stroke-width': 2 }, g);
      var lab = q.k === 'default' ? T.op_default : q.k === 'f1' ? T.js_f1_marker : T.js_cost_marker;
      T_(g, cx, ly, lab + ' ' + ft(q.o.t), 'lbl', cx > w - 90 ? 'end' : 'middle');
    });
    var hl = S('line', { 'class': 'hover-line', y1: m.t, y2: H - m.b, opacity: 0 }, g);
    var hit = S('rect', { x: m.l, y: m.t, width: w - m.l - m.r, height: H - m.t - m.b, 'class': 'hit' }, svg);
    bindHover(hit, function (ev) {
      var t = x.inv(localX(ev, svg)), i = 0, best = 9; G.forEach(function (gv, j) { if (Math.abs(gv - t) < best) { best = Math.abs(gv - t); i = j; } });
      hl.setAttribute('x1', x(G[i])); hl.setAttribute('x2', x(G[i])); hl.setAttribute('opacity', 1);
      var o = op(i, st.c);
      showTip('<b>' + T.js_threshold + ' ' + ft(G[i]) + '</b><div>' + o.tp + ' / ' + fraudTest + ' ' + T.js_caught + '</div><div>' + fix(o.fp) + ' ' + T.js_fa + '</div><div>' + fix(o.alerts) + ' ' + T.js_alerts + ' / 100k</div><div><b>' + T.js_cost + ' ' + eur(o.total) + '</b></div>', ev);
    });
    hit._leave = function () { hl.setAttribute('opacity', 0); };
  });
  addTable('ch-cost', [T.js_tbl_t, T.js_tbl_tp, T.js_tbl_fp, T.js_tbl_cost], G.map(function (t, i) {
    return [fix(t, 3), SW.test.tp[i] + ' / ' + fraudTest, fix(SW.test.fp[i]), eur(SW.test.missed[i] + P.fa_cost * SW.test.fp[i])];
  }));
  slider.addEventListener('input', update); update();
})();

/* ---------- 8. importance bars ---------- */
(function () {
  var col = MODEL_CLASS[D.final.key] || 'aqua';
  function hbars(id, items) {
    chart(id, function (root, w) {
      var rowH = 26, m = { t: 6, r: 48, b: 6, l: 82 }, H = m.t + items.length * rowH + m.b, svg = frame(root, w, H, ''), g = S('g', {}, svg);
      var mx = Math.max.apply(null, items.map(function (i) { return i.value; })) * 1.02, x = lin(0, mx, m.l, w - m.r);
      S('line', { x1: m.l, x2: m.l, y1: m.t, y2: H - m.b, stroke: 'var(--axis)' }, g);
      items.forEach(function (it, i) {
        var y = m.t + i * rowH + 5, bw = Math.max(2, x(it.value) - m.l);
        S('path', { d: rbar(m.l, y, bw, 15, 4, 'right'), 'class': 'f-' + col }, g);
        T_(g, m.l - 10, y + 12, fname(it.feature), 'lbl', 'end');
        T_(g, m.l + bw + 6, y + 12, fix(it.value, id === 'ch-imp-shap' ? 2 : 3), 'val');
      });
    });
  }
  hbars('ch-imp-native', D.importance.native.slice(0, 10));
  hbars('ch-imp-shap', D.importance.shap.slice(0, 10));
})();

/* ---------- 9. SHAP beeswarm ---------- */
(function () {
  var B = D.beeswarm, F = B.features, nF = F.length, np = B.shap[0].length;
  var all = [].concat.apply([], B.shap), lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), padv = (hi - lo) * 0.04;
  chart('ch-bee', function (root, w) {
    var rowH = 40, m = { t: 6, r: 14, b: 44, l: 70 }, H = m.t + nF * rowH + m.b, svg = frame(root, w, H, T.bee_h), g = S('g', {}, svg);
    var x = lin(lo - padv, hi + padv, m.l, w - m.r), r = 2.6;
    niceTicks(Math.max(Math.abs(lo), Math.abs(hi)), 4).forEach(function (v) { [v, -v].forEach(function (t, k) { if (k && !v) return; if (t < lo - padv || t > hi + padv) return;
      var gg = S('g', { 'class': 'grid' }, g); S('line', { x1: x(t), x2: x(t), y1: m.t, y2: H - m.b }, gg); T_(g, x(t), H - m.b + 16, fix(t, 0), '', 'middle'); }); });
    S('line', { x1: x(0), x2: x(0), y1: m.t, y2: H - m.b, stroke: 'var(--axis)', 'stroke-width': 1.5 }, g);
    T_(g, (m.l + w - m.r) / 2, H - 6, T.bee_x, 'ttl', 'middle');
    F.forEach(function (f, row) {
      var cy = m.t + row * rowH + rowH / 2; T_(g, m.l - 10, cy + 4, fname(f), 'lbl', 'end');
      var bins = {}, bwid = 7, amp = rowH * 0.44, i, kx;
      for (i = 0; i < np; i++) { kx = Math.round(x(B.shap[row][i]) / bwid); bins[kx] = (bins[kx] || 0) + 1; }
      var mxc = 0; for (kx in bins) mxc = Math.max(mxc, bins[kx]);
      for (i = 0; i < np; i++) {
        var px = x(B.shap[row][i]), dens = (bins[Math.round(px / bwid)] / mxc), jit = (((i * 2654435761 + row * 40503) >>> 0) % 1000) / 500 - 1;
        var v = B.value[row][i], cls = 'v' + Math.min(4, Math.floor(v * 5));
        var c = S('circle', { cx: px, cy: cy + jit * amp * Math.sqrt(dens), r: r, 'class': 'bee-pt ' + cls }, g);
        c._i = [row, i];
      }
    });
    var hit = g;
    hit.addEventListener('pointermove', function (ev) {
      var t = ev.target; if (!t._i) { hideTip(); return; } var row = t._i[0], i = t._i[1], s = B.shap[row][i];
      showTip('<b>' + fname(F[row]) + '</b><div>' + T.js_shap_axis + ': ' + (s > 0 ? '+' : '') + fix(s, 2) + ' (' + (s > 0 ? T.js_pushes_fraud : T.js_pushes_legit) + ')</div><div>' + T.bee_value + ': ' + fix(B.value[row][i], 2) + ' [0–1]</div><div>' + T.js_true_class + ': ' + (B.is_fraud[i] ? T.js_fraud : T.js_legit) + '</div>', ev);
    });
    hit.addEventListener('pointerleave', hideTip);
  });
})();

/* ---------- 10. individual explanations ---------- */
(function () {
  var host = $('#cases'); if (!host) return;
  var mx = 0; D.cases.forEach(function (c) { c.contributions.forEach(function (k) { mx = Math.max(mx, Math.abs(k.shap)); }); });
  D.cases.forEach(function (c, ci) {
    var f = el('figure', 'card chart case', '', host); f.id = 'case-' + ci;
    el('h4', '', T.js_cases[c.kind] || c.kind, f);
    el('div', 'meta', T.case_score + ' ' + pct(c.probability, 1) + ' · ' + T.case_amount + ' ' + eur(c.amount, 2) + ' · ' + T.case_hour + ' ' + c.hour + 'h', f);
    el('div', 'plot', '', f);
    chart('case-' + ci, function (root, w) {
      var rowH = 38, m = { t: 4, r: 8, b: 22, l: 8 }, H = m.t + c.contributions.length * rowH + m.b, svg = frame(root, w, H, T.js_cases[c.kind]), g = S('g', {}, svg);
      var x = lin(-mx * 1.3, mx * 1.3, m.l, w - m.r), x0 = x(0);
      S('line', { x1: x0, x2: x0, y1: m.t, y2: H - m.b, stroke: 'var(--axis)' }, g);
      c.contributions.forEach(function (k, i) {
        var y = m.t + i * rowH, pos = k.shap > 0, bw = Math.max(2, Math.abs(x(k.shap) - x0)), val = k.feature === 'log_amount' ? eur(Math.expm1(k.value), 2) : k.feature === 'hour' ? k.value + 'h' : fix(k.value, 2);
        T_(g, m.l, y + 12, fname(k.feature) + ' = ' + val, 'lbl');
        S('path', { d: rbar(pos ? x0 : x(k.shap), y + 18, bw, 12, 4, pos ? 'right' : 'left'), 'class': pos ? 'f-pos' : 'f-neg' }, g);
        T_(g, pos ? x(k.shap) + 6 : x(k.shap) - 6, y + 28, (pos ? '+' : '') + fix(k.shap, 1), 'val', pos ? 'start' : 'end');
      });
      T_(g, x0, H - 4, '0', '', 'middle');
    });
  });
})();

/* ---------- chrome: theme, copy, reveal ---------- */
(function () {
  var root = document.documentElement;
  $('#theme-btn').addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', next);
    try { localStorage.setItem('ccf-theme', next); } catch (e) {}
  });
  var cb = $('#copy-btn');
  cb.addEventListener('click', function () {
    var txt = $('#code-block').innerText;
    var done = function () { cb.textContent = cb.dataset.done; setTimeout(function () { cb.textContent = cb.dataset.copy; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function () {}); else done();
  });
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    $$('.sec > h2, .sec > .lead2, .card, .story-t, .flow li, .kpi, .nexts > div').forEach(function (n) { n.classList.add('reveal'); io.observe(n); });
  }
})();
})();
