from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# ---------------- FCFS ----------------
def fcfs(tasks):
    current_time = 0
    result = []

    for task in tasks:
        waiting_time = current_time
        turnaround_time = waiting_time + task["burst"]

        result.append({
            "id": task["id"],
            "location": task["location"],
            "priority": task["priority"],
            "burst": task["burst"],
            "waiting": waiting_time,
            "turnaround": turnaround_time
        })

        current_time += task["burst"]

    return result


# ---------------- SJF ----------------
def sjf(tasks):
    sorted_tasks = sorted(tasks, key=lambda x: x["burst"])
    return fcfs(sorted_tasks)


# ---------------- Priority ----------------
def priority_scheduling(tasks):
    # Lower number = higher priority
    sorted_tasks = sorted(tasks, key=lambda x: x["priority"])
    return fcfs(sorted_tasks)


# ---------------- Vehicle Allocation ----------------
def allocate_vehicles(tasks, vehicles):
    allocations = []

    for i, task in enumerate(tasks):

        if i < len(vehicles):
            allocations.append({
                "task_id": task["id"],
                "location": task["location"],
                "vehicle": vehicles[i],
                "status": "Assigned"
            })
        else:
            allocations.append({
                "task_id": task["id"],
                "location": task["location"],
                "vehicle": "None",
                "status": "Waiting"
            })

    return allocations


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/schedule", methods=["POST"])
def schedule():

    data = request.get_json()

    tasks = data["tasks"]
    algorithm = data["algorithm"]

    if algorithm == "FCFS":
        result = fcfs(tasks)

    elif algorithm == "SJF":
        result = sjf(tasks)

    elif algorithm == "Priority":
        result = priority_scheduling(tasks)

    else:
        result = []

    return jsonify(result)


@app.route("/allocate", methods=["POST"])
def allocate():

    data = request.get_json()

    tasks = data["tasks"]
    vehicles = data["vehicles"]

    result = allocate_vehicles(tasks, vehicles)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
