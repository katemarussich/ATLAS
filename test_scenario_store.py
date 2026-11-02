
import unittest
import tempfile
import os
from unittest.mock import patch

import scenario_store


class TestScenarioStore(unittest.TestCase):

    def test_save_and_load_scenario(self):

        with tempfile.TemporaryDirectory() as folder:

            test_database = os.path.join(
                folder,
                "test_atlas.db"
            )

            with patch.object(
                scenario_store,
                "DATABASE_FILE",
                test_database
            ):

                scenario_id = scenario_store.save_scenario(
                    name="Main Reactor Failure",
                    failed_equipment=["R-101"],
                    downtime_hours=8,
                    selling_price=15,
                    contribution_margin=5,
                    existing_production=600,
                    production_loss=2400,
                    recommended_strategy="No Additional Recovery",
                    estimated_impact=12000
                )

                saved = scenario_store.load_scenarios()

                self.assertEqual(scenario_id, 1)
                self.assertEqual(len(saved), 1)
                self.assertEqual(
                    saved[0]["failed_equipment"],
                    ["R-101"]
                )
                self.assertEqual(
                    saved[0]["estimated_impact"],
                    12000
                )

    def test_empty_name_is_rejected(self):

        with self.assertRaises(ValueError):
            scenario_store.save_scenario(
                name=" ",
                failed_equipment=["R-101"],
                downtime_hours=8,
                selling_price=15,
                contribution_margin=5,
                existing_production=600,
                production_loss=2400,
                recommended_strategy="No Additional Recovery",
                estimated_impact=12000
            )


if __name__ == "__main__":
    unittest.main()
