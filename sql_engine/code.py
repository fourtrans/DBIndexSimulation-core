from typing import List, Dict, Tuple, Set


class Code(object):

    def __init__(self, opc: str, opr):
        self.opc = opc
        self.opr = opr

    def __eq__(self, other):
        if self.opc == other.opc:
            # 判断操作数是否一致
            if self.opc == 'locate':
                # 条件定位
                if len(self.opr) == len(other.opr):
                    # 判断每个元组是否相等
                    for i in range(len(self.opr)):
                        for j in range(len(self.opr[i])):
                            if self.opr[i][j] != other.opr[i][j]:
                                return False
                    return True
                else:
                    # 长度不一致
                    return False
        else:
            return False
