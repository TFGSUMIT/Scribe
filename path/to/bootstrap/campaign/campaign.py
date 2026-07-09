# complete code
"""
Campaign Data Storage and Serialization
---------------------------------------

This module provides a Campaign class that stores and serializes campaign data.
It also defines methods for loading and saving campaign data.

Classes:
    Campaign: A class representing a campaign with stored data and serialization methods.
"""

import dataclasses
from typing import Dict

@dataclasses.dataclass
class Campaign:
    data: Dict

    def serialize(self) -> Dict:
        """
        Serialize the campaign data into a dictionary.

        Returns:
            A dictionary representing the campaign data.
        """
        return dataclasses.asdict(self)

    def deserialize(self, data: Dict) -> Dict:
        """
        Deserialize a dictionary into campaign data.

        Args:
            data: A dictionary representing the campaign data.

        Returns:
            A dictionary representing the deserialized campaign data.
        """
        return dataclasses.asdict(dataclasses.make_dataclass("Campaign", dataclasses.fields(self)))