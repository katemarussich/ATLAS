# Define connections between plant equipment

plant_network = {
    "T-101": ["R-101", "R-102"],
    "R-101": ["S-101"],
    "R-102": ["S-101"],
    "S-101": []
}

print("--- ATLAS Equipment Network ---")

for equipment_id, connected_equipment in plant_network.items():
    print(f"{equipment_id} connects to: {connected_equipment}")

# Find all equipment downstream of a selected unit

def find_downstream(network, starting_equipment):
    visited = set()
    to_visit = list(network[starting_equipment])

    while to_visit:
        current = to_visit.pop()

        if current not in visited:
            visited.add(current)
            to_visit.extend(network[current])

    return visited


# Interactive downstream equipment analysis

print("\n--- Downstream Equipment Analysis ---")

selected_equipment = input(
    "Enter equipment ID (T-101, R-101, R-102, S-101): "
).strip().upper()

if selected_equipment in plant_network:

    downstream = find_downstream(
        plant_network,
        selected_equipment
    )

    print(f"\nSelected Equipment: {selected_equipment}")

    if downstream:
        for equipment_id in sorted(downstream):
            print(f"Downstream: {equipment_id}")
    else:
        print("No downstream equipment found.")

else:
    print("Error: Equipment ID not found.")

# Find all possible production routes

def find_routes(network, start, end, path=None):
    if path is None:
        path = []

    path = path + [start]

    if start == end:
        return [path]

    routes = []

    for next_equipment in network[start]:
        if next_equipment not in path:
            new_routes = find_routes(
                network,
                next_equipment,
                end,
                path
            )
            routes.extend(new_routes)

    return routes


print("\n--- Available Production Routes ---")

routes = find_routes(
    plant_network,
    "T-101",
    "S-101"
)

for route in routes:
    print(" -> ".join(route))

# Determine which routes remain available after a failure

equipment_status = {
    "T-101": "Running",
    "R-101": "Running",
    "R-102": "Running",
    "S-101": "Running"
}

# Let the user select equipment to simulate a failure

print("\n--- Equipment Failure Selection ---")

failed_equipment = input(
    "Enter equipment to fail (T-101, R-101, R-102, S-101): "
).strip().upper()

if failed_equipment in equipment_status:
    equipment_status[failed_equipment] = "Offline"
    print(f"{failed_equipment} is now Offline.")
else:
    print("Invalid equipment ID. No failure simulated.")

print("\n--- Production Routes After Failure ---")

for route in routes:

    route_available = all(
        equipment_status[equipment_id] == "Running"
        for equipment_id in route
    )

    if route_available:
        print("AVAILABLE:", " -> ".join(route))
    else:
        print("BLOCKED:", " -> ".join(route))

# Equipment processing capacities in kg/hr

equipment_capacity = {
    "T-101": 1200,
    "R-101": 1000,
    "R-102": 600,
    "S-101": 950
}

print("\n--- Available Route Capacities ---")

for route in routes:

    route_available = all(
        equipment_status[equipment_id] == "Running"
        for equipment_id in route
    )

    if route_available:
        route_capacity = min(
            equipment_capacity[equipment_id]
            for equipment_id in route
        )

        print(
            f"{' -> '.join(route)}: "
            f"{route_capacity} kg/hr"
        )

# Calculate total plant capacity with parallel reactors

print("\n--- Total Plant Capacity ---")

feed_capacity = equipment_capacity["T-101"]
separator_capacity = equipment_capacity["S-101"]

reactor_capacity = 0

for reactor_id in ["R-101", "R-102"]:
    if equipment_status[reactor_id] == "Running":
        reactor_capacity += equipment_capacity[reactor_id]

# Check whether shared equipment is operational
if (
    equipment_status["T-101"] == "Offline"
    or equipment_status["S-101"] == "Offline"
):
    total_capacity = 0

else:
    total_capacity = min(
        feed_capacity,
        reactor_capacity,
        separator_capacity
    )

print(f"Available Reactor Capacity: {reactor_capacity} kg/hr")
print(f"Total Plant Capacity: {total_capacity} kg/hr")

def calculate_plant_capacity(status, capacity):

    # Shared equipment must be operational
    if (
        status["T-101"] != "Running"
        or status["S-101"] != "Running"
    ):
        return 0

    # Add capacities of operational reactors
    available_reactor_capacity = 0

    for reactor_id in ["R-101", "R-102"]:
        if status[reactor_id] == "Running":
            available_reactor_capacity += capacity[reactor_id]

    # Shared equipment limits total throughput
    return min(
        capacity["T-101"],
        available_reactor_capacity,
        capacity["S-101"]
    )


print("\n--- Capacity Function Test ---")

result = calculate_plant_capacity(
    equipment_status,
    equipment_capacity
)

print(f"Calculated Plant Capacity: {result} kg/hr")
