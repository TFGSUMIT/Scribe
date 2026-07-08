# complete code
"""
Project Service

This module implements a project service that provides access to project data.
"""
from typing import Dict
from dataclasses import asdict
from bootstrap.utils.json_loader import JsonLoader

class ProjectService:
    """
    Project Service

    This class implements a project service that provides access to project data.
    """

    def __init__(self):
        """
        Initialize the project service.
        """
        self.project_data = JsonLoader.load_json("project.json")

    def get_project_data(self) -> Dict:
        """
        Get the project data.

        Returns:
            Dict: The project data.
        """
        return self.project_data