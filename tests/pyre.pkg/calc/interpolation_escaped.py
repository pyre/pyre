#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that doubled braces in interpolations stand for literal braces, and that a reference wrapped
in them is still a reference
"""


def test():
    # access the package
    import pyre.calc

    # build a model
    model = pyre.calc.model()

    # escaped macro delimiters
    node = model.interpolation("{{production}}")
    # verify it made a variable
    assert type(node) is model.node.variable

    # and another
    node = model.interpolation("{{{{cost per unit}}}}")
    # verify it made a variable
    assert type(node) is model.node.variable

    # finally
    tricky = model.interpolation("{{{number of items}}}")
    # verify it made an interpolation
    assert type(tricky) is model.node.interpolation
    # with an unresolved node
    try:
        # so asking for its value
        tricky.value
        # must fail
        assert False
    # with the correct error
    except tricky.UnresolvedNodeError:
        # which is what we expect
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
