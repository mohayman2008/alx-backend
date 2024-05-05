#!/usr/bin/env python3
'''This module contains the definition of the class "Server"'''
import csv
import math
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        '''Constructor'''
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            # truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        '''get_hyper_index: Fetch the appropriate page of the dataset alongside
        some state meta-data in a dictionary
        >
        @index: the current start index of the requested page number
            (Optional integer >=0)
        @page_size: the size of each page in the pagination system
            (have to be integer and greater than 0)
        >
        return: dictionary containing the requested page and the related
        state meta-data
        Key-> Value:
            index: the index of the first item in the current page
            next_index: the next index to query the next page with, it's the
                index of the item after the last item on the current page.
            page_size: the length of the returned dataset page
            data: the dataset page requested as list of rows
        '''
        dataset = self.indexed_dataset()
        keys = dataset.keys()
        data_len = len(keys)

        assert (index is None or
                (type(index) == (int) and 0 <= index < data_len))
        assert (type(page_size) == int and page_size > 0)

        index = index if index is not None else 0
        end = index + page_size
        end = end if end <= data_len else data_len

        if index >= data_len:
            data = []
        else:
            data = [dataset[i] for i in range(index, end) if i in keys]

        return {
            "index": index,
            "next_index": end if end < data_len else None,
            "page_size": len(data),
            "data": data
        }
