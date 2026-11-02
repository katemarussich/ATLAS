from recovery import calculate_recovery
from plant import calculate_plant_capacity, calculate_production_loss

print("ATLAS — Industrial Crisis Response Simulator")

plant = {
    "T-101": {
        "name": "Feed Tank",
        "capacity": 1200,
        "status": "Running",
        "flow": 900
    },
    "R-101": {
        "name": "Reactor",
        "capacity": 1000,
        "status": "Running",
        "flow": 900
    },
    "S-101": {
        "name": "Separator",
        "capacity": 950,
        "status": "Running",
        "flow": 900
    }
}

print("\nPlant Operating Conditions:")

for equipment_id, equipment in plant.items():
    print(f"\n{equipment_id} - {equipment['name']}")
    print(f"Status: {equipment['status']}")
    print(f"Capacity: {equipment['capacity']} kg/hr")
    print(f"Actual Flow: {equipment['flow']} kg/hr")

# Identify the equipment with the lowest capacity

bottleneck_id = min(
    plant,
    key=lambda equipment_id: plant[equipment_id]["capacity"]
)

bottleneck = plant[bottleneck_id]

print("\n--- Bottleneck Analysis ---")
print(f"Bottleneck: {bottleneck['name']} ({bottleneck_id})")
print(f"Maximum Plant Throughput: {bottleneck['capacity']} kg/hr")

# Simulate an equipment failure

failed_equipment = "R-101"

plant[failed_equipment]["status"] = "Offline"
plant[failed_equipment]["flow"] = 0

print("\n--- Equipment Failure Simulation ---")
print(f"Equipment Failed: {plant[failed_equipment]['name']}")

# Calculate production capacity after failure

if any(equipment["status"] == "Offline" for equipment in plant.values()):
    new_throughput = 0
else:
    new_throughput = min(
        equipment["capacity"] for equipment in plant.values()
    )

print(f"New Plant Throughput: {new_throughput} kg/hr")
print(f"Production Capacity Lost: {bottleneck['capacity'] - new_throughput} kg/hr")

# Calculate financial impact of the reactor failure

while True:
    try:
        downtime_hours = float(
            input("\nEnter reactor downtime in hours: ")
        )

        if downtime_hours <= 0:
            print("Error: Downtime must be greater than zero.")
            continue

        break

    except ValueError:
        print("Error: Please enter a valid number.")

product_value = 15  # $ per kg

normal_production = 900  # kg/hr
production_lost = (normal_production - new_throughput) * downtime_hours
revenue_at_risk = production_lost * product_value

print("\n--- Financial Impact Analysis ---")
print(f"Downtime Duration: {downtime_hours} hours")
print(f"Lost Production: {production_lost:,.0f} kg")
print(f"Revenue at Risk: ${revenue_at_risk:,.2f}")

# Simulate production recovery using a backup reactor

backup_reactor_capacity = 600  # kg/hr

# Production cannot exceed feed, backup reactor, or separator capacity
recovered_throughput = min(
    plant["T-101"]["capacity"],
    backup_reactor_capacity,
    plant["S-101"]["capacity"]
)

recovered_production = recovered_throughput * downtime_hours
revenue_protected = recovered_production * product_value

print("\n--- Backup Reactor Recovery ---")
print(f"Backup Reactor Capacity: {backup_reactor_capacity} kg/hr")
print(f"Recovered Throughput: {recovered_throughput} kg/hr")
print(f"Recovered Production: {recovered_production:,.0f} kg")
print(f"Revenue Protected: ${revenue_protected:,.2f}")

# Calculate remaining losses after recovery

remaining_production_loss = production_lost - recovered_production

remaining_revenue_at_risk = remaining_production_loss * product_value

recovery_percentage = (recovered_production / production_lost) * 100

print("\n--- Recovery Performance ---")
print(f"Original Production Loss: {production_lost:,.0f} kg")
print(f"Recovered Production: {recovered_production:,.0f} kg")
print(f"Remaining Production Loss: {remaining_production_loss:,.0f} kg")
print(f"Remaining Revenue at Risk: ${remaining_revenue_at_risk:,.2f}")
print(f"Production Recovered: {recovery_percentage:.1f}%")

# Compare multiple recovery strategies

recovery_options = {
    "Backup Reactor": {
        "capacity": 600,
        "cost": 8000,
        "startup_hours": 2
    },
    "Temporary Processing Unit": {
        "capacity": 750,
        "cost": 20000,
        "startup_hours": 4
    },
    "Contract Manufacturer": {
        "capacity": 850,
        "cost": 35000,
        "startup_hours": 6
    }
}

print("\n--- Recovery Strategy Comparison ---")

for option_name, option in recovery_options.items():

    total_impact = calculate_recovery(
        normal_production=normal_production,
        recovery_capacity=option["capacity"],
        downtime_hours=downtime_hours,
        product_value=product_value,
        recovery_cost=option["cost"],
        startup_hours=option["startup_hours"]
    )

    print(f"\nStrategy: {option_name}")
    print(f"Startup Delay: {option['startup_hours']} hours")
    print(f"Total Estimated Impact: ${total_impact:,.2f}")# Automatically identify the best recovery strategy

best_strategy = None
lowest_impact = float("inf")

for option_name, option in recovery_options.items():

    total_impact = calculate_recovery(
        normal_production=normal_production,
        recovery_capacity=option["capacity"],
        downtime_hours=downtime_hours,
        product_value=product_value,
        recovery_cost=option["cost"],
	startup_hours=option["startup_hours"]
    )

    if total_impact < lowest_impact:
        lowest_impact = total_impact
        best_strategy = option_name

print("\n--- ATLAS Recommendation ---")
print(f"Recommended Strategy: {best_strategy}")
print(f"Estimated Financial Impact: ${lowest_impact:,.2f}")

# Compare recovery strategies across different shutdown durations

print("\n--- Shutdown Duration Comparison ---")

for hours in [2, 8, 24]:

    best_option = None
    best_cost = float("inf")

    for option_name, option in recovery_options.items():

        total_cost = calculate_recovery(
            normal_production=normal_production,
            recovery_capacity=option["capacity"],
            downtime_hours=hours,
            product_value=product_value,
            recovery_cost=option["cost"],
            startup_hours=option["startup_hours"]
        )

        if total_cost < best_cost:
            best_cost = total_cost
            best_option = option_name

    print(f"\nShutdown Duration: {hours} hours")
    print(f"Best Strategy: {best_option}")
    print(f"Estimated Financial Impact: ${best_cost:,.2f}")

# Test our imported recovery function

test_impact = calculate_recovery(
    normal_production=900,
    recovery_capacity=600,
    downtime_hours=8,
    product_value=15,
    recovery_cost=8000
)

print("\n--- Recovery Module Test ---")
print(f"Calculated Financial Impact: ${test_impact:,.2f}")

# Test the imported plant capacity function

test_status = {
    "T-101": "Running",
    "R-101": "Offline",
    "R-102": "Running",
    "S-101": "Running"
}

test_capacity = {
    "T-101": 1200,
    "R-101": 1000,
    "R-102": 600,
    "S-101": 950
}

test_plant_capacity = calculate_plant_capacity(
    test_status,
    test_capacity
)

print("\n--- Plant Module Test ---")
print(f"Available Plant Capacity: {test_plant_capacity} kg/hr")

# Calculate production loss using the plant model

normal_status = {
    "T-101": "Running",
    "R-101": "Running",
    "R-102": "Running",
    "S-101": "Running"
}

# Calculate maximum capacity before failure
normal_capacity = calculate_plant_capacity(
    normal_status,
    test_capacity
)

# Calculate maximum capacity after failure
failed_capacity = calculate_plant_capacity(
    test_status,
    test_capacity
)

# Calculate the reduction in capacity
capacity_reduction = normal_capacity - failed_capacity

print("\n--- Integrated Failure Analysis ---")
print(f"Normal Plant Capacity: {normal_capacity} kg/hr")
print(f"Capacity After Failure: {failed_capacity} kg/hr")
print(f"Capacity Reduction: {capacity_reduction} kg/hr")

# Calculate actual production loss after equipment failure

normal_operating_rate = 900  # kg/hr

# Actual output cannot exceed available capacity
production_after_failure = min(
    normal_operating_rate,
    failed_capacity
)

# Calculate actual production reduction
actual_production_loss = (
    normal_operating_rate - production_after_failure
)

print("\n--- Actual Production Analysis ---")
print(f"Normal Production: {normal_operating_rate} kg/hr")
print(f"Production After Failure: {production_after_failure} kg/hr")
print(f"Actual Production Reduction: {actual_production_loss} kg/hr")

# Calculate production loss over the shutdown duration

total_production_loss = (
    actual_production_loss * downtime_hours
)

production_value_at_risk = (
    total_production_loss * product_value
)

print("\n--- Integrated Production Loss ---")
print(f"Shutdown Duration: {downtime_hours} hours")
print(f"Normal Production Rate: {normal_operating_rate} kg/hr")
print(f"Reduced Production Rate: {production_after_failure} kg/hr")
print(f"Total Production Loss: {total_production_loss:,.0f} kg")
print(f"Production Value at Risk: ${production_value_at_risk:,.2f}")

# Calculate production loss including backup startup delay

backup_startup_hours = recovery_options["Backup Reactor"]["startup_hours"]

# Time available for the backup reactor to operate
backup_operating_hours = max(
    0,
    downtime_hours - backup_startup_hours
)

# Production recovered by the backup reactor
backup_production = (
    production_after_failure * backup_operating_hours
)

# Production that would occur without failure
expected_production = (
    normal_operating_rate * downtime_hours
)

# Production lost after accounting for startup
adjusted_production_loss = calculate_production_loss(
    normal_rate=normal_operating_rate,
    recovery_rate=production_after_failure,
    downtime_hours=downtime_hours,
    startup_hours=backup_startup_hours
)

print("\n--- Startup-Adjusted Production Analysis ---")
print(f"Backup Startup Time: {backup_startup_hours} hours")
print(f"Backup Operating Time: {backup_operating_hours} hours")
print(f"Expected Production: {expected_production:,.0f} kg")
print(f"Recovered Production: {backup_production:,.0f} kg")
print(f"Adjusted Production Loss: {adjusted_production_loss:,.0f} kg")

# Calculate financial impact using the integrated plant model

backup_recovery_cost = recovery_options["Backup Reactor"]["cost"]

integrated_financial_impact = (
    adjusted_production_loss * product_value
    + backup_recovery_cost
)

print("\n--- Integrated Financial Analysis ---")
print(f"Production Shortfall: {adjusted_production_loss:,.0f} kg")
print(f"Production Value at Risk: ${adjusted_production_loss * product_value:,.2f}")
print(f"Recovery Cost: ${backup_recovery_cost:,.2f}")
print(f"Total Estimated Impact: ${integrated_financial_impact:,.2f}")