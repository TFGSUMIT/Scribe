# complete code
"""
Campaign
========

This module represents a campaign, which is the core data structure for Scribe.
It contains the campaign's history, including NPCs, locations, quests, items, encounters, and important events.

Classes:
    Campaign: The campaign class that represents the campaign data.
"""

from typing import Dict
from bootstrap.utils.json_loader import JsonLoader

class Campaign:
    def __init__(self, id: int, name: str, history: Dict):
        self.id = id
        self.name = name
        self.history = history

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Create a campaign object from a dictionary.

        Args:
            data (Dict): The dictionary containing the campaign data.

        Returns:
            Campaign: The campaign object created from the dictionary.
        """
        return cls(data["id"], data["name"], data["history"])

    def to_dict(self) -> Dict:
        """
        Convert the campaign data to a dictionary.

        Returns:
            Dict: The campaign data in dictionary format.
        """
        return {
            "id": self.id,
            "name": self.name,
            "history": self.history
        }