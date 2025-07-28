import json
from dataclasses import dataclass
from typing import Dict, Any
import dacite
from .models import InputConfig

class ConfigLoader:
    @staticmethod
    def load_input_config(input_json_path: str) -> InputConfig:
        """Load and parse the input JSON configuration file."""
        try:
            with open(input_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Use dacite to convert dictionary to InputConfig dataclass
            config = dacite.from_dict(data_class=InputConfig, data=data)
            return config
            
        except FileNotFoundError:
            raise Exception(f"Input configuration file not found: {input_json_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in file: {input_json_path}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")