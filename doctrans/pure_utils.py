"""
Pure utils for pure functions. For the same input will always produce the same output.
"""
from platform import python_version_tuple
from pprint import PrettyPrinter
from sys import version

pp = PrettyPrinter(indent=4).pprint
tab = " " * 4
simple_types = {"int": 0, float: 0.0, "str": "", "bool": False}


# From https://github.com/Suor/funcy/blob/0ee7ae8/funcy/funcs.py#L34-L36
def rpartial(func, *args):
    """Partially applies last arguments."""
    return lambda *a: func(*(a + args))


def identity(s):
    """
    Identity function

    :param s: Any value
    :type s: ```Any```

    :returns: the input value
    :rtype: ```Any```
    """
    return s


PY3_8 = version.startswith("3.8")
PY_GTE_3_9 = python_version_tuple() >= ("3", "9")
