from typing import List, Dict, Tuple, Set
from .sql_engine import SqlEngine, Code
from .data_storage import StorageCoordinator


class SqlVm(object):
    def __init__(self):
        pass

    def run(self, code_list: List[Code], db: StorageCoordinator):
        pass


class Core(object):
    def __init__(self, table_definition: dict, table_data: List[tuple]):
        pass

    def execute_sql_expr(self, request: dict) -> dict:
        pass

    def generate_index_picture(self, output_path: str, attribute: int) -> None:
        pass
