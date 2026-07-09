# complete code
"""
Campaign Exporter
================

This module implements a campaign exporter that adheres to Core's export interface.
It exports the campaign's history, including NPCs, locations, quests, items, encounters, and important events.
The exporter also reconstructs the campaign's persisted data from the exported JSON.

Classes:
    CampaignExporter: The campaign exporter class that implements the export interface.
"""

import json
from typing import Dict, List
from bootstrap.campaign import Campaign
from bootstrap.services.project_service import ProjectService

class CampaignExporter:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def export(self, campaign: Campaign) -> Dict:
        """
        Export the campaign's history to JSON.

        Args:
            campaign (Campaign): The campaign to export.

        Returns:
            Dict: The exported campaign data in JSON format.
        """
        try:
            # Serialize the campaign data to JSON
            campaign_data = json.dumps(campaign.to_dict())
            return json.loads(campaign_data)
        except Exception as e:
            # Handle any errors that occur during serialization
            print(f"Error exporting campaign: {e}")
            return {}

    def reconstruct(self, json_data: Dict) -> Campaign:
        """
        Reconstruct the campaign's persisted data from the exported JSON.

        Args:
            json_data (Dict): The exported campaign data in JSON format.

        Returns:
            Campaign: The reconstructed campaign data.
        """
        try:
            # Deserialize the JSON data into a campaign object
            campaign_data = json.loads(json.dumps(json_data))
            return Campaign.from_dict(campaign_data)
        except Exception as e:
            # Handle any errors that occur during deserialization
            print(f"Error reconstructing campaign: {e}")
            return Campaign()