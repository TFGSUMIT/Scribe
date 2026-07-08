# complete code
"""
Service for label data.
"""
import json
from typing import Dict

class LabelService:
    def get_label_data(self) -> Dict:
        """
        Get the label data.
        """
        try:
            label_data = {
                "label_id": 1,
                "name": "Label 1"
            }
            return label_data
        except Exception as e:
            raise