# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# my superclass
from .Executive import Executive


# declaration
class Forkserver(Executive, family="pyre.shells.forkserver"):
    """
    A shell that never runs the application, and instead serves the recruiter that started it
    by forking crew members on request

    The recruiter spawns the application from its own command line, in this shell, so the
    helper loads the same code and the same configuration as the application; the helper then
    does nothing but wait for requests, so the members it forks are copies of a process that
    has touched nothing, however long the application has been running
    """

    # user configurable state
    control = pyre.properties.int(default=None)
    control.doc = "the descriptor of the channel the recruiter sends its requests down"

    journal = pyre.properties.int(default=None)
    journal.doc = "the descriptor of the channel that carries my journal entries back"

    model = pyre.properties.str(default="forkserver")
    model.doc = "the programming model"

    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Serve the recruiter that started me, instead of running {application}
        """
        # without a control channel
        if self.control is None:
            # make a channel
            channel = application.error
            # complain
            channel.line("the forkserver shell is started by a recruiter, not by hand")
            channel.line(f"'{self.pyre_name}.control' names no channel to serve")
            # flush
            channel.log()
            # and bail, in case errors are not fatal
            return 1
        # get the recruiter that knows how to serve
        from ..nexus.Forkserver import Forkserver as recruiter

        # make one, named after me
        server = recruiter(name=f"{self.pyre_name}.recruiter")
        # and serve
        return server.serve(control=self.control, journal=self.journal)


# end of file
