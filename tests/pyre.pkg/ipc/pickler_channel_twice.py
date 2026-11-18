#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a channel that appears more than once in a message travels once, and arrives as a
single channel wherever it appears
"""


def test():
    # access the package
    import pyre.ipc

    # the channel
    from pyre.ipc.File import File

    # the channel the message travels over
    parent, child = pyre.ipc.newSocket().open()
    # and the marshaler
    pickler = pyre.ipc.newPickler()

    # make a channel over a file with no name
    payload = File.temporary()
    # and put something in it
    payload.write(bytes=b"once")
    # send a message in which it appears three times
    manifest = pickler.send(item=[payload, payload, {"again": payload}], channel=parent)
    # the manifest names it once
    assert manifest.channels == [payload]
    # and its descriptor travels once
    assert manifest.descriptors == [payload.descriptor]

    # receive the message
    first, second, third = pickler.recv(channel=child)
    # every reference is to the same channel
    assert first is second
    # all three of them
    assert first is third["again"]
    # nothing is left over from the trip
    assert child.arrivals == []
    # and the channel reads the contents
    view = first.map()
    # all of them
    assert view[:] == b"once"

    # clean up
    view.close()
    # the channels
    for channel in (payload, first, parent, child):
        # one at a time
        channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
