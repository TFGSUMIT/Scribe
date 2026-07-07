import httpx

from json import JSONDecodeError
from bootstrap.config import Config
from bootstrap.utils.logger import get_logger


logger = get_logger(__name__)


class GitHubClient:
    BASE_URL = "https://api.github.com"
    GRAPHQL_URL = f"{BASE_URL}/graphql"

    def __init__(self, config: Config):
        self.config = config
        self.repo_url = f"/repos/{config.owner}/{config.repo}"
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

    def paginate(self, endpoint: str):
        """GET every page of a REST list endpoint, following the `Link: rel="next"`
        header, and return all items concatenated into a single list."""
        items = []
        url = f"{self.BASE_URL}{endpoint}"

        while url:
            response = self._send("GET", url)
            items.extend(response.json())
            url = response.links.get("next", {}).get("url")

        return items

    def graphql(self, query: str, variables: dict = None):
        """Run a GraphQL query/mutation against the v4 API. Required for anything
        touching Projects v2, which has no REST equivalent."""
        logger.info("POST /graphql")
        logger.debug(f"query:\n{query.strip()}\nvariables: {variables or {}}")

        response = httpx.post(
            self.GRAPHQL_URL,
            headers = self.headers,
            json = {"query": query, "variables": variables or {}}
        )

        response.raise_for_status()

        payload = response.json()

        # GraphQL reports failures inside a 200 OK body, so raise_for_status()
        # alone would let a failed mutation through silently.
        if "errors" in payload:
            logger.error(f"GraphQL errors: {payload['errors']}")
            raise RuntimeError(f"GraphQL request failed: {payload['errors']}")

        return payload["data"]

    def _request(self, method: str, endpoint: str, body: dict = None):
        response = self._send(method, f"{self.BASE_URL}{endpoint}", body)

        try:
            return response.json()
        except JSONDecodeError:
            return None

    def _send(self, method: str, url: str, body: dict = None):
        logger.info(f"{method} {url}")

        if body is not None:
            logger.debug(f"body: {body}")

        response = httpx.request(method, url, headers = self.headers, json = body)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            logger.error(
                f"{method} {url} failed: {response.status_code} {response.text}"
            )
            raise error

        return response

