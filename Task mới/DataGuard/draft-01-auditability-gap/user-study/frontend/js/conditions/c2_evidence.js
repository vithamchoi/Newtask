/* C2 -- evidence-grounded AI: C1 plus highlighted candidate evidence and
 * an AI-suggested judgment per axis with an uncertainty band.
 *
 * Critical UX rule: the AI suggestion is shown BUT the participant must click
 * the highlight to expand the supporting evidence before the form
 * locks in the suggested radio button. This implements R1 (evidence-first)
 * at the interface level. */

window.renderC2 = function(stim, root) {
  root.innerHTML = "";

  // Left panel: structured Data Safety (same as C1)
  const ds = document.createElement("div");
  ds.className = "panel panel-ds";
  ds.innerHTML = `<h3>Structured Data Safety</h3>` + renderDataSafety(stim.data_safety);
  root.appendChild(ds);

  // Right panel: extracted policy with highlights for evidence spans
  const pp = document.createElement("div");
  pp.className = "panel panel-pp";
  let shareTxt = stim.section_share || "";
  let collectTxt = stim.section_collect || "";
  for (const span of (stim.evidence_share || [])) shareTxt = highlight(shareTxt, span);
  for (const span of (stim.evidence_collect || [])) collectTxt = highlight(collectTxt, span);

  const aiSug = stim.ai_suggestion || {};
  pp.innerHTML = `<h3>Policy evidence with AI highlights</h3>`
               + sectionWithSug("Data Share section",   shareTxt,   aiSug, ["share_corr","share_comp"])
               + sectionWithSug("Data Collect section", collectTxt, aiSug, ["coll_corr","coll_comp"])
               + `<details><summary>Show full policy</summary>
                    <div class="policy">${escapeHtml(stim.policy_text || "")}</div>
                  </details>`;
  root.appendChild(pp);

  // Wire the "Accept AI" buttons -- but require an evidence click first
  pp.querySelectorAll(".accept-ai").forEach(btn => {
    const axis = btn.dataset.axis;
    btn.disabled = true;
    btn.title = "Click the highlighted evidence first";
    const span = pp.querySelector(`mark[data-axis-${axis}]`);
    if (span) {
      span.addEventListener("click", () => { btn.disabled = false; btn.title = "Accept this AI suggestion"; });
    }
    btn.addEventListener("click", () => {
      const value = aiSug[axis]?.label;
      const radio = document.querySelector(`input[name="j_${axis}"][value="${value}"]`);
      if (radio) radio.checked = true;
      window.__c2_accepted = 1;
      btn.textContent = "Accepted";
      btn.disabled = true;
    });
  });

  // Track whether the participant overrides any suggested radio
  let overridden = 0;
  document.querySelectorAll('input[type=radio]').forEach(r => {
    r.addEventListener("change", () => {
      const axis = r.name.replace("j_", "");
      const suggested = aiSug[axis]?.label;
      if (suggested && r.value !== suggested) overridden++;
      window.__c2_overridden_axes = overridden;
    });
  });
  window.__c2_accepted = 0;
  window.__c2_overridden_axes = 0;
};

function highlight(text, span) {
  if (!text || !span?.match) return text;
  const idx = text.indexOf(span.match);
  if (idx < 0) return text;
  const before = text.slice(0, idx);
  const hit    = text.slice(idx, idx + span.match.length);
  const after  = text.slice(idx + span.match.length);
  return escapeHtml(before)
       + `<mark class="evidence" data-axis-${span.axis} title="evidence for ${span.axis}">${escapeHtml(hit)}</mark>`
       + escapeHtml(after);
}

function sectionWithSug(title, htmlText, ai, axes) {
  const sugs = axes.map(a => {
    const s = ai[a];
    if (!s) return "";
    const uncertain = (s.uncertainty ?? 0) > 0.4;
    return `<div><span class="axis">${a}:</span>
              suggested <b>${escapeHtml(s.label)}</b>
              <span class="uncert">uncertainty ${(s.uncertainty ?? 0).toFixed(2)}${uncertain ? " ⚠" : ""}</span>
              <button type="button" class="accept-ai" data-axis="${a}">Accept</button>
            </div>`;
  }).join("");
  return `<div class="ds-section">
            <h4>${title}</h4>
            <div class="policy">${htmlText}</div>
            <div class="ai-suggest">${sugs}</div>
          </div>`;
}
