# complete code
"""
Service for project data.
"""
import json
from typing import Dict

from bootstrap.services.label_service import LabelService
from bootstrap.services.milestone_service import MilestoneService

class ProjectService:
    def __init__(self, label_service: LabelService, milestone_service: MilestoneService):
        self.label_service = label_service
        self.milestone_service = milestone_service

    def get_project_data(self) -> Dict:
        """
        Get the project data.
        """
        try:
            label_data = self.label_service.get_label_data()
            milestone_data = self.milestone_service.get_milestone_data()
            project_data = self._generate_project_data(label_data, milestone_data)
            return project_data
        except Exception as e:
            raise

    def _generate_project_data(self, label_data: Dict, milestone_data: Dict) -> Dict:
        """
        Generate the project data from the label and milestone data.
        """
        project_data = {
            "project_id": label_data["label_id"],
            "name": milestone_data["milestone_name"]
        }
        return project_data