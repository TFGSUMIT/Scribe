# complete code
"""
Service for milestone data.
"""
import json
from typing import Dict

class MilestoneService:
    def get_milestone_data(self) -> Dict:
        """
        Get the milestone data.
        """
        try:
            milestone_data = {
                "milestone_name": "Milestone 1"
            }
            return milestone_data
        except Exception as e:
            raise