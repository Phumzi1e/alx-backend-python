#!/usr/bin/env python3
"""GitHub Organization Client
"""
from typing import List, Dict
from utils import get_json, access_nested_map, memoize

class GithubOrgClient:
    """GitHub Organization Client
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize the GitHubOrgClient"""
        self._org_name = org_name

    @memoize
    def org_info(self) -> Dict:
        """Memoized organization information"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def public_repos_url(self) -> str:
        """Public repositories URL"""
        return self.org_info()["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """Memoized repositories payload"""
        return get_json(self.public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """List public repositories optionally filtered by license"""
        json_payload = self.repos_payload()
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]

        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if a repository has a specific license"""
        assert license_key is not None, "license_key cannot be None"
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False

