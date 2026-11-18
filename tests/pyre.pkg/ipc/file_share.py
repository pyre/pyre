#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a file channel shares its file as a python file object of its own, which stays open
after the channel is closed
"""


def test():
    # externals
    import os

    # the channel
    from pyre.ipc.File import File

    # make a channel over a file with no name
    channel = File.temporary()
    # and put something in it
    channel.write(bytes=b"shared")

    # share the file
    shared = channel.share()
    # what comes back is a file object over a descriptor of its own
    assert shared.fileno() != channel.descriptor

    # close the channel
    channel.close()
    # the shared file still reaches the contents
    assert os.pread(shared.fileno(), 6, 0) == b"shared"

    # clean up
    shared.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
