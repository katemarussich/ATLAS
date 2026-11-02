def calculate_plant_capacity(status, capacity, derating=None):

    # Default: all equipment operates at full capacity
    if derating is None:
        derating = {}

    # Shared equipment must be operational
    if (
        status["T-101"] != "Running"
        or status["S-101"] != "Running"
    ):
        return 0

    # Calculate available reactor capacity
    reactor_capacity = 0

    for reactor_id in ["R-101", "R-102"]:
        if status[reactor_id] == "Running":

            operating_fraction = derating.get(reactor_id, 1.0)

            reactor_capacity += calculate_derated_capacity(
                capacity[reactor_id],
                operating_fraction
            )

    return min(
        capacity["T-101"],
        reactor_capacity,
        capacity["S-101"]
    )

def calculate_production_loss(
    normal_rate,
    recovery_rate,
    downtime_hours,
    startup_hours
):
    # Production expected without a failure
    expected_production = normal_rate * downtime_hours

    # Time available after backup startup
    operating_hours = max(
        0,
        downtime_hours - startup_hours
    )

    # Actual recovered production
    recovered_production = min(
        normal_rate,
        recovery_rate
    ) * operating_hours

    # Remaining production shortfall
    production_loss = (
        expected_production - recovered_production
    )

    return production_loss

def calculate_derated_capacity(
    rated_capacity,
    operating_fraction
):
    # Operating fraction must be between 0 and 1
    if not 0 <= operating_fraction <= 1:
        raise ValueError(
            "Operating fraction must be between 0 and 1."
        )

    return rated_capacity * operating_fraction