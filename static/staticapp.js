async function korrigjo() {
  const text = document.getElementById("input").value;

  // Clear previous results
  document.getElementById("output").innerText = "";
  document.getElementById("corrections-list").innerHTML = "";
  document.getElementById("improvements-list").innerHTML = "";

  try {
    // Make the request to the backend with cache-busting
    const res = await fetch(`/autocorrect?text=${encodeURIComponent(text)}&t=${new Date().getTime()}`);
    if (!res.ok) {
      document.getElementById("output").innerText = `Error: ${res.status} ${res.statusText}`;
      return;
    }
    const data = await res.json();

    // Display the corrected text
    document.getElementById("output").innerText = data.result || "";

    // Display the corrections (if any) — guard against undefined
    const correctionsList = document.getElementById("corrections-list");
    (data.corrections || []).forEach(correction => {
      const li = document.createElement("li");
      li.innerText = `${correction.old} → ${correction.new}`;
      correctionsList.appendChild(li);
    });

    // Display improvements (if any)
    const improvementsList = document.getElementById("improvements-list");
    (data.improvements || []).forEach(improvement => {
      const li = document.createElement("li");
      li.innerText = improvement;
      improvementsList.appendChild(li);
    });
  } catch (err) {
    console.error(err);
    document.getElementById("output").innerText = "Network or parsing error — see console for details";
  }
}

// Theme toggle: toggles 'dark' class on body and saves preference
function toggleTheme() {
  const body = document.body;
  const isDark = body.classList.toggle("dark");
  localStorage.setItem("theme", isDark ? "dark" : "light");
  updateThemeButton();
}

function updateThemeButton() {
  const btn = document.getElementById("themeBtn");
  if (!btn) return;
  btn.innerText = document.body.classList.contains("dark") ? "☀️" : "🌙";
}

// On load, wire events and apply saved theme
document.addEventListener("DOMContentLoaded", () => {
  // Apply saved theme
  const saved = localStorage.getItem("theme");
  if (saved === "dark") document.body.classList.add("dark");

  // Wire buttons
  const btn = document.getElementById("korrigjoBtn");
  if (btn) btn.addEventListener("click", korrigjo);

  const themeBtn = document.getElementById("themeBtn");
  if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

  updateThemeButton();
});
