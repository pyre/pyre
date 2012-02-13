#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that syntax errors in interpolations are caught
"""


def test():
    import pyre.algebraic

    # build a model
    model = pyre.algebraic.model(name='interpolation_escaped')

    # escaped macro delimiters
    node = model.interpolation('{{production}}')
    assert node.value == '{production}'

    # and another
    node = model.interpolation('{{{{cost per unit}}}}')
    assert node.value == '{{cost per unit}}'

    # finally
    tricky = model.interpolation('{{{number of items}}}')
    # check that the escaped delimiters were processed correctly
    try:
        tricky.value
        assert False
    except tricky.UnresolvedNodeError:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
