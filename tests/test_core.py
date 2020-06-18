import unittest
from typing import List, Dict, Tuple, Set
from functools import reduce
from core import SqlVm, Core, Code


class MockStorageCoordinator(object):
    def __init__(self, locate_result: dict, table_definition: dict, table_content: List[tuple]):
        self.locate_result = locate_result
        self.table_definition = table_definition
        self.table_content = table_content
        self.call_seq = []  # record every method call, use for validation

    def insert(self, record: tuple) -> None:
        self.call_seq.append(('insert', record))

    def locate(self, attribute_index: int, compare: str, value) -> List[int]:
        self.call_seq.append(('locate', attribute_index, compare, value))
        return self.locate_result[(attribute_index, compare, value)]

    def locate_all(self) -> List[int]:
        self.call_seq.append(('locate_all'))
        return list(reduce(lambda x, y: x.union(y), map(set, self.locate_result.values())))

    def delete(self, sub: List[int]) -> None:
        self.call_seq.append(('delete', sub))

    def update(self, new_values: dict, indexes: List[int]) -> None:
        self.call_seq.append(('update', new_values, indexes))

    def query(self, sub: List[int]) -> List[tuple]:
        self.call_seq.append(('query', sub))
        retTbl = []
        for index in sub:
            retTbl.append(self.table_content[index])
        return retTbl

    def get_data_definition(self) -> dict:
        self.call_seq.append(('get_data_definition'))
        return self.table_definition

    def get_index_structure(self, attribute: int):
        self.call_seq.append(('get_index_structure'))


LOCATE_RESULT_SAMPLE_STR = {
    ('sno', '>', 10): [1, 2, 3, 4, 5],
    ('name', '=', 'JackSon Li'): [1],
    ('cno', '<>', 3): [1, 3, 5, 7, 9],
    ('name', '<>', ''): [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
LOCATE_RESULT_SAMPLE_INT = {
    (0, '>', 10): [1, 2, 3, 4, 5],
    (2, '=', 'JackSon Li'): [1],
    (1, '<>', 3): [1, 3, 5, 7, 9],
    (2, '<>', ''): [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
TABLE_DEFINITION_SAMPLE = {
    0: {
        'name': 'sno',
        'type': 'int',
        'is_nullable': False,
        'is_unique': True,
        'is_key': True
    },
    1: {
        'name': 'cno',
        'type': 'int',
        'is_nullable': False,
        'is_unique': False,
        'is_key': False
    },
    2: {
        'name': 'name',
        'type': 'str',
        'is_nullable': False,
        'is_unique': False,
        'is_key': False
    },
    3: {
        'name': 'grade',
        'type': 'int',
        'is_nullable': True,
        'is_unique': False,
        'is_key': True
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


class Test_SqlVm_locate(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.db = MockStorageCoordinator(LOCATE_RESULT_SAMPLE_STR, TABLE_DEFINITION_SAMPLE, [])
        self.vm = SqlVm()

    def test_locate_sample1(self):
        sample_condition = [
            [
                ('sno', '>', 10),
                ('name', '=', 'JackSon Li')
            ],
            [
                ('cno', '<>', 3),
                ('name', '<>', '')
            ]
        ]
        self.vm.locate(sample_condition, self.db)
        self.assertEqual([1, 3, 5, 7, 9], self.vm.reg_selector)

    def test_locate_sample2(self):
        sample_condition = [
            [
                ('sno', '>', 10),
                ('cno', '<>', 3)
            ]
        ]
        self.vm.locate(sample_condition, self.db)
        self.assertEqual([1, 3, 5], self.vm.reg_selector)

    def test_locate_sample3(self):
        sample_condition = [
            [
                ('sno', '>', 10)
            ],
            [
                ('cno', '<>', 3),
                ('name', '<>', '')
            ]
        ]
        self.vm.locate(sample_condition, self.db)
        self.assertEqual([1, 2, 3, 4, 5, 7, 9], self.vm.reg_selector)


class Test_SqlVm_project(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.db = MockStorageCoordinator(LOCATE_RESULT_SAMPLE_INT, TABLE_DEFINITION_SAMPLE, TABLE_CONTENT_SAMPLE)
        self.vm = SqlVm()

    def setUp(self):
        self.vm.reg_selector = []
        self.vm.reg_table = []

    def test_project_sample1(self):
        expect_tbl = [
            (3, 'Alice', 80),
            (1, 'JackSon Li', 83),
            (3, 'Alpha', 85),
            (1, 'Beta', 88),
            (3, 'Gamma', 90),
            (2, 'Delta', 93),
            (3, 'Epsilon', 96),
            (2, 'Zeta', 97),
            (3, 'Iota', 99),
            (2, 'Kappa', 77),
            (3, 'Omega', 79)
        ]
        self.vm.reg_table = TABLE_CONTENT_SAMPLE
        self.vm.project([1, 2, 3])
        self.assertEqual(expect_tbl, self.vm.reg_table)

    def test_project_sample2(self):
        expect_tbl = [
            (3, 3, 'Alice', 80),
            (1, 1, 'JackSon Li', 83),
            (3, 3, 'Alpha', 85),
            (1, 1, 'Beta', 88),
            (3, 3, 'Gamma', 90),
            (2, 2, 'Delta', 93),
            (3, 3, 'Epsilon', 96),
            (2, 2, 'Zeta', 97),
            (3, 3, 'Iota', 99),
            (2, 2, 'Kappa', 77),
            (3, 3, 'Omega', 79)
        ]
        self.vm.reg_table = TABLE_CONTENT_SAMPLE
        self.vm.project([1, 1, 2, 3])
        self.assertEqual(expect_tbl, self.vm.reg_table)

    def test_project_sample3(self):
        expect_tbl = [
            (3, 'Alice', 80, 'Alice', 80),
            (1, 'JackSon Li', 83, 'JackSon Li', 83),
            (3, 'Alpha', 85, 'Alpha', 85),
            (1, 'Beta', 88, 'Beta', 88),
            (3, 'Gamma', 90, 'Gamma', 90),
            (2, 'Delta', 93, 'Delta', 93),
            (3, 'Epsilon', 96, 'Epsilon', 96),
            (2, 'Zeta', 97, 'Zeta', 97),
            (3, 'Iota', 99, 'Iota', 99),
            (2, 'Kappa', 77, 'Kappa', 77),
            (3, 'Omega', 79, 'Omega', 79)
        ]
        self.vm.reg_table = TABLE_CONTENT_SAMPLE
        self.vm.project([1, 2, 3, 2, 3])
        self.assertEqual(expect_tbl, self.vm.reg_table)


class Test_SqlVm(unittest.TestCase):
    def setUp(self):
        self.db = MockStorageCoordinator(LOCATE_RESULT_SAMPLE_INT, TABLE_DEFINITION_SAMPLE, TABLE_CONTENT_SAMPLE)
        self.vm = SqlVm()

    def test_run_sample1(self):
        codes = [Code(opc='locate', opr=None),
                 Code(opc='query', opr=None),
                 Code(opc='project', opr=None)]
        codes[0].opr = [
            [
                (2, '<>', '')
            ],
            [
                (1, '<>', 3),
                (2, '=', 'JackSon Li'),
                (0, '>', 10)
            ]
        ]
        codes[2].opr = [0, 1, 2, 3]
        expect_tbl = [
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
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(expect_tbl, vmResult['content'])

    def test_run_sample2(self):
        codes = [Code(opc='locate', opr=None),
                 Code(opc='query', opr=None),
                 Code(opc='project', opr=None)]
        codes[0].opr = [
            [
                (2, '=', 'JackSon Li'),
                (2, '<>', '')
            ],
            [
                (1, '<>', 3),
                (0, '>', 10)
            ]
        ]
        codes[2].opr = [0, 1, 2, 3]
        expect_tbl = [
            (11, 1, 'JackSon Li', 83),
            (13, 1, 'Beta', 88),
            (15, 2, 'Delta', 93)
        ]
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(expect_tbl, vmResult['content'])

    def test_run_sample3(self):
        codes = [Code(opc='insert', opr=None)]
        codes[0].opr = (99, 9, 'Lucas', 90)
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(1, len(self.db.call_seq))
        self.assertEqual(('insert', codes[0].opr), self.db.call_seq[0])

    def test_run_sample4(self):
        codes = [Code(opc='locate', opr=None),
                 Code(opc='delete', opr=None)]
        codes[0].opr = [[(2, '=', 'JackSon Li')]]
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(3, len(self.db.call_seq))
        self.assertEqual(('locate_all'), self.db.call_seq[0])
        self.assertEqual(('locate', 2, '=', 'JackSon Li'), self.db.call_seq[1])
        self.assertEqual(('delete', [1]), self.db.call_seq[2])

    def test_run_sample5(self):
        codes = [Code(opc='locate', opr=None),
                 Code(opc='update', opr=None)]
        codes[0].opr = [[(2, '=', 'JackSon Li'), (2, '<>', '')],
                        [(1, '<>', 3)]]
        codes[1].opr = {3: '95'}
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        seq = self.db.call_seq
        self.assertEqual(5, len(seq))
        self.assertEqual(('locate_all'), seq[0])
        self.assertEqual(('locate', 2, '=', 'JackSon Li'), seq[1])
        self.assertEqual(('locate', 2, '<>', ''), seq[2])
        self.assertEqual(('locate', 1, '<>', 3), seq[3])
        self.assertEqual(('update', {3: '95'}, [1, 3, 5, 7, 9]), self.db.call_seq[4])


if __name__ == '__main__':
    unittest.main()
