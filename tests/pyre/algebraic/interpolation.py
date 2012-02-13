#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that expressions work
"""


def test():
    import os
    import pyre.algebraic

    # set up the model
    model = pyre.algebraic.model(name="interpolation")

    home = '/opt/local'
    model["tools"] = home
    model["bin"] = model.interpolation("{tools}/bin")
    model["lib"] = model.interpolation("{tools}/lib")
    model["include"] = model.interpolation("{tools}/include")

    # check the values
    # print("before:")
    # print("  tools:", model["tools"])
    # print("  bin:", model["bin"])
    # print("  lib:", model["lib"])
    # print("  include:", model["include"])
    assert model["tools"] == home
    assert model["bin"] == os.path.join(home, 'bin')
    assert model["lib"] == os.path.join(home, 'lib')
    assert model["include"] == os.path.join(home, 'include')

    # make a change
    home = '/Users/mga/tools'
    model["tools"] = home

    # check again
    # print("after:")
    # print("  tools:", model["tools"])
    # print("  bin:", model["bin"])
    # print("  lib:", model["lib"])
    # print("  include:", model["include"])
    assert model["tools"] == home
    assert model["bin"] == os.path.join(home, 'bin')
    assert model["lib"] == os.path.join(home, 'lib')
    assert model["include"] == os.path.join(home, 'include')

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
