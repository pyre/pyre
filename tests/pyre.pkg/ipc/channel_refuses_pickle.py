#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that channels refuse to be pickled or copied outside a marshaler, and that a file
channel still travels inside a marshaled message
"""


def test():
    # externals
    import copy
    import pickle

    # access the package
    import pyre.ipc

    # the channels with ends
    from pyre.ipc.Pipe import Pipe
    from pyre.ipc.SocketPair import SocketPair

    # a channel over a file with no name
    file = pyre.ipc.file.temporary()
    # the ends of a pipe
    pipe = Pipe.open()
    # and of a socket pair
    pair = SocketPair.open()

    # go through one channel of each kind
    for channel in (file, pipe.parent, pair.parent):
        # and the ways of duplicating it outside a marshaler
        for duplicate in (pickle.dumps, copy.copy, copy.deepcopy):
            # carefully
            try:
                # try to duplicate the channel
                duplicate(channel)
            # it refuses
            except pyre.ipc.exceptions.ChannelError as error:
                # naming the channel
                assert error.channel is channel
            # anything else
            else:
                # is a failure
                assert False, f"{duplicate.__name__} duplicated a {type(channel).__name__}"

    # the file still travels inside a marshaled message
    marshaler = pyre.ipc.newPickler()
    # the payload
    payload = b"a channel travels inside a message"
    # goes into the file
    file.write(bytes=payload)
    # which is sent along a socket pair
    marshaler.send(item=file, channel=pair.parent)
    # and arrives at the other end
    clone = marshaler.recv(channel=pair.child)
    # as a file channel of its own
    assert isinstance(clone, pyre.ipc.file) and clone is not file
    # over the same file
    mapped = clone.map(size=len(payload))
    # which holds the payload
    assert mapped[:] == payload

    # clean up
    mapped.close()
    # the clone
    clone.close()
    # all of it
    file.close()
    # both ends of the pipe
    pipe.parent.close()
    pipe.child.close()
    # and of the socket pair
    pair.parent.close()
    pair.child.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
