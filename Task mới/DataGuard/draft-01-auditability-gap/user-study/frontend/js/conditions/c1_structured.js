/* C1 -- structured side-by-side: structured Data Safety + extracted policy
 * sections (Data Share, Data Collect). No AI assistance. */

window.renderC1 = function(stim, root) {
  root.innerHTML = "";
  const ds = document.createElement("div");
  ds.className = "panel panel-ds";
  ds.innerHTML = `<h3>Structured Data Safety</h3>` + renderDataSafety(stim.data_safety);
  root.appendChild(ds);

  const pp = document.createElement("div");
  pp.className = "panel panel-pp";
  pp.innerHTML = `<h3>Policy evidence (extracted)</h3>`
               + `<div class="ds-section"><h4>Data Share section</h4>
                    <div class="policy">${escapeHtml(stim.section_share || "(empty)")}</div></div>`
               + `<div class="ds-section"><h4>Data Collect section</h4>
                    <div class="policy">${escapeHtml(stim.section_collect || "(empty)")}</div></div>`
               + `<details><summary>Show full policy</summary>
                    <div class="policy">${escapeHtml(stim.policy_text || "")}</div>
                  </details>`;
  root.appendChild(pp);

  window.__c2_accepted = null;
  window.__c2_overridden_axes = null;
};
