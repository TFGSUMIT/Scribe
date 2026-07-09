# complete code
"""
Campaign Service
----------------

This module provides the campaign service, which handles the campaign data storage and retrieval.
"""

import logging

from bootstrap.campaign import Campaign
from bootstrap.exporters.campaign_exporter import CampaignExporter

logger = logging.getLogger(__name__)

class CampaignService:
    """
    Campaign Service
    """

    def __init__(self):
        """
        Initialize the campaign service.
        """
        self.campaign_exporter = CampaignExporter(self)

    def get_campaign(self, campaign_id: int) -> Campaign:
        """
        Get the campaign by ID.

        Args:
            campaign_id (int): The campaign ID.

        Returns:
            Campaign: The campaign instance.
        """
        try:
            campaign = Campaign.query.get(campaign_id)
            if campaign is None:
                raise ValueError("Campaign not found")

            return campaign

        except Exception as e:
            logger.error(f"Failed to get campaign: {str(e)}")
            raise ValueError("Failed to get campaign")

    def export_campaign(self, campaign_id: int) -> str:
        """
        Export the campaign's history in JSON format.

        Args:
            campaign_id (int): The campaign ID.

        Returns:
            str: The campaign's history in JSON format.
        """
        try:
            history = self.campaign_exporter.export(campaign_id)
            json_data = json.dumps(history, indent=4)
            return json_data

        except Exception as e:
            logger.error(f"Failed to export campaign history: {str(e)}")
            raise ValueError("Failed to export campaign history")