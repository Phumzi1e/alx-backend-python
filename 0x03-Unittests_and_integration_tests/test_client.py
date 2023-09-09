#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import (
    GithubOrgClient
)
from fixtures import TEST_PAYLOAD


class NewGithubOrgClientTests(unittest.TestCase):
    """Tests for the `GithubOrgClient` class."""
    
    def test_org_request(self):
        """Test the `org` method for requesting organization info."""
        org_name = "openai"
        org_data = {'login': org_name}
        
        with patch("client.get_json") as mocked_get_json:
            mocked_get_json.return_value = org_data
            
            github_org_client = GithubOrgClient(org_name)
            result = github_org_client.org()
            
            self.assertEqual(result, org_data)
            mocked_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url_property(self):
        """Test the `_public_repos_url` property."""
        org_name = "openai"
        repos_url = f"https://api.github.com/orgs/{org_name}/repos"
        
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': repos_url}
            github_org_client = GithubOrgClient(org_name)
            result = github_org_client._public_repos_url
            
            self.assertEqual(result, repos_url)

    def test_public_repos_request(self):
        """Test the `public_repos` method for requesting public repositories."""
        org_name = "openai"
        repo1 = {"name": "repository1", "license": {"key": "mit"}}
        repo2 = {"name": "repository2", "license": {"key": "apache-2.0"}}
        repos_data = [repo1, repo2]
        
        with patch("client.get_json") as mocked_get_json, \
             patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_repos_url:
            mocked_get_json.return_value = repos_data
            mock_repos_url.return_value = f"https://api.github.com/orgs/{org_name}/repos"
            
            github_org_client = GithubOrgClient(org_name)
            result = github_org_client.public_repos()
            
            self.assertEqual(result, [repo1["name"], repo2["name"]])
            mock_repos_url.assert_called_once()
            mocked_get_json.assert_called_once()

    def test_has_license(self):
        """Test the `has_license` method."""
        org_name = "openai"
        repo = {"license": {"key": "mit"}}
        
        github_org_client = GithubOrgClient(org_name)
        
        # Check if the method correctly identifies the license
        result_true = github_org_client.has_license(repo, "mit")
        self.assertTrue(result_true)
        
        # Check if the method correctly identifies the absence of a license
        result_false = github_org_client.has_license(repo, "apache-2.0")
        self.assertFalse(result_false)

if __name__ == "__main__":
    unittest.main()

