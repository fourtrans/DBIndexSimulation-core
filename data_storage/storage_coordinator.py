from typing import List, Dict, Tuple, Set
from .bplus_tree import Node, BPlusTree
from .data_table import DataTable
from collections import defaultdict
import re


class NotUniqueException(Exception):
    def __init__(self, err: str):
        Exception.__init__(self, '[NotUniqueException]' + err)


class StorageCoordinator(object):
    def __init__(self, table: List[tuple], table_definition: dict):
        self.table_m = DataTable()
        self.empty_m = []
        self.table_definition_m = table_definition
        self.bplustree_m = []
        for i in table_definition:
            if table_definition[i]["is_key"]:
                tree = BPlusTree(i)
                self.bplustree_m.append(tree)
        if table:
            for item in self.bplustree_m:
                item.insert(table[0][item.tree_name_m], 0)
            self.table_m.insert(0, table[0])
            for item in table[1:]:
                self.insert(item)

    def insert(self, record: tuple) -> None:
        # 唯一性检查
        for key in self.table_definition_m:
            if self.table_definition_m[key]["is_unique"]:
                if self.table_definition_m[key]["is_key"]:
                    for tree in self.bplustree_m:
                        if tree.tree_name_m == key:
                            if len(tree.find(record[key], "=")) > 0:
                                raise NotUniqueException("insert error")
                            else:
                                break
                else:
                    old_record = self.table_m.get_record()
                    for i in old_record:
                        if i[key] == record[key]:
                            raise NotUniqueException("insert error")
        # 若当前数据表有空行，则取空行行号
        if self.empty_m:
            sub = self.empty_m.pop()
        else:  # 否则新增一行
            sub = len(self.table_m.get_record())
        self.table_m.insert(sub, record)
        # 维护B+树索引
        for item in self.bplustree_m:
            item.insert(record[item.tree_name_m], sub)

    def locate(self, attribute_index: int, compare: str, value) -> List[int]:
        # 对LIKE操作直接使用顺序查找
        # self.bplustree_m[0].show()
        sub = []
        if compare == "Like":
            # 对数据表顺序遍历取满足条件的行号index
            z = re.sub(r'%', '.*', value)
            p = re.compile(z)
            j = 0
            for i in self.table_m.get_record():
                if i is not None:
                    if p.match(i[attribute_index]):  # 匹配？？？？？？？？？？？？？？？
                        sub.append(j)
                j = j + 1
            return sub
            # 对其他操作符
        # 若当前属性已建立索引，则利用B+树索引定位行号
        for tree in self.bplustree_m:
            if attribute_index == tree.tree_name_m:
                if compare == "<>":  # 采用B+树索引时，若operation为<>，则取补集
                    sub = tree.find(value, "=")
                    sub = list(
                        set(range(len(self.table_m.get_record()))).difference(set(self.empty_m)).difference(set(sub)))
                else:
                    sub = tree.find(value, compare)
                return sub
        # 若当前属性未建立索引，则顺序查找定位行号
        record = self.table_m.get_record()
        for index in range(len(record)):
            if record[index] is not None:

                if compare == "=":
                    if value == record[index][attribute_index]:
                        sub.append(index)  # 若满足条件则取其行号
                elif compare == ">":
                    if record[index][attribute_index] > value:
                        sub.append(index)  # 若满足条件则取其行号
                elif compare == "<":
                    if record[index][attribute_index] < value:
                        sub.append(index)  # 若满足条件则取其行号
                elif compare == "<>":
                    if value != record[index][attribute_index]:
                        sub.append(index)  # 若满足条件则取其行号
                elif compare == ">=":
                    if record[index][attribute_index] >= value:
                        sub.append(index)  # 若满足条件则取其行号
                elif compare == "<=":
                    if record[index][attribute_index] <= value:
                        sub.append(index)  # 若满足条件则取其行号
        return sub

    def locate_all(self) -> List[int]:
        return list(set(range(len(self.table_m.get_record()))).difference(set(self.empty_m)))

    def delete(self, sub: List[int]) -> None:
        for i in sub:
            # 先处理索引
            for item in self.bplustree_m:
                item.delete(i, self.table_m.get_record()[i][item.tree_name_m])
            # 再处理数据表
            self.table_m.delete(i)
            self.empty_m.append(i)

    def update(self, new_values: dict, indexes: List[int]) -> None:
        # 唯一性检查
        for key in new_values:
            if self.table_definition_m[key]["is_unique"]:
                if self.table_definition_m[key]["is_key"]:
                    for tree in self.bplustree_m:
                        if tree.tree_name_m == key:
                            if len(tree.find(new_values[key], "=")) > 0:
                                raise NotUniqueException("update error")
                            else:
                                break
                else:
                    old_record = self.table_m.get_record()
                    for i in old_record:
                        if i[key] == new_values[key]:
                            raise NotUniqueException("update error")

        # 先处理索引
        for tree in self.bplustree_m:
            if tree.tree_name_m in new_values:
                att = tree.tree_name_m
                for index in indexes:
                    tree.delete(index, self.table_m.get_record()[index][att])
                    tree.insert(new_values[tree.tree_name_m], index)
        # 再处理数据表
        for key in new_values:
            for index in indexes:
                self.table_m.update(index, key, new_values[key])

    def query(self, sub: List[int]) -> List[tuple]:
        record = []
        for i in sub:
            record.append(tuple(self.table_m.get_record()[i]))
        return record

    def get_data_definition(self) -> dict:
        return self.table_definition_m

    def get_index_structure(self, attribute: int) -> dict:
        for tree in self.bplustree_m:
            if tree.tree_name_m == attribute:
                return tree.dict_structure()
