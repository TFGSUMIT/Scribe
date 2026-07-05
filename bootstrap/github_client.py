import httpx

from bootstrap.config import Config

BASE_URL = "https://api.github.com"

class GitHubClient:

    def __init__(self, config: Config):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.token}",
            "Accept": "application/vnd.github+json"
        }

    def get(self, endpoint: str):
        return self._request("GET", endpoint)

    def post(self, endpoint: str, body: dict):
        return self._request("POST", endpoint, body)

    def patch(self, endpoint: str, body: dict):
        return self._request("PATCH", endpoint, body)

    def put(self, endpoint: str, body: dict):
        return self._request("PUT", endpoint, body)

    def delete(self, endpoint: str):
        return self._request("DELETE", endpoint)

    # def graphql(self, endpoint: str):

    # def paginate(self, endpoint: str):

    def _request(self, method: str, endpoint: str, body: dict = None):
        response = httpx.request(
            method,
            f"{BASE_URL}{endpoint}",
            headers = self.headers,
            json = body
        )

        response.raise_for_status()

        return response.json()
