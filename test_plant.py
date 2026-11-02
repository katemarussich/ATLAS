import unittest
from plant import calculate_plant_capacity, calculate_production_loss
from recovery import calculate_production_value_at_risk

class TestPlantCapacity(unittest.TestCase):

    def setUp(self):
        self.capacity = {
            "T-101": 1200,
            "R-101": 1000,
            "R-102": 600,
            "S-101": 950
        }

        self.status = {
            "T-101": "Running",
            "R-101": "Running",
            "R-102": "Running",
            "S-101": "Running"
        }

    def test_normal_operation(self):
        result = calculate_plant_capacity(
            self.status, self.capacity
        )
        self.assertEqual(result, 950)

    def test_main_reactor_failure(self):
        self.status["R-101"] = "Offline"

        result = calculate_plant_capacity(
            self.status, self.capacity
        )
        self.assertEqual(result, 600)

    def test_separator_failure(self):
        self.status["S-101"] = "Offline"

        result = calculate_plant_capacity(
            self.status, self.capacity
        )
        self.assertEqual(result, 0)

    def test_production_loss_with_startup(self):
        result = calculate_production_loss(
            normal_rate=900,
            recovery_rate=600,
            downtime_hours=8,
            startup_hours=2
        )

        self.assertEqual(result, 3600)
    def test_shutdown_shorter_than_startup(self):
        result = calculate_production_loss(
            normal_rate=900,
            recovery_rate=600,
            downtime_hours=1,
            startup_hours=2
        )

        self.assertEqual(result, 900)

    def test_no_backup_available(self):
        result = calculate_production_loss(
            normal_rate=900,
            recovery_rate=0,
            downtime_hours=8,
            startup_hours=0
        )

        self.assertEqual(result, 7200)

    def test_partial_reactor_failure(self):
        derating = {
            "R-101": 0.4,
            "R-102": 1.0
        }

        result = calculate_plant_capacity(
            self.status,
            self.capacity,
            derating
        )

        self.assertEqual(result, 950)

    def test_severe_reactor_derating(self):
        derating = {
            "R-101": 0.2,
            "R-102": 1.0
        }

        result = calculate_plant_capacity(
            self.status,
            self.capacity,
            derating
        )

        self.assertEqual(result, 800)

    def test_production_loss_with_derating(self):
        derating = {
            "R-101": 0.2,
            "R-102": 1.0
        }

        # Calculate plant capacity with derating
        available_capacity = calculate_plant_capacity(
            self.status,
            self.capacity,
            derating
        )

        # Calculate lost production over 8 hours
        production_loss = calculate_production_loss(
            normal_rate=900,
            recovery_rate=available_capacity,
            downtime_hours=8,
            startup_hours=0
        )

        self.assertEqual(production_loss, 800)

    def test_derating_financial_impact(self):

        # Main reactor operates at 20% capacity
        derating = {
            "R-101": 0.2,
            "R-102": 1.0
        }

        available_capacity = calculate_plant_capacity(
            self.status,
            self.capacity,
            derating
        )

        production_loss = calculate_production_loss(
            normal_rate=900,
            recovery_rate=available_capacity,
            downtime_hours=8,
            startup_hours=0
        )

        financial_impact = calculate_production_value_at_risk(
            production_loss=production_loss,
            product_value=15
        )

        self.assertEqual(financial_impact, 12000)

if __name__ == "__main__":
    unittest.main()