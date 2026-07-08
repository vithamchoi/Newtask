global.fetch = () => Promise.reject(new TypeError("Failed to fetch"));
global.window = {};
require("./apps_data.js");
require("./mcq_data.js");

async function loadResources() {
  try {
    const [appsRes, mcqRes] = await Promise.all([
      fetch("apps.json"),
      fetch("mcq_bank.json"),
    ]);
    if (!appsRes.ok || !mcqRes.ok) throw new Error("fetch returned non-OK");
    return { apps: await appsRes.json(), mcq: await mcqRes.json() };
  } catch (e) {
    if (window.__APPS_FALLBACK && window.__MCQ_FALLBACK) {
      console.warn("[study] fetch unavailable. Using inline fallback.");
      return { apps: window.__APPS_FALLBACK, mcq: window.__MCQ_FALLBACK };
    }
    throw e;
  }
}
loadResources().then(r => {
  console.log("✓ Fallback path works");
  console.log(`  ${r.apps.length} apps loaded (first: ${r.apps[0].name})`);
  console.log(`  ${Object.keys(r.mcq).filter(k => !k.startsWith('_')).length} MCQ templates loaded`);
  console.log(`  Sample b3 label: ${r.mcq.b3.label}`);
}).catch(err => {
  console.log("✗ FAILED:", err.message);
  process.exit(1);
});
