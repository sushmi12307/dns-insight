
const $ = (id) => document.getElementById(id);

const form = $("lookupForm");
const domainInput = $("domain");
const recordTypeInput = $("recordType");
const resolveBtn = $("resolveBtn");

let totalLatency = [];
let queryLabels = [];

const latencyChart = new Chart($("latencyChart"), {
    type: "line",
    data: {
        labels: queryLabels,
        datasets: [{
            label: "Lookup latency (ms)",
            data: totalLatency,
            borderColor: "#60a5fa",
            backgroundColor: "#60a5fa25",
            fill: true,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

const cacheChart = new Chart($("cacheChart"), {
    type: "doughnut",
    data: {
        labels: ["Cache hits", "Cache misses"],
        datasets: [{
            data: [0, 0],
            backgroundColor: ["#34d399", "#f59e0b"]
        }]
    },
    options: {
        responsive: true
    }
});

async function api(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || data.error || "Request failed.");
    }

    return data;
}

function showMessage(message) {
    $("message").textContent = message;
}

async function refreshStats() {
    try {
        const stats = await api("/api/stats");

        $("hits").textContent = stats.hits;
        $("misses").textContent = stats.misses;
        $("hitRatio").textContent = `${stats.hit_ratio}%`;

        cacheChart.data.datasets[0].data = [
            stats.hits,
            stats.misses
        ];
        cacheChart.update();
    } catch (error) {
        console.error("Statistics error:", error);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const domain = domainInput.value.trim();
    const recordType = recordTypeInput.value.split(" ")[0];

    if (!domain) {
        showMessage("Please enter a domain name.");
        return;
    }

    resolveBtn.disabled = true;
    showMessage("Resolving DNS...");
    $("resultArea").hidden = true;

    try {
        const data = await api(
            `/api/lookup?domain=${encodeURIComponent(domain)}&type=${recordType}`
        );

        $("latency").textContent =
            data.latency_ms !== undefined
                ? `${data.latency_ms} ms`
                : "-- ms";

        if (data.latency_ms !== undefined) {
            queryLabels.push(`${queryLabels.length + 1}`);
            totalLatency.push(data.latency_ms);

            if (queryLabels.length > 15) {
                queryLabels.shift();
                totalLatency.shift();
            }

            latencyChart.update();
        }

        const body = $("recordsBody");
        body.replaceChildren();

        if (data.records && data.records.length > 0) {
            data.records.forEach((record) => {
                const row = document.createElement("tr");

                [
                    data.domain || domain,
                    data.record_type || recordType,
                    record,
                    data.ttl ?? "N/A"
                ].forEach((value) => {
                    const cell = document.createElement("td");
                    cell.textContent = String(value);
                    row.appendChild(cell);
                });

                body.appendChild(row);
            });
        } else {
            const row = document.createElement("tr");
            const cell = document.createElement("td");

            cell.colSpan = 4;
            cell.textContent = "No records returned.";
            row.appendChild(cell);
            body.appendChild(row);
        }

        $("resultArea").hidden = false;
        $("diagnosis").textContent =
            data.diagnosis || data.message || data.status;

        showMessage(
            data.status === "success"
                ? "DNS lookup completed successfully."
                : `DNS lookup result: ${data.status}`
        );

        await refreshStats();
    } catch (error) {
        showMessage(`Error: ${error.message}`);
    } finally {
        resolveBtn.disabled = false;
    }
});

$("traceBtn").addEventListener("click", async () => {
    const domain = domainInput.value.trim();

    if (!domain) {
        $("traceMessage").textContent =
            "Enter a domain before playing the trace.";
        return;
    }

    const button = $("traceBtn");
    button.disabled = true;

    try {
        const data = await api(
            `/api/trace?domain=${encodeURIComponent(domain)}`
        );

        const nodes = [...$("traceList").children];

        nodes.forEach((node) => node.classList.remove("active"));

        for (let i = 0; i < data.stages.length; i++) {
            nodes.forEach((node) => node.classList.remove("active"));
            nodes[i].classList.add("active");

            $("traceMessage").textContent =
                `${data.stages[i].stage}: ${data.stages[i].message}`;

            await new Promise((resolve) => setTimeout(resolve, 900));
        }

        $("traceMessage").textContent =
            "Educational trace complete. Stages are simulated.";
    } catch (error) {
        $("traceMessage").textContent = error.message;
    } finally {
        button.disabled = false;
    }
});

$("clearCacheBtn").addEventListener("click", async () => {
    try {
        const result = await api("/api/cache/clear", {
            method: "POST"
        });

        showMessage(result.message);
        await refreshStats();
    } catch (error) {
        showMessage(`Error: ${error.message}`);
    }
});

refreshStats();
