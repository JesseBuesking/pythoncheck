"""
Adding enum support.

See: http://stackoverflow.com/a/1695250/435460
"""


import copy


def enum(*sequential, **named):
    """
    An enumerable object.

    Example:

    >>> Numbers = enum(ONE=1, TWO=2, THREE='three')
    >>> Numbers.ONE
    1
    >>> Numbers.TWO
    2
    >>> Numbers.THREE
    'three'
    >>> Numbers.reverse_mapping['three']
    'THREE'

    :param args sequential: enum values
    :param kwargs named: named enumerations
    :returns: the enumeration object
    :rtype: enum
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums["dict"] = copy.deepcopy(enums)
    enums["reverse_mapping"] = reverse
    return type('Enum', (), enums)

