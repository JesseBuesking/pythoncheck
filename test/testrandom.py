

from unittest import TestCase
from pythoncheck.random import StdGen, rng, split, new_seed
from test.helpers import for_examples


class Test(TestCase):

    @for_examples(
        (100, -9, -12, -8),
        (100, 9, 11, 1),
        (-10, -1, 10, 0)
    )
    def test_div_mod(self, n, d, o, e):
        x = StdGen.div_mod(n, d)
        self.assertEqual((o, e), x)

    @for_examples(
        (0, 1, 1),
        (-1, 2, 1),
        (1, 2, 1)
    )
    def test_mk_StdGen(self, x, a, b):
        x = StdGen.mk_StdGen(x)
        self.assertEqual((a, b), (x.a, x.b))

    @for_examples(
        (StdGen(0, 0), (2147483562, StdGen(0, 0))),
        (StdGen(0, 1), (2147442870, StdGen(0, 40692))),
        (StdGen(0, -1), (40855, StdGen(0, 2147442707))),
        (StdGen(1, 0), (40014, StdGen(40014, 0))),
        (StdGen(-1, 0), (2147483562, StdGen(2147483562, 0)))
    )
    def test_std_next(self, x, y):
        y_0 = y[0]
        y_1 = y[1]

        z = StdGen.std_next(x)
        z_0 = z[0]
        z_1 = z[1]
        self.assertEqual(y_0, z_0)
        self.assertEqual((y_1.a, y_1.b), (z_1.a, z_1.b))

    @for_examples(
        (StdGen(0, 0), (StdGen(1, 0), StdGen(0, -1))),
        (StdGen(0, 1), (StdGen(1, 40692), StdGen(0, 2147483398))),
        (StdGen(0, -1), (StdGen(1, 2147442707), StdGen(0, -2))),
        (StdGen(1, 0), (StdGen(2, 0), StdGen(40014, -1))),
        (StdGen(-1, 0), (StdGen(0, 0), StdGen(2147483562, -1)))
    )
    def test_std_split(self, x, y):
        y_0 = y[0]
        y_1 = y[1]

        z = split(x)
        z_0 = z[0]
        z_1 = z[1]
        self.assertEqual((y_0.a, y_0.b), (z_0.a, z_0.b))
        self.assertEqual((y_1.a, y_1.b), (z_1.a, z_1.b))

    @for_examples(
        (1, 0, 1)
    )
    def test_std_split(self, x, y, z):
        a = StdGen.ilog_base(x, y)
        self.assertEqual(z, a)

    @for_examples(
        (((1, 2), StdGen(0, 0)), (2, StdGen(0, 0))),
        (((3, 7), StdGen(3, 2)), (5, StdGen(120042, 81384))),
        (((2, 7), StdGen(3, 2)), (7, StdGen(120042, 81384)))
    )
    def test_std_range(self, x, y):
        o, p = x[0], x[1]
        y_0 = y[0]
        y_1 = y[1]

        z = rng(o, p)
        z_0 = z[0]
        z_1 = z[1]

        self.assertEqual(y_0, z_0)
        self.assertEqual((y_1.a, y_1.b), (z_1.a, z_1.b))
