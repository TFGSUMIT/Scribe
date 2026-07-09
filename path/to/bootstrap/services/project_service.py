# complete code
"""
Project Service
==============

This module provides a project service that retrieves the campaign data from the database.

Classes:
    ProjectService: The project service class that retrieves the campaign data.
"""

from typing import Dict
from bootstrap.database import Database

class ProjectService:
    def __init__(self, database: Database):
        self.database = database

    def get_campaign(self, id: int) -> Dict:
        """
        Retrieve the campaign data from the database.

        Args:
            id (int): The ID of the campaign to retrieve.

        Returns:
            Dict: The campaign data retrieved from the database.
        """
        try:
            # Retrieve the campaign data from the database
            campaign_data = self.database.get_campaign(id)
            return campaign_data
        except Exception as e:
            # Handle any errors that occur during retrieval
            print(f"Error retrieving campaign: {e}")
            return {}