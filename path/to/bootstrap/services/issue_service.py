# complete code
"""
Service for issue data.
"""
import json
from typing import Dict

class IssueService:
    def get_issue_data(self) -> Dict:
        """
        Get the issue data.
        """
        try:
            issue_data = {
                "issues": [
                    {
                        "issue_id": 1,
                        "title": "Issue 1",
                        "description": "This is issue 1."
                    },
                    {
                        "issue_id": 2,
                        "title": "Issue 2",
                        "description": "This is issue 2."
                    }
                ]
            }
            return issue_data
        except Exception as e:
            raise