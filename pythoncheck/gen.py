from pythoncheck import random
from pythoncheck.random import StdGen, rng


class Gen(object):

    def __init__(self, gen):
        """
        :param function gen: a function
        """
        self.gen = gen

    def Map(self, f):
        """
        :param function f: a function
        """
        return Gen(lambda n, r: f(self.gen(n, r)))

    @classmethod
    def map(cls, gn, f):
        return gn.Map(f)

    @classmethod
    def eval(cls, gn, n, rnd):
        size, rnd_1 = rng((0, n), rnd)
        return gn.gen(size, rnd_1)

    @classmethod
    def sample(cls, gn, size, n):
        def _sample(i, seed, samples):
            if 0 == i:
                return samples
            else:
                samples = [Gen.eval(gn, size, seed)] + samples
                return _sample(
                    i - 1,
                    StdGen.std_split(seed)[1],
                    samples
                )
        return _sample(n, random.new_seed(), [])

    @classmethod
    def rand(cls):
        return Gen(lambda n, r: r)

    @classmethod
    def choose(cls, l, h):
        return Gen.map(
            Gen.rand(),
            lambda stdgen: rng((l, h), stdgen)[0]
        )

    @classmethod
    def elements(cls, xs):
        return Gen.map(
            Gen.choose(0, len(xs) - 1),
            lambda i: xs[i]
        )


class Arbitrary(object):

    def __init__(self):
        self.generator = None
        self.shrinker = []
