import unittest
from data_storage.bplus_tree import Node, BPlusTree
from data_storage.data_table import DataTable
from data_storage.storage_coordinator import StorageCoordinator


class Test_Node(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.node=Node(order=3)
    def test_sample(self):
        sample=["A99","B12"]
        for i, item in enumerate(sample):
            self.node.insert_in_leaf(value=item,pointer=i)
            self.assertEqual(self.node.values,sample[:i+1])


class Test_BPlusTree(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        pass

    def test_data_sample1(self):
        #string
        self.tree = BPlusTree(name=1, order=3)
        sample=["E52","E21","C52","D08","B12","A99"]
        for i,item in enumerate(sample):
            self.tree.insert(value=item,pointer=i)
        #=
        for i,item in enumerate(sample):
            self.assertEqual(self.tree.find(value=item,op="="),[i])

    def test_data_sample2(self):
        #int
        self.tree = BPlusTree(name=1, order=3)
        sample=[58,74,81,88,90,92,95]
        for i,item in enumerate(sample):
            self.tree.insert(value=item,pointer=i)
        #<,<=
        for i,item in enumerate(sample):
            self.assertEqual(self.tree.find(value=item,op="<"),list(reversed(range(i))))
        for i,item in enumerate(sample):
            self.assertEqual(self.tree.find(value=item,op="<="),list(reversed(range(i+1))))
        self.assertEqual(self.tree.find(value=100, op="<="), list(reversed(range(7))))
        self.assertEqual(self.tree.find(value=20, op="<"), [])

    def test_data_sample3(self):
        #float
        self.tree = BPlusTree(name=1, order=3)
        sample=[2.9,9.7,19.22,25.15,32.32]
        for i,item in enumerate(sample):
            self.tree.insert(value=item,pointer=i)
        #>,>=
        for i,item in enumerate(sample):
            self.assertEqual(self.tree.find(value=item,op=">"),list(range(i+1,5)))
        for i,item in enumerate(sample):
            self.assertEqual(self.tree.find(value=item,op=">="),list(range(i,5)))
        self.assertEqual(self.tree.find(value=0, op=">="), list(range(5)))
        self.assertEqual(self.tree.find(value=50, op=">"), [])
        #delete
        for i,item in enumerate(sample):
            self.tree.delete(pointer=i,value=item)
            self.assertEqual(self.tree.find(value=item,op="="),[])

class Test_DataTable(unittest.TestCase):
    pass


class Test_StorageCoordinator(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
