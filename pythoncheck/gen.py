from pythoncheck import random
from pythoncheck.random import StdGen, rng, split, new_seed


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

    def Next(self):
        s = new_seed()
        return self.gen(s.a, new_seed())

    @classmethod
    def bind(cls, m, k):
        def _bind(n, r0):
            r1, r2 = split(r0)
            m_1 = k(m.gen(n, r1))
            return m_1.gen(n, r2)
        return Gen(_bind)

    @classmethod
    def map(cls, f, gn):
        return gn.Map(f)

    @classmethod
    def sized(cls, fgen):
        def _sized(n, r):
            m = fgen(n)
            return m.gen(n, r)
        return Gen(_sized)

    # TODO verify
    @classmethod
    def resize(cls, n, gn):
        return Gen(lambda _, r: gn.gen(n, r))

    @classmethod
    def rand(cls):
        return Gen(lambda n, r: r)

    @classmethod
    def eval(cls, n, rnd, gn):
        size, rnd_1 = rng((0, n), rnd)
        return gn.gen(size, rnd_1)

    @classmethod
    def sample(cls, size, n, gn):
        def _sample(i, seed, samples):
            if 0 == i:
                return samples
            else:
                samples = [Gen.eval(size, seed, gn)] + samples
                return _sample(
                    i - 1,
                    StdGen.std_split(seed)[1],
                    samples
                )
        return _sample(n, random.new_seed(), [])

    @classmethod
    def choose(cls, l, h):
        return Gen.map(
            lambda stdgen: rng((l, h), stdgen)[0],
            Gen.rand()
        )

    @classmethod
    def elements(cls, xs):
        return Gen.map(
            lambda i: xs[i],
            Gen.choose(0, len(xs) - 1)
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

    @classmethod
    def sequence(cls, l):
        def go(gs, acc, size, r0):
            if 0 == len(gs):
                return acc[::-1]
            else:
                g = gs[0]
                gs_1 = gs[1:]
                r1, r2 = split(r0)
                y = g.gen(size, r1)
                acc = [y] + acc
                return go(gs_1, acc, size, r2)
        return Gen(lambda n, r: go(l, [], n, r))

    @classmethod
    def list_of_length(cls, n, gn):
        return Gen.sequence([gn for _ in range(n)])

    @classmethod
    def list_of(cls, gn):
        def _s(n):
            k = Gen.choose(0, n + 1)
            k = k.Next()
            return Gen.list_of_length(k, gn)
        return Gen.sized(_s)

    @classmethod
    def non_empty_list_of(cls, gn):
        def _s(n):
            k = Gen.choose(1, max(1, n))
            k = k.Next()
            return Gen.list_of_length(k, gn)
        return Gen.sized(_s)

    @classmethod
    def sublist_of(cls, l):
        # noinspection PyUnusedLocal
        def _s(n, r):
            size = Gen.choose(0, len(l) - 1).Next()
            indices = Gen.list_of_length(size, Gen.choose(0, len(l) - 1))
            indices = indices.Next()
            indices = list(set(indices))
            subseq = []
            for i in indices:
                subseq.append(l[i])
            return subseq
        return Gen(_s)

    @classmethod
    def constant(cls, v):
        return Gen(lambda n, r: v)

    @classmethod
    def apply(cls, f, gn):
        # noinspection PyUnusedLocal
        def _apply(n, r):
            f_1 = f.Next()
            gn_1 = gn.Next()
            return f_1(gn_1)
        return Gen(_apply)

    @classmethod
    def promote(cls, f):
        return Gen(lambda n, r: lambda a: f(a).gen(n, r))

    # TODO verify
    @classmethod
    def map2(cls, f):
        def _ab(a, b):
            return Gen(lambda n, r: f(a, b))
        return _ab


class Arbitrary(object):

    def __init__(self):
        self.generator = None
        self.shrinker = []
