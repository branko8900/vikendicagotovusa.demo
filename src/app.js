
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const html = document.documentElement;
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const canHover = () => !matchMedia("(max-width: 768px)").matches;
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
window.scrollTo(0, 0);
const D = JSON.parse($("#page-data").textContent);

/* ---------------- Lenis ---------------- */
let lenis = null;
try { const m = await import("lenis"); lenis = new m.default({ smoothWheel: true }); }
catch (e) { console.warn("Lenis nije učitan, koristim nativni scroll.", e); }

/* ---------------- tiny spring engine (react-spring tension/friction model) ---------------- */
const running = new Set();
class Spring {
  constructor(v) { this.x = v; this.v = 0; this.t = v; this.k = 170; this.c = 26; }
  set(t, [k, c]) { this.t = t; this.k = k; this.c = c; }
  jump(v) { this.x = this.t = v; this.v = 0; }
  step(dt) {
    const n = Math.max(1, Math.ceil(dt / 0.004)), h = dt / n;
    for (let i = 0; i < n; i++) { const a = -this.k * (this.x - this.t) - this.c * this.v; this.v += a * h; this.x += this.v * h; }
    if (Math.abs(this.v) < 0.002 && Math.abs(this.x - this.t) < 0.0005) { this.x = this.t; this.v = 0; return true; }
    return false;
  }
}
const DEF = { opacity: 1, x: 0, y: 0, scale: 1, rotate: 0 };
class Anim {
  constructor(el, init = {}) { this.el = el; this.s = {}; for (const k in init) this.s[k] = new Spring(init[k]); this.apply(); }
  to(vals, cfg = [170, 26], delay = 0) {
    clearTimeout(this.tm);
    const go = () => {
      for (const k in vals) { (this.s[k] ||= new Spring(DEF[k])).set(vals[k], cfg); if (reduced) this.s[k].jump(vals[k]); }
      if (reduced) this.apply(); else running.add(this);
    };
    if (delay && !reduced) this.tm = setTimeout(go, delay); else go();
    return this;
  }
  jump(vals) { clearTimeout(this.tm); for (const k in vals) (this.s[k] ||= new Spring(DEF[k])).jump(vals[k]); running.delete(this); this.apply(); return this; }
  step(dt) { let done = true; for (const k in this.s) if (!this.s[k].step(dt)) done = false; this.apply(); return done; }
  apply() {
    const s = this.s, g = k => (s[k] ? s[k].x : DEF[k]);
    let t = "";
    if (s.x || s.y) t += `translate3d(${g("x")}px,${g("y")}px,0)`;
    if (s.scale) t += ` scale(${g("scale")})`;
    if (s.rotate) t += ` rotate(${g("rotate")}deg)`;
    if (t) this.el.style.transform = t;
    if (s.opacity) this.el.style.opacity = g("opacity");
  }
}
const parse = str => { const o = {}; (str || "").split(",").filter(Boolean).forEach(p => { const [k, v] = p.split(":"); o[k.trim()] = parseFloat(v); }); return o; };
const cfgOf = (str, d) => (str || d).split(",").map(Number);

/* ---------------- scroll-progress parallax ---------------- */
const PX = [];
const addPx = (el, sec, axis, from, to) => PX.push({ el, sec, axis, from, to, last: null });
function parallax() {
  const vh = innerHeight;
  for (const p of PX) {
    const r = p.sec.getBoundingClientRect();
    if ((r.bottom < -100 || r.top > vh + 100) && p.last !== null) continue;
    const pr = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
    const v = (p.from + (p.to - p.from) * pr).toFixed(3);
    if (v === p.last) continue;
    p.last = v;
    p.el.style.transform = p.axis === "y" ? `translate3d(0,${v}%,0)` : `translate3d(${v}%,0,0)`;
  }
}
if (!reduced) {
  addPx($("#hero-plate"), $(".hero"), "y", 0, 12);
  $$("#trust-title .gw").forEach(g => { const [a, b] = g.dataset.px.split(",").map(Number); addPx(g, $("#trust"), "x", a, b); });
}

/* ---------------- master rAF loop ---------------- */
let last = performance.now();
function frame(t) {
  const dt = Math.min((t - last) / 1000, 0.05); last = t;
  if (lenis) lenis.raf(t);
  for (const a of running) if (a.step(dt)) running.delete(a);
  parallax();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

/* ---------------- scroll lock ---------------- */
let ready = false, modalOpen = false, menuOpen = false;
const readyQ = [];
const onReady = f => (ready ? f() : readyQ.push(f));
function lock() { lenis && lenis.stop(); html.style.position = "relative"; html.style.overflow = "hidden"; html.style.height = "100%"; }
function unlock() {
  if (modalOpen || menuOpen || !ready) return;
  lenis && lenis.start();
  ["position", "overflow", "height"].forEach(p => html.style.removeProperty(p));
}

/* ---------------- text reveal builders ---------------- */
function buildLines(el) {
  const ls = el.dataset.lines.split("|"), st = +(el.dataset.stagger ?? 120), b = +(el.dataset.base ?? 0), d = +(el.dataset.dur ?? 950);
  el.innerHTML = ls.map((l, i) => `<span class="clip line"><span style="--d:${d}ms;--dl:${b + i * st}ms">${l}</span></span>`).join("");
}
function buildWords(el) {
  const st = +(el.dataset.stagger ?? 140), d = +(el.dataset.dur ?? 1100);
  el.innerHTML = el.dataset.words.split(" ").map((w, i) => `<span class="clip"><span style="--d:${d}ms;--dl:${i * st}ms">${w}</span></span>`).join(" ");
}
$$("[data-lines]").forEach(buildLines);
$$("[data-words]").forEach(buildWords);
const fb = $("#f-body");
fb.innerHTML = fb.textContent.trim().split(/\s+/).map((w, i) => `<span class="w" style="transition-delay:${250 + i * 28}ms">${w}</span>`).join(" ");

function play(el) { el.classList.add("no-tr"); el.classList.remove("is-in"); void el.offsetWidth; el.classList.remove("no-tr"); el.classList.add("is-in"); }

const revIO = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { revIO.unobserve(e.target); e.target.classList.add("is-in"); } }), { threshold: 0.2 });
$$(".reveal").forEach(el => (el.dataset.gate === "ready" ? onReady(() => el.classList.add("is-in")) : revIO.observe(el)));

/* ---------------- Inview springs ---------------- */
const ivIO = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { ivIO.unobserve(e.target); e.target._iv(); } }), { threshold: 0.12 });
$$("[data-iv]").forEach(el => {
  const from = parse(el.dataset.iv), to = {};
  for (const k in from) to[k] = DEF[k];
  const a = new Anim(el, from), cfg = cfgOf(el.dataset.cfg, "200,26"), d = +(el.dataset.delay || 0);
  el._iv = () => a.to(to, cfg, d);
  if (el.dataset.gate === "ready") onReady(el._iv); else ivIO.observe(el);
});

/* ---------------- Hover springs (off ≤768px) ---------------- */
$$("[data-hv]").forEach(el => {
  const to = parse(el.dataset.hv), from = {};
  for (const k in to) from[k] = DEF[k];
  Object.assign(from, parse(el.dataset.hvFrom));
  const a = new Anim(el, from), cfg = cfgOf(el.dataset.hvCfg, "300,22");
  const root = el.closest("[data-hv-root]") || el;
  root.addEventListener("pointerenter", e => { if (e.pointerType === "touch" || !canHover()) return; a.to(to, cfg); });
  root.addEventListener("pointerleave", () => a.to(from, cfg));
});

/* ---------------- carousel dots ---------------- */
function makeDots(box, n, onPick) {
  box.innerHTML = Array.from({ length: n }, (_, i) => `<button type="button" class="dot" aria-label="${D.slide} ${i + 1}"><span></span></button>`).join("");
  const bs = [...box.children];
  bs.forEach((b, i) => b.addEventListener("click", () => onPick(i)));
  return i => bs.forEach((b, j) => b.setAttribute("aria-current", j === i ? "true" : "false"));
}

/* ---------------- hero collection slider ---------------- */
const COLL = D.coll;
COLL.forEach(c => { const i = new Image(); i.src = c.img; });
const stage = $("#coll-stage");
let ci = 0, collT;
const setCollDot = makeDots($("#coll-dots"), COLL.length, i => { showColl(i); collAuto(); });
const cardHTML = c => `<img src="${c.img}" alt="${c.alt}" width="56" height="56" decoding="async"><div class="c-txt"><p class="c-brand">${c.brand}</p><p class="c-title">${c.title}</p><a class="c-cta" href="${c.href === "#book" ? "#kontakt" : c.href}"${c.href === "#book" ? ' data-open="contact"' : ""}>${c.cta} →</a></div>`;
function showColl(i) {
  const next = (i + COLL.length) % COLL.length;
  const old = stage.querySelector(".coll-card:not(.leaving)");
  if (old && next === ci) return;
  ci = next;
  const n = document.createElement("article");
  n.className = "coll-card glass"; n.innerHTML = cardHTML(COLL[ci]);
  stage.appendChild(n); setCollDot(ci);
  if (old) {
    old.classList.add("leaving"); old.setAttribute("aria-hidden", "true");
    new Anim(old, { opacity: 1, y: 0, scale: 1 }).to({ opacity: 0, y: 16, scale: 0.96 }, [210, 24]);
    setTimeout(() => old.remove(), 700);
    new Anim(n, { opacity: 0, y: 16, scale: 0.96 }).to({ opacity: 1, y: 0, scale: 1 }, [210, 24]);
  }
}
function collAuto() { clearInterval(collT); collT = setInterval(() => showColl(ci + 1), 3800); }
showColl(0);
onReady(collAuto);

/* ---------------- trust carousel ---------------- */
const SL = D.slides;
SL.forEach(s => { const i = new Image(); i.sizes = "16rem"; i.srcset = s.srcset; i.src = s.img; });
const tTitle = $("#trust-title"), gwords = $$("#trust-title .gw .clip>span"), media = $("#coach-media");
let ti = -1;
const setTDot = makeDots($("#t-dots"), SL.length, i => setTrust(i));
function setTrust(i) {
  const first = ti === -1, next = (i + SL.length) % SL.length;
  if (next === ti) return;
  ti = next; const s = SL[ti];
  gwords.forEach((w, k) => (w.textContent = s.words[k]));
  $("#trust-sr").textContent = s.words.join(" ");
  if (!first && tTitle.classList.contains("is-in")) play(tTitle);
  const im = new Image(); im.decoding = "async"; im.sizes = "(min-width: 640px) 16rem, 13rem"; im.srcset = s.srcset; im.src = s.img; im.alt = s.alt;
  media.appendChild(im);
  if (!first) {
    new Anim(im, { opacity: 0 }).to({ opacity: 1 }, [260, 26]);
    setTimeout(() => { const kids = [...media.children]; kids.slice(0, kids.indexOf(im)).forEach(n => n.remove()); }, 900);
  }
  $("#coach-name").textContent = s.name; $("#coach-role").textContent = s.role;
  setTDot(ti);
}
setTrust(0);
$("#t-prev").addEventListener("click", () => setTrust(ti - 1));
$("#t-next").addEventListener("click", () => setTrust(ti + 1));

/* ---------------- contact modal ---------------- */
const modal = $("#contact"), mForm = $("#m-form"), mOk = $("#m-success"), mSubmit = $("#m-submit"), mTitle = $("#m-title");
const mBack = new Anim($(".m-back", modal), { opacity: 0 });
const mPanel = new Anim($(".m-panel", modal), { opacity: 0, y: 28, scale: 0.96 });
let lastFocus = null, resetT;
function openModal() {
  if (modalOpen) return;
  clearTimeout(resetT); resetForm();
  modalOpen = true; lastFocus = document.activeElement;
  modal.inert = false; modal.classList.add("open");
  mBack.to({ opacity: 1 }, [240, 30]);
  mPanel.to({ opacity: 1, y: 0, scale: 1 }, [240, 26]);
  play(mTitle);
  lock();
  setTimeout(() => mForm.elements.fullname.focus({ preventScroll: true }), 120);
}
function closeModal() {
  if (!modalOpen) return;
  modalOpen = false; modal.classList.remove("open");
  mBack.to({ opacity: 0 }, [240, 30]);
  mPanel.to({ opacity: 0, y: 28, scale: 0.96 }, [240, 26]);
  unlock();
  resetT = setTimeout(() => { resetForm(); modal.inert = true; }, 350);
  if (lastFocus && document.contains(lastFocus)) lastFocus.focus({ preventScroll: true });
}
function resetForm() {
  mForm.reset(); mForm.hidden = false; mOk.hidden = true;
  $$(".input", mForm).forEach(i => i.removeAttribute("aria-invalid")); $$(".err", mForm).forEach(e => (e.textContent = ""));
  $$(".submit", mForm).forEach(b => (b.disabled = false)); mSubmit.lastChild.textContent = " " + D.send;
  datesMin();
}
const fFrom = mForm.elements.from, fTo = mForm.elements.to;
const iso = d => new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
const pDate = v => (v ? new Date(v + "T12:00:00") : null);
function datesMin() { const t = new Date(); t.setHours(12, 0, 0, 0); fFrom.min = iso(t); fTo.min = iso(new Date(t.getTime() + 864e5)); }
fFrom.addEventListener("change", () => {
  const a = pDate(fFrom.value); if (!a) return;
  fTo.min = iso(new Date(a.getTime() + 864e5));
  if (!fTo.value || pDate(fTo.value) <= a) fTo.value = iso(new Date(a.getTime() + 2 * 864e5));
  fTo.removeAttribute("aria-invalid"); $("#e-to").textContent = "";
});
const nightsWord = n => { const f = D.nights; if (D.lang !== "sr") return n === 1 ? f[0] : f[1];
  if (n % 10 === 1 && n % 100 !== 11) return f[0]; if ([2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100)) return f[1]; return f[2]; };
const fmtD = v => { const d = pDate(v); return D.lang === "sr" ? `${d.getDate()}. ${d.getMonth() + 1}. ${d.getFullYear()}.` : d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }); };
function fieldErr(el, msg) { el.setAttribute("aria-invalid", "true"); $("#e-" + el.name).textContent = msg; }
$$(".input", mForm).forEach(el => el.addEventListener("input", () => { el.removeAttribute("aria-invalid"); const e = $("#e-" + el.name); if (e) e.textContent = ""; }));
mForm.addEventListener("submit", e => {
  e.preventDefault(); /* no server: the message opens in WhatsApp / Viber */
  const f = mForm.elements, via = (e.submitter && e.submitter.value) || "wa";
  let bad = null;
  ["fullname", "from", "to"].forEach(n => { const el = f[n]; el.removeAttribute("aria-invalid"); $("#e-" + n).textContent = ""; if (!el.value.trim()) { fieldErr(el, D.err_req); bad = bad || el; } });
  const n = f.from.value && f.to.value ? Math.round((pDate(f.to.value) - pDate(f.from.value)) / 864e5) : 0;
  if (!bad && n <= 0) { fieldErr(f.to, D.err_dates); bad = f.to; }
  if (bad) { bad.focus(); return; }
  const L = D.labels, lines = [D.intro, "", `${L.dates}: ${fmtD(f.from.value)} – ${fmtD(f.to.value)}`, `${L.nights}: ${n} ${nightsWord(n)}`,
    `${L.guests}: ${f.guests.value}`, `${L.name}: ${f.fullname.value.trim()}`];
  if (f.msg.value.trim()) lines.push(`${L.msg}: ${f.msg.value.trim()}`);
  const text = encodeURIComponent(lines.join("\n"));
  $$(".submit", mForm).forEach(b => (b.disabled = true)); mSubmit.lastChild.textContent = " " + D.sending;
  if (via === "viber") location.href = `viber://chat?number=%2B${D.phone}&draft=${text}`;
  else window.open(`https://wa.me/${D.phone}?text=${text}`, "_blank", "noopener");
  setTimeout(() => {
    const first = f.fullname.value.trim().split(/\s+/)[0];
    $("#m-thanks").textContent = D.thanks.replace("{name}", first);
    mForm.hidden = true; mOk.hidden = false; mOk.focus({ preventScroll: true });
  }, 500);
});
datesMin();

/* ---------------- fullscreen menu ---------------- */
const menu = $("#menu");
const nBack = new Anim($(".menu-back", menu), { opacity: 0 });
const nPanel = new Anim($(".menu-panel", menu), { opacity: 0, y: -24 });
const nLinks = $$(".menu-nav a", menu).map(a => new Anim(a, { opacity: 0, y: 28 }));
function openMenu() {
  if (menuOpen) return;
  menuOpen = true; menu.inert = false; menu.classList.add("open");
  nBack.to({ opacity: 1 }, [260, 30]);
  nPanel.to({ opacity: 1, y: 0 }, [220, 28]);
  nLinks.forEach((a, i) => a.jump({ opacity: 0, y: 28 }).to({ opacity: 1, y: 0 }, [200, 26], 120 + i * 70));
  lock();
  setTimeout(() => $(".x-btn", menu).focus({ preventScroll: true }), 60);
}
function closeMenu() {
  if (!menuOpen) return;
  menuOpen = false; menu.classList.remove("open");
  nBack.to({ opacity: 0 }, [260, 30]);
  nPanel.to({ opacity: 0, y: -24 }, [220, 28]);
  unlock();
  setTimeout(() => { if (!menuOpen) menu.inert = true; }, 400);
}

/* ---------------- global wiring ---------------- */
document.addEventListener("click", e => {
  const op = e.target.closest("[data-open]");
  if (op) {
    e.preventDefault();
    if (op.dataset.open === "menu") openMenu();
    else { if (menuOpen) closeMenu(); openModal(); }
    return;
  }
  const cl = e.target.closest("[data-close]");
  if (cl) { cl.dataset.close === "menu" ? closeMenu() : closeModal(); return; }
  const a = e.target.closest('a[href^="#"]');
  if (a) {
    const id = a.getAttribute("href"); if (id.length < 2) return;
    const t = document.querySelector(id); if (!t) return;
    e.preventDefault();
    if (menuOpen) closeMenu();
    if (lenis) lenis.scrollTo(t, { duration: 1.2 }); else t.scrollIntoView({ behavior: reduced ? "auto" : "smooth" });
  }
});
addEventListener("keydown", e => { if (e.key === "Escape") { if (modalOpen) closeModal(); else if (menuOpen) closeMenu(); } });

/* ---------------- loader / reveal ---------------- */
const MIN_VISIBLE_MS = reduced ? 200 : 1400, MAX_VISIBLE_MS = 2600, EXIT_MS = reduced ? 0 : 850;
const loader = $("#loader");
lock();
const lMark = new Anim($("#l-mark"), { opacity: 0, y: 16 });
requestAnimationFrame(() => { lMark.to({ opacity: 1, y: 0 }, [200, 22]); loader.classList.add("go"); });
let started = false, finished = false;
function finish() {
  if (finished) return; finished = true;
  ready = true; readyQ.splice(0).forEach(f => f());
  unlock();
  loader.style.transition = `transform ${EXIT_MS}ms cubic-bezier(.65,0,.35,1)`;
  loader.style.transform = "translateY(-105%)";
  setTimeout(() => loader.remove(), EXIT_MS + 30);
}
function startCountdown() { if (started) return; started = true; setTimeout(finish, MIN_VISIBLE_MS); }
if (document.readyState === "complete") startCountdown(); else addEventListener("load", startCountdown, { once: true });
setTimeout(() => { if (!started) { started = true; finish(); } }, MAX_VISIBLE_MS);
