# complete code
"""
JSON Loader

This module implements a JSON loader that loads JSON data from files.
"""
import json
from pathlib import Path

class JsonLoader:
    """
    JSON Loader

    This class implements a JSON loader that loads JSON data from files.
    """

    @staticmethod
    def load_json(file_path: str) -> Dict:
        """
        Load JSON data from a file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            Dict: The JSON data.
        """
        try:
            # Load the JSON data from the file
            with Path(file_path).open("r") as file:
                json_data = json.load(file)

            # Return the JSON data
            return json_data

        except Exception as e:
            # Handle any exceptions that occur during the loading process
            print(f"Error loading JSON data: {e}")
            return {}