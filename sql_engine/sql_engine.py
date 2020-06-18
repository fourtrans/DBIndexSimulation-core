from typing import List, Dict, Tuple, Set
from .code import Code
import ply.lex as lex
import ply.yacc as yacc
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
        self.table_definition = table_definition
        self.attr_index_map = {}
        # create attr -> index
        for key in table_definition.keys():
            self.attr_index_map[table_definition[key]['name']] = key

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

        return lex.lex(), tokens

    def gen_yacc(self, lexer, tokens: list):
        def p_sql_stam(p):
            '''sql_stam : select_stam
                        | insert_stam
                        | update_stam
                        | delete_stam'''
            print('生成SQL语句')
            p[0] = p[1]

        def p_select_stam(p):
            '''select_stam : SELECT attr_list cond_stam'''
            print('生成查询语句')
            p[0] = [
                Code(opc='locate', opr=p[3]),
                Code(opc='query', opr=None),
                Code(opc='project', opr=p[2])
            ]

        def p_insert_stam(p):
            '''insert_stam : INSERT attr_list VALUES values_list'''
            # TODO 生成插入语句
            print('生成插入语句')

        def p_update_stam(p):
            '''update_stam : UPDATE SET assg_stam cond_stam'''
            print('生成更新语句')
            p[0] = [
                Code(opc='locate', opr=p[4]),
                Code(opc='update', opr=dict(p[3]))
            ]

        def p_delete_stam(p):
            '''delete_stam : DELETE cond_stam'''
            print('生成删除语句')
            p[0] = [
                Code(opc='locate', opr=p[2]),
                Code(opc='delete', opr=None)
            ]

        def p_attr_list(p):
            '''attr_list : attr COMMA attr_list
                         | attr
                         | STAR
                         | empty'''
            print('生成投影属性列表')
            if p[1] == '*':
                """attr_list : STAR"""
                p[0] = list(range(len(self.attr_index_map)))
            elif p[1] is None:
                """attr_list : empty"""
                p[0] = None
            elif isinstance(p[1], int):
                if len(p) == 4:
                    """attr_list : attr COMMA attr_list"""
                    p[0] = p[3].append(p[1])
                else:
                    p[0] = [p[1]]

        def p_attr(p):
            '''attr : STR'''
            print('获取属性名称')
            if p[1] in self.attr_index_map.keys():
                p[0] = self.attr_index_map[p[1]]
            else:
                raise SqlColumnException('属性' + p[1] + '不存在！')

        def p_cond_stam(p):
            '''cond_stam : WHERE or_cond
                         | empty'''
            print('生成条件表达式')
            if len(p) == 2:
                p[0] = []
            else:
                p[0] = p[2]

        def p_or_cond(p):
            '''or_cond : and_cond OR or_cond
                       | and_cond'''
            print('生成含或项的复合逻辑表达式')
            if len(p) == 4:
                p[0] = p[3].append(p[1])
            else:
                p[0] = [p[1]]

        def p_and_cond(p):
            '''and_cond : cond AND and_cond
                        | cond'''
            print('生成含与项的复合逻辑表达式')
            if len(p) == 4:
                p[0] = p[3].append(p[1])
            else:
                p[0] = [p[1]]

        def p_cond(p):
            '''cond : attr pred value'''
            print('生成元逻辑表达式')
            pattern = self.table_definition[p[1]]['type']
            value = str(type(p[3]))
            if re.search(pattern, value):
                p[0] = (p[1], p[2], p[3])
            else:
                raise ValueInvalidException(p[1] + '和' + p[3] + '类型不匹配！')

        def p_pred(p):
            '''pred : EQ
 	                | NE
 	                | LT
 	                | LE
 	                | GT
 	                | GE
 	                | LIKE'''
            print('获取谓词')
            if re.match('[Ll][Ii][Kk][Ee]', p[1]):
                p[0] = 'LIKE'
            else:
                p[0] = p[1]

        def p_values_list(p):
            '''values_list : value COMMA values_list
 	                       | value'''
            print('生成值列表，插入时使用')
            if len(p) == 4:
                p[0] = p[3].append(p[1])
            else:
                p[0] = [p[1]]

        def p_value(p):
            '''value : STR
 	                 | NUMBER
 	                 | BOOL'''
            print('取值')
            p[0] = p[1]

        def p_assg_stam(p):
            '''assg_stam : assg COMMA assg_stam
 	                     | assg'''
            print('合并赋值表达式，更新时使用')
            if len(p) == 4:
                p[0] = p[3].append(p[1])
            else:
                p[0] = [p[1]]

        def p_assg(p):
            '''assg : attr EQ value'''
            print('将给定值绑定到指定属性上')
            pattern = self.table_definition[p[1]]['type']
            value = str(type(p[3]))
            if re.search(pattern, value):
                p[0] = (p[1], p[3])
            else:
                raise ValueInvalidException(p[1] + '和' + p[3] + '类型不匹配！')

        def p_empty(p):
            'empty :'
            print('空产生式')

        def p_error(p):
            raise SqlSyntaxException('语法解析错误！')

        yaccer = yacc.yacc()
        # yaccer.parse(lexer=lexer)
        return yaccer
