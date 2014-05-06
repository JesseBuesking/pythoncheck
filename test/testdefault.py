

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
        s = Gen.sample(1, 10, x.generator)
        self.assertTrue(True in s)
        self.assertTrue(False in s)

    def test_int(self):
        size = 100
        x = default.Int()
        v = -1

        # test generator
        rs = Gen.resize(size, x.generator)
        s = Gen.sample(1, size, rs)
        for i in s:
            self.assertTrue(-size <= i <= size)

        # test shrinker
        sh = x.shrinker(v)
        for i in sh:
            self.assertTrue(i <= abs(i))
