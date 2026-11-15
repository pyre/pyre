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
from pyre.nexus.Forkserver import Forkserver
from pyre.nexus.messages.Recruit import Recruit


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
        # start the staffing agency
        liaison = Forkserver.start()
        # the channels of a new member, over the socket transport
        transport = pyre.ipc.socket()()
        # the ends of its control channel
        parent, child = transport.open()
        # and of its journal
        parentJournal, childJournal = transport.open()
        # the request for the member
        request = Recruit(crew=pyre.nexus.crew, channel=child, journal=childJournal)
        # claiming that the crew class comes from a file it does not come from
        request.origin = "/nowhere/Crew.py"
        # ask for the member
        pid = liaison.recruit(request=request)
        # release the member's ends
        child.close()
        # and the ends of its journal channel
        childJournal.close()

        # the member leaves on its own, and the agency reports it
        while not liaison.collect(pid=pid)[0]:
            # so listen to the agency until it does
            liaison.hear()
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
            if record.severity == "firewall" and record.channel == "pyre.nexus.staffing"
        ]
        # there is exactly one
        assert len(complaints) == 1, records
        # read it
        text = "\n".join(complaints[0].page)
        # it names the file the class was claimed to come from
        assert "/nowhere/Crew.py" in text, text
        # and the one it came from
        assert Recruit.locate(crew=pyre.nexus.crew) in text, text

        # clean up
        parent.close()
        # release my end of its journal channel
        parentJournal.close()
        # and send the staffing agency home
        Forkserver.stop()

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
