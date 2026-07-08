/* Trust survey (TPA-derived 5-item 7-point Likert), shown after the C2 block.
 * Item t3 is reverse-scored on the server. */

const TRUST_ITEMS = [
  ["t1_reliable",   "The AI suggestions were reliable."],
  ["t2_evidence",   "The highlighted evidence helped me verify the suggested label."],
  ["t3_overrely",   "I sometimes accepted the AI suggestion without checking. (reverse-scored)"],
  ["t4_intent",     "I would use this AI assistant for real privacy reviews."],
  ["t5_understand", "I understood why the AI made its suggestions."],
];

window.runTrust = function() {
  return new Promise(resolve => {
    const root = document.createElement("div");
    root.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;z-index:1000;";
    const card = document.createElement("div");
    card.className = "card";
    card.style.cssText = "max-width:720px;width:90%;";
    card.innerHTML = `<h1>Trust in the AI assistant</h1>
       <p>Please rate each statement (1 = strongly disagree, 7 = strongly agree).</p>`;
    TRUST_ITEMS.forEach(([key, label]) => {
      const fs = document.createElement("fieldset");
      const buttons = [1,2,3,4,5,6,7].map(v =>
        `<label><input type="radio" name="${key}" value="${v}" required> ${v}</label>`
      ).join(" ");
      fs.innerHTML = `<legend>${label}</legend>${buttons}`;
      card.appendChild(fs);
    });
    const btn = document.createElement("button");
    btn.textContent = "Submit and continue";
    card.appendChild(btn);
    root.appendChild(card);
    document.body.appendChild(root);

    btn.addEventListener("click", async () => {
      const payload = {pid: PID};
      for (const [k] of TRUST_ITEMS) {
        const sel = card.querySelector(`input[name=${k}]:checked`);
        payload[k] = sel ? +sel.value : null;
      }
      await fetch("/api/submit_trust", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify(payload),
      });
      root.remove();
      resolve();
    });
  });
};
