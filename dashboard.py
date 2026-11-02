import pandas as pd
import streamlit as st
from plant import calculate_plant_capacity
from simulation import run_simulation
from recovery import recommend_recovery
from scenario_store import save_scenario, load_scenarios
from plant_visual import build_plant_diagram


# Configure dashboard
st.set_page_config(
    page_title="ATLAS",
    page_icon="🏭",
    layout="wide"
)

equipment_capacity = {
    "T-101": 1200,
    "R-101": 1000,
    "R-102": 600,
    "S-101": 950
}

equipment_status = {
    "T-101": "Running",
    "R-101": "Running",
    "R-102": "Running",
    "S-101": "Running"
}

# Let the user select equipment to fail

failure_options = {
    "No Failure": None,
    "Feed Tank (T-101)": "T-101",
    "Main Reactor (R-101)": "R-101",
    "Backup Reactor (R-102)": "R-102",
    "Separator (S-101)": "S-101"
}

selected_failures = st.multiselect(
    "Select Equipment Failures",
    options=[
        "Feed Tank (T-101)",
        "Main Reactor (R-101)",
        "Backup Reactor (R-102)",
        "Separator (S-101)"
    ]
)

failed_equipment_ids = [
    failure_options[name]
    for name in selected_failures
]

for equipment_id in failed_equipment_ids:
    equipment_status[equipment_id] = "Offline"

# Keep a compatibility variable for now
failed_equipment = (
    "R-101" if "R-101" in failed_equipment_ids else None
)

# Recalculate plant capacity
plant_capacity = calculate_plant_capacity(
    equipment_status,
    equipment_capacity
)
# Dashboard heading
st.title("ATLAS")
st.subheader("Industrial Crisis Response Simulator")

st.write(
    "Monitor chemical manufacturing operations, "
    "simulate equipment failures, and evaluate "
    "recovery strategies."
)

st.divider()

# Plant operating conditions
st.header("Plant Overview")

st.subheader("Live Plant Network")

plant_diagram = build_plant_diagram(
    equipment_status,
    equipment_capacity
)

st.graphviz_chart(
    plant_diagram,
    width="stretch"
)

st.caption(
    "Green = operational equipment; red = offline equipment. "
    "Arrows represent permitted process connections, not "
    "measured material flow."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Feed Tank Capacity", "1,200 kg/hr")

with col2:
    st.metric("Reactor Capacity", "1,600 kg/hr")

with col3:
    st.metric("Separator Capacity", "950 kg/hr")

# Display the current plant operating status

if plant_capacity == 0:
    st.error("Plant Status: SHUTDOWN")

elif plant_capacity < 950:
    st.warning("Plant Status: REDUCED CAPACITY")

elif failed_equipment_ids:
    st.warning("Plant Status: EQUIPMENT FAILURE - CAPACITY MAINTAINED")

else:
    st.success("Plant Status: FULLY OPERATIONAL")
st.divider()


# Executive operational summary

st.subheader("Operational Summary")

normal_production_target = 900

current_production = min(
    plant_capacity,
    normal_production_target
)

production_gap = (
    normal_production_target - current_production
)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric(
        "Current Production",
        f"{current_production:,.0f} kg/hr"
    )

with summary_col2:
    st.metric(
        "Production Shortfall",
        f"{production_gap:,.0f} kg/hr"
    )

with summary_col3:
    st.metric(
        "Target Achievement",
        f"{current_production / normal_production_target * 100:.1f}%"
    )


st.header("Calculated Plant Performance")

st.metric(
    "Maximum Plant Throughput",
    f"{plant_capacity:,.0f} kg/hr"
)

# Allow the user to adjust shutdown duration

st.divider()
st.header("Simulation Settings")

downtime_hours = st.slider(
    "Equipment Downtime (hours)",
    min_value=1,
    max_value=48,
    value=8,
    step=1
)

product_value = st.number_input(
    "Product Value ($/kg)",
    min_value=0.0,
    max_value=1000.0,
    value=15.0,
    step=1.0
)


contribution_margin = st.number_input(
    "Contribution Margin ($/kg)",
    min_value=0.0,
    max_value=1000.0,
    value=5.0,
    step=1.0,
    help=(
        "Selling price minus avoidable variable costs "
        "per kilogram. Used to compare recovery strategies."
    )
)

if contribution_margin > product_value:
    st.error(
        "Contribution margin cannot exceed selling price "
        "under the current nonnegative variable-cost assumption."
    )
    st.stop()


# Run the integrated simulation

simulation_results = run_simulation(
    status=equipment_status,
    capacity=equipment_capacity,
    derating={},
    normal_rate=900,
    downtime_hours=downtime_hours,
    product_value=product_value
)

st.divider()
st.header("Financial Impact Analysis")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Production Loss",
        f"{simulation_results['production_loss']:,.0f} kg"
    )

with col2:
    st.metric(
        "Production Value at Risk (Immediate Capacity)",
        f"${simulation_results['value_at_risk']:,.2f}"
    )

st.caption(
    "This estimate assumes all remaining equipment is "
    "immediately available. It excludes startup delays "
    "and additional recovery costs."
)


# Define available recovery strategies
#
# Surviving equipment is already included in plant_capacity.
# Recovery strategies provide ADDITIONAL production only.

normal_production = 900

existing_production = min(
    normal_production,
    plant_capacity
)

# Calculate spare capacity in shared plant equipment
shared_equipment_available = (
    equipment_status["T-101"] == "Running"
    and equipment_status["S-101"] == "Running"
)

if shared_equipment_available:
    shared_capacity = min(
        equipment_capacity["T-101"],
        equipment_capacity["S-101"]
    )
    spare_shared_capacity = max(
        0,
        shared_capacity - existing_production
    )
else:
    spare_shared_capacity = 0

recovery_options = {
    "No Additional Recovery": {
        "capacity": 0,
        "cost": 0,
        "startup_hours": 0,
        "available": True
    },
    "Temporary Processing Unit": {
        "capacity": min(750, spare_shared_capacity),
        "cost": 20000,
        "startup_hours": 4,
        "available": (
            shared_equipment_available
            and spare_shared_capacity > 0
        )
    },
    "Contract Manufacturer": {
        "capacity": 850,
        "cost": 35000,
        "startup_hours": 6,
        "available": True
    }
}

st.divider()
st.header("Recovery Strategy Options")

st.caption(
    "Surviving plant equipment continues producing "
    f"{existing_production:,.0f} kg/hr. Recovery options "
    "provide additional capacity, not replacement capacity. "
    "The temporary unit is assumed to require the existing "
    "feed tank and separator. Contract manufacturing is "
    "assumed independent of the plant."
)

for name, option in recovery_options.items():

    with st.expander(name):

        st.write(
            f"Additional Capacity: "
            f"{option['capacity']:,.0f} kg/hr"
        )

        st.write(
            f"Startup Delay: "
            f"{option['startup_hours']} hours"
        )

        st.write(
            f"Recovery Cost: "
            f"${option['cost']:,.0f}"
        )

        st.write(
            "Available: "
            + ("Yes" if option["available"] else "No")
        )

# Evaluate recovery when production is lost

if failed_equipment_ids and simulation_results["production_loss"] > 0:

    st.subheader("Recovery Strategy Comparison")

    recommendation = recommend_recovery(
        recovery_options=recovery_options,
        normal_production=normal_production,
        downtime_hours=downtime_hours,
        product_value=contribution_margin,
        existing_production=existing_production
    )

    for name, impact in recommendation["all_results"].items():
        st.write(f"{name}: ${impact:,.2f}")

    st.success(
        "Recommended Strategy: "
        + recommendation["recommended_strategy"]
    )

    st.metric(
        "Lowest Estimated Financial Impact",
        f"${recommendation['estimated_impact']:,.2f}"
    )

    st.caption(
    "Estimated financial impact = lost contribution margin "
    "+ recovery activation cost. Recovery strategies are "
    "evaluated against the same disruption duration and "
    "existing plant production. This simplified model "
    "excludes inventory, contractual penalties, variable "
    "recovery operating costs, and uncertainty."
)


# ==========================================
# SCENARIO COMPARISON AND SENSITIVITY ANALYSIS
# ==========================================

if failed_equipment_ids and simulation_results["production_loss"] > 0:

    st.divider()
    st.header("Scenario Analysis")

    st.write(
        "Compare recovery strategies across different "
        "disruption durations using the current plant "
        "configuration and contribution margin."
    )

    # Compare selected downtime scenarios
    scenario_durations = [4, 8, 12, 24, 48]

    scenario_rows = []

    for hours in scenario_durations:

        result = recommend_recovery(
            recovery_options=recovery_options,
            normal_production=normal_production,
            downtime_hours=hours,
            product_value=contribution_margin,
            existing_production=existing_production
        )

        scenario_rows.append({
            "Downtime (hours)": hours,
            "Recommended Strategy": result[
                "recommended_strategy"
            ],
            "Estimated Impact ($)": result[
                "estimated_impact"
            ]
        })

    scenario_df = pd.DataFrame(scenario_rows)

    st.subheader("Recovery Decisions by Downtime")

    st.dataframe(
        scenario_df,
        hide_index=True,
        width="stretch"
    )

    # Financial sensitivity for each available strategy
    st.subheader("Financial Impact vs. Downtime")

    sensitivity_rows = []

    for hours in range(1, 49):

        result = recommend_recovery(
            recovery_options=recovery_options,
            normal_production=normal_production,
            downtime_hours=hours,
            product_value=contribution_margin,
            existing_production=existing_production
        )

        row = {
            "Downtime (hours)": hours
        }

        for name, impact in result["all_results"].items():
            row[name] = impact

        sensitivity_rows.append(row)

    sensitivity_df = pd.DataFrame(
        sensitivity_rows
    ).set_index("Downtime (hours)")

    st.line_chart(sensitivity_df)

    st.caption(
        "Each line represents the modeled financial "
        "impact of one available recovery strategy. "
        "The lowest line at any downtime represents "
        "the least-cost option under the assumptions."
    )

    # Find when additional recovery first becomes cheaper
    st.subheader("Recovery Break-Even Analysis")

    break_even_hour = None
    break_even_strategy = None

    for hours in range(1, 49):

        result = recommend_recovery(
            recovery_options=recovery_options,
            normal_production=normal_production,
            downtime_hours=hours,
            product_value=contribution_margin,
            existing_production=existing_production
        )

        if result["recommended_strategy"] != "No Additional Recovery":
            break_even_hour = hours
            break_even_strategy = result["recommended_strategy"]
            break

    if break_even_hour is not None:

        st.success(
            f"Additional recovery first becomes the "
            f"lowest-cost option at {break_even_hour} "
            f"hours: {break_even_strategy}."
        )

    else:

        st.info(
            "No additional recovery strategy becomes "
            "the lowest-cost option within 48 hours."
        )


# ==========================================
# SAVED SCENARIOS
# ==========================================

st.divider()
st.header("Scenario History")

st.write(
    "Save the current disruption scenario and compare "
    "it against previously evaluated scenarios."
)

if failed_equipment_ids and simulation_results["production_loss"] > 0:

    scenario_name = st.text_input(
        "Scenario Name",
        placeholder="Example: Main reactor failure - 24 hours"
    )

    if st.button("Save Current Scenario"):

        if not scenario_name.strip():
            st.warning("Enter a scenario name before saving.")

        else:
            saved_id = save_scenario(
                name=scenario_name,
                failed_equipment=failed_equipment_ids,
                downtime_hours=downtime_hours,
                selling_price=product_value,
                contribution_margin=contribution_margin,
                existing_production=existing_production,
                production_loss=simulation_results["production_loss"],
                recommended_strategy=recommendation[
                    "recommended_strategy"
                ],
                estimated_impact=recommendation[
                    "estimated_impact"
                ]
            )

            st.success(
                f"Scenario saved successfully (ID: {saved_id})."
            )

else:
    st.info(
        "Select an equipment failure that causes "
        "production loss to save a scenario."
    )

saved_scenarios = load_scenarios()

if saved_scenarios:

    st.subheader("Previously Saved Scenarios")

    history_rows = []

    for scenario in saved_scenarios:

        history_rows.append({
            "ID": scenario["id"],
            "Scenario": scenario["name"],
            "Equipment Failures": ", ".join(
                scenario["failed_equipment"]
            ),
            "Downtime (hours)": scenario["downtime_hours"],
            "Contribution Margin ($/kg)": scenario[
                "contribution_margin"
            ],
            "Recommended Strategy": scenario[
                "recommended_strategy"
            ],
            "Estimated Impact ($)": scenario[
                "estimated_impact"
            ]
        })

    history_df = pd.DataFrame(history_rows)


    # Export saved scenarios for further analysis

    csv_data = history_df.to_csv(index=False)

    st.download_button(
        label="Download Scenario History (CSV)",
        data=csv_data,
        file_name="atlas_scenario_history.csv",
        mime="text/csv"
    )


    st.dataframe(
        history_df,
        hide_index=True,
        width="stretch"
    )

    st.subheader("Compare Saved Financial Impacts")

    comparison_df = history_df.set_index("ID")[
        ["Estimated Impact ($)"]
    ]

    st.bar_chart(comparison_df)

    st.caption(
        "Saved scenarios retain their original assumptions "
        "and results. The chart compares total estimated "
        "financial impacts, not risk-adjusted or normalized "
        "performance. Differences in downtime, margin, and "
        "equipment failures can affect comparability."
    )

else:
    st.info("No scenarios have been saved yet.")

