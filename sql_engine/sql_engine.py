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
        # Regular expression rules for simple tokens
        t_SELECT = r'[Ss][Ee][Ll][Ee][Cc][Tt]'
        t_INSERT = r'[Ii][Nn][Ss][Ee][Rr][Tt]'
        t_DELETE = r'[Dd][Ee][Ll][Ee][Tt][Ee]'
        t_UPDATE = r'[Uu][Pp][Dd][Aa][Tt][Ee]'
        t_SET = r'[Ss][Ee][Tt]'
        t_WHERE = r'[Ww][Hh][Ee][Rr][Ee]'
        t_VALUES = r'[Vv][Aa][Ll][Uu][Ee][Ss]'
        t_STAR = r'\*'
        t_EQ = r'\='
        t_LT = r'\<'
        t_LE = r'\<\='
        t_GT = r'\>'
        t_GE = r'\>\='
        t_NE = r'\<\>'
        t_LIKE = r'[Li][Ii][Kk][Ee]'
        t_COMMA = r','
        t_STR = r'\'[^\']+\'|[^\']+'

        def t_NUMBER(t):
            r'\d+\.?|\.\d+|\d+\.\d+'
            t.value = float(t) if '.' in t else int(t)
            return t

        def t_BOOL(t):
            r'[Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee]'
            t.value = bool(re.match(r'[Tt][Rr][Uu][Ee]', t))
            return t

        return lex.lex()
