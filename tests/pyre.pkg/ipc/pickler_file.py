#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a file channel travels inside a pickled message over a socket pair and arrives as a
working copy, which outlives the copy of the sender
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
    original = File.temporary()
    # and put something in it
    original.write(bytes=b"travelling")
    # send it, inside a message
    pickler.send(item={"payload": original, "note": "a file"}, channel=parent)
    # and receive the message on the other end
    message = pickler.recv(channel=child)

    # the plain part made it
    assert message["note"] == "a file"
    # the file arrived as a file channel
    arrival = message["payload"]
    # of the right kind
    assert isinstance(arrival, File)
    # over a descriptor of its own
    assert arrival.descriptor != original.descriptor
    # nothing is left over from the trip
    assert child.arrivals == []

    # the sender's copy is no longer needed
    original.close()
    # but the arrival still reaches the contents
    view = arrival.map()
    # all of them
    assert view[:] == b"travelling"

    # clean up
    view.close()
    # the arrival
    arrival.close()
    # and the socket pair
    parent.close()
    # both ends
    child.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
