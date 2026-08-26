#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a crew member that dies or misbehaves before checking in gets buried instead of
crashing the event loop or leaking in the registration roster
"""

# externals
import os

# support
import pyre


def stillborn(staff):
    """
    Build a team side proxy whose worker end closed without a word
    """
    # make a child that dies immediately, so there is a real corpse to reap
    pid = os.fork()
    # in the child
    if pid == 0:
        # die on the spot
        os._exit(1)
    # make the channel
    parent, child = pyre.ipc.newSocket().open()
    # the worker end closes without ever writing the registration
    child.close()
    # build the team side proxy
    crew = pyre.nexus.crew(pid=pid, channel=parent)
    # wire it the way the recruiter does
    crew.dispatcher = staff.dispatcher
    crew.marshaler = staff.marshaler
    # and hand it off
    return crew


def test():
    # build a staff of one
    staff = pyre.nexus.staff()(name="test.staff.stillborn")
    staff.size = 1

    # scenario 1: the registration never arrives
    crew = stillborn(staff=staff)
    # enroll the member the way {join} does
    staff.registered.add(crew)
    # fire the registration handler; it finds a closed channel
    keep = crew.activate(channel=crew.channel, team=staff)
    # the handler winds down quietly
    assert keep is False
    # the member was buried and a replacement recruited on the spot
    survivors = list(staff.crews())
    assert crew not in survivors
    assert len(survivors) == 1
    # and the corpse was reaped
    try:
        # so a second wait
        os.waitpid(crew.pid, 0)
        # must not find it
        assert False
    # because it was already collected
    except ChildProcessError:
        # as expected
        pass

    # scenario 2: the registration arrives but does not vouch for a healthy member
    pid = os.fork()
    # in the child
    if pid == 0:
        # die on the spot
        os._exit(1)
    # make the channel
    parent, child = pyre.ipc.newSocket().open()
    # the worker end sends garbage instead of a clean bill of health
    staff.marshaler.send(item="garbage", channel=child)
    # and closes
    child.close()
    # build the team side proxy
    crew = pyre.nexus.crew(pid=pid, channel=parent)
    # wire it
    crew.dispatcher = staff.dispatcher
    crew.marshaler = staff.marshaler
    # enroll it
    staff.registered.add(crew)
    # fire the registration handler; it finds a compromised member
    keep = crew.activate(channel=parent, team=staff)
    # the handler winds down quietly
    assert keep is False
    # and the member was buried, with the staff back at full strength
    survivors = list(staff.crews())
    assert crew not in survivors
    assert len(survivors) == 1

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
