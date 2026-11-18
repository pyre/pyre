#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a file channel opens an existing file for reading
"""


def test():
    # the channel
    from pyre.ipc.File import File

    # open this very file
    channel = File.open(path=__file__)
    # and read its first line
    assert channel.read(minlen=22, maxlen=22) == b"#!/usr/bin/env python3"

    # clean up
    channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
