/* NASA-TLX block survey, shown between condition blocks.
 * Standard 6 sub-scales, 0-100 sliders. Unweighted mean reported as global.
 */

const TLX_ITEMS = [
  ["mental",      "Mental demand", "How mentally demanding was the task?"],
  ["physical",    "Physical demand", "How physically demanding was the task?"],
  ["temporal",    "Temporal demand", "How hurried or rushed was the pace?"],
  ["performance", "Performance",     "How successful were you in your task?"],
  ["effort",      "Effort",          "How hard did you have to work?"],
  ["frustration", "Frustration",     "How insecure, discouraged, irritated, or stressed were you?"],
];

window.runTLX = function(condition) {
  return new Promise(resolve => {
    const root = document.createElement("div");
    root.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;z-index:1000;";
    const card = document.createElement("div");
    card.className = "card";
    card.style.cssText = "max-width:720px;width:90%;";
    card.innerHTML = `<h1>NASA-TLX — after ${condition}</h1>
      <p>Rate the task you just completed in this block.</p>`;
    const grid = document.createElement("div");
    grid.className = "tlx-grid";
    TLX_ITEMS.forEach(([key, label, desc]) => {
      grid.insertAdjacentHTML("beforeend",
        `<label title="${desc}"><b>${label}</b><br><small>${desc}</small></label>
         <input type="range" name="${key}" min="0" max="100" value="50"
                oninput="this.nextElementSibling.textContent=this.value">
         <output>50</output>`);
    });
    card.appendChild(grid);
    const btn = document.createElement("button");
    btn.textContent = "Submit and continue";
    btn.style.marginTop = "14px";
    card.appendChild(btn);
    root.appendChild(card);
    document.body.appendChild(root);

    btn.addEventListener("click", async () => {
      const payload = {pid: PID, condition};
      TLX_ITEMS.forEach(([k]) =>
        payload[k] = +grid.querySelector(`input[name=${k}]`).value);
      await fetch("/api/submit_tlx", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      });
      root.remove();
      resolve();
    });
  });
};
