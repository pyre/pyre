#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the conduit bindings: build ports both ways the module offers, and move text, raw
octets, and arbitrary objects around a ring of processes
"""


def test():
    # access the package that hosts the bindings
    import mpi

    # bring mpi up, arranging for the shutdown
    mpi.init()
    # get the world communicator straight from the bindings
    libmpi = mpi.libmpi
    world = libmpi.world()
    # and its structure
    size = world.size
    rank = world.rank

    # a ring needs at least two processes; with one there is nobody to talk to
    if size < 2:
        return

    # the process i will hear from, and the one i will send to
    preceding = (rank - 1) % size
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

    # ship text to my successor, then take the text my predecessor shipped me
    destination.sendString(f"hello {following}")
    assert source.recvString() == f"hello {rank}"

    # the same, but flattening an arbitrary object on the way out and rebuilding it on the way in
    destination.send({"to": following, "ring": True})
    assert source.recv() == {"to": rank, "ring": True}

    # and once more with raw octets, which must come back byte for byte
    destination.sendBytes(bytes([rank, 0xEE]))
    assert source.recvBytes() == bytes([preceding, 0xEE])

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
