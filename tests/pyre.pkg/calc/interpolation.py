#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that interpolations work
"""


def test():
    # support for building the expected paths
    import os

    # access the package
    import pyre.calc

    # set up the model
    model = pyre.calc.model()

    # pick a location for the tools
    home = "/opt/local"
    # register it
    model["tools"] = home
    # derive the location of the executables from it
    model["bin"] = model.interpolation("{tools}/bin")
    # the libraries
    model["lib"] = model.interpolation("{tools}/lib")
    # and the headers
    model["include"] = model.interpolation("{tools}/include")

    # check the values
    # check the location of the tools
    assert model["tools"] == home
    # the location of the executables
    assert model["bin"] == os.path.join(home, "bin")
    # the libraries
    assert model["lib"] == os.path.join(home, "lib")
    # and the headers
    assert model["include"] == os.path.join(home, "include")

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
