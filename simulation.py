from plant import calculate_plant_capacity, calculate_production_loss
from recovery import calculate_production_value_at_risk


def run_simulation(
    status,
    capacity,
    derating,
    normal_rate,
    downtime_hours,
    product_value
):
    # Calculate available plant capacity
    available_capacity = calculate_plant_capacity(
        status,
        capacity,
        derating
    )

    # Calculate production lost
    production_loss = calculate_production_loss(
        normal_rate=normal_rate,
        recovery_rate=available_capacity,
        downtime_hours=downtime_hours,
        startup_hours=0
    )

    # Calculate financial value at risk
    value_at_risk = calculate_production_value_at_risk(
        production_loss,
        product_value
    )

    return {
        "available_capacity": available_capacity,
        "production_loss": production_loss,
        "value_at_risk": value_at_risk
    }