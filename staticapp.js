async function run() {
  const text = document.getElementById("input").value;

  if (!text.trim()) {
    document.getElementById("output").innerText = "";
    return;
  }

  try {
    const response = await fetch(
      `/autocorrect?text=${encodeURIComponent(text)}`
    );
    const data = await response.json();

    document.getElementById("output").innerText = data.result;
  } catch (err) {
    document.getElementById("output").innerText =
      "Error: backend not responding";
  }
}

function toggle() {
  document.body.classList.toggle("dark");
}
