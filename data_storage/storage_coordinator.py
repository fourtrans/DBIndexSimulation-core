from typing import List, Dict, Tuple, Set
from .bplus_tree import Node, BPlusTree
from .data_table import DataTable


class NotUniqueException(Exception):
    def __init__(self, err: str):
        Exception.__init__(self, '[NotUniqueException]' + err)


class StorageCoordinator(object):
    def __init__(self, table: List[tuple], table_definition: dict):
        pass

    def insert(self, record: tuple) -> None:
        pass

    def locate(self, attribute_index: int, compare: str, value) -> List[int]:
        pass

    def locate_all(self) -> List[int]:
        pass

    def delete(self, sub: List[int]) -> None:
        pass

    def update(self, new_values: dict, indexes: List[int]) -> None:
        pass

    def query(self, sub: List[int]) -> List[tuple]:
        pass

    def get_data_definition(self) -> dict:
        pass

    def get_index_structure(self, attribute: int) -> dict:
        pass
