#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a pipe channel with only one end reads or writes through it, is made of that one
descriptor, and says which end it has, so it can be rebuilt on arrival
"""


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # get the pipe transport
    transport = pyre.ipc.newPipe()
    # make a pipe
    reader, writer = os.pipe()
    # a channel that only reads
    inbound = transport.wrap(infd=reader)
    # and one that only writes
    outbound = transport.wrap(outfd=writer)

    # each is made of its one descriptor
    assert inbound.descriptors() == [reader]
    # on both sides
    assert outbound.descriptors() == [writer]
    # and says which end it has
    assert inbound.hints() == {"ends": "in"}
    # on both sides
    assert outbound.hints() == {"ends": "out"}

    # the writer writes
    outbound.write(bytes=b"one way")
    # and the reader reads
    assert inbound.read(minlen=7, maxlen=7) == b"one way"

    # a channel rebuilt from how the reader leaves
    hints, descriptors = inbound.depart()
    # reads through the same descriptor
    assert pyre.ipc.channel.arrive(hints=hints, descriptors=descriptors).inbound == reader

    # closing the channels closes their descriptors
    inbound.close()
    # both of them
    outbound.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
