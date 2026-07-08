# complete code
"""
Test Exporters

This module implements tests for the campaign exporter.
"""
import unittest
from bootstrap.exporters.campaign_exporter import CampaignExporter
from bootstrap.services.project_service import ProjectService
from bootstrap.utils.json_loader import JsonLoader

class TestCampaignExporter(unittest.TestCase):
    """
    Test Campaign Exporter

    This class implements tests for the campaign exporter.
    """

    def setUp(self):
        # Create a project service instance
        self.project_service = ProjectService()

        # Create a campaign exporter instance
        self.campaign_exporter = CampaignExporter(self.project_service)

    def test_export(self):
        # Export the campaign's history to JSON
        campaign_history = self.campaign_exporter.export()

        # Assert that the campaign history is not empty
        self.assertIsNotNone(campaign_history)

if __name__ == "__main__":
    unittest.main()