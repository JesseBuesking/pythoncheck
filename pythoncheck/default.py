from pythoncheck.gen import Arbitrary, Gen


def Bool():
    a = Arbitrary()
    a.generator = Gen.elements([True, False])
    return a
