from flask import Flask, render_template, request, jsonify
import heapq

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
    available_vehicles = list(vehicles)

    for task in tasks:
        best_vehicle = None
        shortest_distance = float("inf")

        for vehicle in available_vehicles:
            # Vehicle locations will be supplied in the next step.
            if isinstance(vehicle, dict):
                vehicle_name = vehicle.get("name")
                vehicle_location = vehicle.get("location")
            else:
                # Backward compatibility with the existing API.
                vehicle_name = vehicle
                vehicle_location = None

            if not vehicle_location:
                continue

            route = dijkstra(
                ROAD_GRAPH,
                vehicle_location,
                task["location"]
            )

            if route and route["total_distance"] < shortest_distance:
                shortest_distance = route["total_distance"]
                best_vehicle = vehicle_name

        if best_vehicle is not None:
            allocations.append({
                "task_id": task["id"],
                "location": task["location"],
                "vehicle": best_vehicle,
                "status": "Assigned",
                "distance": shortest_distance
            })
            available_vehicles = [
                v for v in available_vehicles
                if (v.get("name") if isinstance(v, dict) else v)
                != best_vehicle
            ]
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
        return jsonify({"error": "Invalid scheduling algorithm"}), 400

    total_waiting = sum(task["waiting"] for task in result)
    total_turnaround = sum(task["turnaround"] for task in result)

    count = len(result)

    average_waiting = (
        total_waiting / count if count > 0 else 0
    )

    average_turnaround = (
        total_turnaround / count if count > 0 else 0
    )

    return jsonify({
        "results": result,
        "average_waiting_time": round(average_waiting, 2),
        "average_turnaround_time": round(average_turnaround, 2)
    })


@app.route("/allocate", methods=["POST"])
def allocate():

    data = request.get_json()

    tasks = data["tasks"]
    vehicles = data["vehicles"]

    result = allocate_vehicles(tasks, vehicles)

    return jsonify(result)


# -----------------------------
# SHORTEST-PATH ROUTING
# -----------------------------

# Sample road network: distances are in kilometres.
# These are illustrative values, not live road distances.

ROAD_GRAPH = {
    "NIET": {
        "Knowledge Park": 2,
        "Pari Chowk": 5
    },
    "Knowledge Park": {
        "NIET": 2,
        "Pari Chowk": 3,
        "Sector 62": 12
    },
    "Pari Chowk": {
        "NIET": 5,
        "Knowledge Park": 3,
        "Sector 62": 10
    },
    "Sector 62": {
        "Knowledge Park": 12,
        "Pari Chowk": 10
    }
}


def dijkstra(graph, source, destination):

    if source not in graph or destination not in graph:
        return None

    distances = {
        location: float("inf")
        for location in graph
    }

    previous = {
        location: None
        for location in graph
    }

    distances[source] = 0

    priority_queue = [(0, source)]

    while priority_queue:

        current_distance, current_location = (
            heapq.heappop(priority_queue)
        )

        if current_distance > distances[current_location]:
            continue

        if current_location == destination:
            break

        for neighbour, distance in graph[current_location].items():

            if distance < 0:
                raise ValueError(
                    "Road distances cannot be negative."
                )

            new_distance = current_distance + distance

            if new_distance < distances[neighbour]:

                distances[neighbour] = new_distance
                previous[neighbour] = current_location

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    if distances[destination] == float("inf"):
        return None

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return {
        "source": source,
        "destination": destination,
        "path": path,
        "total_distance": distances[destination],
        "unit": "km"
    }


@app.route("/route", methods=["POST"])
def find_route():

    data = request.get_json(silent=True) or {}

    source = data.get("source")
    destination = data.get("destination")

    if not source or not destination:
        return jsonify({
            "error": "Source and destination are required."
        }), 400

    result = dijkstra(
        ROAD_GRAPH,
        source,
        destination
    )

    if result is None:
        return jsonify({
            "error": "Unknown location or no route available."
        }), 404

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)
