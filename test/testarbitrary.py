

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
