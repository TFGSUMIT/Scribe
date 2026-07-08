# complete code
"""
Utility for loading JSON data.
"""
import json
import logging
from pathlib import Path

class JsonLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_json(self, data: Dict) -> str:
        """
        Load the JSON data.
        """
        try:
            json_output = json.dumps(data, indent=4)
            return json_output
        except Exception as e:
            self.logger.error(f"Error loading JSON data: {str(e)}")
            raise