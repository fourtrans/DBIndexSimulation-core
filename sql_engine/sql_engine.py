from typing import List, Dict, Tuple, Set
from .code import Code


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
