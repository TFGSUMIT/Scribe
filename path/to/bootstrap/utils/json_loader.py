# complete code
"""
JSON Loader
==========

This module provides a JSON loader that loads JSON data from a file or string.

Classes:
    JsonLoader: The JSON loader class that loads JSON data.
"""

import json

class JsonLoader:
    def load_json(self, file_path: str) -> Dict:
        """
        Load JSON data from a file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            Dict: The loaded JSON data.
        """
        try:
            # Load the JSON data from the file
            with open(file_path, "r") as file:
                json_data = json.load(file)
                return json_data
        except Exception as e:
            # Handle any errors that occur during loading
            print(f"Error loading JSON: {e}")
            return {}

    def load_json_string(self, json_string: str) -> Dict:
        """
        Load JSON data from a string.

        Args:
            json_string (str): The JSON data as a string.

        Returns:
            Dict: The loaded JSON data.
        """
        try:
            # Load the JSON data from the string
            json_data = json.loads(json_string)
            return json_data
        except Exception as e:
            # Handle any errors that occur during loading
            print(f"Error loading JSON: {e}")
            return {}