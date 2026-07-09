# complete code
"""
Campaign Exporter for JSON Format
--------------------------------

This module implements the campaign exporter for JSON format, which reconstructs the campaign's persisted data.
"""

import json
from typing import Dict, List

from bootstrap.campaign import Campaign
from bootstrap.services.campaign_service import CampaignService
from bootstrap.utils.json_loader import JSONLoader

class CampaignExporter:
    """
    Campaign Exporter for JSON Format
    """

    def __init__(self, campaign_service: CampaignService):
        """
        Initialize the campaign exporter with the campaign service.

        Args:
            campaign_service (CampaignService): The campaign service instance.
        """
        self.campaign_service = campaign_service

    def export(self, campaign_id: int) -> Dict:
        """
        Export the campaign's history in JSON format.

        Args:
            campaign_id (int): The campaign ID.

        Returns:
            Dict: The campaign's history in JSON format.
        """
        try:
            campaign = self.campaign_service.get_campaign(campaign_id)
            if campaign is None:
                raise ValueError("Campaign not found")

            history = self._reconstruct_history(campaign)
            return history

        except Exception as e:
            raise ValueError(f"Failed to export campaign history: {str(e)}")

    def _reconstruct_history(self, campaign: Campaign) -> Dict:
        """
        Reconstruct the campaign's history from the persisted data.

        Args:
            campaign (Campaign): The campaign instance.

        Returns:
            Dict: The campaign's history in JSON format.
        """
        history = {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "npcs": self._reconstruct_npcs(campaign),
            "locations": self._reconstruct_locations(campaign),
            "quests": self._reconstruct_quests(campaign),
            "items": self._reconstruct_items(campaign),
            "encounters": self._reconstruct_encounters(campaign),
            "events": self._reconstruct_events(campaign),
        }

        return history

    def _reconstruct_npcs(self, campaign: Campaign) -> List:
        """
        Reconstruct the NPCs from the persisted data.

        Args:
            campaign (Campaign): The campaign instance.

        Returns:
            List: The NPCs in JSON format.
        """
        npcs = []
        for npc in campaign.npcs:
            npc_data = {
                "id": npc.id,
                "name": npc.name,
                "description": npc.description,
            }
            npcs.append(npc_data)

        return npcs

    def _reconstruct_locations(self, campaign: Campaign) -> List:
        """
        Reconstruct the locations from the persisted data.

        Args:
            campaign (Campaign): The campaign instance.

        Returns:
            List: The locations in JSON format.
        """
        locations = []
        for location in campaign.locations:
            location_data = {
                "id": location.id,
                "name": location.name,
                "description": location.description,
            }
            locations.append(location_data)

        return locations

    def _reconstruct_quests(self, campaign: Campaign) -> List:
        """
        Reconstruct the quests from the persisted data.

        Args:
            campaign (Campaign): The campaign instance.

        Returns:
            List: The quests in JSON format.
        """
        quests = []
        for quest in campaign.quests:
            quest_data = {
                "id": quest.id,
                "name": quest.name,
                "description": quest.description,
            }
            quests.append(quest_data)

        return quests

    def _reconstruct_items(self, campaign: Campaign) -> List:
        """
        Reconstruct the items from the persisted data.

        Args:
            campaign (Campaign): The campaign instance.

        Returns:
            List: The items in JSON format.
        """
        items = []
        for item in campaign.items:
            item_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
            }
            items.append(item_data)

        return items

    def _reconstruct_encounters(self, campaign: Campaign) -> List:
        """
        Reconstruct the encounters from the persisted data.

        Args:
            campaign (Campaign): The campaign instance.

        Returns:
            List: The encounters in JSON format.
        """
        encounters = []
        for encounter in campaign.encounters:
            encounter_data = {
                "id": encounter.id,
                "name": encounter.name,
                "description": encounter.description,
            }
            encounters.append(encounter_data)

        return encounters

    def _reconstruct_events(self, campaign: Campaign) -> List:
        """
        Reconstruct the events from the persisted data.

        Args:
            campaign (Campaign): The campaign instance.

        Returns:
            List: The events in JSON format.
        """
        events = []
        for event in campaign.events:
            event_data = {
                "id": event.id,
                "name": event.name,
                "description": event.description,
            }
            events.append(event_data)

        return events