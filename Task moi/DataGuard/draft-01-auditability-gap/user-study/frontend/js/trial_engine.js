/* Trial engine: fetch next trial, dispatch to the right condition renderer,
 * collect responses, post them back. Also drives the TLX modal after each
 * condition block and the TPA trust survey after C2. */

const PID = sessionStorage.getItem("pid");
const ORDER = (sessionStorage.getItem("condition_order") || "").split(",");
const SESSION_TOTAL = Number(sessionStorage.getItem("n_trials") || 0);
let CURRENT_TRIAL = null;
let LAST_CONDITION = null;

const renderers = {
  C0: window.renderC0,
  C1: window.renderC1,
  C2: window.renderC2,
};

async function nextTrial() {
  const r = await fetch(`/api/next_trial?pid=${PID}`);
  const data = await r.json();
  if (data.done) return finishOrTransition();

  CURRENT_TRIAL = data;
  const total = data.n_trials || SESSION_TOTAL || 1;
  document.getElementById("trial-order").textContent = data.trial_order;
  document.getElementById("trial-total").textContent = total;
  document.getElementById("cond").textContent = data.condition;
  document.getElementById("prog").max = total;
  document.getElementById("prog").value = data.trial_order - 1;

  const s = data.stimulus;
  document.getElementById("app-name").textContent = s.app_name || s.app_id;
  document.getElementById("app-cat").textContent = s.category || "";
  document.getElementById("play-link").href = s.play_url || "#";
  document.getElementById("policy-link").href = s.policy_url || "#";

  resetForm();
  detectBlockTransition(data.condition);
  renderers[data.condition](s, document.getElementById("panels"));
}

function resetForm() {
  document.querySelectorAll('input[type=radio]').forEach(r => r.checked = false);
  document.querySelectorAll('input[type=range]').forEach(r => {
    r.value = 50; r.nextElementSibling.textContent = 50;
  });
  document.querySelectorAll('textarea').forEach(t => t.value = "");
}

async function detectBlockTransition(cond) {
  if (LAST_CONDITION && LAST_CONDITION !== cond) {
    // We just finished a block under LAST_CONDITION.
    await runTLX(LAST_CONDITION);
    if (LAST_CONDITION === "C2") await runTrust();
  }
  LAST_CONDITION = cond;
}

async function submitTrial() {
  const required = ["j_share_corr", "j_share_comp", "j_coll_corr", "j_coll_comp"];
  const missing = required.filter(name => !document.querySelector(`input[name=${name}]:checked`));
  if (missing.length) {
    alert("Please choose a verdict for all four judgment axes before continuing.");
    return;
  }
  const f = new FormData();
  document.querySelectorAll('input[type=radio]:checked, input[type=range], textarea')
    .forEach(el => f.append(el.name, el.value));
  const payload = Object.fromEntries(f.entries());
  payload.trial_id = CURRENT_TRIAL.trial_id;
  payload.pid = PID;
  if (CURRENT_TRIAL.condition === "C2") {
    payload.ai_suggestion_accepted = window.__c2_accepted ?? null;
    payload.ai_overridden_axes = window.__c2_overridden_axes ?? null;
  }
  const r = await fetch("/api/submit_trial", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload),
  });
  if (!r.ok) { alert("Could not submit. Please retry."); return; }
  nextTrial();
}

async function finishOrTransition() {
  if (LAST_CONDITION) {
    await runTLX(LAST_CONDITION);
    if (LAST_CONDITION === "C2") await runTrust();
  }
  await fetch("/api/finish", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({pid: PID}),
  });
  location.href = "/done.html";
}

document.getElementById("submit").addEventListener("click", submitTrial);
nextTrial();
