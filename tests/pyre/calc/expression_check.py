#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise the expression recognizer
"""


def test():
    import pyre.calc

    # sucesses
    assert pyre.calc.isExpression("{test}") is not None
    assert pyre.calc.isExpression("{{test}}") is not None

    # failures
    assert pyre.calc.isExpression("test") is None

    return pyre.calc.isExpression


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file 
