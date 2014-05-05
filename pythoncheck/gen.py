from pythoncheck import random
from pythoncheck.random import StdGen, rng, split


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
    def bind(cls, m, k):
        def _bind(n, r0):
            r1, r2 = split(r0)
            m_1 = k(m.gen(n, r1))
            return m_1.gen(n, r2)
        return Gen(_bind)

    @classmethod
    def map(cls, gn, f):
        return gn.Map(f)

    @classmethod
    def sized(cls, fgen):
        def _sized(n, r):
            m = fgen(n)
            return m.gen(n, r)
        return Gen(_sized)

    # TODO verify
    @classmethod
    def resize(cls, gn, n):
        return Gen(lambda _, r: gn.gen(n, r))

    @classmethod
    def rand(cls):
        return Gen(lambda n, r: r)

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

    @classmethod
    def oneof(cls, gens):
        """
        :param list gens: a list of generators
        """
        return Gen.bind(Gen.elements(gens), lambda x: x)

    @classmethod
    def frequency(cls, xs):
        tot = sum([i[0] for i in xs])

        def _pick(n, ys):
            (k, x), xs = ys[0], ys[1:]
            if n <= k:
                return x
            else:
                return _pick(n - k, xs)

        return Gen.bind(Gen.choose(1, tot), lambda n: _pick(n, xs))


class Arbitrary(object):

    def __init__(self):
        self.generator = None
        self.shrinker = []
