import unittest
from sql_engine.code import Code
from sql_engine.sql_engine import SqlEngine


class Test_Core(unittest.TestCase):
    pass


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


class Test_SqlEngine_lex(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.engine = SqlEngine(TABLE_DEFINITION_SAMPLE)
        self.lexer, _ = self.engine.gen_lex()

    def test_gen_lexer_sample1(self):

        sample = "SELECT  * WHERE Sno > 1 and name ='JackSon Li' Or cno <> 3 and name <> ''"
        sample_toktype = ['SELECT', 'STAR', 'WHERE', 'STR', 'GT', 'NUMBER', 'AND', 'STR', 'EQ', 'STR', 'OR', 'STR',
                          'NE', 'NUMBER', 'AND', 'STR', 'NE', 'STR']
        self.lexer.input(sample)
        for i in range(len(sample_toktype)):
            self.assertEqual(self.lexer.token().type, sample_toktype[i])

    def test_gen_lexer_sample2(self):
        sample = "SELECT name, sno, cno WHERE sno <= 1 OR name LIKE '%JACK%'"
        sample_toktype = ['SELECT', 'STR', 'COMMA', 'STR', 'COMMA', 'STR', 'WHERE', 'STR', 'LE', 'NUMBER', 'OR',
                          'STR', 'LIKE', 'STR']
        self.lexer.input(sample)
        for i in range(len(sample_toktype)):
            self.assertEqual(self.lexer.token().type, sample_toktype[i])

    def test_gen_lexer_sample3(self):
        sample = "DELETE WHERE sno < 30 AND sno > 9999 OR cno > 10"
        sample_toktype = ['DELETE', 'WHERE', 'STR', 'LT', 'NUMBER', 'AND', 'STR', 'GT', 'NUMBER',
                          'OR', 'STR', 'GT', 'NUMBER']
        self.lexer.input(sample)
        for i in range(len(sample_toktype)):
            self.assertEqual(self.lexer.token().type, sample_toktype[i])

    def test_gen_lexer_sample4(self):
        sample = "UPDATE SET grade=100, name='amazing' WHERE cno = 99"
        sample_toktype = ['UPDATE', 'SET', 'STR', 'EQ', 'NUMBER', 'COMMA', 'STR', 'EQ', 'STR', 'WHERE',
                          'STR', 'EQ', 'NUMBER']
        self.lexer.input(sample)
        for i in range(len(sample_toktype)):
            self.assertEqual(self.lexer.token().type, sample_toktype[i])

    def test_gen_lexer_sample5(self):
        sample = "INSERT sno, cno, name, grade VALUES 1234, 3, 'Alice', 90"
        sample_toktype = ['INSERT', 'STR', 'COMMA', 'STR', 'COMMA', 'STR', 'COMMA', 'STR', 'VALUES', 'NUMBER',
                          'COMMA', 'NUMBER', 'COMMA', 'STR', 'COMMA', 'NUMBER']
        self.lexer.input(sample)
        for i in range(len(sample_toktype)):
            self.assertEqual(self.lexer.token().type, sample_toktype[i])

    pass


class Test_SqlEngine_yacc(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.engine = SqlEngine(TABLE_DEFINITION_SAMPLE)
        self.lexer, self.tokens = self.engine.gen_lex()
        self.parser = self.engine.gen_yacc(self.lexer, self.tokens)

    def test_gen_yacc_sample1(self):
        sample = "SELECT  * WHERE sno > 1 and name ='JackSon Li' Or cno <> 3 and name <> ''"
        res = self.parser.parse(input=sample, lexer=self.lexer)
        pass

    def test_gen_yacc_sample2(self):
        sample = "SELECT name, sno, cno WHERE sno <= 1 OR name LIKE '%JACK%'"
        res = self.parser.parse(input=sample, lexer=self.lexer)
        pass

    def test_gen_yacc_sample3(self):
        sample = "DELETE WHERE sno < 30 AND sno > 9999 OR cno > 10"
        out = [Code(opc='locate', opr=None),
               Code(opc='query', opr=None),
               Code(opc='project', opr=None)]
        out[0].opr = [
            [
                (2, '<>', '')
            ],
            [
                (1, '<>', 3),
                (2, '=', 'JackSon Li'),
                (0, '>', 1)
            ]
        ]
        out[2].opr = [0, 1, 2, 3]
        res = self.parser.parse(input=sample, lexer=self.lexer)
        pass

    def test_gen_yacc_sample4(self):
        sample = "UPDATE SET grade=100, name='amazing' WHERE cno = 99"
        res = self.parser.parse(input=sample, lexer=self.lexer)
        pass

    def test_gen_yacc_sample5(self):
        sample = "INSERT sno, cno, grade VALUES 1234, 3, 90"
        res = self.parser.parse(input=sample, lexer=self.lexer)
        pass


if __name__ == '__main__':
    unittest.main()
