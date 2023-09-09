#!/usr/bin/env python3
"""A module for testing the utilities module.
"""
import unittest
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock
from parameterized import parameterized

from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class NewAccessNestedMapTests(unittest.TestCase):
    """Tests for the `access_nested_map` function."""
    
    def test_access_nested_map_existing_key(self):
        """Test `access_nested_map` with an existing key."""
        nested_map = {"a": {"b": 2}}
        path = ("a", "b")
        expected = 2
        
        result = access_nested_map(nested_map, path)
        
        self.assertEqual(result, expected)

    def test_access_nested_map_missing_key(self):
        """Test `access_nested_map` with a missing key."""
        nested_map = {"a": 1}
        path = ("a", "b")
        
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class NewGetJsonTests(unittest.TestCase):
    """Tests for the `get_json` function."""
    
    def test_get_json_with_mocked_request(self):
        """Test `get_json` with a mocked request."""
        test_url = "http://example.com"
        test_payload = {"payload": True}
        
        attrs = {'json.return_value': test_payload}
        with patch("requests.get", return_value=Mock(**attrs)) as req_get:
            result = get_json(test_url)
            
            self.assertEqual(result, test_payload)
            req_get.assert_called_once_with(test_url)

class NewMemoizeTests(unittest.TestCase):
    """Tests for the `memoize` decorator."""
    
    def test_memoize_cache(self):
        """Test `memoize` caching."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        
        with patch.object(TestClass, "a_method", return_value=42) as memo_fxn:
            test_class = TestClass()
            result1 = test_class.a_property()
            result2 = test_class.a_property()
            
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            memo_fxn.assert_called_once()

if __name__ == "__main__":
    unittest.main()

