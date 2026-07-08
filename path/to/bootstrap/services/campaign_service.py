# complete code
import json
from pathlib import Path
from typing import Dict

class CampaignService:
    def __init__(self, campaign_data: Dict):
        self.campaign_data = campaign_data

    def get_campaign_data(self) -> Dict:
        return self.campaign_data