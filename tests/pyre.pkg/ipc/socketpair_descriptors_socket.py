#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Delegate a client connection to a worker process

The parent holds a connection to a client and a channel to a worker; it ships the connection's
descriptor to the worker, which then responds to the client directly, without the parent ever
touching the payload. This is the pattern that lets a server offload response generation to
worker processes
"""

# the response the worker sends to the client
response = b"served directly by the worker"


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # the command channel between the server and the worker
    parent, child = pyre.ipc.socketpair()
    # and a second pair that stands in for a client connection to the server
    client, connection = pyre.ipc.socketpair()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the server behavior
        return onServer(worker_pid=pid, channel=parent, client=client, connection=connection)
    # in the child
    return onWorker(channel=child, client=client, connection=connection)


def onServer(worker_pid, channel, client, connection):
    """Hand the client connection to the worker and read the response as the client"""
    # externals
    import os

    # ship the connection's descriptor to the worker
    channel.sendDescriptors(descriptors=[connection.fileno()])
    # and retire my copy; the worker owns the conversation now
    connection.close()
    # play the client: read the response, which comes from the worker, not from me
    incoming = client.read(minlen=len(response))
    # check it
    assert incoming == response
    # harvest the worker and verify it exited cleanly
    _, status = os.waitpid(worker_pid, 0)
    assert status == 0
    # all done
    return


def onWorker(channel, client, connection):
    """Receive the client connection and respond to it directly"""
    # access the package
    import pyre.ipc

    # the fork duplicated the parent's endpoints in me; retire the copies so descriptor
    # ownership stays with the processes that speak through them
    client.close()
    connection.close()

    # receive the connection's descriptor
    _, descriptors = channel.recvDescriptors(limit=1)
    # exactly one made the trip
    assert len(descriptors) == 1
    # wrap it in a channel
    delegated = pyre.ipc.socketpair(descriptor=descriptors[0])
    # respond to the client directly
    delegated.write(bytes=response)
    # and close the conversation
    delegated.close()
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
