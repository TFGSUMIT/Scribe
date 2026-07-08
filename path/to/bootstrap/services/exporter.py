# complete code
"""
Exporter for campaign history in JSON format.
"""
import json
from typing import Dict

from bootstrap.services.campaign_service import CampaignService
from bootstrap.utils.json_loader import JsonLoader

class CampaignExporter:
    def __init__(self, campaign_service: CampaignService, json_loader: JsonLoader):
        self.campaign_service = campaign_service
        self.json_loader = json_loader

    def export(self) -> Dict:
        """
        Export the campaign history in JSON format.
        """
        try:
            campaign_data = self.campaign_service.get_campaign_data()
            exporter_data = self._generate_exporter_data(campaign_data)
            json_output = self.json_loader.load_json(exporter_data)
            return json_output
        except Exception as e:
            self.json_loader.log_error(f"Error exporting campaign history: {str(e)}")
            raise

    def _generate_exporter_data(self, campaign_data: Dict) -> Dict:
        """
        Generate the exporter data from the campaign data.
        """
        exporter_data = {
            "campaign_id": campaign_data["campaign_id"],
            "history": campaign_data["history"]
        }
        return exporter_data