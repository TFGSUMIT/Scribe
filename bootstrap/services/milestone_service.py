from bootstrap.github_client import GitHubClient
from bootstrap.utils.json_loader import load_json
from bootstrap.utils.markers import CREATED, DELETED, SKIPPED, UPDATED
from bootstrap.utils.paths import RESOURCES_DIR


class MilestoneService:
    def __init__(self, client: GitHubClient):
        self.client = client
        self.created = 0
        self.updated = 0
        self.skipped = 0
        self.deleted = 0

    def sync(self):
        desired_milestones = self._load_desired_milestones()
        existing_milestones = self._load_existing_milestones()

        for milestone in desired_milestones:
            self._sync_milestone(milestone, existing_milestones)

        self._delete_orphan_milestones(desired_milestones, existing_milestones)

        self._print_summary()

        # Re-fetch so callers (e.g. IssueService) get every milestone's
        # number, including the ones just created/updated above.
        return self._title_to_number(self._load_existing_milestones())

    def _load_desired_milestones(self):
        return load_json(RESOURCES_DIR / 'milestones.json')

    def _load_existing_milestones(self):
        milestones = self.client.get(f"{self.client.repo_url}/milestones")

        return {
            milestone['title']: milestone
            for milestone in milestones
        }

    def _title_to_number(self, milestones_by_title):
        return {
            title: milestone['number']
            for title, milestone in milestones_by_title.items()
        }

    def _sync_milestone(self, desired_milestone, existing_milestones):
        existing = existing_milestones.get(desired_milestone['title'])

        if existing is None:
            self._create_milestone(desired_milestone)
            return

        if self._milestones_are_equal(desired_milestone, existing):
            print(f"{SKIPPED} {desired_milestone['title']}")
            self.skipped += 1
            return

        self._update_milestone(desired_milestone, existing)

    def _create_milestone(self, milestone):
        print(f"{CREATED} {milestone['title']}")

        self.client.post(f"{self.client.repo_url}/milestones", milestone)

        self.created += 1

    def _update_milestone(self, milestone, existing):
        print(f"{UPDATED} {milestone['title']}")

        # The milestones API is keyed by number, not title — title is just a
        # field on the resource, so it can't be used as the URL identifier.
        self.client.patch(
            f"{self.client.repo_url}/milestones/{existing['number']}",
            milestone
        )

        self.updated += 1

    def _milestones_are_equal(self, desired, existing):
        return desired['description'] == existing['description']

    def _delete_orphan_milestones(self, desired_milestones, existing_milestones):
        desired_titles = {
            milestone['title']
            for milestone in desired_milestones
        }

        for milestone_title, existing in existing_milestones.items():
            if milestone_title not in desired_titles:
                self._delete_milestone(existing)

    def _delete_milestone(self, existing):
        print(f"{DELETED} {existing['title']}")

        self.client.delete(f"{self.client.repo_url}/milestones/{existing['number']}")

        self.deleted += 1

    def _print_summary(self):
        print('\nMilestones Summary:')
        print(f"Created: {self.created}")
        print(f"Updated: {self.updated}")
        print(f"Skipped: {self.skipped}")
        print(f"Deleted: {self.deleted}")