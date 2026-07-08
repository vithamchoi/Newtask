/* C0 -- raw review: structured Data Safety screenshot-style + full policy text. */

window.renderC0 = function(stim, root) {
  root.innerHTML = "";
  const ds = document.createElement("div");
  ds.className = "panel panel-ds";
  ds.innerHTML = `<h3>Data Safety panel</h3>` + renderDataSafety(stim.data_safety);
  root.appendChild(ds);

  const pp = document.createElement("div");
  pp.className = "panel panel-pp";
  pp.innerHTML = `<h3>Privacy policy (full text)</h3>` +
                 `<div class="policy">${escapeHtml(stim.policy_text || "")}</div>`;
  root.appendChild(pp);

  window.__c2_accepted = null;
  window.__c2_overridden_axes = null;
};

function renderDataSafety(ds) {
  if (!ds || typeof ds !== "object") return "<i>No structured data.</i>";
  const block = (title, rows) => {
    if (!rows || !rows.length) return `<div class="ds-section"><h4>${title}</h4><i>(no entries)</i></div>`;
    const items = rows.map(r => {
      const types = (r.sub_info || []).map(s => s.data_type).join(", ");
      return `<div class="ds-section">
                <h4>${escapeHtml(r.category || "")}</h4>
                <div class="ds-types">${escapeHtml(types) || "—"}</div>
              </div>`;
    }).join("");
    return `<div><b>${title}</b>${items}</div>`;
  };
  return block("Data shared", ds.data_shared) +
         block("Data collected", ds.data_collected) +
         block("Security practices", ds.security_practices);
}

function escapeHtml(s) {
  return (s || "").replace(/[&<>"']/g, c =>
    ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
