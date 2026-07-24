#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the failure mode when a required package cannot be located

The configuration file {unavailable.yaml} restricts the host to the bare engine over the
fixture installation, which does not provide petsc; the application must construct anyway,
and the first access of the facility must fail loudly with a {DefaultError} that names the
protocol
"""

# support
import pyre

# the exception the facility binding is expected to raise
from pyre.components.exceptions import DefaultError


# the application
class unavailable(pyre.application):
    """
    An application that requires a package the host cannot provide
    """

    # the requirement
    petsc = pyre.externals.petsc()
    petsc.doc = "the PETSc installation"


def test():
    """
    Verify that an unsatisfiable facility complains on first access, not at construction
    """
    # instantiating the application must succeed: the missing package must not prevent the
    # application from coming to life
    app = unavailable(name="unavailable")
    # attempt to
    try:
        # touch the facility
        app.petsc
    # the access must fail with the protocol in the complaint
    except DefaultError as error:
        # check that the complaint names the category
        assert "petsc" in str(error)
    # anything else is a bug
    else:
        # the access must not succeed
        assert False, "unresolvable facility bound silently"
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
