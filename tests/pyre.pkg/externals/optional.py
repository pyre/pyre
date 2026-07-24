#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that facilities marked {optional} bind {None} when their package cannot be located

The configuration file {optional.yaml} restricts the host to the bare engine over the
fixture installation, which provides gsl but not petsc; the required facility must resolve,
and the optional one must quietly bind {None}
"""

# support
import pyre


# the application
class optional(pyre.application):
    """
    An application with one requirement it can satisfy and one it can live without
    """

    # a package the fixture provides
    gsl = pyre.externals.gsl()
    gsl.doc = "the GSL installation"

    # a package the fixture does not provide, marked as survivable
    petsc = pyre.externals.petsc(optional=True)
    petsc.doc = "the PETSc installation, if there is one"


def test():
    """
    Resolve both facilities and verify the optional one degrades to {None}
    """
    # instantiate the application; this loads {optional.yaml}
    app = optional(name="optional")
    # the required facility must have been satisfied by the fixture
    assert app.gsl is not None
    # with its traits populated by discovery
    assert list(app.gsl.libraries) == ["gsl", "gslcblas"]
    # the optional facility must have quietly degraded
    assert app.petsc is None
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
