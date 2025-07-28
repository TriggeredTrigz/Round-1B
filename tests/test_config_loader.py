import unittest
import os
from src.config_loader import ConfigLoader

class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        self.test_json_path = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'test_input.json'
        )
    
    def test_load_input_config(self):
        config = ConfigLoader.load_input_config(self.test_json_path)
        
        self.assertEqual(config.challenge_info.challenge_id, "round_1b_002")
        self.assertEqual(config.challenge_info.test_case_name, "travel_planner")
        self.assertEqual(len(config.documents), 7)
        self.assertEqual(config.persona.role, "Travel Planner")
        self.assertEqual(
            config.job_to_be_done.task,
            "Plan a trip of 4 days for a group of 10 college friends."
        )

if __name__ == '__main__':
    unittest.main()