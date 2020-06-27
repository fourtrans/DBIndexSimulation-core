from typing import List, Dict, Tuple, Set
from graphviz import Digraph, nohtml
from functools import reduce
from sql_engine import SqlEngine, Code
from sql_engine import SqlSyntaxException, SqlColumnException, ValueInvalidException
from data_storage import StorageCoordinator
from data_storage import NotUniqueException


class SqlVm(object):
    def __init__(self):
        self.reg_selector = []
        self.reg_table = [[]]
        self.pc = 0

    def locate(self, conditions: List[List[tuple]], db: StorageCoordinator) -> None:
        self.reg_selector = db.locate_all()
        if conditions == []:
            return
        or_selector = []
        for and_cond in conditions:
            and_selector = []
            for cond in and_cond:
                and_selector.append(db.locate(*cond))
            or_selector.append(list(reduce(lambda x, y: x.intersection(y), map(set, and_selector))))
        or_selector = list(reduce(lambda x, y: x.union(y), map(set, or_selector)))
        self.reg_selector = list(set(or_selector).intersection(self.reg_selector))

    def project(self, columns: List[int]):
        new_tbl = []
        for record in self.reg_table:
            one_new_record = []
            for index in columns:
                one_new_record.append(record[index])
            new_tbl.append(tuple(one_new_record))
        self.reg_table = new_tbl

    def run(self, code_list: List[Code], db: StorageCoordinator):
        vm_result = {}
        self.reg_selector = []
        self.reg_table = []
        self.pc = 0
        try:
            while self.pc != len(code_list):
                code = code_list[self.pc]
                if code.opc == 'insert':
                    db.insert(code.opr)
                elif code.opc == 'update':
                    db.update(code.opr, self.reg_selector)
                elif code.opc == 'delete':
                    db.delete(self.reg_selector)
                elif code.opc == 'locate':
                    self.locate(code.opr, db)
                elif code.opc == 'query':
                    self.reg_table = db.query(self.reg_selector)
                elif code.opc == 'project':
                    self.project(code.opr)
                else:
                    raise Exception('[FATAL][Internal Error]SqlVm found unknown opc' + str(code.opc))
                self.pc += 1
        except Exception as e:
            vm_result['is_success'] = False
            vm_result['content'] = []
            vm_result['error_msg'] = str(e)
        else:
            vm_result['is_success'] = True
            vm_result['content'] = self.reg_table
            vm_result['error_msg'] = ''
        return vm_result


class Core(object):
    def __init__(self, table_definition: dict, table_data: List[tuple]):
        self.vm_m = SqlVm()
        self.table_definition_m = table_definition
        self.engine_m = SqlEngine(table_definition)
        self.db_m = StorageCoordinator(table_data, table_definition)

    def execute_sql_expr(self, request: dict) -> dict:
        sql_result = {}
        try:
            # prepare failure result
            sql_result['is_success'] = False
            sql_result['content'] = []
            sql_result['error_msg'] = []
            sql_result['sql_expr'] = request['sql_expr']
            sql_result['serial_number'] = request['serial_number']

            # run sql
            code_list = self.engine_m.resolve_sql_expr(request['sql_expr'])
            vm_result = self.vm_m.run(code_list, self.db_m)

            # rewrite result
            if vm_result['is_success'] == True:
                # compose success sql_result
                sql_result['is_success'] = True
                sql_result['content'] = vm_result['content']
                sql_result['error_msg'] = ''
            else:
                # compose failure sql_result
                sql_result['is_success'] = False
                sql_result['content'] = []
                sql_result['error_msg'] = vm_result['error_msg']

        except KeyError as e:
            sql_result['error_msg'] = '[Exception][KeyError] request to Core is unrecognized format. ' + str(e)
        except SqlSyntaxException as e:
            sql_result['error_msg'] = '[Exception]' + str(e)
        except SqlColumnException as e:
            sql_result['error_msg'] = '[Exception]' + str(e)
        except ValueInvalidException as e:
            sql_result['error_msg'] = '[Exception]' + str(e)
        except NotUniqueException as e:
            sql_result['error_msg'] = '[Exception]' + str(e)
        except Exception as e:
            sql_result['error_msg'] = '[Exception][InternalError] unexpected exception occur. ' + str(e)
        return sql_result

    def generate_index_picture(self, output_path: str, attribute: int) -> None:
        def generate_bplustree_picture(dat: dict, tree_order=3) -> None:
            nonlocal output_path
            dot = Digraph(format='png', node_attr={'shape': 'Mrecord'})
            nodeid2index: Dict[int, int] = {}
            leaf_index: List[int] = []
            index_counter = 0

            def value_str_short(value, truncate: int = 5):
                value_str = str(value)
                if len(value_str) > truncate:
                    value_str = value_str[:truncate] + '...'
                return value_str

            def value_list_2htmltab(value_list: list, leaf_pointer: list = [], is_leaf: bool = False):
                nonlocal tree_order
                tab_body = ''
                writed_block = 0

                it = iter(leaf_pointer)
                for value in value_list:
                    tab_body += f'<f{str(writed_block)}>'
                    tab_body += value_str_short(value)
                    if writed_block != tree_order - 1:
                        tab_body += '|'
                    writed_block += 1

                for i in range(tree_order - writed_block):
                    tab_body += f'<f{str(writed_block)}>'
                    if writed_block != tree_order - 1:
                        tab_body += '|'
                    writed_block += 1

                if is_leaf:
                    tab_body += nohtml(r'|<next>Next-\>')

                return f'''{{{tab_body}}}'''

            def dfs_traverse(node: dict, father_index: int = None):
                nonlocal nodeid2index, leaf_index, index_counter
                nonlocal dot
                nonlocal tree_order

                # get current node index
                current_index = 0
                if id(node) in nodeid2index:
                    current_index = nodeid2index[id(node)]
                else:
                    current_index = index_counter
                    nodeid2index[id(node)] = current_index  # update index map
                    index_counter += 1

                # build current node and expand to children
                if node['type'] == 'node':
                    dot.attr('node', style='filled', fillcolor='lightblue2', color='black')
                    dot.node(str(current_index), value_list_2htmltab(node['node_value']))
                    for child_node in node['node_pointer']:
                        dfs_traverse(child_node, father_index=current_index)
                elif node['type'] == 'leaf':
                    dot.attr('node', style='filled', fillcolor='lightyellow', color='black')
                    dot.node(str(current_index),
                             value_list_2htmltab(node['leaf_value'], is_leaf=True, leaf_pointer=node['leaf_pointer']))
                    leaf_index.append(current_index)
                else:
                    raise Exception('InteralError: index tree data is not formatted')

                # add edge to father
                if father_index is not None:
                    dot.edge(str(father_index), str(current_index))

            # build tree
            dfs_traverse(dat)

            # # add edge to next_leaf if this node is leaf
            # using constraint attribute will make graphviz failed to process, reason unknown
            # for i in range(len(leaf_index)):
            #     if i != len(leaf_index) - 1:
            #         dot.edge(str(leaf_index[i]) + ':next', str(leaf_index[i + 1]), constraint="false")

            dot.render(filename=output_path)

        dat = self.db_m.get_index_structure(attribute)
        generate_bplustree_picture(dat)
