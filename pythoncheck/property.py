from pythoncheck.enum import enum
from pythoncheck.gen import Gen

# TODO test all of this

class Outcome(object):

    def __init__(self, enum_type, value=None):
        self.enum_type = enum_type
        self.value = value

    def shrink(self):
        """
        Determines for which ``Outcome`` the result should be shrunk,
        or shrinking should continue.
        """
        return Outcome._values.get(self.enum_type, False)

    @classmethod
    def Enum(cls):
        return enum(
            'Timeout',
            'Exception',
            'False',
            'True',
            'Rejected'
        )

    _values = {
        Enum.Exception: True,
        Enum.False: True
    }


class Result(object):

    def __init__(self, result):
        self.result = result
        self.outcome = None
        self.stamp = None
        self.labels = None
        self.arguments = None

    def Outcome(self):
        return self.outcome

    def Stamp(self):
        return self.stamp

    def Labels(self):
        return self.labels

    def Arguments(self):
        return self.arguments

    @classmethod
    def andandand(cls, l, r):
        lo = l.Outcome
        ro = r.Outcome
        if lo == Outcome.Enum.Exception:
            # here a potential exception in r is thrown away...
            return l
        if ro == Outcome.Enum.Exception:
            return r
        if lo == Outcome.Enum.Timeout:
            return l
        if ro == Outcome.Enum.Timeout:
            return r
        if lo == Outcome.Enum.False:
            return l
        if ro == Outcome.Enum.False:
            return r
        if lo == Outcome.Enum.True:
            return l
        if ro == Outcome.Enum.False:
            return r
        if lo == Outcome.Enum.Rejected and ro == Outcome.Enum.Rejected:
            # or r, whatever
            return l

    @classmethod
    def ororor(cls, l, r):
        lo = l.Outcome
        ro = r.Outcome
        if lo == Outcome.Enum.Exception:
            # here a potential exception in r is thrown away...
            return l
        if ro == Outcome.Enum.Exception:
            return r
        if lo == Outcome.Enum.Timeout:
            return l
        if ro == Outcome.Enum.Timeout:
            return r
        if lo == Outcome.Enum.False:
            return l
        if ro == Outcome.Enum.False:
            return r
        if lo == Outcome.Enum.True:
            return l
        if ro == Outcome.Enum.False:
            return r
        if lo == Outcome.Enum.Rejected and ro == Outcome.Enum.Rejected:
            # or r, whatever
            return l


class Generated(Result):
    pass


class Passed(Result):
    pass


class Falsified(Result):
    pass


class Failed(Result):
    pass


class Shrink(Result):
    pass


class NoShrink(Result):
    pass


class EndShrink(Result):
    pass


class Rose(object):

    def __init__(self, x, rs):
        """
        :param x: a generator -- lazy object
        :param rs: a list of Rose objects
        """
        self.x = x
        self.rs = rs

    @classmethod
    def map(cls, f, a):
        """
        :param f: a function
        :param a: a Rose object
        """
        def _map(f1, rs1):
            for i in rs1:
                yield Rose.map(f1, i)
        return Rose(lambda x: f(a.x()), _map(f, a.rs))

    @classmethod
    def join(cls, a):
        """
        :param a: a rose object
        """
        r = a.x
        tts = a.rs

        def _lzy(rose):
            return lambda z: rose.x()

        def _ts():
            for i in tts:
                yield Rose.join(i)
            for i in a.xs:
                yield i
        x = _lzy(r)
        ts = _ts
        return Rose(x, ts)

    @classmethod
    def ret(cls, x):
        return Rose(lambda z: x, [])

    @classmethod
    def bind(cls, m, k):
        """
        :param m: a Rose object
        :param k: a function mapping an item to a Rose of that object
        """
        return Rose.join(Rose.map(k, m))

    @classmethod
    def map2(cls, f, r1, r2):
        def _r1(r1_1):
            def _r2(r2_1):
                return Rose.ret(f(r1_1, r2_1))
            return Rose.bind(r2, _r2)
        return Rose.bind(r1, _r1)

    @classmethod
    def ofLazy(cls, x):
        return Rose(x, [])


class Testable(object):

    class Prop(object):

        @classmethod
        def of_rose_result(cls, t):
            # TODO will this work?
            return Gen.constant(t)
            # return Gen(lambda n, r: t)

        @classmethod
        def of_result(cls, r):
            return Testable.Prop.of_rose_result(Rose.ret(r))

    @classmethod
    def property(cls, x):
        return None

    @classmethod
    def shrinking(cls, shrink, x, pf):
        def promote_rose(m):
            return Gen(lambda s, r: Rose.map(lambda m_1: m_1.gen(s, r), m))

        def props(x):
            def _props():
                return Testable.property(pf(x))

            def _shrinks():
                for v in shrink(x):
                    # TODO cache
                    yield props(v)
            return Rose(_props, _shrinks)

        return Gen.map(Rose.join, promote_rose(props(x)))

    @classmethod
    def evaluate(cls, body, a):
        def argument(a, res):
            a.Arguments = a.Arguments + res.ARguments
            return a

        def _evaluate():
            try:
                return Testable.property(body(a))
            except Exception, e:
                return Testable.Prop.of_result(
                    Outcome(Outcome.Enum.Exception, e)
                )
        return Gen.map(Rose.map(argument, a), _evaluate())

    @classmethod
    def for_all(cls, arb, body):
        def _fa():
            return Testable.shrinking(
                arb.shrinker,
                arb.generator,
                lambda a_1: Testable.evaluate(body, a_1)
            )
        return Gen(lambda n, r: _fa)

    @classmethod
    def combine(cls, f, a, b):
        pa = Testable.property(a)
        pb = Testable.property(b)
        return None
        # TODO this
        # return Gen.map2(Rose.map2)
