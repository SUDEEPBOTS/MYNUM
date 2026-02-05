async function checkNumber() {
    const numInput = document.getElementById("phoneInput");
    const num = numInput.value.trim();
    const loader = document.getElementById("loader");
    const resultBox = document.getElementById("resultBox");
    const errorBox = document.getElementById("errorBox");
    const outputGrid = document.getElementById("outputGrid");
    const searchBtn = document.getElementById("searchBtn");

    // Reset UI
    resultBox.classList.add("hidden");
    errorBox.classList.add("hidden");
    errorBox.innerText = "";
    
    if (!num) {
        showError("Please enter a valid phone number.");
        return;
    }

    // UI Loading State
    loader.classList.remove("hidden");
    searchBtn.disabled = true;
    searchBtn.style.opacity = "0.7";

    try {
        // Fetch API
        const res = await fetch(`/api/lookup?number=${encodeURIComponent(num)}`);
        const data = await res.json();

        if (data.status === "success") {
            // Build Grid HTML
            let html = "";
            for (const [key, value] of Object.entries(data.data)) {
                html += `
                <div class="data-row">
                    <span class="label">${key}</span>
                    <span class="value">${value || "N/A"}</span>
                </div>`;
            }
            outputGrid.innerHTML = html;
            resultBox.classList.remove("hidden");
        } else {
            showError(data.message || "Invalid Number");
        }

    } catch (err) {
        showError("Server Connection Failed.");
    } finally {
        // Stop Loading
        loader.classList.add("hidden");
        searchBtn.disabled = false;
        searchBtn.style.opacity = "1";
    }
}

function showError(msg) {
    const errorBox = document.getElementById("errorBox");
    errorBox.innerText = msg;
    errorBox.classList.remove("hidden");
}

async function pasteNum() {
    try {
        const text = await navigator.clipboard.readText();
        document.getElementById("phoneInput").value = text;
    } catch (err) {
        alert("Permission needed to paste.");
    }
}

function copyResult() {
    const rows = document.querySelectorAll(".data-row");
    let text = "--- Phone Report ---\n";
    rows.forEach(row => {
        const label = row.querySelector(".label").innerText;
        const value = row.querySelector(".value").innerText;
        text += `${label}: ${value}\n`;
    });
    
    navigator.clipboard.writeText(text);
    
    // Change Button Text Temporarily
    const btn = document.querySelector(".copy-btn");
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="ph ph-check"></i> Copied';
    setTimeout(() => { btn.innerHTML = original; }, 2000);
}

// Enter Key Support
document.getElementById("phoneInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        checkNumber();
    }
});
