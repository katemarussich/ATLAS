import unittest

from recovery import (
    calculate_recovery,
    calculate_production_value_at_risk,
    recommend_recovery
)

class TestRecovery(unittest.TestCase):

    def test_backup_reactor(self):
        result = calculate_recovery(
            900, 600, 8, 15, 8000
        )
        self.assertEqual(result, 44000)

    def test_temporary_unit(self):
        result = calculate_recovery(
            900, 750, 8, 15, 20000
        )
        self.assertEqual(result, 38000)

    def test_contract_manufacturer(self):
        result = calculate_recovery(
            900, 850, 8, 15, 35000
        )
        self.assertEqual(result, 41000)

    def test_startup_delay(self):
        result = calculate_recovery(
            normal_production=900,
            recovery_capacity=600,
            downtime_hours=8,
            product_value=15,
            recovery_cost=8000,
            startup_hours=2
        )

        self.assertEqual(result, 62000)

    def test_production_value_at_risk(self):
        result = calculate_production_value_at_risk(
            production_loss=800,
            product_value=15
        )

        self.assertEqual(result, 12000)

    def test_recovery_recommendation(self):

        options = {
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

        result = recommend_recovery(
            recovery_options=options,
            normal_production=900,
            downtime_hours=8,
            product_value=15
        )

        self.assertEqual(
            result["recommended_strategy"],
            "Backup Reactor"
        )

        self.assertEqual(
            result["estimated_impact"],
            62000
        )

    def test_unavailable_backup_reactor(self):

        options = {
            "Backup Reactor": {
                "capacity": 600,
                "cost": 8000,
                "startup_hours": 2,
                "available": False
            },
            "Temporary Processing Unit": {
                "capacity": 750,
                "cost": 20000,
                "startup_hours": 4,
                "available": True
            },
            "Contract Manufacturer": {
                "capacity": 850,
                "cost": 35000,
                "startup_hours": 6,
                "available": True
            }
        }

        result = recommend_recovery(
            recovery_options=options,
            normal_production=900,
            downtime_hours=8,
            product_value=15
        )

        self.assertEqual(
            result["recommended_strategy"],
            "Temporary Processing Unit"
        )

        self.assertNotIn(
            "Backup Reactor",
            result["all_results"]
        )

    def test_recovery_with_existing_production(self):

        impact = calculate_recovery(
            normal_production=900,
            recovery_capacity=300,
            downtime_hours=8,
            product_value=15,
            recovery_cost=8000,
            startup_hours=2,
            existing_production=600
        )

        self.assertEqual(impact, 17000)


    def test_existing_production_not_double_counted(self):
        options = {
            "No Additional Recovery": {
                "capacity": 0,
                "cost": 0,
                "startup_hours": 0
            },
            "Temporary Processing Unit": {
                "capacity": 350,
                "cost": 20000,
                "startup_hours": 4
            }
        }

        result = recommend_recovery(
            recovery_options=options,
            normal_production=900,
            downtime_hours=8,
            product_value=15,
            existing_production=600
        )

        self.assertEqual(
            result["recommended_strategy"],
            "No Additional Recovery"
        )
        self.assertEqual(
            result["estimated_impact"],
            36000
        )

    def test_long_downtime_justifies_recovery(self):
        options = {
            "No Additional Recovery": {
                "capacity": 0,
                "cost": 0,
                "startup_hours": 0
            },
            "Temporary Processing Unit": {
                "capacity": 350,
                "cost": 20000,
                "startup_hours": 4
            }
        }

        result = recommend_recovery(
            recovery_options=options,
            normal_production=900,
            downtime_hours=24,
            product_value=15,
            existing_production=600
        )

        self.assertEqual(
            result["recommended_strategy"],
            "Temporary Processing Unit"
        )
        self.assertEqual(
            result["estimated_impact"],
            38000
        )

    def test_unavailable_recovery_is_excluded(self):
        options = {
            "No Additional Recovery": {
                "capacity": 0,
                "cost": 0,
                "startup_hours": 0
            },
            "Temporary Processing Unit": {
                "capacity": 350,
                "cost": 20000,
                "startup_hours": 4,
                "available": False
            }
        }

        result = recommend_recovery(
            recovery_options=options,
            normal_production=900,
            downtime_hours=24,
            product_value=15,
            existing_production=600
        )

        self.assertEqual(
            result["recommended_strategy"],
            "No Additional Recovery"
        )
        self.assertNotIn(
            "Temporary Processing Unit",
            result["all_results"]
        )


if __name__ == "__main__":
    unittest.main()