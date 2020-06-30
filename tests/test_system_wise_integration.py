import unittest

from core import Core

TABLE_DEFINITION_SAMPLE = {
    0: {
        'name': 'sno',
        'type': 'str',
        'is_nullable': False,
        'is_unique': True,
        'is_key': True
    },
    1: {
        'name': 'name',
        'type': 'str',
        'is_nullable': False,
        'is_unique': False,
        'is_key': False
    },
    2: {
        'name': 'academy',
        'type': 'str',
        'is_nullable': False,
        'is_unique': False,
        'is_key': False
    },
    3: {
        'name': 'major',
        'type': 'str',
        'is_nullable': False,
        'is_unique': False,
        'is_key': False
    },
    4: {
        'name': 'mid_grade',
        'type': 'int',
        'is_nullable': True,
        'is_unique': False,
        'is_key': False
    },
    5: {
        'name': 'final_grade',
        'type': 'int',
        'is_nullable': True,
        'is_unique': False,
        'is_key': True
    },
    6: {
        'name': 'usual_grade',
        'type': 'int',
        'is_nullable': True,
        'is_unique': False,
        'is_key': False
    },
    7: {
        'name': 'total_grade',
        'type': 'int',
        'is_nullable': True,
        'is_unique': False,
        'is_key': True
    },
}

INSERTION_SQL_EXPR = [
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E003','张三','计科院','计科',100,98,58,92",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P104','莫晨云','物院','材料',90,100,99,98",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E106','王啸','计科院','软件',92,100,82,96",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F010','朱荣耀','外院','英语',99,86,83,87",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P002','李丽容','物院','物理',99,79,94,84",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F008','鲁子豪','外院','英语',99,43,85,57",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D103','唐楠林','数院','基础数学',98,76,73,78",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P103','张丽','物院','材料',95,99,91,97",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D108','沈丽辉','数院','基础数学',94,97,89,95",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E102','冯零','计科院','软件',93,81,71,81",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E002','钱小三','计科院','计科',92,84,76,84",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E005','孙五','计科院','计科',91,91,91,91",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P004','韩欣冉','物院','物理',91,65,90,72",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E104','吴顺','计科院','软件',90,95,84,92",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P102','汪洁','物院','材料',89,69,86,74",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D107','鲍悦','数院','基础数学',89,58,64,63",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P001','张天欣','物院','物理',88,76,94,80",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F204','储彩玉','外院','俄语',88,73,82,76",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E004','张柳','计科院','计科',87,92,62,86",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F102','叶凯强','外院','法语',87,87,99,88",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F104','陈晓娴','外院','法语',87,53,57,58",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P101','吕筱涵','物院','材料',86,97,99,95",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E105','陈银萍','计科院','软件',86,95,91,93",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'P003','张方露','物院','物理',86,77,97,81",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F004','方雅琪','外院','英语',86,62,98,71",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F012','张欣浩','外院','英语',85,58,81,65",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F206','杨慧','外院','俄语',82,96,92,93",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F007','陈志辉','外院','英语',81,91,85,88",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E103','强金烨','计科院','软件',80,84,96,85",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F203','刘梦欣','外院','俄语',80,45,85,56",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F001','陶海霞','外院','英语',79,77,78,77",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F011','王蕾','外院','英语',77,66,93,71",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F202','任婧婧','外院','俄语',75,92,82,87",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D104','王馨阁','数院','基础数学',71,86,68,81",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E108','唐清华','计科院','软件',71,66,89,70",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E101','郑旺','计科院','软件',70,96,89,91",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F205','杨雨林','外院','俄语',70,79,88,79",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D109','洪晓琪','数院','基础数学',69,60,73,63",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E107','吴青勇','计科院','软件',68,95,87,89",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F106','储庆庆','外院','法语',68,55,50,56",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D106','黄鹏程','数院','基础数学',67,78,94,78",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E109','陈新岳','计科院','软件',66,86,94,84",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F201','周峰','外院','俄语',66,62,61,62",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F103','陈静','外院','法语',65,50,89,58",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E001','赵小二','计科院','计科',64,87,79,82",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F105','滕越','外院','法语',63,81,56,74",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D105','韩杰','数院','基础数学',63,67,45,63",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F101','刘光中','外院','法语',61,98,84,90",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F002','刘海燕','外院','英语',61,54,79,58",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E007','周五','计科院','计科',60,92,44,80",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D004','陈甜甜','数院','应用数学',60,76,91,75",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D002','曾雨舟','数院','应用数学',58,51,85,57",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D101','殷雨生','数院','基础数学',54,52,67,54",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D110','陈艺凡','数院','基础数学',51,55,68,56",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F005','周雨辰','外院','英语',49,97,53,83",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F003','李思琪','外院','英语',49,63,46,58",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F009','余欣雨','外院','英语',48,70,87,69",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D003','樊荣','数院','应用数学',48,55,87,58",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D102','朱晶晶','数院','基础数学',48,47,97,54",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'E006','李一','计科院','计科',47,97,98,89",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D006','雍家伟','数院','应用数学',45,58,44,53",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D001','蒋建','数院','应用数学',41,95,84,85",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'F006','许婷','外院','英语',41,87,59,75",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D005','修苹苹','数院','应用数学',41,44,76,48",
    "INSERT sno, name, academy, major, mid_grade, final_grade, usual_grade, total_grade VALUES 'D007','唐文鹃','数院','应用数学',40,59,47,54"
]

sql_counter = 0


def make_sql_request(sql: str) -> dict:
    global sql_counter
    sql_counter += 1
    return {'sql_expr': sql, 'serial_number': sql_counter}


class Test_System_Integration_Insert(unittest.TestCase):
    def setUp(self) -> None:
        self.core = Core(TABLE_DEFINITION_SAMPLE, [])

    def run_sql(self, sql) -> dict:
        return self.core.execute_sql_expr(make_sql_request(sql))

    def test_insert_1(self):
        self.assertTrue(self.run_sql(INSERTION_SQL_EXPR[0])['is_success'])
        result = self.run_sql('SELECT *')
        self.assertEqual(1, len(result['content']))

    def test_insert_all(self):
        for sql in INSERTION_SQL_EXPR:
            self.core.execute_sql_expr(make_sql_request(sql))
        result = self.run_sql('SELECT *')
        self.assertEqual(65, len(result['content']))


class Test_System_Integration_Delete(unittest.TestCase):
    def setUp(self) -> None:
        self.core = Core(TABLE_DEFINITION_SAMPLE, [])
        for sql in INSERTION_SQL_EXPR:
            self.core.execute_sql_expr(make_sql_request(sql))

    def run_sql(self, sql) -> dict:
        return self.core.execute_sql_expr(make_sql_request(sql))

    def test_delete_1(self):
        self.assertEqual(65, len(self.run_sql("SELECT *")['content']))
        self.assertTrue(self.run_sql("delete WHERE sno = 'E003'")['is_success'])
        self.assertEqual(64, len(self.run_sql("SELECT *")['content']))

    def test_delete_multiple(self):
        self.assertEqual(65, len(self.run_sql("SELECT *")['content']))
        self.assertTrue(self.run_sql("delete WHERE total_grade >= 60")['is_success'])
        self.assertEqual(15, len(self.run_sql("SELECT *")['content']))


class Test_System_Integration_Select(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.core = Core(TABLE_DEFINITION_SAMPLE, [])
        for sql in INSERTION_SQL_EXPR:
            self.core.execute_sql_expr(make_sql_request(sql))

    def run_sql(self, sql) -> dict:
        return self.core.execute_sql_expr(make_sql_request(sql))

    def test_sample1(self):
        self.assertEqual(28, len(self.run_sql('SELECT * WHERE mid_grade > 80')['content']))

    def test_sample2(self):
        self.assertEqual(38, len(self.run_sql('SELECT * WHERE final_grade > 75')['content']))

    def test_sample3(self):
        self.assertEqual(46, len(self.run_sql('SELECT * WHERE usual_grade < 90')['content']))

    def test_sample4(self):
        self.assertEqual(15, len(self.run_sql('SELECT * WHERE total_grade < 60')['content']))

    def test_sample5(self):
        self.assertEqual(15, len(self.run_sql('SELECT * WHERE total_grade <= 59')['content']))

    def test_sample6(self):
        self.assertEqual(2, len(self.run_sql("SELECT * WHERE name LIKE '朱%'")['content']))

    def test_sample7(self):
        self.assertEqual(12, len(self.run_sql("SELECT * WHERE major = '英语'")['content']))

    def test_sample8(self):
        self.assertEqual(33, len(self.run_sql("SELECT * WHERE academy = '计科院' OR academy = '数院'")['content']))

    def test_sample9(self):
        self.assertEqual(61, len(self.run_sql("SELECT * WHERE major <> '材料'")['content']))

    def test_sample10(self):
        self.assertEqual(20, len(self.run_sql(
            "SELECT * WHERE name = '朱晶晶' OR major = '计科' OR major = '英语' AND total_grade > 60 OR major = '应用数学' AND usual_grade >= 85")[
                                     'content']))

    def test_sample11(self):
        self.assertEqual([(87, 99, 86)],
                         self.run_sql("SELECT total_grade, mid_grade, final_grade WHERE name = '朱荣耀'")['content'])

    def test_sample12(self):
        self.assertEqual([('张三', '计科院', '计科', 100, 92, 92, 'E003')], self.run_sql(
            "SELECT name, academy, major, mid_grade, total_grade, total_grade, sno WHERE name = '张三'")['content'])


class Test_System_Integration_Update(unittest.TestCase):
    def setUp(self) -> None:
        self.core = Core(TABLE_DEFINITION_SAMPLE, [])
        for sql in INSERTION_SQL_EXPR:
            self.core.execute_sql_expr(make_sql_request(sql))

    def run_sql(self, sql) -> dict:
        return self.core.execute_sql_expr(make_sql_request(sql))

    def test_update_1record(self):
        self.run_sql("UPDATE SET name='法外狂徒张三' WHERE name = '张三'")
        self.assertEqual(0, len(self.run_sql("SELECT * WHERE name = '张三'")['content']))
        self.assertEqual(1, len(self.run_sql("SELECT * WHERE name = '法外狂徒张三'")['content']))

    def test_update_multiple_records(self):
        self.run_sql("UPDATE SET name='守法良民' WHERE name <> '张三'")
        self.assertEqual(64, len(self.run_sql("SELECT * WHERE name = '守法良民'")['content']))
        self.assertEqual(1, len(self.run_sql("SELECT * WHERE name <> '守法良民'")['content']))


if __name__ == '__main__':
    unittest.main()
