

from unittest import TestCase
from pythoncheck import default
from pythoncheck.default import shrink_number
from pythoncheck.gen import Gen


class Test(TestCase):

    def test_shrink_number(self):
        x = shrink_number(-10)
        # self.assertEqual([10, 0, -5, -8, -9], x)
        self.assertEqual([10, 0, -5, -7, -8, -9], x)

    def test_bool(self):
        x = default.Bool()
        s = Gen.sample(x.generator, 1, 10)
        self.assertTrue(True in s)
        self.assertTrue(False in s)

    # def test_int(self):
    #     x = default.Int()
    #     s = Gen.sample(x.generator, 10, 10)
    #     for v in s:
    #         shrinks = x.shrinker(v)
