import unittest
from simulation import run_simulation


class TestSimulation(unittest.TestCase):

    def test_partial_reactor_failure(self):

        status = {
            "T-101": "Running",
            "R-101": "Running",
            "R-102": "Running",
            "S-101": "Running"
        }

        capacity = {
            "T-101": 1200,
            "R-101": 1000,
            "R-102": 600,
            "S-101": 950
        }

        derating = {
            "R-101": 0.2,
            "R-102": 1.0
        }

        result = run_simulation(
            status=status,
            capacity=capacity,
            derating=derating,
            normal_rate=900,
            downtime_hours=8,
            product_value=15
        )

        self.assertEqual(result["available_capacity"], 800)
        self.assertEqual(result["production_loss"], 800)
        self.assertEqual(result["value_at_risk"], 12000)


if __name__ == "__main__":
    unittest.main()