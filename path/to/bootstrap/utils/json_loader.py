# complete code
"""
JSON Loader and Serializer
---------------------------

This module provides a JsonLoader class that loads and serializes JSON data.
It uses the json module for loading and serializing JSON data.

Classes:
    JsonLoader: A class representing a JSON loader and serializer.
"""

import json
from typing import Dict

class JsonLoader:
    def serialize(self, data: Dict) -> Dict:
        """
        Serialize the given data into a JSON object.

        Args:
            data: A dictionary representing the data to serialize.

        Returns:
            A dictionary representing the serialized data in JSON format.
        """
        return json.loads(json.dumps(data))

    def deserialize(self, json_data: Dict) -> Dict:
        """
        Deserialize a JSON object into a dictionary.

        Args:
            json_data: A dictionary representing the JSON data.

        Returns:
            A dictionary representing the deserialized JSON data.
        """
        return json.loads(json.dumps(json_data))