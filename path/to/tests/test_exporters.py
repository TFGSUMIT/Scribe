# complete code
"""
Unit Tests for JSON Exporter
---------------------------

This module provides unit tests for the JsonExporter class.
It tests the export and load methods to ensure they work correctly.

Imports:
    from bootstrap.exporters.json_exporter import JsonExporter
    from bootstrap.campaign.campaign import Campaign
    from bootstrap.utils.json_loader import JsonLoader
"""

import unittest
from unittest.mock import Mock
from bootstrap.exporters.json_exporter import JsonExporter
from bootstrap.campaign.campaign import Campaign
from bootstrap.utils.json_loader import JsonLoader

class TestJsonExporter(unittest.TestCase):
    def test_export(self):
        # Create a mock campaign object
        campaign = Mock(spec=Campaign)
        campaign.data = {"key": "value"}

        # Create a JsonExporter instance
        exporter = JsonExporter(campaign)

        # Export the campaign data
        json_data = exporter.export()

        # Assert that the exported data is correct
        self.assertEqual(json_data, {"key": "value"})

    def test_load(self):
        # Create a mock JSON data object
        json_data = {"key": "value"}

        # Create a JsonLoader instance
        loader = JsonLoader()

        # Load the JSON data
        campaign = loader.deserialize(json_data)

        # Assert that the loaded data is correct
        self.assertEqual(campaign.data, {"key": "value"})

if __name__ == "__main__":
    unittest.main()