
import unittest
from plant_visual import build_plant_diagram


class TestPlantVisual(unittest.TestCase):

    def setUp(self):
        self.status = {
            "T-101": "Running",
            "R-101": "Running",
            "R-102": "Running",
            "S-101": "Running"
        }

        self.capacity = {
            "T-101": 1200,
            "R-101": 1000,
            "R-102": 600,
            "S-101": 950
        }

    def test_all_equipment_appears(self):
        diagram = build_plant_diagram(
            self.status,
            self.capacity
        )

        for equipment_id in self.status:
            self.assertIn(equipment_id, diagram)

    def test_failed_reactor_is_red(self):
        self.status["R-101"] = "Offline"

        diagram = build_plant_diagram(
            self.status,
            self.capacity
        )

        self.assertIn(
            '"R-101" [label=',
            diagram
        )
        self.assertIn(
            'fillcolor="#fee2e2"',
            diagram
        )

    def test_process_connections(self):
        diagram = build_plant_diagram(
            self.status,
            self.capacity
        )

        self.assertIn(
            '"T-101" -> "R-102"',
            diagram
        )
        self.assertIn(
            '"R-102" -> "S-101"',
            diagram
        )


if __name__ == "__main__":
    unittest.main()
