import json
from collections import Iterator


class DatasetInfo:
    def __init__(self, info_addr):
        with open(info_addr) as f:
            info = json.load(f)
            for info_key, info_value in info.items():
                setattr(self, info_key, info_value)


class BaseIterator(Iterator):

    def __init__(self, iterator, num_lines):
        self.iterator = iterator
        self.num_lines = num_lines
        self.current_pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        # if self.current_pos == self.num_lines - 1:
        #     raise StopIteration
        item = next(self.iterator)
        if self.current_pos is None:
            self.current_pos = 0
        else:
            self.current_pos += 1
        return item

    def __len__(self):
        return self.num_lines

    def pos(self):
        """
        Returns current position of the iterator. This returns None
        if the iterator hasn't been used yet.
        """
        return self.current_pos


class BaseDataset:
    """Abstract dataset class for dataset-like object, like list and array.
    All datasets(sub-classes) should inherit.
    Args:
        data (list, array, tuple): dataset-like object
    """

    def __init__(self, info):
        self.info = info

    def set_iterators(self, iterators_dict):
        if type(iterators_dict) != dict:
            self.data = iterators_dict
        else:
            for iterator_name, iterator_func in iterators_dict.items():
                setattr(self, iterator_name, iterator_func)

    def __getattr__(self, attr):
        raise AttributeError("'this dataset has no {} attribute. available splits for this dataset : {}".format(attr, list(self.__dict__.keys())))