
def build_plant_diagram(equipment_status, equipment_capacity):
    """Build a Graphviz diagram of the plant network."""

    labels = {
        "T-101": "Feed Tank",
        "R-101": "Main Reactor",
        "R-102": "Backup Reactor",
        "S-101": "Separator"
    }

    lines = [
        "digraph ATLAS {",
        'rankdir=LR;',
        'graph [bgcolor="transparent", pad="0.3", nodesep="0.7"];',
        'node [shape=box, style="rounded,filled", '
        'fontname="Arial", fontsize=12, margin="0.18"];',
        'edge [color="#64748b", penwidth=2];'
    ]

    for equipment_id, name in labels.items():

        running = equipment_status[equipment_id] == "Running"

        fill_color = "#dcfce7" if running else "#fee2e2"
        border_color = "#15803d" if running else "#b91c1c"
        state = "RUNNING" if running else "OFFLINE"

        label = (
            f"{name}\\n"
            f"{equipment_id}\\n"
            f"{equipment_capacity[equipment_id]:,} kg/hr\\n"
            f"{state}"
        )

        lines.append(
            f'"{equipment_id}" [label="{label}", '
            f'fillcolor="{fill_color}", '
            f'color="{border_color}", '
            f'fontcolor="#111827"];'
        )

    connections = [
        ("T-101", "R-101"),
        ("T-101", "R-102"),
        ("R-101", "S-101"),
        ("R-102", "S-101")
    ]

    for source, target in connections:
        lines.append(f'"{source}" -> "{target}";')

    lines.append("}")

    return "\n".join(lines)
