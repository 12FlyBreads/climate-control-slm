# === utils.py ===

# Libraries
import yaml
from typing import Dict, Any
import os

# Function to load configuration from a YAML file
def load_config() -> Dict[str, Any]:
    """Load the YAML configuration file."""

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.yaml')

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found. Make sure it is in the root folder.")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        raise
