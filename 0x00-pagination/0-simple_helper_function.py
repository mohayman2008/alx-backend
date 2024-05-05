#!/usr/bin/env python3
'''This module contains the definition of the function "index_range"'''
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''index_range: calculates and return a tuple of size two containing
    a start index and an end index corresponding to the range of indexes
    in a list for pagination
    >
    @page: the page number to get the corresponding index for
    @page_size: the size of each page in the pagination system
    >
    return: tuple containing the start and end indices
    '''
    return ((page - 1) * page_size, page * page_size)
