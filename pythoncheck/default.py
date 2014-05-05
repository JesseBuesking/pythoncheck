from pythoncheck.gen import Arbitrary, Gen


def shrink_number(n):
    two = 1 + 1

    def _nums():
        if 0 > n:
            yield -n
        if 0 != n:
            yield 0

        def halver(st):
            st /= two
            nst = n - st
            if abs(nst) <= abs(n):
                yield nst
            for v in halver(st):
                yield v

        for v in halver(n):
            yield v

    ret = []
    for v in _nums():
        if v in ret:
            return list(set(ret))
        ret.append(v)


def Bool():
    a = Arbitrary()
    a.generator = Gen.elements([True, False])
    return a


def Int():
    a = Arbitrary()
    a.generator = Gen.sized(lambda n: Gen.choose(-n, n))
    a.shrinker = lambda n: shrink_number(n)
    return a
