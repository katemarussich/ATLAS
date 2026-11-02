
def calculate_recovery(
    normal_production,
    recovery_capacity,
    downtime_hours,
    product_value,
    recovery_cost,
    startup_hours=0,
    existing_production=0
):
    # Calculate available operating time
    operating_hours = max(
        0,
        downtime_hours - startup_hours
    )

    # Production maintained by existing equipment
    existing_kg = min(
        normal_production,
        existing_production
    ) * downtime_hours

    # Additional recovery cannot exceed unmet demand
    additional_rate = min(
        recovery_capacity,
        max(0, normal_production - existing_production)
    )

    recovered_kg = (
        existing_kg + additional_rate * operating_hours
    )

    # Calculate production shortfall
    potential_loss = normal_production * downtime_hours
    remaining_loss = potential_loss - recovered_kg

    # Calculate financial impact
    total_impact = (
        remaining_loss * product_value
        + recovery_cost
    )

    return total_impact


def calculate_production_value_at_risk(
    production_loss,
    product_value
):
    return production_loss * product_value



def recommend_recovery(
    recovery_options,
    normal_production,
    downtime_hours,
    product_value,
    existing_production=0
):
    results = {}

    for name, option in recovery_options.items():

        if not option.get("available", True):
            continue

        impact = calculate_recovery(
            normal_production=normal_production,
            recovery_capacity=option["capacity"],
            downtime_hours=downtime_hours,
            product_value=product_value,
            recovery_cost=option["cost"],
            startup_hours=option["startup_hours"],
            existing_production=existing_production
        )

        results[name] = impact

    if not results:
        raise ValueError("No available recovery options.")

    best_strategy = min(results, key=results.get)

    return {
        "recommended_strategy": best_strategy,
        "estimated_impact": results[best_strategy],
        "all_results": results
    }
