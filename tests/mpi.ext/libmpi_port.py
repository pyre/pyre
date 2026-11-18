#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the conduit bindings: build ports both ways the module offers, and move text, raw
    octets, and arbitrary objects around a ring of processes
    """
    # access the package that hosts the bindings
    import mpi

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the bindings
    libmpi = mpi.libmpi
    # and the world communicator straight from them
    world = libmpi.world()
    # and its structure: the number of processes
    size = world.size
    # and my place among them
    rank = world.rank

    # a ring needs at least two processes; with one there is nobody to talk to
    if size < 2:
        # so there is nothing to check
        return

    # the process i will hear from
    preceding = (rank - 1) % size
    # and the one i will send to
    following = (rank + 1) % size

    # build the conduit to my predecessor the way a communicator hands it over
    source = world.port(peer=preceding, tag=1)
    # and the one to my successor by asking the bound constructor directly
    destination = libmpi.Port(communicator=world, peer=following, tag=1)
    # both remember the communicator they belong to
    assert destination.communicator.size == size
    # the peer at the other end
    assert source.peer == preceding
    # and the label their messages carry
    assert source.tag == 1

    # ship text to my successor
    destination.sendString(f"hello {following}")
    # then take the text my predecessor shipped me
    assert source.recvString() == f"hello {rank}"

    # the same, but flattening an arbitrary object on the way out
    destination.send({"to": following, "ring": True})
    # and rebuilding it on the way in
    assert source.recv() == {"to": rank, "ring": True}

    # and once more with raw octets
    destination.sendBytes(bytes([rank, 0xEE]))
    # which must come back byte for byte
    assert source.recvBytes() == bytes([preceding, 0xEE])

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
