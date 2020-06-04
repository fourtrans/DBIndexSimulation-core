import unittest


def return_x(x):
    return x


# 测试以类为单位，叫“测试套件”，一个类就是一个测试套件，其命名就是你测试套件的名字，测试类必须继承unittest.TestCase
class TestSampleClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # 必须使用@classmethod 装饰器，所有test运行前运行一次
        # 该方法会在整个测试套件中首先执行，即先于其他所有方法之前执行，相当于测试前的准备工作
        print('[CLASS_LEVEL]setUpClass')

    @classmethod
    def tearDownClass(self):
        # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
        # 该方法会在测试套件最后执行，即所有其他测试方法结束后执行, 相当于测试的扫尾工作
        print('[CLASS_LEVEL]tearDownClass')

    def setUp(self):
        # 该方法会在每个测试方法运行前执行
        print('setUp for one method')
        pass

    def tearDown(self):
        # 该方法会在每个测试方法运行后执行
        print('tearDown for one method')
        pass

    # 在测试类中定义以test开头命名的方法，就是你的测试内容
    def test_sample_method(self):
        # 该方法为测试测试代码
        self.assertEqual(return_x(1), 1)
        self.assertNotEqual(return_x(2),1)
        self.assertTrue(return_x(True), True)
        self.assertFalse(return_x(False), False)
        self.assertIsNone(return_x(None))
        self.assertIsNotNone(return_x(1))
        self.assertIn(return_x(2),[1,2,3])
        self.assertNotIn(return_x(10),(1,2,3,4))

    def test_foo(self):
        # 该方法为测试测试代码
        self.assertEqual(self.foo(), None)

    def foo(self):
        pass
