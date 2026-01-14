async function korrigjo() {
  const text = document.getElementById("input").value;
  
  // Bëjmë cache busting duke shtuar një parameter të ri me timestamp
  const res = await fetch(`/autocorrect?text=${encodeURIComponent(text)}&t=${new Date().getTime()}`);
  const data = await res.json();
  
  document.getElementById("output").innerText = data.result;
}
