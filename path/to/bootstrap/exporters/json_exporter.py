# complete code
"""
JSON Exporter for Campaign History
-----------------------------------

This module implements a custom JSON exporter for campaign history.
It utilizes the existing campaign data storage and serialization mechanisms
to ensure that the exported JSON data can be reconstructed into the original campaign data.

Classes:
    JsonExporter: A custom JSON exporter that implements the export interface from Core.
"""

import json
from typing import Dict, List
from bootstrap.campaign.campaign import Campaign
from bootstrap.utils.json_loader import JsonLoader

class JsonExporter:
    def __init__(self, campaign: Campaign):
        self.campaign = campaign
        self.json_loader = JsonLoader()

    def export(self) -> Dict:
        """
        Export the campaign history as a JSON object.

        Returns:
            A dictionary representing the campaign history in JSON format.
        """
        try:
            # Serialize campaign data into a JSON object
            json_data = self.json_loader.serialize(self.campaign.data)
            return json_data
        except Exception as e:
            # Handle any errors that occur during serialization
            print(f"Error serializing campaign data: {e}")
            return None

    def load(self, json_data: Dict) -> Campaign:
        """
        Load the campaign history from a JSON object.

        Args:
            json_data: A dictionary representing the campaign history in JSON format.

        Returns:
            A Campaign object representing the loaded campaign history.
        """
        try:
            # Deserialize JSON data into a Campaign object
            campaign_data = self.json_loader.deserialize(json_data)
            return Campaign(campaign_data)
        except Exception as e:
            # Handle any errors that occur during deserialization
            print(f"Error deserializing campaign data: {e}")
            return None