#!/usr/bin/env python3
'''This module contains the definition of the helper function "index_range"
and the class "Server"'''
import csv
import math
from typing import Any, List, MutableMapping, Tuple, Union


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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        '''Constructor'''
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''get_page: Fetch the appropriate page of the dataset
        >
        @page: the page number (have to be integer and greater than 0)
        @page_size: the size of each page in the pagination system
            (have to be integer and greater than 0)
        >
        return: list of rows corresponding the requested page from the dataset
            If the requested page is out of range for the dataset,
            an empty list is returned instead.
        '''
        assert (type(page) == int and page > 0)
        assert (type(page_size) == int and page_size > 0)

        start, end = index_range(page, page_size)
        dataset = self.dataset()
        data_len = len(dataset)

        if start > data_len:
            return []
        if end > data_len:
            return dataset[start:]
        return dataset[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10
                  ) -> MutableMapping[str, Union[int, List[List]]]:
        '''get_hyper: Fetch the appropriate page of the dataset alongside
        some meta-data in a dictionary
        >
        @page: the page number (have to be integer and greater than 0)
        @page_size: the size of each page in the pagination system
            (have to be integer and greater than 0)
        >
        return: dictionary containing the requested page and the related
        meta-data
        Key-> Value:
            page_size: the length of the returned dataset page
            page: the current page number
            data: the dataset page requested as list of rows
            next_page: number of the next page, None if no next page
            prev_page: number of the previous page, None if no previous page
            total_pages: the total number of pages in the dataset
        '''
        hyper: MutableMapping[str, Any] = {}
        hyper["data"] = self.get_page(page, page_size)
        hyper["page_size"] = len(hyper["data"])
        hyper["page"] = page

        dataset_len = len(self.dataset())
        hyper["total_pages"] = math.ceil(dataset_len / page_size)

        start, end = index_range(page, page_size)

        if end >= dataset_len:
            hyper["next_page"] = None
        else:
            hyper["next_page"] = page + 1

        if page <= 1:
            hyper["prev_page"] = None
        else:
            hyper["prev_page"] = page - 1

        return hyper
