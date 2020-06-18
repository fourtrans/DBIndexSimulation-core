import unittest
from sql_engine.code import Code
from sql_engine.sql_engine import SqlEngine


class Test_Core(unittest.TestCase):
    pass


class Test_SqlEngine_lex(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.engine = SqlEngine({})
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
        self.engine = SqlEngine({})
        self.lexer, self.tokens = self.engine.gen_lex()
        self.parser = self.engine.gen_yacc(self.lexer, self.tokens)

    def test_gen_yacc_sample1(self):
        sample = "SELECT * WHERE Sno > 1 and name ='JackSon Li' Or cno <> 3 and name <> ''"
        sample_toktype = ['SELECT', 'STAR', 'WHERE', 'STR', 'GT', 'NUMBER', 'AND', 'STR', 'EQ', 'STR', 'OR', 'STR',
                          'NE', 'NUMBER', 'AND', 'STR', 'NE', 'STR']
        # self.lexer.input(sample)
        # for i in range(len(sample_toktype)):
        #     self.assertEqual(self.lexer.token().type, sample_toktype[i])
        self.parser.parse(input=sample, lexer=self.lexer)

    def test_gen_yacc_sample2(self):
        sample = "SELECT * WHERE Sno > 1 OR name ='JackSon Li' and cno <> 3 and name <> ''"
        self.parser.parse(input=sample, lexer=self.lexer)

    def test_gen_yacc_sample3(self):
        sample = "SELECT * WHERE Sno > 1 and name ='JackSon Li' and cno <> 3 OR name <> ''"
        out = [Code(opc='locate', opr=None),
               Code(opc='query', opr=None),
               Code(opc='project', opr=None)]
        out[0].opr = [[('Sno', '>', 1),
                       ('name', '=', 'JackSon Li'),
                       ('cno', '<>', 3)],
                      [('name', '<>', '')]]
        out[1].opr = [0, 1, 2, 3]
        print(self.engine.attr_index_map)
        self.parser.parse(input=sample, lexer=self.lexer)


if __name__ == '__main__':
    unittest.main()
