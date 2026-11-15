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
    A shell that never runs the application, and instead turns it into the staffing agency of
    the process that started it, which forks crew members on request

    The liaison spawns the application from its own command line, in this shell, so the agency
    loads the same code and the same configuration as the application; the agency then does
    nothing but serve requests, so the members it forks are copies of a process that has
    touched nothing, however long the application has been running
    """

    # user configurable state
    control = pyre.properties.int(default=None)
    control.doc = "the descriptor of the channel the recruiter sends its requests down"

    # where my journal goes
    journal = pyre.properties.int(default=None)
    journal.doc = "the descriptor of the channel that carries my journal entries back"

    # my programming model
    model = pyre.properties.str(default="forkserver")
    model.doc = "the programming model"

    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Serve as the staffing agency of the process that started me, instead of running
        {application}
        """
        # without a control channel
        if self.control is None:
            # make a channel
            channel = application.error
            # complain
            channel.line("the forkserver shell is started by a staffing liaison, not by hand")
            # and what is missing
            channel.line(f"'{self.pyre_name}.control' names no channel to serve")
            # flush
            channel.log()
            # and bail, in case errors are not fatal
            return 1
        # get the agency
        from ..nexus.StaffingAgency import StaffingAgency

        # make one, named after me
        agency = StaffingAgency(name=f"{self.pyre_name}.agency")
        # and serve
        return agency.serve(control=self.control, journal=self.journal)


# end of file
