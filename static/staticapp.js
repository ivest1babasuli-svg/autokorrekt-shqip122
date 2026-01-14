async function korrigjo() {
  const text = document.getElementById("input").value;

  // Clear previous results
  document.getElementById("output").innerText = "";
  document.getElementById("corrections-list").innerHTML = '';
  document.getElementById("improvements-list").innerHTML = '';

  // Make the request to the backend with cache-busting
  const res = await fetch(`/autocorrect?text=${encodeURIComponent(text)}&t=${new Date().getTime()}`);
  const data = await res.json();

  // Display the corrected text
  document.getElementById("output").innerText = data.result;

  // Display the corrections
  const correctionsList = document.getElementById("corrections-list");
  data.corrections.forEach(correction => {
    const li = document.createElement("li");
    li.innerText = `${correction.old} → ${correction.new}`;
    correctionsList.appendChild(li);
  });

  // Display improvements
  const improvementsList = document.getElementById("improvements-list");
  data.improvements.forEach(improvement => {
    const li = document.createElement("li");
    li.innerText = improvement;
    improvementsList.appendChild(li);
  });
}
