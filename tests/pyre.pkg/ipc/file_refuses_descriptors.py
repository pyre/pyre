#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a file channel refuses to carry open descriptors, and writes nothing when it does
"""


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # the channel
    from pyre.ipc.File import File

    # make a channel over a file with no name
    channel = File.temporary()
    # carefully
    try:
        # ask it to carry its own descriptor
        channel.write(bytes=b"x", descriptors=[channel.descriptor])
    # it refuses
    except pyre.ipc.exceptions.CarriageError as error:
        # naming the channel
        assert error.channel is channel
    # anything else
    else:
        # is a failure
        assert False, "the file carried descriptors"
    # and the file is still empty
    assert os.fstat(channel.descriptor).st_size == 0

    # clean up
    channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
