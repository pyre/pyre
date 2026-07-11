#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the module level runtime: bring mpi up, ask it what it granted, and check the standard
communicators, the clock, and the host name
"""


def test():
    # access the package that hosts the bindings
    import mpi

    # and the bindings themselves
    libmpi = mpi.libmpi

    # importing the package does not bring mpi up, so nothing has been initialized yet
    assert libmpi.initialized() is False
    # and nothing has been taken down
    assert libmpi.finalized() is False

    # bring mpi up through the package, which also arranges for the shutdown at exit; asking for
    # the level of thread support reports what mpi settled on, as one of the levels it names
    granted = libmpi.initialize()
    # which is one of the {Thread} values
    assert isinstance(granted, libmpi.Thread)
    # and the package's own {init} agrees mpi is now up
    mpi.init()
    # so the runtime says so
    assert libmpi.initialized() is True

    # the communicator that holds every process in the job
    world = libmpi.world()
    # its size is at least one
    assert world.size >= 1
    # and my rank sits inside it
    assert world.rank in range(world.size)

    # the communicator that holds this process alone
    alone = libmpi.self()
    # has exactly one member
    assert alone.size == 1
    # in which i am the only rank
    assert alone.rank == 0

    # the communicator that holds nobody at all
    nothing = libmpi.null()
    # names no communicator
    assert nothing.isNull() is True
    # so it is false in a boolean test
    assert bool(nothing) is False

    # the clock hands back a real number of seconds
    assert isinstance(libmpi.wtime(), float)
    # and its resolution is a positive number of seconds
    assert libmpi.wtick() > 0.0

    # time only moves forward, so a later reading is no earlier than an earlier one
    first = libmpi.wtime()
    second = libmpi.wtime()
    assert second >= first

    # the host this process runs on has a name
    host = libmpi.processorName()
    # which is a non-empty string
    assert isinstance(host, str)
    assert len(host) > 0

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
