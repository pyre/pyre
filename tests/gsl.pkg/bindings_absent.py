#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the package imports without its bindings, as it must in installations that cannot
build them, e.g. the pip wheels, and reports their absence
"""


def test():
    # support
    import sys

    # make the bindings unimportable, as they are when they were never built
    sys.modules["gsl.libgsl"] = None
    # import the package, which must succeed regardless
    import gsl

    # the bindings are reported as absent
    assert gsl.gsl is None
    # and so is everything they publish
    assert gsl.version is None
    assert gsl.vector is None
    assert gsl.matrix is None
    assert gsl.Transpose is None
    assert gsl.linalg is None
    # while the generic helpers that need no bindings are still there
    assert callable(gsl.zero)
    assert callable(gsl.fill)
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
