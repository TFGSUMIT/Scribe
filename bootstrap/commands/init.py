from bootstrap.config import load_config
from bootstrap.github_client import GitHubClient
from bootstrap.services.issue_service import IssueService
from bootstrap.services.label_service import LabelService
from bootstrap.services.milestone_service import MilestoneService
from bootstrap.services.project_service import ProjectService


def initialize():
    print("Loading configuration...")

    config = load_config()
    client = GitHubClient(config)
    user = client.get("/user")

    print(f"Connected as {user['login']}")

    print()

    print("Synchronizing labels...")
    LabelService(client).sync()

    print()

    print("Synchronizing milestones...")
    # {title: number} — issues need the milestone's number, not its title.
    milestones = MilestoneService(client).sync()

    print()

    print("Synchronizing project board...")
    # {project_id, fields, options} — issues need this to be added to the
    # board and have their Epic/Sprint/Story Points fields filled in.
    project = ProjectService(client).sync()

    print()

    print("Synchronizing issues...")
    IssueService(client, milestones, project).sync()

    print()

    print("Bootstrap completed.")