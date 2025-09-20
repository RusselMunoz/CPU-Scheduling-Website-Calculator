async function calculate() {
    const arrivalInput = document.getElementById("ArrivalTime").value.trim();
    const burstInput = document.getElementById("BurstTime").value.trim();
    
    // Validate inputs
    if (!arrivalInput || !burstInput) {
        document.getElementById("output").textContent = "Please enter both arrival times and burst times.";
        return;
    }
    
    try {
        // Convert space-separated strings to arrays of numbers
        const arrival = arrivalInput.split(" ").map(Number);
        const burst = burstInput.split(" ").map(Number);
        
        // Validate that arrays have same length and contain valid numbers
        if (arrival.length !== burst.length) {
            document.getElementById("output").textContent = "Number of arrival times must match number of burst times.";
            return;
        }
        
        if (arrival.some(isNaN) || burst.some(isNaN)) {
            document.getElementById("output").textContent = "Please enter valid numbers only.";
            return;
        }
        
        // Send request to backend
        console.log("Sending data:", { arrival, burst });
        const response = await fetch("http://127.0.0.1:5000/fcfs", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({ 
                arrival: arrival,  // Now sending both arrival and burst
                burst: burst 
            })
        });
        
        // Check if the response is OK (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        // Parse the JSON response
        const result = await response.json();
        
        // Update the output
        const outputElement = document.getElementById("output");
        if (outputElement) {
            outputElement.innerHTML = 
                "<h3>Results:</h3>" +
                "<p><strong>Gantt Chart:</strong> " + result.gantt.join(" | ") + "</p>" +
                "<p><strong>Process Order:</strong> " + (result.process_order ? result.process_order.join(" → ") : "N/A") + "</p>" +
                "<p><strong>Average Waiting Time:</strong> " + result.avg_wt.toFixed(2) + "</p>" +
                "<p><strong>Average Turnaround Time:</strong> " + result.avg_tat.toFixed(2) + "</p>";
        } else {
            console.error("Output element not found.");
        }
    } catch (error) {
        console.error("Error during calculation:", error);
        const outputElement = document.getElementById("output");
        if (outputElement) {
            outputElement.textContent = "Error: " + error.message + ". Make sure your Flask server is running on the correct port.";
        }
    }
}