#!/usr/bin/env python3
'''This module contains the declaration of class "MRUCache"'''
from collections import OrderedDict
from typing import Any, Hashable, Optional

from base_caching import BaseCaching


class MRUCache (BaseCaching):
    '''MRUCache: caching system using MRU replacement algorithm'''

    def __init__(self):
        '''Constructor'''
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key: Optional[Hashable], item: Optional[Any]):
        '''Add an item in the cache'''
        if key is None or item is None:
            return

        keys = self.cache_data.keys()
        if key in keys:
            self.cache_data.move_to_end(key)
        elif len(keys) >= self.MAX_ITEMS:
            popped_key, pooped_val = self.cache_data.popitem()
            print(f"DISCARD: {popped_key}")

        self.cache_data[key] = item

    def get(self, key: Optional[Hashable]) -> Optional[Any]:
        '''Get an item by key'''
        if key is None:
            return None

        if key in self.cache_data.keys():
            self.cache_data.move_to_end(key)
            return self.cache_data.get(key)
        return None
