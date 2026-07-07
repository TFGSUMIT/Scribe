from bootstrap.github_client import GitHubClient
from bootstrap.utils.json_loader import load_json
from bootstrap.utils.logger import get_logger
from bootstrap.utils.markers import CREATED, SKIPPED
from bootstrap.utils.paths import RESOURCES_DIR

logger = get_logger(__name__)

# GitHub Projects (v2) lives entirely behind the GraphQL API — there is no
# REST equivalent for creating a project board or its custom fields.
#
# Also: "views" (the Board/Table/Roadmap layouts described in views.json)
# have no mutation anywhere in the public schema. They can only be created
# and arranged by hand in the GitHub UI, so views.json stays as
# documentation only — this service never touches it.

_DATA_TYPE_BY_FIELD_TYPE = {
    "single_select": "SINGLE_SELECT",
    "number": "NUMBER",
}


class ProjectService:
    def __init__(self, client: GitHubClient):
        self.client = client
        self.project_created = False
        self.fields_created = 0
        self.fields_skipped = 0

    def sync(self):
        desired = self._load_desired_project()
        viewer_id = self._fetch_viewer_id()

        project = self._find_or_create_project(
            viewer_id, desired["name"], desired.get("description")
        )
        self._ensure_linked_to_repository(project["id"])

        field_ids, option_ids = self._sync_fields(project["id"], desired["fields"])

        self._print_summary()

        # Context the IssueService needs to add issues to the board and fill
        # in their Epic/Sprint/Story Points values.
        return {
            "project_id": project["id"],
            "fields": field_ids,
            "options": option_ids,
        }

    def _load_desired_project(self):
        return load_json(RESOURCES_DIR / "project.json")

    # --- Project ---------------------------------------------------------

    def _fetch_viewer_id(self):
        data = self.client.graphql("query { viewer { id } }")
        return data["viewer"]["id"]

    def _find_or_create_project(self, viewer_id, title, description):
        existing = self._find_project(title)

        if existing:
            print(f"{SKIPPED} Project: {title}")
            return existing

        return self._create_project(viewer_id, title, description)

    def _find_project(self, title):
        data = self.client.graphql(
            """
            query {
              viewer {
                projectsV2(first: 100) {
                  nodes { id title }
                }
              }
            }
            """
        )

        for project in data["viewer"]["projectsV2"]["nodes"]:
            if project["title"] == title:
                return project

        return None

    def _create_project(self, viewer_id, title, description):
        print(f"{CREATED} Project: {title}")

        data = self.client.graphql(
            """
            mutation($ownerId: ID!, $title: String!) {
              createProjectV2(input: {ownerId: $ownerId, title: $title}) {
                projectV2 { id title }
              }
            }
            """,
            {"ownerId": viewer_id, "title": title},
        )

        project = data["createProjectV2"]["projectV2"]
        self.project_created = True

        if description:
            self._set_project_description(project["id"], description)

        return project

    def _set_project_description(self, project_id, description):
        self.client.graphql(
            """
            mutation($projectId: ID!, $description: String!) {
              updateProjectV2(
                input: {projectId: $projectId, shortDescription: $description}
              ) {
                projectV2 { id }
              }
            }
            """,
            {"projectId": project_id, "description": description},
        )

    def _ensure_linked_to_repository(self, project_id):
        repository = self.client.get(self.client.repo_url)
        repository_id = repository["node_id"]

        if self._is_already_linked(project_id, repository_id):
            return

        self.client.graphql(
            """
            mutation($projectId: ID!, $repositoryId: ID!) {
              linkProjectV2ToRepository(
                input: {projectId: $projectId, repositoryId: $repositoryId}
              ) {
                repository { id }
              }
            }
            """,
            {"projectId": project_id, "repositoryId": repository_id},
        )

    def _is_already_linked(self, project_id, repository_id):
        data = self.client.graphql(
            """
            query($id: ID!) {
              node(id: $id) {
                ... on Repository {
                  projectsV2(first: 50) {
                    nodes { id }
                  }
                }
              }
            }
            """,
            {"id": repository_id},
        )

        linked_ids = {node["id"] for node in data["node"]["projectsV2"]["nodes"]}
        return project_id in linked_ids

    # --- Fields ------------------------------------------------------------

    def _sync_fields(self, project_id, desired_fields):
        existing_fields = self._load_existing_fields(project_id)

        field_ids = {}
        option_ids = {}

        for field in desired_fields:
            existing = existing_fields.get(field["name"])

            if existing is None:
                existing = self._create_field(project_id, field)
                self.fields_created += 1
            else:
                print(f"{SKIPPED} Field: {field['name']}")
                self.fields_skipped += 1
                self._warn_about_missing_options(field, existing)

            field_ids[field["name"]] = existing["id"]
            option_ids[field["name"]] = {
                option["name"]: option["id"]
                for option in existing.get("options", [])
            }

        return field_ids, option_ids

    def _load_existing_fields(self, project_id):
        data = self.client.graphql(
            """
            query($projectId: ID!) {
              node(id: $projectId) {
                ... on ProjectV2 {
                  fields(first: 50) {
                    nodes {
                      ... on ProjectV2FieldCommon {
                        id
                        name
                      }
                      ... on ProjectV2SingleSelectField {
                        options { id name }
                      }
                    }
                  }
                }
              }
            }
            """,
            {"projectId": project_id},
        )

        return {
            field["name"]: field
            for field in data["node"]["fields"]["nodes"]
            if field.get("name")
        }

    def _create_field(self, project_id, field):
        print(f"{CREATED} Field: {field['name']}")

        variables = {
            "projectId": project_id,
            "dataType": _DATA_TYPE_BY_FIELD_TYPE[field["type"]],
            "name": field["name"],
            "options": self._build_options_input(field),
        }

        data = self.client.graphql(
            """
            mutation(
              $projectId: ID!
              $dataType: ProjectV2CustomFieldType!
              $name: String!
              $options: [ProjectV2SingleSelectFieldOptionInput!]
            ) {
              createProjectV2Field(
                input: {
                  projectId: $projectId
                  dataType: $dataType
                  name: $name
                  singleSelectOptions: $options
                }
              ) {
                projectV2Field {
                  ... on ProjectV2FieldCommon { id name }
                  ... on ProjectV2SingleSelectField { id name options { id name } }
                }
              }
            }
            """,
            variables,
        )

        return data["createProjectV2Field"]["projectV2Field"]

    def _build_options_input(self, field):
        if field["type"] != "single_select":
            return None

        return [
            {"name": option, "color": "GRAY", "description": ""}
            for option in field["options"]
        ]

    def _warn_about_missing_options(self, desired_field, existing_field):
        if desired_field["type"] != "single_select":
            return

        existing_names = {
            option["name"] for option in existing_field.get("options", [])
        }
        missing = [
            name for name in desired_field["options"] if name not in existing_names
        ]

        if not missing:
            return

        # Replacing a single-select field's options via the API re-creates
        # every option with a new id, which would silently wipe the value
        # already set on any existing project item. Safer to flag it and let
        # a human add the missing options by hand in the project settings.
        logger.warning(
            f"Field '{desired_field['name']}' is missing options {missing} — "
            "add them manually in the project settings."
        )

    def _print_summary(self):
        print('\nProject Summary:')
        print(f"Project created: {self.project_created}")
        print(f"Fields created: {self.fields_created}")
        print(f"Fields skipped: {self.fields_skipped}")
