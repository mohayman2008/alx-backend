#!/usr/bin/env python3
'''This module contains the declaration of class "BasicCache"'''
from typing import Any, Hashable, Optional

from base_caching import BaseCaching


class BasicCache (BaseCaching):
    '''BasicCache: Basic caching system'''

    def put(self, key: Optional[Hashable], item: Optional[Any]):
        '''Add an item in the cache'''
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key: Optional[Hashable]) -> Optional[Any]:
        '''Get an item by key'''
        if key is None:
            return None
        return self.cache_data.get(key, None)
