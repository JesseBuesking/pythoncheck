from datetime import datetime
import numpy as np
from math import copysign


class StdGen(object):

    q1 = 53668.0
    a1 = 40014.0
    r1 = 12211.0
    m1 = 2147483563.0

    q2 = 52774.0
    a2 = 40692.0
    r2 = 3791.0
    m2 = 2147483399.0

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return 'StdGen({}, {})'.format(self.a, self.b)

    @classmethod
    def sign(cls, x):
        return 0 if x == 0 else copysign(1, x)

    @classmethod
    def div_mod(cls, n, d):
        q, r = divmod(n, d)
        if StdGen.sign(r) == -StdGen.sign(d):
            return q-1, r+d
        else:
            return q, r

    @classmethod
    def h_mod(cls, n, d):
        _, r = StdGen.div_mod(n, d)
        return r

    @classmethod
    def mk_StdGen(cls, s):
        s = -s if s < 0 else s
        q, s1 = StdGen.div_mod(s, StdGen.m1-1)
        s2 = StdGen.h_mod(q, StdGen.m2-1)
        return StdGen(int(s1+1), int(s2+1))

    @classmethod
    def std_next(cls, x):
        s1, s2 = x.a, x.b

        k = int(s1 / StdGen.q1)
        s1_1 = StdGen.a1 * (s1 - k * StdGen.q1) - k * StdGen.r1
        s1_2 = int(s1 + StdGen.m1 if (s1_1 < 0) else s1_1)
        k_1 = int(s2 / StdGen.q2)
        s2_1 = StdGen.a2 * (s2 - k_1 * StdGen.q2) - k_1 * StdGen.r2
        s2_2 = int(s2_1 + StdGen.m2 if s2_1 < 0 else s2_1)
        z = s1_2 - s2_2
        z_1 = z + StdGen.m1 - 1 if z < 1 else z
        return z_1, StdGen(s1_2, s2_2)

    @classmethod
    def std_split(cls, x):
        s1, s2 = x.a, x.b

        new_s1 = int(1 if s1 == (StdGen.m1 - 1) else s1 + 1)
        new_s2 = int(StdGen.m2 - 1 if s2 == 1 else s2 - 1)
        y = StdGen.std_next(x)[1]
        t1, t2 = y.a, y.b
        left = StdGen(new_s1, t2)
        right = StdGen(t1, new_s2)
        return left, right

    @classmethod
    def ilog_base(cls, b, i):
        if i < b:
            return 1
        else:
            return 1 + StdGen.ilog_base(b, (i / b))

    @classmethod
    def std_range(cls, k, rng):
        l, h = k
        if l > h:
            return StdGen.std_range((h, l), rng), rng
        else:
            k = h - l + 1
            # b = 2147483561 # TODO use this
            # noinspection PyUnresolvedReferences
            b = np.int32(2147483561)
            n = StdGen.ilog_base(b, k)

            def f(n, acc, g):
                if n == 0:
                    return acc, g
                else:
                    x, g_1 = StdGen.std_next(g)
                    # TODO undo np stuff
                    # noinspection PyUnresolvedReferences
                    x = np.int32(x)
                    res_1, res_2 = f((n - 1), (x + acc * b), g_1)
                    return res_1, res_2
            f_res1, f_res2 = f(n, 1, rng)
            return l + (abs(f_res1) % abs(k)), f_res2


rng = StdGen.std_range
split = StdGen.std_split


def new_seed():
    diff = (datetime.utcnow() - datetime.utcfromtimestamp(0))
    diff = int(diff.total_seconds() * 1000)
    return StdGen.mk_StdGen(diff)
