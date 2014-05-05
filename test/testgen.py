

from unittest import TestCase
from pythoncheck import default
from pythoncheck.gen import Gen


class Test(TestCase):

    def test_sized(self):
        def test(a):
            return Gen(lambda n, r: a + 3)
        k = Gen.sized(test)
        ks = Gen.sample(k, 1, 10)
        self.assertTrue(3 in ks)
        self.assertTrue(4 in ks)

    def test_oneof(self):
        k = Gen.oneof([default.Bool().generator, default.Bool().generator])
        ks = Gen.sample(k, 1, 10)
        self.assertTrue(True in ks)
        self.assertTrue(False in ks)

    def test_frequency(self):
        k = Gen.frequency([
            (1, default.Bool().generator),
            (2, default.Bool().generator)
        ])
        ks = Gen.sample(k, 1, 10)
        self.assertTrue(True in ks)
        self.assertTrue(False in ks)
