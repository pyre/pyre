#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a file channel maps its file, whole or in part
"""


def test():
    # the channel
    from pyre.ipc.File import File

    # make a channel over a file with no name
    channel = File.temporary()
    # and put something in it
    channel.write(bytes=b"mapped contents")

    # map all of it
    whole = channel.map()
    # and check
    assert whole[:] == b"mapped contents"
    # map just the start of it
    start = channel.map(size=6)
    # and check
    assert start[:] == b"mapped"

    # clean up
    start.close()
    # both maps
    whole.close()
    # and the channel
    channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
