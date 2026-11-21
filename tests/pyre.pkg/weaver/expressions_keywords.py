#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the expression mills render literals when the caller passes keyword arguments
"""


def test():
    """
    Render a literal and an operation through the python mill, with a keyword argument
    """
    # get the package
    import pyre

    # instantiate a weaver
    weaver = pyre.weaver.weaver(name="keywords")
    # that speaks python
    weaver.language = "python"
    # access its mill
    mill = weaver.language

    # build a node
    one = pyre.calc.var(value=1)

    # a literal renders as itself
    assert mill.expression(one, context=None) == "1"
    # and so do the operands of an operation
    assert mill.expression(one + one, context=None) == "(1) + (1)"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
