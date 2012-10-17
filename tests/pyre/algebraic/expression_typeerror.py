#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that model initialization fails correctly in the presence of expressions that cannot be
evaluated even though they have no syntax errors
"""


def test():
    import pyre.algebraic

    # a model
    model = pyre.algebraic.model()
    # the nodes
    model["production"] = 80.
    model["shipping"] = 20.
    model["cost"] = model.expression("{production}&{shipping}")

    try:
        model["cost"]
        assert False
    except model.EvaluationError as error:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
