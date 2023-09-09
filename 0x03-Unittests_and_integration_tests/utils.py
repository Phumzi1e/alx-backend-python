#!/usr/bin/env python3
"""Utility functions for GitHub organization client.
"""
import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable

__all__ = ["nested_map_get", "fetch_json", "memoize"]

def nested_map_get(nested_map: Mapping, path: Sequence) -> Any:
    """Get a value from a nested map using a path of keys.
    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        A sequence of keys representing a path to the value
    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> nested_map_get(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map

def fetch_json(url: str) -> Dict:
    """Fetch JSON data from a remote URL.
    """
    response = requests.get(url)
    return response.json()

def memoize(fn: Callable) -> Callable:
    """Decorator to memoize a method.
    Example
    -------
    class MyClass:
        @memoize
        def a_method(self):
            print("a_method called")
            return 42
    >>> my_object = MyClass()
    >>> my_object.a_method
    a_method called
    42
    >>> my_object.a_method
    42
    """
    attr_name = f"_memo_{fn.__name__}"

    @wraps(fn)
    def memoized(self):
        """Memoized wrapper"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)

