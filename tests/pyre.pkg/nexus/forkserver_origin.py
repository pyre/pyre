#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a member recruited through the forkserver refuses to serve when its crew class
comes from a different file than it does in the team's process, says so on the journal it
ships to the team, and leaves
"""

# externals
import os

# support
import pyre
import journal

# the machinery under test
import pyre.nexus.Forkserver as forkserver


# the application
class Origin(pyre.application, family="tests.pyre.nexus.forkserver.origin"):
    """
    An application that claims its crew class comes from somewhere else
    """

    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # start the helper
        helper = forkserver.Forkserver.start()
        # the channels of a new member, over the socket transport
        transport = pyre.ipc.socket()()
        parent, child = transport.open()
        parentJournal, childJournal = transport.open()
        # claim that the crew class comes from a file it does not come from
        actual = forkserver.origin
        forkserver.origin = lambda cls: "/nowhere/Crew.py"
        # ask for the member
        pid = helper.recruit(
            crew=pyre.nexus.crew,
            transport="socket",
            channel=[child.fileno()],
            journal=[childJournal.fileno()],
        )
        # put things back
        forkserver.origin = actual
        # release the member's ends
        child.close()
        childJournal.close()

        # the member leaves on its own
        assert helper.exited(pid=pid, patience=30)
        # after saying why, on the journal it ships to the team
        data = b""
        # collect everything it said
        while True:
            # read what is there
            chunk = parentJournal.recv(64 * 1024)
            # until the member's end is closed
            if not chunk:
                # and there is nothing more
                break
            # add it to the pile
            data += chunk
        # decode the records
        records = [journal.record.decode(line) for line in data.split(b"\n") if line]
        # one of them is the complaint
        complaints = [
            record
            for record in records
            if record.severity == "firewall" and record.channel == "pyre.nexus.forkserver"
        ]
        assert len(complaints) == 1, records
        # which names both files
        text = "\n".join(complaints[0].page)
        assert "/nowhere/Crew.py" in text, text
        assert actual(pyre.nexus.crew) in text, text

        # clean up
        parent.close()
        parentJournal.close()
        forkserver.Forkserver.stop()

        # all done
        return 0


# main
if __name__ == "__main__":
    # instantiate
    app = Origin(name="forkserver_origin")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
