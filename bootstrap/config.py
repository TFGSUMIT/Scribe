import os
from dataclasses import dataclass

from dotenv import load_dotenv

from bootstrap.utils.paths import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class Config:
    token: str
    owner: str
    repo: str
    project_name: str

def load_config():
    return Config(
        token = os.getenv("GITHUB_TOKEN"),
        owner = os.getenv("GITHUB_OWNER"),
        repo = os.getenv("GITHUB_REPO"),
        project_name = os.getenv(
            "PROJECT_NAME", 
            f"{os.getenv('GITHUB_REPO')} Project Board"
        )
    )
