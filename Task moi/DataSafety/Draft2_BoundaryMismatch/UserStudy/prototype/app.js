/* Shared rendering logic for the BLE prototype.
 * Two conditions:
 *   "current" — flag-only renderer mimicking Google Play Data Safety
 *   "ble"     — adds drawers for any item carrying a `boundary` field
 *
 * The same apps.json drives both conditions so the manipulation is
 * purely the renderer.
 */

// Community signal data measured in the published survey (filtered N=62)
const COMMUNITY = {
  b1: { yes: 62.1, no: 23.0, maybe: 14.9, name: "On-device only",         tier: "Capability"    },
  b2: { yes: 69.0, no: 17.2, maybe: 13.8, name: "End-to-end encryption",  tier: "Recipient"     },
  b3: { yes: 48.3, no: 23.0, maybe: 28.7, name: "Off-device ephemeral",   tier: "Reversibility" },
  b4: { yes: 58.6, no: 21.8, maybe: 19.5, name: "Redirect to service",    tier: "Recipient"     },
  b5: { yes: 58.6, no: 28.7, maybe: 12.6, name: "User-initiated",         tier: "Consent"       },
  b6: { yes: 56.3, no: 28.7, maybe: 14.9, name: "Prominent consent",      tier: "Consent"       },
  b7: { yes: 51.7, no: 28.7, maybe: 19.5, name: "Service provider",       tier: "Recipient"     },
  b8: { yes: 55.2, no: 25.3, maybe: 19.5, name: "Legal transfer",         tier: "Recipient"     },
  b9: { yes: 55.2, no: 23.0, maybe: 21.8, name: "Anonymised transfer",    tier: "Reversibility" },
};

function getParam(name, fallback) {
  const v = new URLSearchParams(location.search).get(name);
  return v == null ? fallback : v;
}

async function loadApps() {
  // Try fetch first; fall back to inline data if blocked (e.g. file://).
  try {
    const r = await fetch("apps.json");
    if (!r.ok) throw new Error("non-OK");
    return await r.json();
  } catch (e) {
    if (window.__APPS_FALLBACK) {
      console.warn("[app] fetch unavailable. Using inline fallback.");
      return window.__APPS_FALLBACK;
    }
    throw e;
  }
}

// Seeded PRNG (Mulberry32) so each participant's app subset is
// deterministic given their pid and re-loadable for replication.
function mulberry32(seed) {
  return function() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function hashString(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

/**
 * Select K apps from the pool for this participant, stratified to
 * cover the three typology families (Reversibility, Recipient, Consent)
 * at least once each. Selection is deterministic given the pid+study tag.
 */
function selectAppsForParticipant(pool, pid, K = 4) {
  const rng = mulberry32(hashString(pid + "::2024-bcm-bleeval"));
  // Tag each app with its families based on contested cells.
  const tagged = pool.map(a => {
    const tiers = new Set();
    [...a.collected, ...a.shared].forEach(it => { if (it.tier) tiers.add(it.tier); });
    return { app: a, tiers };
  });
  // Greedy stratified selection: first ensure at least one of each family,
  // then top up at random.
  const need = new Set(["Reversibility", "Recipient", "Consent"]);
  const chosen = [];
  const pickedIds = new Set();
  const shuffled = tagged.slice().sort(() => rng() - 0.5);
  for (const t of shuffled) {
    if (chosen.length >= K) break;
    const fills = [...t.tiers].some(x => need.has(x));
    if (fills) {
      chosen.push(t.app); pickedIds.add(t.app.id);
      [...t.tiers].forEach(x => need.delete(x));
    }
  }
  // Top up if we hit K before covering all families (rare): pick from
  // the remainder at random.
  for (const t of shuffled) {
    if (chosen.length >= K) break;
    if (!pickedIds.has(t.app.id)) {
      chosen.push(t.app); pickedIds.add(t.app.id);
    }
  }
  return chosen;
}

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === "class") e.className = v;
    else if (k === "html") e.innerHTML = v;
    else e.setAttribute(k, v);
  });
  children.flat().forEach(c => {
    if (c == null) return;
    e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  });
  return e;
}

function appHeader(app) {
  const initial = app.name[0].toUpperCase();
  return el("div", { class: "app-head" },
    el("div", { class: "app-icon" }, initial),
    el("div", {},
      el("div", { class: "app-name" }, app.name),
      el("div", { class: "app-dev" }, app.developer, " • ", app.installs, " installs • ★ ", String(app.rating)),
      el("div", { class: "app-meta" }, app.size_mb + " MB • " + app.tagline)
    )
  );
}

function labelRow(item) {
  const contested = !!item.boundary;
  const row = el("div", { class: "label-row" + (contested ? " contested" : "") },
    el("div", { class: "label-cat" }, item.category),
    el("div", { class: "label-tag" }, item.purposes.join(" • "))
  );
  if (contested) {
    row.appendChild(el("div", { class: "label-flag-chip" }, "boundary " + item.boundary));
  }
  return row;
}

function bleDrawer(item) {
  if (!item.boundary) return null;
  const c = COMMUNITY[item.boundary] || {};
  const drawer = el("div", { class: "ble-drawer" });
  drawer.appendChild(el("div", { class: "ble-head" },
    el("strong", {}, "Boundary applied: " + (c.name || item.boundary)),
    el("span", { class: "tier-pill tier-" + (item.tier || c.tier) }, item.tier || c.tier)
  ));
  drawer.appendChild(el("div", { class: "ble-rule" }, "“" + item.rule_clause + "”"));
  drawer.appendChild(el("div", { class: "ble-signal" },
    `Community: ${c.yes}% accept · ${c.maybe}% unsure · ${c.no}% disagree`));
  const btn = el("button", { class: "ble-toggle-btn" }, "▾ Show what this label would say if the rule did not apply");
  const counter = el("div", { class: "counter", style: "display:none" },
    "If the ‘" + (c.name || item.boundary) + "’ rule did not apply, the platform would have to declare this " +
    "as " + (item._kind === "collected" ? "collected" : "shared") + " in plain terms, with no exception.");
  btn.addEventListener("click", () => {
    const open = counter.style.display !== "none";
    counter.style.display = open ? "none" : "block";
    btn.textContent = (open ? "▾" : "▴") + " " + (open ? "Show" : "Hide") + " what this label would say if the rule did not apply";
    // record interaction
    log("toggle_" + (open ? "close" : "open"), { boundary: item.boundary, app: item._appId });
  });
  drawer.appendChild(btn);
  drawer.appendChild(counter);
  return drawer;
}

function renderApp(app, condition, mount) {
  mount.innerHTML = "";
  const card = el("div", { class: "app-card" });
  card.appendChild(appHeader(app));
  card.appendChild(el("div", { class: "app-desc" }, app.description));
  card.appendChild(el("button", { class: "install-btn" }, "Install"));

  // Collected
  card.appendChild(el("div", { class: "section-title" }, "Data this app may COLLECT"));
  app.collected.forEach(item => {
    item._appId = app.id;
    item._kind = "collected";
    card.appendChild(labelRow(item));
    if (condition === "ble") {
      const d = bleDrawer(item);
      if (d) card.appendChild(d);
    }
  });

  // Shared
  card.appendChild(el("div", { class: "section-title" }, "Data this app may SHARE with third parties"));
  app.shared.forEach(item => {
    item._appId = app.id;
    item._kind = "shared";
    card.appendChild(labelRow(item));
    if (condition === "ble") {
      const d = bleDrawer(item);
      if (d) card.appendChild(d);
    }
  });

  mount.appendChild(card);
}

// Lightweight interaction logger (would POST to a server in deployment)
const _log = [];
function log(event, payload = {}) {
  _log.push({ t: Date.now(), event, ...payload });
  // For pilot we just stash in localStorage
  try {
    localStorage.setItem("ble_log", JSON.stringify(_log));
  } catch (e) { /* ignore */ }
}
window.__bleLog = _log;

async function init() {
  const condition = getParam("condition", "ble");      // "current" | "ble"
  const pid       = getParam("pid", "");               // Prolific ID
  let   appId     = getParam("app", "");
  const K         = parseInt(getParam("k", "4"));

  document.body.classList.add("cond-" + condition);
  const condChip = document.querySelector("#condition-chip");
  if (condChip) condChip.textContent = condition === "ble" ? "BLE-enhanced" : "Current Data Safety";

  const pool = await loadApps();

  // Determine the selected app subset for THIS participant. If a pid is
  // provided we sample 4 apps stratified by typology family; otherwise
  // we show the full pool and let the operator pick one (preview mode).
  let participantApps = pool;
  if (pid) {
    participantApps = selectAppsForParticipant(pool, pid, K);
    log("participant_assigned", { pid, K, picked: participantApps.map(a => a.id) });
  }

  // Pick which one to render now.
  if (!appId) appId = participantApps[0].id;
  const app = participantApps.find(a => a.id === appId) || participantApps[0];
  log("view_app", { app: app.id, condition, pid });

  const mount = document.querySelector("#app-mount");
  renderApp(app, condition, mount);

  // Build the navigation buttons based on the participant subset.
  const navMount = document.querySelector("#nav-mount");
  if (navMount) {
    navMount.innerHTML = "";
    participantApps.forEach(a => {
      const b = document.createElement("button");
      b.textContent = a.name;
      b.classList.add(a.id === app.id ? "active" : "");
      b.addEventListener("click", () => {
        const u = new URL(location.href);
        u.searchParams.set("app", a.id);
        u.searchParams.set("condition", condition);
        if (pid) u.searchParams.set("pid", pid);
        location.href = u.toString();
      });
      navMount.appendChild(b);
    });
  }

  // Legacy data-jump support (used by the index page).
  document.querySelectorAll("[data-jump]").forEach(b => {
    b.addEventListener("click", () => {
      const next = b.getAttribute("data-jump");
      const u = new URL(location.href);
      u.searchParams.set("app", next);
      u.searchParams.set("condition", condition);
      if (pid) u.searchParams.set("pid", pid);
      location.href = u.toString();
    });
  });
}

window.addEventListener("DOMContentLoaded", init);
