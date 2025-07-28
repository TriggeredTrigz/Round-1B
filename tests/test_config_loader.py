import unittest
import os
import json
import tempfile
from src.config_loader import ConfigLoader
from src.models import InputConfig

class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        self.test_json_path = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'test_input.json'
        )
        
    def test_load_input_config(self):
        config = ConfigLoader.load_input_config(self.test_json_path)
        
        # Test challenge info
        self.assertEqual(config.challenge_info.challenge_id, "round_1b_002")
        self.assertEqual(config.challenge_info.test_case_name, "travel_planner")
        self.assertEqual(config.challenge_info.description, "France Travel")
        
        # Test documents
        self.assertEqual(len(config.documents), 1)
        self.assertEqual(
            config.documents[0].filename,
            "South of France - Cities.pdf"
        )
        
        # Test persona and job
        self.assertEqual(config.persona.role, "Travel Planner")
        self.assertEqual(
            config.job_to_be_done.task,
            "Plan a trip of 4 days for a group of 10 college friends."
        )
        
    def test_load_invalid_json(self):
        # Create temporary invalid JSON file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("invalid json content")
            temp_path = f.name
            
        with self.assertRaises(Exception):
            ConfigLoader.load_input_config(temp_path)
            
        # Cleanup
        os.unlink(temp_path)
        
    def test_load_nonexistent_file(self):
        with self.assertRaises(Exception):
            ConfigLoader.load_input_config("nonexistent.json")
            
    def test_load_missing_fields(self):
        # Create temporary JSON with missing fields
        incomplete_config = {
            "challenge_info": {
                "challenge_id": "test_001"
                # Missing other required fields
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(incomplete_config, f)
            temp_path = f.name
            
        with self.assertRaises(Exception):
            ConfigLoader.load_input_config(temp_path)
            
        # Cleanup
        os.unlink(temp_path)

if __name__ == '__main__':
    unittest.main()