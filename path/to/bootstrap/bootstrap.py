# complete code
import json
from pathlib import Path
from typing import Dict

from services.export_service import ExportService
from services.campaign_service import CampaignService

def main():
    # Load campaign data
    campaign_data = load_campaign_data()

    # Create export service
    export_service = ExportService(campaign_data)

    # Create campaign service
    campaign_service = CampaignService(campaign_data)

    # Export campaign data to JSON
    export_service.export_to_json('campaign_data.json')

def load_campaign_data() -> Dict:
    # Load campaign data from database or other source
    return {
        'campaign_name': 'My Campaign',
        'campaign_description': 'This is my campaign.',
        'campaign_data': {
            'npcs': ['NPC 1', 'NPC 2'],
            'locations': ['Location 1', 'Location 2'],
            'quests': ['Quest 1', 'Quest 2']
        }
    }

if __name__ == '__main__':
    main()