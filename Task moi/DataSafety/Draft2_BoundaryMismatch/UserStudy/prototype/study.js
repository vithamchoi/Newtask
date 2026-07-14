/*
 * study.js — single-page study runner for the BLE vignette experiment.
 *
 * Flow:
 *   landing -> consent -> pretask -> per-app * 4 -> attention -> posttask -> debrief
 *
 * Everything is local-first: the participant's responses are kept in
 * window.STATE and mirrored to localStorage so a refresh does not lose
 * progress. On submit, the response is POSTed to BACKEND_URL (if
 * configured) AND offered as a downloadable JSON as a backup.
 *
 * No external dependencies; pure vanilla JS.
 */

// =====================================================================
// 0. Configuration
// =====================================================================
const STUDY_ID    = "2024-bcm-bleeval";
const STUDY_VER   = "1.0.0";
const N_APPS      = 4;
const BACKEND_URL = "https://script.google.com/macros/s/AKfycbyjB46G9lBUaIHOLs6sXe0amqUfKkKDGtEKth_zQCuGa6r6fh35O-OtBEWDaHkGh0ngPA/exec";
const FALLBACK_DOWNLOAD = true;

// =====================================================================
// 1. Tiny utilities
// =====================================================================
function el(tag, attrs, ...children) {
  const e = document.createElement(tag);
  Object.entries(attrs || {}).forEach(([k, v]) => {
    if (k === "class") e.className = v;
    else if (k === "html") e.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function") e[k] = v;
    else e.setAttribute(k, v);
  });
  children.flat().forEach(c => {
    if (c == null) return;
    e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  });
  return e;
}
function $(sel) { return document.querySelector(sel); }
function getParam(name, fallback) {
  const v = new URLSearchParams(location.search).get(name);
  return v == null ? fallback : v;
}
function fnv1a(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}
function mulberry32(seed) {
  return function () {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function shuffled(arr, rng) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function genCode() {
  return "BCM-" + Math.random().toString(36).slice(2, 6).toUpperCase()
       + "-" + Math.random().toString(36).slice(2, 6).toUpperCase();
}

// =====================================================================
// 2. State (persisted)
// =====================================================================
const STATE = {
  meta: {
    study_id: STUDY_ID,
    study_ver: STUDY_VER,
    pid: getParam("pid", ""),
    pid_source: getParam("pid", "") ? "url" : "anonymous",
    started_at: null,
    user_agent: navigator.userAgent,
  },
  consent: null,
  condition: null,         // "current" | "ble"
  pretask: {},
  apps: [],                // ordered list of app objects shown
  per_app: {},             // { app_id: { mcq: ..., L3_2: ..., ... } }
  attention: null,
  posttask: {},
  events: [],              // interaction log
  completion_code: null,
};
function log(event, payload) {
  STATE.events.push({ t: Date.now(), event, ...(payload || {}) });
  persist();
}
function persist() {
  try { localStorage.setItem("bcm_state", JSON.stringify(STATE)); }
  catch (e) { /* quota — non-fatal */ }
}
function restore() {
  try {
    const raw = localStorage.getItem("bcm_state");
    if (raw) {
      const saved = JSON.parse(raw);
      if (saved.meta && saved.meta.study_id === STUDY_ID) {
        Object.assign(STATE, saved);
      }
    }
  } catch (e) { /* ignore */ }
}

// =====================================================================
// 3. Community signal (from the published survey)
// =====================================================================
const COMMUNITY = {
  b1: { yes: 80.9, no: 0,  maybe: 19.1, name: "On-device only",         tier: "Capability"    },
  b2: { yes: 83.3, no: 0,  maybe: 16.7, name: "End-to-end encryption",  tier: "Recipient"     },
  b3: { yes: 61.8, no: 0,  maybe: 38.2, name: "Off-device ephemeral",   tier: "Reversibility" },
  b4: { yes: 75.4, no: 0,  maybe: 24.6, name: "Redirect to service",    tier: "Recipient"     },
  b5: { yes: 82.3, no: 0,  maybe: 17.7, name: "User-initiated",         tier: "Consent"       },
  b6: { yes: 79.0, no: 0,  maybe: 21.0, name: "Prominent consent",      tier: "Consent"       },
  b7: { yes: 72.6, no: 0,  maybe: 27.4, name: "Service provider",       tier: "Recipient"     },
  b8: { yes: 73.9, no: 0,  maybe: 26.2, name: "Legal transfer",         tier: "Recipient"     },
  b9: { yes: 71.6, no: 0,  maybe: 28.4, name: "Anonymised transfer",    tier: "Reversibility" },
};

// =====================================================================
// 4. App-pool sampling + condition assignment
// =====================================================================
async function loadResources() {
  // Strategy: try fetch() first (works when hosted via HTTP). If it fails
  // — typical when the file is opened directly from disk via file:// —
  // fall back to the inline data loaded by the <script> tags in the HTML
  // (apps_data.js, mcq_data.js).
  try {
    const [appsRes, mcqRes] = await Promise.all([
      fetch("apps.json"),
      fetch("mcq_bank.json"),
    ]);
    if (!appsRes.ok || !mcqRes.ok) throw new Error("fetch returned non-OK");
    return { apps: await appsRes.json(), mcq: await mcqRes.json() };
  } catch (e) {
    if (window.__APPS_FALLBACK && window.__MCQ_FALLBACK) {
      console.warn("[study] fetch unavailable (file://?). Using inline fallback.");
      return { apps: window.__APPS_FALLBACK, mcq: window.__MCQ_FALLBACK };
    }
    throw e;
  }
}
function assignCondition(pid) {
  if (!pid) return Math.random() < 0.5 ? "current" : "ble";
  return (fnv1a(pid + ":cond:" + STUDY_ID) % 2 === 0) ? "current" : "ble";
}
function selectAppsForParticipant(pool, pid, K) {
  const seedKey = (pid || "anonymous-" + Math.floor(Math.random() * 1e9))
                + "::" + STUDY_ID;
  const rng = mulberry32(fnv1a(seedKey));
  const tagged = pool.map(a => {
    const tiers = new Set();
    [...a.collected, ...a.shared].forEach(it => { if (it.tier) tiers.add(it.tier); });
    return { app: a, tiers };
  });
  const need = new Set(["Reversibility", "Recipient", "Consent"]);
  const chosen = [], picked = new Set();
  const order = shuffled(tagged, rng);
  for (const t of order) {
    if (chosen.length >= K) break;
    if ([...t.tiers].some(x => need.has(x))) {
      chosen.push(t.app); picked.add(t.app.id);
      [...t.tiers].forEach(x => need.delete(x));
    }
  }
  for (const t of order) {
    if (chosen.length >= K) break;
    if (!picked.has(t.app.id)) { chosen.push(t.app); picked.add(t.app.id); }
  }
  return chosen;
}

// =====================================================================
// 5. Renderer (current vs ble) — re-implemented inline for SPA
// =====================================================================
function renderLabel(app, condition, mount) {
  mount.innerHTML = "";
  const card = el("div", { class: "app-card" });
  card.appendChild(el("div", { class: "app-head" },
    el("div", { class: "app-icon" }, app.name[0]),
    el("div", {},
      el("div", { class: "app-name" }, app.name),
      el("div", { class: "app-dev" },
        app.developer, " · ", app.installs, " installs · ★ " + app.rating),
      el("div", { class: "app-meta" }, app.size_mb + " MB · " + app.tagline)
    )
  ));
  card.appendChild(el("div", { class: "app-desc" }, app.description));

  const renderRow = (item, kind) => {
    const contested = !!item.boundary;
    card.appendChild(el("div",
      { class: "label-row" + (contested ? " contested" : "") },
      el("div", { class: "label-cat" }, item.category),
      el("div", { class: "label-tag" }, item.purposes.join(" · "))
    ));
    if (condition === "ble" && contested) {
      const c = COMMUNITY[item.boundary] || {};
      const drawer = el("div", { class: "ble-drawer" });
      drawer.appendChild(el("div", { class: "ble-head" },
        el("strong", {}, "Boundary applied: " + (c.name || item.boundary)),
        el("span", {
          class: "tier-pill tier-" + (item.tier || c.tier)
        }, item.tier || c.tier)
      ));
      drawer.appendChild(el("div", { class: "ble-rule" }, "“" + item.rule_clause + "”"));
      drawer.appendChild(el("div", { class: "ble-signal" },
        `Community: ${c.yes}% accept · ${c.maybe}% unsure`));
      const btn = el("button", {
        class: "ble-toggle-btn",
        onclick: function () {
          const open = counter.style.display !== "none";
          counter.style.display = open ? "none" : "block";
          this.textContent = (open ? "▾" : "▴")
            + " " + (open ? "Show" : "Hide")
            + " what this label would say if the rule did not apply";
          log("ble_toggle_" + (open ? "close" : "open"),
              { app: app.id, boundary: item.boundary });
        }
      }, "▾ Show what this label would say if the rule did not apply");
      const counter = el("div", { class: "counter", style: "display:none" },
        "If the ‘" + (c.name || item.boundary)
        + "’ rule did not apply, the platform would have to declare this "
        + kind + " in plain terms, with no exception.");
      drawer.appendChild(btn);
      drawer.appendChild(counter);
      card.appendChild(drawer);
    }
  };

  card.appendChild(el("div", { class: "section-title" }, "Data this app may COLLECT"));
  app.collected.forEach(it => renderRow(it, "collected"));
  card.appendChild(el("div", { class: "section-title" }, "Data this app may SHARE with third parties"));
  app.shared.forEach(it => renderRow(it, "shared"));
  mount.appendChild(card);
}

// =====================================================================
// 6. Phase renderers
// =====================================================================
function progress(pct) {
  const bar = $("#progress");
  if (bar) bar.firstElementChild.style.width = pct + "%";
}

function phaseLanding(root) {
  progress(0);
  root.innerHTML = "";
  root.appendChild(el("div", { class: "phase" },
    el("h1", {}, "Understanding app privacy labels"),
    el("p", {},
      "Thank you for taking part. The study takes about 15 minutes. You will look at the privacy section of four fictional apps and answer a few short questions about each."),
    el("p", {},
      "There are no right or wrong answers. We are testing the design, not you."),
    el("div", { class: "banner info" },
      "Participant ID: ", el("code", {}, STATE.meta.pid || "(anonymous demo)"),
      ".  Browser progress is saved automatically; you may refresh without losing your answers."),
    el("div", { class: "nav-row" },
      el("span"),
      el("button", { class: "btn-primary", onclick: () => { STATE.meta.started_at = Date.now(); log("study_start"); go("consent"); } }, "Start")
    )
  ));
}

function phaseConsent(root) {
  progress(8);
  root.innerHTML = "";
  let c1 = false, c2 = false;
  const advance = el("button", { class: "btn-primary", disabled: "" }, "Continue");
  const refresh = () => {
    if (c1 && c2) advance.removeAttribute("disabled");
    else advance.setAttribute("disabled", "");
  };
  advance.onclick = () => { STATE.consent = { c1, c2, at: Date.now() }; log("consent_given"); go("pretask"); };

  root.appendChild(el("div", { class: "phase" },
    el("h1", {}, "Consent"),
    el("p", {}, "Please read the information below and tick both boxes to continue."),
    el("h2", {}, "What is this study about?"),
    el("p", {}, "We are studying how people read app-store privacy labels. You will look at the privacy sections of four fictional apps and answer one multiple-choice question and three short rating questions about each."),
    el("h2", {}, "What information do we collect?"),
    el("p", {}, "Your responses, the time you spend on each screen, and which drawers you open inside the prototype. No name, email, or device identifier is collected by us."),
    el("h2", {}, "Your rights"),
    el("p", {}, "You can stop the study at any time without penalty. You may ask for your data to be deleted up to the point of publication by contacting the research team via the platform you joined through."),
    el("div", { class: "consent-check" },
      el("input", {
        type: "checkbox", id: "c1",
        onchange: function () { c1 = this.checked; refresh(); }
      }),
      el("label", { for: "c1" }, "I have read and understood the information above.")
    ),
    el("div", { class: "consent-check" },
      el("input", {
        type: "checkbox", id: "c2",
        onchange: function () { c2 = this.checked; refresh(); }
      }),
      el("label", { for: "c2" }, "I agree to participate.")
    ),
    el("div", { class: "nav-row" },
      el("button", { class: "btn-secondary", onclick: () => location.reload() }, "Exit"),
      advance
    )
  ));
}

function radioGroup(name, options) {
  return el("div", { class: "radio-list" },
    options.map(o => el("label", {},
      el("input", { type: "radio", name, value: o.value }),
      el("span", {}, o.label)
    ))
  );
}
function getRadio(name) {
  const r = document.querySelector(`input[name="${name}"]:checked`);
  return r ? r.value : null;
}

function likert7(name, anchors) {
  const wrap = el("div");
  wrap.appendChild(el("div", { class: "likert-anchor" },
    el("span", {}, anchors[0]),
    el("span", {}, anchors[1])
  ));
  const grid = el("div", { class: "likert-7" });
  for (let i = 1; i <= 7; i++) {
    grid.appendChild(el("label", {},
      el("input", { type: "radio", name, value: String(i) }),
      el("span", {}, String(i))
    ));
  }
  wrap.appendChild(grid);
  return wrap;
}

function phasePretask(root) {
  progress(16);
  root.innerHTML = "";
  const advance = el("button", { class: "btn-primary" }, "Continue");
  advance.onclick = () => {
    const q21 = getRadio("q2_1"), q22 = getRadio("q2_2");
    const q23 = $("#q2_3").value;
    if (!q21 || !q22) { alert("Please answer both questions."); return; }
    STATE.pretask = { q21, q22, q23: Number(q23) };
    log("pretask_done", STATE.pretask);
    go("assign");
  };
  root.appendChild(el("div", { class: "phase" },
    el("h1", {}, "A few quick questions about you"),
    el("h2", {}, "How long have you used an Android phone?"),
    radioGroup("q2_1", [
      { value: "lt1y",   label: "Less than 1 year" },
      { value: "1to3",   label: "1–3 years" },
      { value: "3to5",   label: "3–5 years" },
      { value: "gt5y",   label: "More than 5 years" },
      { value: "notnow", label: "I do not currently use an Android phone" }
    ]),
    el("h2", {}, "Before today, had you ever looked at the Data Safety section on Google Play?"),
    radioGroup("q2_2", [
      { value: "reg", label: "Yes, regularly" },
      { value: "occ", label: "Yes, occasionally" },
      { value: "mb",  label: "I might have but I don't recall" },
      { value: "no",  label: "No, never" },
      { value: "dk",  label: "I don't know what that is" }
    ]),
    el("h2", {}, "How concerned are you about data being collected from your phone? (1 = not at all, 10 = extremely)"),
    el("div", { class: "slider-row" },
      el("input", { type: "range", min: "1", max: "10", step: "1", value: "5", id: "q2_3",
        oninput: function () { $("#q2_3_out").textContent = this.value; } }),
      el("div", {},
        "Concern: ", el("output", { id: "q2_3_out" }, "5")
      )
    ),
    el("div", { class: "nav-row" }, el("span"), advance)
  ));
}

function phaseAssign(root) {
  progress(20);
  STATE.condition = STATE.condition || assignCondition(STATE.meta.pid);
  if (!STATE.apps.length) {
    STATE.apps = selectAppsForParticipant(window.__APPS, STATE.meta.pid, N_APPS);
  }
  log("assigned", { condition: STATE.condition, apps: STATE.apps.map(a => a.id) });
  persist();
  go("app", 0);
}

function phaseAppBlock(root, idx) {
  progress(20 + Math.floor((idx) * 60 / N_APPS));
  const app = STATE.apps[idx];
  const cond = STATE.condition;
  log("view_app", { app: app.id, condition: cond, idx });

  // Find the first contested cell that drives the MCQ
  const contested = [...app.collected, ...app.shared].find(it => it.boundary);
  if (!contested) {
    // safety: if no contested cell, skip MCQ
    advanceApp(idx, { mcq_skipped: true });
    return;
  }
  const mcqT = window.__MCQ[contested.boundary];
  const rng = mulberry32(fnv1a((STATE.meta.pid || "x") + ":mcq:" + app.id));
  const opts = shuffled([
    { text: mcqT.correct_text, correct: true },
    ...mcqT.distractors.map(d => ({ text: d, correct: false }))
  ], rng);

  root.innerHTML = "";
  const phase = el("div", { class: "phase" });
  phase.appendChild(el("h1", {}, `App ${idx + 1} of ${N_APPS}: ${app.name}`));
  phase.appendChild(el("p", {}, "Look at the privacy section below, then answer the questions."));
  const mount = el("div");
  phase.appendChild(mount);
  renderLabel(app, cond, mount);

  // MCQ
  phase.appendChild(el("h2", {}, mcqT.stem.replace("{category}", contested.category)));
  const mcqList = el("div", { class: "radio-list" });
  opts.forEach((o, i) => {
    mcqList.appendChild(el("label", {},
      el("input", { type: "radio", name: "mcq", value: String(i) }),
      el("span", {}, o.text)
    ));
  });
  phase.appendChild(mcqList);

  // Likerts
  phase.appendChild(el("h2", {}, "This label accurately describes what this app does with your data."));
  phase.appendChild(likert7("L3_2", ["strongly disagree", "strongly agree"]));
  phase.appendChild(el("h2", {}, "This label gives me enough information to decide whether to install this app."));
  phase.appendChild(likert7("L3_3", ["strongly disagree", "strongly agree"]));
  phase.appendChild(el("h2", {}, "How likely are you to install this app?"));
  phase.appendChild(likert7("L3_4", ["definitely would not", "definitely would"]));
  phase.appendChild(el("h2", {}, "In one sentence, what made you choose that answer?"));
  phase.appendChild(el("div", { class: "free-text" },
    el("textarea", { id: "T3_5", placeholder: "Optional but appreciated…" })
  ));

  const nextBtn = el("button", { class: "btn-primary" },
    idx + 1 < N_APPS ? "Next app" : "Finish app section");
  nextBtn.onclick = () => {
    const mcq = getRadio("mcq");
    const L32 = getRadio("L3_2"), L33 = getRadio("L3_3"), L34 = getRadio("L3_4");
    if (mcq == null || !L32 || !L33 || !L34) {
      alert("Please answer the multiple-choice and all three rating questions.");
      return;
    }
    const chosen = opts[Number(mcq)];
    STATE.per_app[app.id] = {
      app_id: app.id,
      idx,
      condition: cond,
      contested_boundary: contested.boundary,
      contested_category: contested.category,
      mcq_choice_idx: Number(mcq),
      mcq_chosen_text: chosen.text,
      mcq_correct: chosen.correct,
      L3_2: Number(L32), L3_3: Number(L33), L3_4: Number(L34),
      T3_5: $("#T3_5").value || "",
      t_view_ms: Date.now() - (STATE.events.filter(e => e.event === "view_app" && e.app === app.id).slice(-1)[0]?.t ?? Date.now())
    };
    log("app_done", { app: app.id, idx, correct: chosen.correct });
    advanceApp(idx);
  };
  phase.appendChild(el("div", { class: "nav-row" }, el("span"), nextBtn));
  root.appendChild(phase);
  window.scrollTo({ top: 0, behavior: "instant" });
}
function advanceApp(idx, extra) {
  if (extra) STATE.per_app[STATE.apps[idx].id] = Object.assign(STATE.per_app[STATE.apps[idx].id] || {}, extra);
  if (idx + 1 < N_APPS) go("app", idx + 1);
  else go("attention");
}

function phaseAttention(root) {
  progress(82);
  root.innerHTML = "";
  const advance = el("button", { class: "btn-primary" }, "Continue");
  advance.onclick = () => {
    const v = getRadio("A4_1");
    if (!v) { alert("Please select an option."); return; }
    STATE.attention = { value: Number(v), pass: Number(v) === 4 };
    log("attention", STATE.attention);
    go("posttask");
  };
  root.appendChild(el("div", { class: "phase" },
    el("h1", {}, "One last check"),
    el("p", {}, "To show you are paying attention, please select 4 for this item."),
    likert7("A4_1", ["1", "7"]),
    el("div", { class: "nav-row" }, el("span"), advance)
  ));
}

function phasePostTask(root) {
  progress(90);
  root.innerHTML = "";
  const isBLE = STATE.condition === "ble";
  const advance = el("button", { class: "btn-primary" }, "Submit");
  advance.onclick = () => {
    const Q61 = getRadio("Q6_1");
    if (!Q61) { alert("Please answer the honesty item."); return; }
    STATE.posttask = {
      Q5_1: isBLE ? getRadio("Q5_1") : null,
      L5_2: isBLE ? Number(getRadio("L5_2")) || null : null,
      T5_3: isBLE ? ($("#T5_3")?.value || "") : null,
      Q6_1: Q61,
      T6_2: $("#T6_2").value || "",
      age:    getRadio("age"),
      gender: getRadio("gender"),
      edu:    getRadio("edu"),
      it_bg:  getRadio("it_bg"),
    };
    log("posttask_done", STATE.posttask);
    submitStudy();
  };

  const blePart = isBLE ? [
    el("h2", {}, "During the study, did you open any Boundary-Layer Explainer drawers (the yellow boxes)?"),
    radioGroup("Q5_1", [
      { value: "many",     label: "Yes, I opened several" },
      { value: "one",      label: "Yes, I opened one" },
      { value: "noticed",  label: "I noticed them but didn't open them" },
      { value: "missed",   label: "I don't remember seeing them" }
    ]),
    el("h2", {}, "How useful would you find the BLE drawer on a real label?"),
    likert7("L5_2", ["not at all useful", "extremely useful"]),
    el("h2", {}, "What would you change about the BLE drawer to make it more useful?"),
    el("div", { class: "free-text" }, el("textarea", { id: "T5_3" }))
  ] : [];

  root.appendChild(el("div", { class: "phase" },
    el("h1", {}, "Almost done — just a few last questions"),
    ...blePart,
    el("h2", {}, "Did you complete the four apps in good faith and read each label?"),
    radioGroup("Q6_1", [
      { value: "yes",     label: "Yes" },
      { value: "rushed",  label: "No, I rushed some" }
    ]),
    el("h2", {}, "Anything else you want to tell us?"),
    el("div", { class: "free-text" }, el("textarea", { id: "T6_2" })),
    el("h2", {}, "Demographics"),
    el("p", { style: "color:var(--ink-soft);font-size:0.85rem" },
      "Optional. None of these are used to identify you."),
    radioGroup("age", [
      { value: "18_24", label: "Age: 18–24" },
      { value: "25_34", label: "Age: 25–34" },
      { value: "35_44", label: "Age: 35–44" },
      { value: "45_54", label: "Age: 45–54" },
      { value: "55_64", label: "Age: 55–64" },
      { value: "65p",   label: "Age: 65+" },
      { value: "pnts",  label: "Prefer not to say" }
    ]),
    radioGroup("gender", [
      { value: "woman", label: "Gender: woman" },
      { value: "man",   label: "Gender: man" },
      { value: "nb",    label: "Gender: non-binary" },
      { value: "self",  label: "Gender: prefer to self-describe" },
      { value: "pnts",  label: "Gender: prefer not to say" }
    ]),
    radioGroup("edu", [
      { value: "hs",  label: "Education: high school" },
      { value: "sc",  label: "Education: some college" },
      { value: "ba",  label: "Education: bachelor's" },
      { value: "ma",  label: "Education: master's" },
      { value: "phd", label: "Education: doctoral" },
      { value: "oth", label: "Education: other" }
    ]),
    radioGroup("it_bg", [
      { value: "yes",  label: "I work in computing, IT, or cybersecurity" },
      { value: "no",   label: "I do not work in computing, IT, or cybersecurity" },
      { value: "pnts", label: "Prefer not to say" }
    ]),
    el("div", { class: "nav-row" }, el("span"), advance)
  ));
}

function submitStudy() {
  STATE.completion_code = STATE.completion_code || genCode();
  log("submit");
  const payload = JSON.stringify(STATE);
  // Try server submit
  let serverOk = false;
  if (BACKEND_URL) {
    fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload
    }).then(r => { serverOk = r.ok; }).catch(() => {});
  }
  // Show debrief
  go("debrief");
}

function phaseDebrief(root) {
  progress(100);
  root.innerHTML = "";
  const code = STATE.completion_code;
  const blob = new Blob([JSON.stringify(STATE, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const filename = "bcm-" + (STATE.meta.pid || "anonymous") + "-" + code + ".json";

  root.appendChild(el("div", { class: "phase" },
    el("h1", {}, "Thank you"),
    el("p", {},
      "The apps you saw (SocialNova, ChatBuzz, PhotoPals, MapMate, Tunesy, VibeVoice, Trekly, Questly, LingoMate, BookBuddy, FitCircle, DiaryNow) are fictional and were created for research purposes only. The Boundary-Layer Explainer (BLE) is a research prototype that does not exist in the real Play Store."),
    el("h2", {}, "Your completion code"),
    el("p", {},
      "Please paste this code into the platform you joined through to confirm your participation:"),
    el("div", { style: "text-align:center;margin:14px 0" },
      el("span", { class: "code-pill" }, code)),
    BACKEND_URL
      ? el("div", { class: "banner ok" }, "Your responses were sent to the research server.")
      : el("div", { class: "banner warn" },
          "No server is configured for this build. Please download your response file below and email it to the research team."),
    FALLBACK_DOWNLOAD ? el("p", { style: "text-align:center" },
      el("a", { href: url, download: filename, class: "btn-secondary" }, "Download your response (JSON)")) : null,
    el("p", { style: "color:var(--ink-soft);font-size:0.85rem;margin-top:18px" },
      "You may now close the tab.")
  ));
}

// =====================================================================
// 7. Router
// =====================================================================
function go(phase, ...args) {
  STATE.meta.last_phase = phase;
  persist();
  const root = $("#root");
  if (phase === "landing")   return phaseLanding(root);
  if (phase === "consent")   return phaseConsent(root);
  if (phase === "pretask")   return phasePretask(root);
  if (phase === "assign")    return phaseAssign(root);
  if (phase === "app")       return phaseAppBlock(root, args[0]);
  if (phase === "attention") return phaseAttention(root);
  if (phase === "posttask")  return phasePostTask(root);
  if (phase === "debrief")   return phaseDebrief(root);
  root.textContent = "Unknown phase: " + phase;
}

// =====================================================================
// 8. Boot
// =====================================================================
async function boot() {
  restore();
  let res;
  try {
    res = await loadResources();
  } catch (err) {
    const root = $("#root");
    root.innerHTML = "";
    root.appendChild(el("div", { class: "phase" },
      el("h1", {}, "Cannot load study data"),
      el("div", { class: "banner error" },
        el("strong", {}, "Resource load failed. "),
        "The browser could not read the study's data files. This usually means the page was opened directly from disk (the URL starts with ", el("code", {}, "file://"), "), which modern browsers block for security reasons."
      ),
      el("h2", {}, "Quick fix — serve the folder from a tiny local server"),
      el("p", {}, "Open a terminal in this folder and run:"),
      el("pre", { style: "background:#f5f5f7;padding:10px;border-radius:6px;font-size:0.9rem;overflow:auto;" }, "cd UserStudy/prototype\npython3 -m http.server 8080"),
      el("p", {},
        "Then open ",
        el("code", {}, "http://localhost:8080/study.html?pid=PILOT-001"),
        " in your browser."),
      el("p", { style: "color:var(--ink-soft);font-size:0.85rem;margin-top:14px;" },
        "Alternatively, host the ", el("code", {}, "prototype/"), " folder on GitHub Pages or Netlify (see ", el("code", {}, "deploy/README.md"), ") and visit the public URL.")
    ));
    return;
  }
  window.__APPS = res.apps;
  window.__MCQ  = res.mcq;
  // If the participant already completed, show debrief.
  if (STATE.completion_code) { go("debrief"); return; }
  // Resume from where they were, else start from landing.
  if (STATE.meta.last_phase && STATE.meta.last_phase !== "landing") {
    // resume to the same phase; idx for app phase is derived from per_app keys
    if (STATE.meta.last_phase === "app") {
      const done = Object.keys(STATE.per_app).length;
      if (done >= N_APPS) go("attention");
      else go("app", done);
    } else {
      go(STATE.meta.last_phase);
    }
  } else {
    go("landing");
  }
}
window.addEventListener("DOMContentLoaded", boot);
