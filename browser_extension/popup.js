let currentUrl = "";

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  if (tabs.length > 0) {
    currentUrl = tabs[0].url || "";
    document.getElementById("urlText").textContent = currentUrl;
  } else {
    document.getElementById("urlText").textContent = "Could not get tab URL.";
  }
});

document.getElementById("checkBtn").addEventListener("click", async function () {
  const resultBox = document.getElementById("resultBox");
  resultBox.style.display = "none";
  resultBox.className = "result";

  if (!currentUrl) {
    resultBox.style.display = "block";
    resultBox.classList.add("error");
    resultBox.innerHTML = `
      <div class="title">Input Error</div>
      <div class="small">No URL found for the current tab.</div>
    `;
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: currentUrl })
    });

    const data = await response.json();

    resultBox.style.display = "block";

    let title = "";
    let message = "";

    if (data.result === "Phishing Website") {
      resultBox.classList.add("phishing");
      title = "⚠ Phishing Website";
      message = "This page appears highly suspicious. Do not enter sensitive information.";
    } else if (data.result === "Suspicious Website") {
      resultBox.classList.add("suspicious");
      title = "⚠ Suspicious Website";
      message = "This page may not be safe. Verify carefully before continuing.";
    } else {
      resultBox.classList.add("safe");
      title = "✅ Legitimate Website";
      message = "This page appears safe based on the current analysis.";
    }

    resultBox.innerHTML = `
      <div class="title">${title}</div>
      <div class="small">${message}</div>
      <div class="small"><strong>Probability:</strong> ${data.phishing_probability}</div>
    `;
  } catch (error) {
    resultBox.style.display = "block";
    resultBox.classList.add("error");
    resultBox.innerHTML = `
      <div class="title">Connection Error</div>
      <div class="small">Could not connect to local API. Make sure Flask server is running.</div>
    `;
  }
});