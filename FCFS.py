from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve the HTML file
@app.route("/")
def index():
    with open('index.html', 'r') as file:
        return file.read()

@app.route("/fcfs", methods=["POST"])
def fcfs():
    try:
        data = request.json
        arrival = data["arrival"]
        burst = data["burst"]
        
        print(f"Received data: arrival={arrival}, burst={burst}")
        
        n = len(burst)
        
        # Create processes with their indices
        processes = []
        for i in range(n):
            processes.append({
                'id': i + 1,
                'arrival': arrival[i],
                'burst': burst[i]
            })
        
        print("Process     Arrival Time     Burst Time")
        for i, process in enumerate(processes):
            print(f"Process {process['id']}:   {process['arrival']}   {process['burst']}")
        
        # Sort processes by arrival time (FCFS)
        processes.sort(key=lambda x: x['arrival'])
        
        # Calculate completion times and Gantt chart
        gantt = [0]
        process_order = []
        current_time = 0
        waiting_times = []
        turnaround_times = []
        
        for process in processes:
            # If current time is less than arrival time, CPU is idle
            if current_time < process['arrival']:
                current_time = process['arrival']
            
            # Process starts execution
            process_order.append(f"P{process['id']}")
            current_time += process['burst']
            gantt.append(current_time)
            
            # Calculate times
            completion_time = current_time
            turnaround_time = completion_time - process['arrival']
            waiting_time = turnaround_time - process['burst']
            
            waiting_times.append(waiting_time)
            turnaround_times.append(turnaround_time)
            
            print(f"Process {process['id']}: WT={waiting_time}, TAT={turnaround_time}")
        
        avg_wt = sum(waiting_times) / n
        avg_tat = sum(turnaround_times) / n
        
        print("Gantt chart:", gantt)
        print(f"Average Waiting Time: {avg_wt}")
        print(f"Average Turnaround Time: {avg_tat}")
        
        return jsonify({
            "gantt": gantt,
            "process_order": process_order,
            "avg_wt": avg_wt,
            "avg_tat": avg_tat
        })
        
    except Exception as e:
        print(f"Error in fcfs route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    print("Server will run on: http://127.0.0.1:5000")
    print("Available routes:")
    print("  GET  / (serves index.html)")
    print("  POST /fcfs (FCFS calculation)")
    app.run(debug=True, host='127.0.0.1', port=5000)