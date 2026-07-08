# complete code
"""
Service for campaign data.
"""
import json
from typing import Dict

from bootstrap.services.project_service import ProjectService
from bootstrap.services.issue_service import IssueService

class CampaignService:
    def __init__(self, project_service: ProjectService, issue_service: IssueService):
        self.project_service = project_service
        self.issue_service = issue_service

    def get_campaign_data(self) -> Dict:
        """
        Get the campaign data.
        """
        try:
            project_data = self.project_service.get_project_data()
            issue_data = self.issue_service.get_issue_data()
            campaign_data = self._generate_campaign_data(project_data, issue_data)
            return campaign_data
        except Exception as e:
            raise

    def _generate_campaign_data(self, project_data: Dict, issue_data: Dict) -> Dict:
        """
        Generate the campaign data from the project and issue data.
        """
        campaign_data = {
            "campaign_id": project_data["project_id"],
            "history": issue_data["issues"]
        }
        return campaign_data