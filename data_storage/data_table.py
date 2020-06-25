from typing import List, Dict, Tuple, Set


class DataTable(object):
    def __init__(self):
        self.table_name_m = "test"
        self.record_m = []

    def insert(self, sub: int, record: tuple) -> None:
        if sub >= len (self.record_m):
            self.record_m.append(list(record))
        else:
            self.record_m[sub] = list(record)

    def delete(self, sub: int) -> None:
        self.record_m[sub] = None

    def update(self, sub: int, attribute_index: int, value) -> None:
        self.record_m[sub][attribute_index] = value

    def get_record(self) -> List[list]:
        return self.record_m
