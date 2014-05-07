from pythoncheck.gen import Gen
from pythoncheck.property import Outcome, Failed, Passed, Falsified, EndShrink
from pythoncheck.random import split


class Config(object):
    """
    Configuration options for tests.
    """

    def __init__(self):
        self.values = dict()

    def max_test(self):
        """
        The maximum number of tests that are run.
        """
        return self.values.get('max_test', 100)

    def max_fail(self):
        """
        The maximum number of tests where values are rejected.
        e.g. as the result of ==>
        """
        return self.values.get('max_fail', 1)

    def replay(self):
        """
        If set, the seed to use to start testing. allows reproduction of
        previous runs.
        """
        return self.values.get('replay', None)

    def name(self):
        """
        Name of the test.
        """
        return self.values.get('name', None)

    def start_size(self):
        """
        The size to use for the first test.
        """
        return self.values.get('start_size', 1)

    def end_size(self):
        """
        The size to use for the last test, when all the tests are passing. the
        size increases linearly between ``start_size`` and ``end_size``.
        """
        return self.values.get('end_size', 100)

    def every(self):
        """
        What to print when the new arguments args are generated in test n.
        """
        return self.values.get('every', lambda n, r: None)

    def every_shrink(self):
        """
        What to print every time a counter-example is successfully shrunk.
        """
        return self.values.get('every_shrink', lambda n: None)

    def arbitrary(self):
        """
        The arbitrary instances on this class will be merged in back to front
        order, i.e. instances for the same generated type at the front of the
        list will override those at the back. The instances on ``default`` are
        always known, and are at the back (so they can always be overridden).
        """
        return self.values.get('arbitrary', None)


class Runner(object):

    @classmethod
    def shrink_result(cls, result, shrinks):
        # TODO this
        pass

    @classmethod
    def test(cls, init_size, resize, rnd0, gen):
        """
        :param init_size:
        :param resize:
        :param rnd0:
        :param gen:
        """
        while True:
            rnd1, rnd2 = split(rnd0)
            new_size = resize(init_size)
            rnd = int(round(new_size))
            rose = Gen.eval(rnd, rnd2, gen)
            result = rose.x()
            yield result.Arguments()
            oc = result.Outcome()
            if oc == Outcome.Enum.Rejected:
                yield Failed(result)
            elif oc == Outcome.Enum.True:
                yield Passed(result)
            elif hasattr(oc, 'shrink'):
                yield Falsified(result)
                yield Runner.shrink_result(result, rose.rs)
            else:
                yield Falsified(result)
                yield EndShrink(result)
            yield Runner.test(new_size, resize, rnd1, gen)
