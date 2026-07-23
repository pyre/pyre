#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that users can declare installations the framework has never heard of

The configuration file {custom.yaml} binds the mpi facility to a fully user specified
installation of the fictional 'vampich' flavor, laid out in the fixture tree; no package
database is consulted
"""

# support
import pyre


# the application
class custom(pyre.application):
    """
    An application with an external package requirement
    """

    # the requirement
    mpi = pyre.externals.mpi()
    mpi.doc = "the MPI installation"


def test():
    """
    Resolve the mpi facility and verify the user specified configuration
    """
    # instantiate the application; this loads {custom.yaml}
    app = custom(name="custom")
    # get the selected installation
    mpi = app.mpi
    # the user's choice must have been honored
    assert mpi.pyre_name == "vampich"
    # with all traits exactly as configured
    assert mpi.version == "4.0.4"
    assert mpi.launcher == "mpirun.vampich"
    assert [str(folder) for folder in mpi.incdir] == ["prefix/include/vampich"]
    assert [str(folder) for folder in mpi.libdir] == ["prefix/lib/vampich"]
    assert list(mpi.libraries) == ["mpi"]
    # the configuration must be valid: the fixture folders exist
    assert not mpi.pyre_configurationErrors
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
