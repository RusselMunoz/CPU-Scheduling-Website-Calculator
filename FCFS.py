from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/fcsfs", methods=["POST"])
def fcfs():
    data = request.json
    arr = data["arrival"]
    burst = data["burst"]

    process = []
    process.append([arr, burst])

    print("Process     Arrival Time     Burst Time")
    for i in range(len(arr)):
        print(f"Process {i+1}:   {arr[i]}   {burst[i]}")

    print("Process List:", process)

    sorted_burst = sorted(burst)
    gantt = []
    total = 0

    for b in sorted_burst:
        gantt.append(total)
        total += b

    print("Gantt chart:", *gantt)
    print("Waiting Time:", sum(gantt[:-1]) / len(burst))
    print("Turnaround Time:", sum(gantt) / len(burst))

    return jsonify({
        "gantt": gantt,
        "avg_wt": sum(gantt[:-1]) / len(burst),
        "avg_tat": sum(gantt) / len(burst)
    })


if __name__ == "__main__":
    app.run(debug=True)
