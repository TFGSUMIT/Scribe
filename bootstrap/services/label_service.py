from bootstrap.github_client import GitHubClient
from bootstrap.utils.json_loader import load_json
from bootstrap.utils.paths import RESOURCES_DIR


class LabelService:

    def __init__(self, client: GitHubClient):
        self.client = client

    def sync(self):
        labels = load_json(RESOURCES_DIR / "labels.json")

        print(f"Found {len(labels)} labels.")

        existing = self.client.get(
            f"/repos/{self.client.config.owner}/{self.client.config.repo}/labels"
        )

        existing_names = {
            label["name"] for label in existing
        }

        for label in labels:
            if label["name"] in existing_names:
                print(f"⏭ {label['name']} already exists.")
                continue

            print(f"➕ Creating {label['name']}")

            self.client.post(
                f"/repos/{self.client.config.owner}/{self.client.config.repo}/labels",
                label
            )
