from bootstrap.config import load_config
from bootstrap.github_client import GitHubClient
from bootstrap.services.label_service import LabelService


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

    print("Bootstrap completed.")