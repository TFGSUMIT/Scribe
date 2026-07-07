from bootstrap.github_client import GitHubClient
from bootstrap.utils.json_loader import load_json
from bootstrap.utils.logger import get_logger
from bootstrap.utils.markers import CREATED, SKIPPED
from bootstrap.utils.paths import RESOURCES_DIR

logger = get_logger(__name__)


class IssueService:
    """Creates the backlog issues and places each one on the project board
    with its Epic/Sprint/Story Points fields filled in.

    Unlike labels and milestones, issues are never deleted here: closing or
    removing a real GitHub issue is a product decision, not something a
    reconcile script should do automatically.
    """

    def __init__(self, client: GitHubClient, milestones: dict, project: dict):
        self.client = client
        # {title: number}, from MilestoneService.sync()
        self.milestones = milestones
        # {project_id, fields, options}, from ProjectService.sync()
        self.project = project
        self.created = 0
        self.skipped = 0

    def sync(self):
        desired_issues = self._load_desired_issues()
        existing_issues = self._load_existing_issues()

        for issue in desired_issues:
            self._sync_issue(issue, existing_issues)

        self._print_summary()

    def _load_desired_issues(self):
        issues_dir = RESOURCES_DIR / "issues"
        issues = []

        # Every *.json file under resources/issues/ contributes issues — this
        # lets the backlog be split by epic instead of one giant file.
        for path in sorted(issues_dir.glob("*.json")):
            issues.extend(load_json(path))

        return issues

    def _load_existing_issues(self):
        # state=all so an issue that was already closed isn't recreated.
        issues = self.client.paginate(f"{self.client.repo_url}/issues?state=all")

        return {
            issue["title"]: issue
            for issue in issues
            if "pull_request" not in issue  # the issues endpoint also lists PRs
        }

    def _sync_issue(self, desired, existing_issues):
        existing = existing_issues.get(desired["title"])

        if existing is None:
            issue = self._create_issue(desired)
            self.created += 1
        else:
            print(f"{SKIPPED} {desired['title']}")
            self.skipped += 1
            issue = existing

        self._add_to_project(issue, desired)

    def _create_issue(self, desired):
        print(f"{CREATED} {desired['title']}")

        body = {
            "title": desired["title"],
            "body": desired.get("body", ""),
            "labels": desired.get("labels", []),
        }

        milestone_title = desired.get("milestone")

        if milestone_title:
            milestone_number = self.milestones.get(milestone_title)

            if milestone_number is None:
                logger.warning(
                    f"Milestone '{milestone_title}' not found for issue "
                    f"'{desired['title']}' — creating without a milestone."
                )
            else:
                body["milestone"] = milestone_number

        return self.client.post(f"{self.client.repo_url}/issues", body)

    # --- Project board ------------------------------------------------

    def _add_to_project(self, issue, desired):
        # addProjectV2ItemById is idempotent — adding the same issue twice
        # returns the existing item instead of duplicating it, so this is
        # safe to run again even for issues that were skipped above.
        item_id = self._add_item(issue["node_id"])

        self._set_option_field(item_id, "Epic", desired.get("epic"))
        self._set_option_field(item_id, "Sprint", desired.get("sprint"))
        self._set_number_field(item_id, "Story Points", desired.get("story_points"))

    def _add_item(self, content_id):
        data = self.client.graphql(
            """
            mutation($projectId: ID!, $contentId: ID!) {
              addProjectV2ItemById(
                input: {projectId: $projectId, contentId: $contentId}
              ) {
                item { id }
              }
            }
            """,
            {"projectId": self.project["project_id"], "contentId": content_id},
        )

        return data["addProjectV2ItemById"]["item"]["id"]

    def _set_option_field(self, item_id, field_name, option_name):
        if option_name is None:
            return

        field_id = self.project["fields"].get(field_name)
        option_id = self.project["options"].get(field_name, {}).get(option_name)

        if field_id is None or option_id is None:
            logger.warning(
                f"Skipping '{field_name}' = '{option_name}' — field or option "
                "not found on the project."
            )
            return

        self._set_field_value(item_id, field_id, {"singleSelectOptionId": option_id})

    def _set_number_field(self, item_id, field_name, value):
        if value is None:
            return

        field_id = self.project["fields"].get(field_name)

        if field_id is None:
            logger.warning(f"Skipping '{field_name}' — field not found on the project.")
            return

        self._set_field_value(item_id, field_id, {"number": value})

    def _set_field_value(self, item_id, field_id, value):
        self.client.graphql(
            """
            mutation(
              $projectId: ID!
              $itemId: ID!
              $fieldId: ID!
              $value: ProjectV2FieldValue!
            ) {
              updateProjectV2ItemFieldValue(
                input: {
                  projectId: $projectId
                  itemId: $itemId
                  fieldId: $fieldId
                  value: $value
                }
              ) {
                projectV2Item { id }
              }
            }
            """,
            {
                "projectId": self.project["project_id"],
                "itemId": item_id,
                "fieldId": field_id,
                "value": value,
            },
        )

    def _print_summary(self):
        print('\nIssues Summary:')
        print(f"Created: {self.created}")
        print(f"Skipped: {self.skipped}")
