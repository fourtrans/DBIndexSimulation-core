from typing import List, Dict, Tuple, Set
from .code import Code
import ply.lex as lex
import re


class SqlSyntaxException(Exception):
    def __init__(self, err: str):
        Exception.__init__(self, '[SqlSyntaxException]' + err)


class SqlColumnException(Exception):
    def __init__(self, err: str):
        Exception.__init__(self, '[SqlColumnException]' + err)


class ValueInvalidException(Exception):
    def __init__(self, err: str):
        Exception.__init__(self, '[ValueInvalidException]' + err)


class SqlEngine(object):
    def __init__(self, table_definition: dict):
        pass

    def resolve_sql_expr(self, sql_expr: str) -> List[Code]:
        pass

    def gen_lex(self):
        # reserved keyword or operator
        reserved = {
            'select': 'SELECT',
            'insert': 'INSERT',
            'delete': 'DELETE',
            'update': 'UPDATE',
            'set': 'SET',
            'where': 'WHERE',
            'values': 'VALUES',
            '*': 'STAR',
            '=': 'EQ',
            '<': 'LT',
            '<=': 'LE',
            '>': 'GT',
            '>=': 'GE',
            '<>': 'NE',
            'like': 'LIKE',
            ',': 'COMMA',
            'and': 'AND',
            'or': 'OR'
        }

        # define tokens
        tokens = ['STR', 'NUMBER', 'BOOL', 'KEYWORD'] + list(reserved.values())  # 'KEYWORD' only for lexical analysis

        # define ignore
        t_ignore = r' '

        # # Regular expression rules for simple tokens
        # t_STR = r"(?<=')[^']+(?=')|[^\s']+"

        def t_NUMBER(t):
            r'\d+\.?|\.\d+|\d+\.\d+'
            t.value = float(t.value) if '.' in t.value else int(t.value)
            return t

        def t_BOOL(t):
            r'[Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee]'
            t.value = bool(re.match(r'[Tt][Rr][Uu][Ee]', t))
            return t

        def t_KEYWORD(t):
            r'[a-zA-Z]+|\=|\>\=|\<\=|\<\>|\<|\>|\*|,'
            t.type = reserved.get(t.value.lower(), 'STR')
            return t

        def t_STR(t):
            r"'[^']*'|[^\s']+"
            if t.value[0] == "'" and t.value[-1] == "'":  # remove STR's quotation marks
                t.value = t.value[1:-1]
            return t

        def t_error(t):
            raise SqlSyntaxException('lexical anayasis failed at:(%s)' % t.value)

        return lex.lex()
