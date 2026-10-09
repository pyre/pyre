#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import os


def test() -> None:
    """
    Verify that the mirror of a courier can be replaced, and removed
    """
    # access
    from journal import libjournal

    # make a pipe
    reader, writer = os.pipe()
    # make two mirrors
    first = libjournal.Trash()
    second = libjournal.Trash()
    # make a courier that mirrors to the first one
    courier = libjournal.Courier(descriptor=writer, mirror=first)
    # verify it
    assert courier.mirror is first
    # switch to the second one
    courier.mirror = second
    # verify the switch
    assert courier.mirror is second
    # stop the mirroring
    courier.mirror = None
    # verify it
    assert courier.mirror is None
    # release the descriptor
    courier.close()
    # and the far end
    os.close(reader)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
