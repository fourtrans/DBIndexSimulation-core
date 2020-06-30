from typing import List, Dict, Tuple, Set
import math


class Node(object):
    def __init__(self, order: int):
        self.order = order
        self.values = []
        self.pointers = []
        self.right = None
        self.left = None
        self.parent = None
        self.is_leaf = False

    def insert_in_leaf(self, value, pointer: int) -> None:
        if self.values:
            temp = self.values
            for i in range(len(temp)):
                if temp[i] == value:  # equal
                    self.pointers[i].append(pointer)
                    break
                if value < temp[i]:  # less
                    self.pointers.insert(i, [pointer])
                    self.values.insert(i, value)
                    break
                if i + 1 == len(temp):  # biggest
                    self.pointers.append([pointer])
                    self.values.append(value)
                    break
        else:  # first couple
            self.values.append(value)
            self.pointers.append([pointer])


class BPlusTree(object):
    def __init__(self, name: int, order: int = 3):
        self.tree_name_m = name
        self.root = Node(order)
        self.root.is_leaf = True

    def insert(self, value, pointer: int) -> None:
        leaf = self.search(value)
        leaf.insert_in_leaf(value, pointer)

        if len(leaf.values) == leaf.order:  # split the leaf node according to the order
            new_node = Node(leaf.order)
            new_node.is_leaf = True
            new_node.parent = leaf.parent
            mid = int(math.ceil(leaf.order / 2))
            new_node.values = leaf.values[mid:]
            new_node.pointers = leaf.pointers[mid:]
            leaf.values = leaf.values[:mid]
            leaf.pointers = leaf.pointers[:mid]
            # new_node 在leaf 右边，更新左右兄弟
            new_node.right = leaf.right
            if leaf.right is not None:
                leaf.right.left = new_node
            leaf.right = new_node
            new_node.left = leaf
            # 插入维护
            self.__insert_in_parent(leaf, new_node, new_node.values[0])

    def __insert_in_parent(self, node1, node2, value):
        if node1 == self.root:
            rootNode = Node(node1.order)
            rootNode.values = [value]
            rootNode.pointers = [node1, node2]
            node1.parent = rootNode
            node2.parent = rootNode
            self.root = rootNode
            return

        parentNode = node1.parent
        temp = parentNode.pointers
        for i in range(len(temp)):
            if temp[i] == node1:
                parentNode.values.insert(i, value)
                parentNode.pointers.insert(i + 1, node2)
                if len(parentNode.pointers) > parentNode.order:
                    uncle = Node(parentNode.order)
                    uncle.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2))
                    uncle.values = parentNode.values[mid:]
                    uncle.pointers = parentNode.pointers[mid:]
                    newvalue = parentNode.values[mid - 1]
                    if mid == 1:
                        parentNode.values = parentNode.values[:mid]
                    else:
                        parentNode.values = parentNode.values[:mid - 1]
                    parentNode.pointers = parentNode.pointers[:mid]
                    for n in parentNode.pointers:
                        n.parent = parentNode
                    for n in uncle.pointers:
                        n.parent = uncle
                    self.__insert_in_parent(parentNode, uncle, newvalue)
                else:
                    break

    def search(self, value) -> Node:  # get the leaf node where the value might in
        current_node = self.root
        while not current_node.is_leaf:
            for i in range(len(current_node.values)):
                if current_node.values[i] == value:
                    current_node = current_node.pointers[i + 1]
                    break
                if value < current_node.values[i]:
                    current_node = current_node.pointers[i]
                    break
                if i + 1 == len(current_node.values):
                    current_node = current_node.pointers[i + 1]
                    break
        return current_node

    def find(self, value, op: str) -> list:  # get the list of pointer whose values is op(<.>,=,<=,>=) vaule
        # global i, item
        leaf = self.search(value)
        addr = []
        if not leaf.values:
            return addr
        for i, item in enumerate(leaf.values):
            if value <= item:
                break
        if op == "=":
            if value == item:
                addr.append(leaf.pointers[i])
        elif ">" in op:
            addr += leaf.pointers[i:]
            temp = leaf.right
            while temp is not None:
                addr += temp.pointers
                temp = temp.right
            if "=" not in op and value == item:  # 大于
                addr.pop(0)
            elif value > item:
                addr.pop(0)
        elif "<" in op:
            if "=" in op and value == item:
                addr.append(leaf.pointers[i])
            elif item < value:
                addr.append(leaf.pointers[i])
            addr += list(reversed(leaf.pointers[:i]))
            temp = leaf.left
            while temp is not None:
                addr += temp.pointers[::-1]
                temp = temp.left

        addr = [sub for group in addr for sub in group]  # flatten
        return addr

    def delete(self, pointer: int, value) -> int:
        node = self.search(value)

        temp = 0
        for i, item in enumerate(node.values):
            if item == value:
                temp = 1

                if pointer in node.pointers[i]:
                    if len(node.pointers[i]) > 1:
                        node.pointers[i].remove(pointer)
                    elif node == self.root:
                        node.values.pop(i)
                        node.pointers.pop(i)
                    else:
                        del node.pointers[i]
                        node.values.pop(i)
                        self.__delete_parents(node, pointer, value)

    def __delete_parents(self, node, pointer, value):
        if not node.is_leaf:  # not leaf,then delete the pointer and value
            for i, item in enumerate(node.pointers):
                if item == pointer:
                    node.pointers.pop(i)
                    break
            for i, item in enumerate(node.values):
                if item == value:
                    node.values.pop(i)
                    break
        if self.root == node and len(node.pointers) == 1:
            self.root = node.pointers[0]
            node.pointers[0].parent = None
            del node
            return
        # 每个中间节点至少有ceil(m/2)个孩子，最多m个孩子；每个叶子节点至少都包含ceil(m/2)-1个元素
        elif (len(node.pointers) < int(math.ceil(node.order / 2)) and node.is_leaf == False) or \
                (len(node.values) < int(math.ceil(node.order / 2) - 1) and node.is_leaf == True):

            is_predecessor = 0
            parentNode = node.parent
            PrevNode = -1  # 左兄弟结点
            NextNode = -1  # 右兄弟节点
            PrevK = -1  # 指针左边的数值
            PostK = -1  # 指针右边的数值
            for i, item in enumerate(parentNode.pointers):

                if item == node:
                    if i > 0:  # 不是父结点的第一个孩子
                        PrevNode = parentNode.pointers[i - 1]
                        PrevK = parentNode.values[i - 1]

                    if i < len(parentNode.pointers) - 1:  # 不是父结点的最后一个孩子
                        NextNode = parentNode.pointers[i + 1]
                        PostK = parentNode.values[i]

            if PrevNode == -1:  # 第一个孩子
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1:  # 最后一个孩子
                is_predecessor = 1
                ndash = PrevNode
                value_ = PrevK
            else:  # 中间孩子
                if len(node.values) + len(NextNode.values) < node.order:  # 右兄弟结点不富余
                    ndash = NextNode
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK

            if len(node.values) + len(ndash.values) < node.order:  # 兄弟结点不富余：合并处理
                if is_predecessor == 0:
                    node, ndash = ndash, node  # ndash是node的左兄弟
                ndash.pointers += node.pointers  # 合并两结点的pointers
                if not node.is_leaf:  # 内部节点
                    ndash.values.append(value_)  # 父结点值下移
                else:  # 叶子结点需处理左右兄弟指针
                    ndash.right = node.right
                    if node.right is not None:
                        node.right.left = ndash
                ndash.values += node.values  # 合并左右兄弟的values

                if not ndash.is_leaf:  # 内部结点需将新增的pointer的父结点设为自己
                    for j in ndash.pointers:
                        j.parent = ndash

                self.__delete_parents(node.parent, node, value_)
                del node
            else:  # 兄弟结点富余
                if is_predecessor == 1:
                    if not node.is_leaf:  # 内部节点：父结点value下移，兄弟结点value上移
                        ndashpm = ndash.pointers.pop(-1)
                        ndashkm_1 = ndash.values.pop(-1)
                        node.pointers = [ndashpm] + node.pointers
                        node.values = [value_] + node.values
                        parentNode = node.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm_1
                                break
                    else:  # 叶子结点：
                        ndashpm = ndash.pointers.pop(-1)
                        ndashkm = ndash.values.pop(-1)
                        node.pointers = [ndashpm] + node.pointers
                        node.values = [ndashkm] + node.values
                        parentNode = node.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashkm
                                break
                else:
                    if not node.is_leaf:  # 内部节点
                        ndashp0 = ndash.pointers.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node.pointers = node.pointers + [ndashp0]
                        node.values = node.values + [value_]
                        parentNode = node.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndashk0
                                break
                    else:  # 叶子结点
                        ndashp0 = ndash.pointers.pop(0)
                        ndashk0 = ndash.values.pop(0)
                        node.pointers = node.pointers + [ndashp0]
                        node.values = node.values + [ndashk0]
                        parentNode = node.parent
                        for i, item in enumerate(parentNode.values):
                            if item == value_:
                                parentNode.values[i] = ndash.values[0]
                                break
                # 把交换的结点的父结点设为当前结点
                if not ndash.is_leaf:
                    for j in ndash.pointers:
                        j.parent = ndash
                if not node.is_leaf:
                    for j in node.pointers:
                        j.parent = node
                if not parentNode.is_leaf:
                    for j in parentNode.pointers:
                        j.parent = parentNode

    def dict_structure(self, node=0):
        if node == 0:
            node = self.root
        if node.is_leaf:
            dict_set = {
                "type": 'leaf',
                "node_value": None,
                "node_pointer": None,
                'leaf_value': node.values,
                'leaf_pointer': node.pointers,
                'leaf_next_leaf': self.dict_structure(node.right) if node.right is not None else None
            }

        else:
            dict_set = {
                "type": 'node',
                "node_value": node.values,
                "node_pointer": [self.dict_structure(n) for n in node.pointers],
                'leaf_value': None,
                'leaf_pointer': None,
                'leaf_next_leaf': None
            }

        return dict_set
