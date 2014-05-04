"""
Helpers for writing unit tests.
"""


import sys


def for_examples(*parameters):
    """
    Decorator for supplying input for multiple tests.

    :param parameters:
    """

    def tuplify(x):
        """

        :param x:
        :return:
        """
        if not isinstance(x, tuple):
            return x,
        return x

    def decorator(method, parameters=parameters):
        """

        :param method:
        :param parameters:
        :return:
        """
        for parameter in (tuplify(x) for x in parameters):

            # noinspection PyDocstring
            def method_for_parameter(self, method=method, parameter=parameter):
                method(self, *parameter)
            param_args = ",".join(repr(v) for v in parameter)
            name_for_parameter = method.__name__ + "(" + param_args + ")"
            frame = sys._getframe(1)  # pylint: disable-msg=W0212
            frame.f_locals[name_for_parameter] = method_for_parameter
            frame.f_locals[name_for_parameter].__doc__ = method.__doc__
        return None
    return decorator
