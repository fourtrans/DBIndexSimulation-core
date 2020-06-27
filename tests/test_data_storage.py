import unittest
from data_storage.bplus_tree import Node, BPlusTree
from data_storage.data_table import DataTable
from data_storage.storage_coordinator import StorageCoordinator,NotUniqueException


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
        self.tree=BPlusTree(name=1,order=3)

    def test_data_sample1(self):
        #string
        sample=["E52","E21","C52","D08","B12","A99"]
        for i,item in enumerate(sample):
            self.tree.insert(value=item,pointer=i)
        #=
        for i,item in enumerate(sample):
            self.assertEqual(self.tree.find(value=item,op="="),[i])

    def test_data_sample2(self):
        #int
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
    @classmethod
    def setUpClass(self) -> None:
        self.table = DataTable()
        self.table.record_m = [['E01', 'SX01', 'fei', 99],
                               ['E02', 'SX01', 'zhang', 89],
                               ['E03', 'SX01', 'cai', 79],
                               ['E04', 'SX01', 'zhao', 69]]

    def test_init(self):
        self.assertEqual(self.table.table_name_m, 'test')

    def test_insert(self):
        self.table.insert(4, ('E21', 'SX01', 'fei', 99))
        self.assertEqual(self.table.record_m[4], ['E21', 'SX01', 'fei', 99])

    def test_delete(self):
        self.table.delete(0)
        self.assertEqual(self.table.record_m[0], None)
        self.table.insert(0, ('E22', 'SX01', 'chen', 99))
        self.assertEqual(self.table.record_m[0], ['E22', 'SX01', 'chen', 99])

    def test_update(self):
        self.table.update(1, 3, 30)
        self.assertEqual(self.table.record_m[1][3], 30)

    def test_get_record(self):
        self.assertEqual(sorted(self.table.get_record()), sorted([['E22', 'SX01', 'chen', 99],
                                                   ['E02', 'SX01', 'zhang', 89],
                                                   ['E03', 'SX01', 'cai', 79],
                                                   ['E04', 'SX01', 'zhao', 69],
                                                   ]))


class Test_StorageCoordinator(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        TABLE_DEFINITION_SAMPLE = {
            0: {
                'name': 'sno',
                'type': 'int',
                'is_nullable': False,
                'is_unique': True,
                'is_key': True,
            },
            1: {
                'name': 'cno',
                'type': 'int',
                'is_nullable': False,
                'is_unique': False,
                'is_key': False,
            },
            2: {
                'name': 'name',
                'type': 'str',
                'is_nullable': False,
                'is_unique': False,
                'is_key': False,
            },
            3: {
                'name': 'grade',
                'type': 'int',
                'is_nullable': True,
                'is_unique': False,
                'is_key': False,
            }
        }
        TABLE_CONTENT_SAMPLE = [
            (0, 3, 'Alice', 80),
            (11, 1, 'JackSon Li', 83),
            (12, 3, 'Alpha', 85),
            (13, 1, 'Beta', 88),
            (14, 3, 'Gamma', 90),
            (15, 2, 'Delta', 93),
            (1, 3, 'Epsilon', 96),
            (2, 2, 'Zeta', 97),
            (3, 3, 'Iota', 99),
            (4, 2, 'Kappa', 77),
            (5, 3, 'Omega', 79)
        ]
        self.storage=StorageCoordinator(TABLE_CONTENT_SAMPLE,TABLE_DEFINITION_SAMPLE)

    def test_locate(self):
        self.storage.insert((7, 3, 'Tom', 88))
        self.assertEqual(sorted(self.storage.locate(0,'>',5)),sorted([1,2,3,4,5,11]))
        self.storage.delete([0,2,10])
        self.assertEqual(sorted(self.storage.locate(1,'=',3)),sorted([4,6,8,11]))
        self.storage.update({1:4,3:60},[1,3])
        self.assertEqual(sorted(self.storage.locate(3,'<=',60)),sorted([1,3]))
        self.assertEqual(sorted(self.storage.locate(1, '>=', 4)), sorted([1, 3]))
        self.assertEqual(self.storage.locate(2,'Like','%A%'),[])
        self.assertEqual(sorted(self.storage.locate(2, 'Like', '%a%')), sorted([1,3,4,5,7,8,9]))
        self.assertEqual(sorted(self.storage.locate(2, 'Like', '%t%')), sorted([3, 5, 7, 8]))
        self.assertEqual(sorted(self.storage.locate(1, '<>', 3)), sorted([1, 3, 5, 7, 9]))

    def test_locate_all(self):
        self.storage.delete([1,3])
        self.assertEqual(self.storage.locate_all(),[4,5,6,7,8,9,11])

    def test_query(self):
        anw=self.storage.query([4,8])
        self.assertEqual(anw,[(14, 3, 'Gamma', 90),(3, 3, 'Iota', 99)])


if __name__ == '__main__':
    unittest.main()
