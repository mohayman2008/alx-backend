#!/usr/bin/env python3
'''This module contains the declaration of class "LFUCache"'''
import datetime
from typing import Any, Hashable, Optional

from base_caching import BaseCaching

now = datetime.datetime.now


class LFUCache (BaseCaching):
    '''LFUCache: caching system using LFU replacement algorithm'''

    def __init__(self):
        '''Constructor'''
        super().__init__()
        # self.access_data contain data about each key item in the form
        # {key: (access_count, last_access_time), ...}
        self.access_data = {}

    def put(self, key: Optional[Hashable], item: Optional[Any]):
        '''Add an item in the cache'''
        if key is None or item is None:
            return

        keys = list(self.cache_data.keys())
        ad = self.access_data

        if key in keys:
            ad[key] = (ad[key][0] + 1, now())
        elif len(keys) >= self.MAX_ITEMS:
            lf_lru = keys[0]  # least-frequent least-recently used
            count, last_accessed = ad[lf_lru]

            for k in keys[1:]:
                if ad[k][0] < count or (ad[k][0] == count and
                                        ad[k][1] < last_accessed):
                    lf_lru = k
                    count, last_accessed = ad[k]
            print(f"DISCARD: {lf_lru}")
            del ad[lf_lru]
            del self.cache_data[lf_lru]

            ad[key] = (1, now())
        else:
            ad[key] = (1, now())

        self.cache_data[key] = item

    def get(self, key: Optional[Hashable]) -> Optional[Any]:
        '''Get an item by key'''
        if key is None:
            return None

        if key in self.cache_data.keys():
            self.access_data[key] = (self.access_data.get(key, (0,))[0] + 1,
                                     now())
            return self.cache_data.get(key)
        return None
