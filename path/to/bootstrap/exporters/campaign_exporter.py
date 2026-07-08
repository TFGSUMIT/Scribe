# complete code
"""
Campaign Exporter

This module implements a campaign exporter that exports the campaign's history to JSON.
"""
from typing import Dict, List
from dataclasses import asdict
from bootstrap.services.project_service import ProjectService
from bootstrap.utils.json_loader import JsonLoader

class CampaignExporter:
    """
    Campaign Exporter

    This class implements a campaign exporter that exports the campaign's history to JSON.
    """

    def __init__(self, project_service: ProjectService):
        """
        Initialize the campaign exporter.

        Args:
            project_service (ProjectService): The project service instance.
        """
        self.project_service = project_service

    def export(self) -> Dict:
        """
        Export the campaign's history to JSON.

        Returns:
            Dict: The campaign's history as a JSON object.
        """
        try:
            # Get the project data from the project service
            project_data = self.project_service.get_project_data()

            # Convert the project data to a dictionary
            project_dict = asdict(project_data)

            # Get the campaign history from the project data
            campaign_history = project_dict.get("campaign_history")

            # Convert the campaign history to a dictionary
            campaign_history_dict = asdict(campaign_history)

            # Return the campaign history as a JSON object
            return campaign_history_dict

        except Exception as e:
            # Handle any exceptions that occur during the export process
            print(f"Error exporting campaign history: {e}")
            return {}

def main():
    # Create a project service instance
    project_service = ProjectService()

    # Create a campaign exporter instance
    campaign_exporter = CampaignExporter(project_service)

    # Export the campaign's history to JSON
    campaign_history = campaign_exporter.export()

    # Print the campaign history
    print(campaign_history)

if __name__ == "__main__":
    main()