from typing import List, Dict, Tuple, Set


class Node(object):
    def __init__(self, order: int):
        self.order = order
        self.values = []
        self.pointers = []
        self.right = None
        self.left=None
        self.parent = None
        self.is_leaf = False

    def insert_in_leaf(self, value, pointer:int) -> None:
        if self.values:
            temp=self.values
            for i in range(len(temp)):
                if temp[i] == value:#equal
                    self.pointers[i].append(pointer)
                    break
                if value<temp[i]:#less
                    self.pointers.insert(i,pointer)
                    self.values.insert(i,value)
                    break
                if i+1 == len(temp):#biggest
                    self.pointers.append([pointer])
                    self.values.append(value)
                    break
        else:#first couple
            self.values.append(value)
            self.pointers.append([pointer])




class BPlusTree(object):
    def __init__(self, order: int):
        self.root=Node(order)
        self.root.is_leaf=True

    def insert(self, value, pointer: int) -> None:
        pass

    def search(self, value) -> Node:#get the leaf node where the value might in
        current_node=self.root
        while(current_node.is_leaf==False):
            for i in range(len(current_node.values)):
                if current_node[i]==value or i+1==len(current_node.values):
                    current_node=current_node.pointers[i+1]
                    break
                if value<current_node[i]:
                    current_node = current_node.pointers[i]
                    break
        return  current_node

    def find(self, value, op:str) -> list:#get the list of pointer whose values is op(<.>,=,<=,>=) vaule
        global i, item
        leaf=self.search(value)
        addr=[]
        for i,item in enumerate(leaf.values):
            if value<=item:
                break
        if op == "=":
            if value == item:
                addr += leaf.pointers[i]
        elif ">" in op:
            addr+=leaf.pointers[i:]
            temp = leaf.right
            while temp!=None:
                addr+=temp.pointers
                temp=temp.right
            if "=" not in op and value==item:
                addr.pop(0)
        elif "<" in op:
            addr+=leaf.pointers[:i]
            temp=leaf.left
            while temp != None:
                addr+=temp.pointers
                temp=temp.left
            if "=" in op and value == item:
                addr.append(leaf.pointers[i])
        addr=[sub for group in addr for sub in group]#flatten
        return addr



    def delete(self, pointer: int, value) -> int:
        pass
