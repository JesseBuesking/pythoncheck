

from unittest import TestCase
from pythoncheck import default
from pythoncheck.gen import Gen


class Test(TestCase):

    def test_bool(self):
        x = default.Bool()
        s = Gen.sample(x.generator, 1, 10)
        self.assertTrue(True in s)
        self.assertTrue(False in s)
