#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Sanity check: verify that the bindings module publishes every entity its clients are told to
    expect, so that a missing or misnamed binding is caught here rather than deep inside a test that
    happens to lean on it
    """
    # access the bindings directly, without bringing mpi up
    from mpi import libmpi

    # the structural classes the module hands back: communicators
    assert libmpi.Communicator is not None
    # cartesian ones
    assert libmpi.Cartesian is not None
    # groups
    assert libmpi.Group is not None
    # ports
    assert libmpi.Port is not None
    # the receipts of transfers in flight
    assert libmpi.Request is not None
    # and the reports on finished ones
    assert libmpi.Status is not None

    # the cartesian communicator is a refinement of the plain one
    assert issubclass(libmpi.Cartesian, libmpi.Communicator)

    # the enumerations: the reduction operators
    assert libmpi.Op is not None
    # the outcomes of comparisons
    assert libmpi.Comparison is not None
    # and the levels of thread support
    assert libmpi.Thread is not None

    # the exception hierarchy: its root
    assert libmpi.Error is not None
    # the complaints of the library
    assert libmpi.MPIError is not None
    # and the refusals of mismatched shapes
    assert libmpi.ShapeError is not None

    # the runtime entry points: bringing mpi up
    assert callable(libmpi.initialize)
    # bringing it down
    assert callable(libmpi.finalize)
    # and asking whether either has happened
    assert callable(libmpi.initialized)
    # in both directions
    assert callable(libmpi.finalized)

    # the standard communicators: everybody
    assert callable(libmpi.world)
    # this process alone
    assert callable(libmpi.self)
    # and nobody
    assert callable(libmpi.null)

    # the clock
    assert callable(libmpi.wtime)
    # its resolution
    assert callable(libmpi.wtick)
    # and the host
    assert callable(libmpi.processorName)

    # the collective waits that live on the module, since neither belongs to a single receipt:
    # for all of them
    assert callable(libmpi.waitAll)
    # and for any of them
    assert callable(libmpi.waitAny)

    # the constants, each of which is a whole number: the mark of an undefined rank
    assert isinstance(libmpi.undefined, int)
    # the wildcard source
    assert isinstance(libmpi.anySource, int)
    # the wildcard tag
    assert isinstance(libmpi.anyTag, int)
    # and the process that is nobody
    assert isinstance(libmpi.procNull, int)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
