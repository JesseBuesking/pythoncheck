

from unittest import TestCase
from pythoncheck import default
from pythoncheck.gen import Gen
from pythoncheck.random import new_seed


class Test(TestCase):

    def test_sized(self):
        def test(a):
            return Gen(lambda n, r: a + 3)
        k = Gen.sized(test)
        ks = Gen.sample(1, 10, k)
        self.assertTrue(3 in ks)
        self.assertTrue(4 in ks)

    def test_oneof(self):
        k = Gen.oneof([default.Bool().generator, default.Bool().generator])
        ks = Gen.sample(1, 10, k)
        self.assertTrue(True in ks)
        self.assertTrue(False in ks)

    def test_frequency(self):
        k = Gen.frequency([
            (1, default.Bool().generator),
            (2, default.Bool().generator)
        ])
        ks = Gen.sample(1, 10, k)
        self.assertTrue(True in ks)
        self.assertTrue(False in ks)

    def test_sequence(self):
        s = Gen.sequence([Gen.constant(1), Gen.constant(3)])
        ss = Gen.sample(1, 10, s)
        for v in ss:
            self.assertEqual(1, v[0])
            self.assertEqual(3, v[1])

    def test_list_of_length(self):
        s = Gen.list_of_length(2, Gen.constant(1))
        ss = Gen.sample(1, 10, s)
        for v in ss:
            self.assertEqual(1, v[0])
            self.assertEqual(1, v[1])

    def test_list_of(self):
        s = Gen.list_of(Gen.constant(1))
        ss = Gen.sample(1, 10, s)
        lens = set()
        for v in ss:
            lens.add(len(v))
            for i in v:
                self.assertEqual(1, i)

        self.assertTrue(0 < len(lens) < 4)
        for l in lens:
            self.assertTrue(l in {0, 1, 2})

    def test_non_empty_list_of(self):
        s = Gen.non_empty_list_of(Gen.constant(1))
        ss = Gen.sample(1, 10, s)
        lens = set()
        for v in ss:
            lens.add(len(v))
            for i in v:
                self.assertEqual(1, i)

        self.assertTrue(0 < len(lens) < 4)
        for l in lens:
            self.assertTrue(l in {1, 2})
            self.assertNotEqual(0, l)

    def test_sublist_of(self):
        s = Gen.sublist_of([1, 2, 3, 4, 5])
        for i in range(10):
            ss = Gen.eval(1, new_seed(), s)
            self.assertTrue(0 <= len(ss) <= 5)
            for v in ss:
                self.assertTrue(v in {1, 2, 3, 4, 5})

    def test_apply(self):
        for i in range(10):
            for j in range(10):
                s = Gen.apply(
                    Gen(lambda n, r: lambda a: a + i),
                    Gen(lambda n, r: j)
                )
                ss = s.Next()
                self.assertEqual(i + j, ss)

    def test_promote(self):
        for i in range(10):
            for j in range(10):
                s = Gen.promote(lambda a: Gen(lambda n, r: a + j))
                ss = s.Next()
                self.assertEqual(i + j, ss(i))
