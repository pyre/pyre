#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a file channel over a temporary file reads back what was written to it, through the
one descriptor that is both of its ends
"""


def test():
    # externals
    import os

    # the channel
    from pyre.ipc.File import File

    # make a channel over a file with no name
    channel = File.temporary()
    # it is made of a single descriptor
    assert channel.descriptors() == [channel.descriptor]
    # which it both reads from
    assert channel.inbound == channel.descriptor
    # and writes to
    assert channel.outbound == channel.descriptor

    # write something
    assert channel.write(bytes=b"hello, file") == 11
    # go back to the start of the file
    os.lseek(channel.descriptor, 0, os.SEEK_SET)
    # and read it back
    assert channel.read(minlen=11, maxlen=11) == b"hello, file"
    # at the end of the file, there is nothing more to read
    assert channel.read(minlen=1, maxlen=1) == b""

    # close it
    channel.close()
    # after which it is made of nothing
    assert channel.descriptors() == []
    # and closing it again does no harm
    channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
