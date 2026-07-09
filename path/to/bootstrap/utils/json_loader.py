# complete code
"""
JSON Loader
------------

This module provides the JSON loader utility, which loads JSON data from a file or string.
"""

import json

class JSONLoader:
    """
    JSON Loader
    """

    @staticmethod
    def load_json_file(file_path: str) -> Dict:
        """
        Load JSON data from a file.

        Args:
            file_path (str): The file path.

        Returns:
            Dict: The JSON data.
        """
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
                return json_data

        except Exception as e:
            raise ValueError(f"Failed to load JSON file: {str(e)}")

    @staticmethod
    def load_json_string(json_string: str) -> Dict:
        """
        Load JSON data from a string.

        Args:
            json_string (str): The JSON string.

        Returns:
            Dict: The JSON data.
        """
        try:
            json_data = json.loads(json_string)
            return json_data

        except Exception as e:
            raise ValueError(f"Failed to load JSON string: {str(e)}")