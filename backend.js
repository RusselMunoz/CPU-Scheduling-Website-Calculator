async function calculate() {
    const burst = document.getElementById("BurstTime").value.split(" ").map(Number);

    const response = await fetch("/fcfs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ burst })
    });
    
    const result = await response.json();
    document.getElementById("output").textContent =
    "Gantt: " + result.gantt.join(" ") + "\n" +
    "Average WT: " + result.avg_wt;
    }