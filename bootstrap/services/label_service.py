from bootstrap.github_client import GitHubClient
from bootstrap.utils.json_loader import load_json
from bootstrap.utils.markers import CREATED, DELETED, SKIPPED, UPDATED
from bootstrap.utils.paths import RESOURCES_DIR


class LabelService:
    def __init__(self, client: GitHubClient):
        self.client = client
        self.created = 0
        self.updated = 0
        self.skipped = 0
        self.deleted = 0

    def sync(self):
        desired_labels = self._load_desired_labels()
        existing_labels = self._load_existing_labels()

        for label in desired_labels:
            self._sync_label(label, existing_labels)

        self._delete_orphan_labels(desired_labels, existing_labels)

        self._print_summary()

    def _load_desired_labels(self):
        return load_json(RESOURCES_DIR / 'labels.json')

    def _load_existing_labels(self):
        labels = self.client.get(f"{self.client.repo_url}/labels")

        return {
            label['name']: label
            for label in labels
        }

    def _sync_label(self, desired_label, existing_labels):
        existing = existing_labels.get(desired_label['name'])

        if existing is None:
            self._create_label(desired_label)
            return

        if self._labels_are_equal(desired_label, existing):
            print(f"{SKIPPED} {desired_label['name']}")
            self.skipped += 1
            return

        self._update_label(desired_label)

    def _create_label(self, label):
        print(f"{CREATED} {label['name']}")

        self.client.post(f"{self.client.repo_url}/labels", label)

        self.created += 1

    def _update_label(self, label):
        print(f"{UPDATED} {label['name']}")

        self.client.patch(
            f"{self.client.repo_url}/labels/{label['name']}",
            label
        )

        self.updated += 1

    def _labels_are_equal(self, desired, existing):
        return (
            desired['color'] == existing['color']
            and
            desired['description'] == existing['description']
        )

    def _delete_orphan_labels(self, desired_labels, existing_labels):
        desired_names = {
            label['name']
            for label in desired_labels
        }

        for label_name in existing_labels:
            if label_name not in desired_names:
                self._delete_label(label_name)

    def _delete_label(self, name):
        print(f"{DELETED} {name}")

        self.client.delete(f"{self.client.repo_url}/labels/{name}")

        self.deleted += 1

    def _print_summary(self):
        print('\nLabels Summary:')
        print(f"Created: {self.created}")
        print(f"Updated: {self.updated}")
        print(f"Skipped: {self.skipped}")
        print(f"Deleted: {self.deleted}")