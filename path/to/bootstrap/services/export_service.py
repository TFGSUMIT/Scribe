# complete code
import json
from pathlib import Path
from typing import Dict

class ExportService:
    def __init__(self, campaign_data: Dict):
        self.campaign_data = campaign_data

    def export_to_json(self, filename: str) -> bool:
        try:
            with open(filename, 'w') as file:
                json.dump(self.campaign_data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False