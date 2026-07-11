#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the bindings module publishes every entity its clients are told to
expect, so that a missing or misnamed binding is caught here rather than deep inside a test that
happens to lean on it
"""


def test():
    # access the bindings directly, without bringing mpi up
    from mpi import libmpi

    # the structural classes the module hands back
    assert libmpi.Communicator is not None
    assert libmpi.Cartesian is not None
    assert libmpi.Group is not None
    assert libmpi.Port is not None
    assert libmpi.Request is not None
    assert libmpi.Status is not None

    # the cartesian communicator is a refinement of the plain one
    assert issubclass(libmpi.Cartesian, libmpi.Communicator)

    # the enumerations
    assert libmpi.Op is not None
    assert libmpi.Comparison is not None
    assert libmpi.Thread is not None

    # the exception hierarchy
    assert libmpi.Error is not None
    assert libmpi.MPIError is not None
    assert libmpi.ShapeError is not None

    # the runtime entry points
    assert callable(libmpi.initialize)
    assert callable(libmpi.finalize)
    assert callable(libmpi.initialized)
    assert callable(libmpi.finalized)

    # the standard communicators
    assert callable(libmpi.world)
    assert callable(libmpi.self)
    assert callable(libmpi.null)

    # the clock and the host
    assert callable(libmpi.wtime)
    assert callable(libmpi.wtick)
    assert callable(libmpi.processorName)

    # the collective waits that live on the module, since neither belongs to a single receipt
    assert callable(libmpi.waitAll)
    assert callable(libmpi.waitAny)

    # the constants, each of which is a whole number
    assert isinstance(libmpi.undefined, int)
    assert isinstance(libmpi.anySource, int)
    assert isinstance(libmpi.anyTag, int)
    assert isinstance(libmpi.procNull, int)

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
