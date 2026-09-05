# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# my user configurable state
from .Recruiter import Recruiter


# declaration
class Team(pyre.protocol, family="pyre.nexus.teams"):
    """
    The specification for a process collective that coöperate to carry out a work plan
    """

    # user configurable state
    size = pyre.properties.int()
    size.doc = "the number of team members to recruit"

    recruiter = Recruiter()
    recruiter.doc = "the strategy for recruiting team members"

    # interface
    @pyre.provides
    def assemble(self, workplan, **kwds):
        """
        Recruit a team to execute the set of tasks in my {workplan}
        """

    @pyre.provides
    def vacancies(self):
        """
        Compute how may recruits are needed to take the team to full strength
        """

    @pyre.provides
    def overhear(self, crew, record):
        """
        Take delivery of a journal {record} produced by the {crew} member
        """

    @pyre.provides
    def instruct(self, control):
        """
        Apply the journal {control} instruction here and in every crew member
        """

    # my default
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default {Team} implementation
        """
        # use a distributed pool of processes
        from .Pool import Pool

        # so make its component factory available
        return Pool


# end of file
