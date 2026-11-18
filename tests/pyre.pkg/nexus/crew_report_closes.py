#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a crew member closes its copies of the channels its report carried, while the team
receives working copies of its own
"""

# externals
import os

# support
import pyre

# the file channel
from pyre.ipc.File import File


def test():
    # make a channel
    parent, child = pyre.ipc.newSocket().open()
    # build a worker side member; nothing gets reaped here, so my own pid will do
    worker = pyre.nexus.crew(pid=os.getpid(), channel=child)

    # the result of a task: a file with something in it
    payload = File.temporary()
    # put something in it
    payload.write(bytes=b"the result")
    # report it
    keep = worker.report(
        channel=child,
        crewstatus=worker.crewcodes.healthy,
        taskstatus=worker.taskcodes.completed,
        result=payload,
    )
    # the handler is done
    assert keep is False
    # and the member closed its copy of the file
    assert payload.descriptors() == []

    # the team side receives the report
    crewstatus, taskstatus, result = worker.marshaler.recv(channel=parent)
    # with the statuses intact
    assert crewstatus is worker.crewcodes.healthy
    # both of them
    assert taskstatus is worker.taskcodes.completed
    # and a copy of the file
    assert isinstance(result, File)
    # whose contents can still be mapped
    view = result.map()
    # all of them
    assert view[:] == b"the result"

    # clean up
    view.close()
    # the copy
    result.close()
    # and the channel
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
