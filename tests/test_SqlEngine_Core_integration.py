import unittest
from typing import List, Dict, Tuple, Set
from functools import reduce
from core import SqlVm, Core
from sql_engine.code import Code
from sql_engine.sql_engine import SqlEngine


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


LOCATE_RESULT_SAMPLE = {
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


class Test_Core_SqlEngine_integration1(unittest.TestCase):
    def setUp(self):
        self.db = MockStorageCoordinator(LOCATE_RESULT_SAMPLE, TABLE_DEFINITION_SAMPLE, TABLE_CONTENT_SAMPLE)
        self.engine = SqlEngine(TABLE_DEFINITION_SAMPLE)
        self.vm = SqlVm()
        lexer, tokens = self.engine.gen_lex()
        self.parser = self.engine.gen_yacc(lexer, tokens)

    def test_runSql_sample1(self):
        sql_expr = "SELECT * WHERE sno > 10 and name ='JackSon Li' and cno <> 3 OR name <> ''"
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='query', opr=None),
        #          Code(opc='project', opr=None)]
        # codes[0].opr = [
        #     [
        #         (2, '<>', '')
        #     ],
        #     [
        #         (1, '<>', 3),
        #         (2, '=', 'JackSon Li'),
        #         (0, '>', 10)
        #     ]
        # ]
        # codes[2].opr = [0, 1, 2, 3]
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
        codes = self.parser.parse(sql_expr)
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(expect_tbl, vmResult['content'])

    def test_runSql_sample2(self):
        sql_expr = "SELECT * WHERE sno > 10 and cno <> 3 OR name ='JackSon Li' and  name <> ''"
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='query', opr=None),
        #          Code(opc='project', opr=None)]
        # codes[0].opr = [
        #     [
        #         (2, '=', 'JackSon Li'),
        #         (2, '<>', '')
        #     ],
        #     [
        #         (1, '<>', 3),
        #         (0, '>', 10)
        #     ]
        # ]
        # codes[2].opr = [0, 1, 2, 3]
        expect_tbl = [
            (11, 1, 'JackSon Li', 83),
            (13, 1, 'Beta', 88),
            (15, 2, 'Delta', 93)
        ]
        codes = self.parser.parse(sql_expr)
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(expect_tbl, vmResult['content'])

    def test_run_sample3(self):
        sql_expr = "INSERT grade, sno, cno, name VALUES 90, 99, 9, 'Lucas'"
        # codes = [Code(opc='insert', opr=None)]
        # codes[0].opr = (99, 9, 'Lucas', 90)
        expect_insertion = (99, 9, 'Lucas', 90)
        codes = self.parser.parse(sql_expr)
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(1, len(self.db.call_seq))
        self.assertEqual(('insert', expect_insertion), self.db.call_seq[0])

    def test_run_sample4(self):
        sql_expr = "DELETE WHERE name = 'JackSon Li'"
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='delete', opr=None)]
        # codes[0].opr = [[(2, '=', 'JackSon Li')]]
        codes = self.parser.parse(sql_expr)
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        self.assertEqual(3, len(self.db.call_seq))
        self.assertEqual(('locate_all'), self.db.call_seq[0])
        self.assertEqual(('locate', 2, '=', 'JackSon Li'), self.db.call_seq[1])
        self.assertEqual(('delete', [1]), self.db.call_seq[2])

    def test_run_sample5(self):
        sql_expr = "UPDATE SET grade=95 WHERE name = 'JackSon Li' and name <> '' OR cno <> 3"
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='update', opr=None)]
        # codes[0].opr = [[(2, '=', 'JackSon Li'), (2, '<>', '')],
        #                 [(1, '<>', 3)]]
        # codes[1].opr = {3: '95'}
        codes = self.parser.parse(sql_expr)
        vmResult = self.vm.run(codes, self.db)
        self.assertTrue(vmResult['is_success'])
        seq = self.db.call_seq
        self.assertEqual(5, len(seq))
        self.assertEqual(('locate_all'), seq[0])
        self.assertEqual(('update', {3: 95}, [1, 3, 5, 7, 9]), self.db.call_seq[4])


class Test_Core_SqlEngine_integration2(unittest.TestCase):
    def setUp(self):
        self.core = Core(TABLE_DEFINITION_SAMPLE, [])
        self.core.db_m = MockStorageCoordinator(LOCATE_RESULT_SAMPLE, TABLE_DEFINITION_SAMPLE, TABLE_CONTENT_SAMPLE)

    def test_runSql_sample1(self):
        sql_expr = "SELECT * WHERE sno > 10 and name ='JackSon Li' and cno <> 3 OR name <> ''"
        sql_request = {'serial_number': 1, 'sql_expr': sql_expr}
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='query', opr=None),
        #          Code(opc='project', opr=None)]
        # codes[0].opr = [
        #     [
        #         (2, '<>', '')
        #     ],
        #     [
        #         (1, '<>', 3),
        #         (2, '=', 'JackSon Li'),
        #         (0, '>', 10)
        #     ]
        # ]
        # codes[2].opr = [0, 1, 2, 3]
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
        result = self.core.execute_sql_expr(sql_request)
        self.assertTrue(result['is_success'])
        self.assertEqual(sql_request['serial_number'], result['serial_number'])
        self.assertEqual(sql_request['sql_expr'], result['sql_expr'])
        self.assertEqual(expect_tbl, result['content'])

    def test_runSql_sample2(self):
        sql_expr = "SELECT * WHERE sno > 10 and cno <> 3 OR name ='JackSon Li' and  name <> ''"
        sql_request = {'serial_number': 1, 'sql_expr': sql_expr}
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='query', opr=None),
        #          Code(opc='project', opr=None)]
        # codes[0].opr = [
        #     [
        #         (2, '=', 'JackSon Li'),
        #         (2, '<>', '')
        #     ],
        #     [
        #         (1, '<>', 3),
        #         (0, '>', 10)
        #     ]
        # ]
        # codes[2].opr = [0, 1, 2, 3]
        expect_tbl = [
            (11, 1, 'JackSon Li', 83),
            (13, 1, 'Beta', 88),
            (15, 2, 'Delta', 93)
        ]
        result = self.core.execute_sql_expr(sql_request)
        self.assertTrue(result['is_success'])
        self.assertEqual(sql_request['serial_number'], result['serial_number'])
        self.assertEqual(sql_request['sql_expr'], result['sql_expr'])
        self.assertEqual(expect_tbl, result['content'])

    def test_run_sample3(self):
        sql_expr = "INSERT grade, sno, cno, name VALUES 90, 99, 9, 'Lucas'"
        sql_request = {'serial_number': 1, 'sql_expr': sql_expr}
        # codes = [Code(opc='insert', opr=None)]
        # codes[0].opr = (99, 9, 'Lucas', 90)
        expect_insertion = (99, 9, 'Lucas', 90)
        result = self.core.execute_sql_expr(sql_request)
        self.assertTrue(result['is_success'])
        self.assertEqual(sql_request['serial_number'], result['serial_number'])
        self.assertEqual(sql_request['sql_expr'], result['sql_expr'])
        self.assertEqual(1, len(self.core.db_m.call_seq))
        self.assertEqual(('insert', expect_insertion), self.core.db_m.call_seq[0])

    def test_run_sample4(self):
        sql_expr = "DELETE WHERE name = 'JackSon Li'"
        sql_request = {'serial_number': 1, 'sql_expr': sql_expr}
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='delete', opr=None)]
        # codes[0].opr = [[(2, '=', 'JackSon Li')]]
        result = self.core.execute_sql_expr(sql_request)
        self.assertTrue(result['is_success'])
        self.assertEqual(sql_request['serial_number'], result['serial_number'])
        self.assertEqual(sql_request['sql_expr'], result['sql_expr'])
        self.assertEqual(3, len(self.core.db_m.call_seq))
        self.assertEqual(('locate_all'), self.core.db_m.call_seq[0])
        self.assertEqual(('locate', 2, '=', 'JackSon Li'), self.core.db_m.call_seq[1])
        self.assertEqual(('delete', [1]), self.core.db_m.call_seq[2])

    def test_run_sample5(self):
        sql_expr = "UPDATE SET grade=95 WHERE name = 'JackSon Li' and name <> '' OR cno <> 3"
        sql_request = {'serial_number': 1, 'sql_expr': sql_expr}
        # codes = [Code(opc='locate', opr=None),
        #          Code(opc='update', opr=None)]
        # codes[0].opr = [[(2, '=', 'JackSon Li'), (2, '<>', '')],
        #                 [(1, '<>', 3)]]
        # codes[1].opr = {3: '95'}
        result = self.core.execute_sql_expr(sql_request)
        self.assertTrue(result['is_success'])
        self.assertEqual(sql_request['serial_number'], result['serial_number'])
        self.assertEqual(sql_request['sql_expr'], result['sql_expr'])
        seq = self.core.db_m.call_seq
        self.assertEqual(5, len(seq))
        self.assertEqual(('locate_all'), seq[0])
        self.assertEqual(('update', {3: 95}, [1, 3, 5, 7, 9]), self.core.db_m.call_seq[4])
