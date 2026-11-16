# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import pickle
import sys

# my superclass
from .Message import Message


# declaration
class Recruit(Message):
    """
    A request for new crew members of one class: the class to build them from, and, for each of
    them, the member's ends of the channels it talks to its team over

    The class travels pickled, so the staffing agency passes it along without loading it: the
    members are the ones that import its module, after the fork, and the agency stays as clean as
    it started. It travels with the file its module was loaded from in the team's process, which
    is where the members must load it from too. The channels travel inside the request, and the
    agency receives copies of them
    """

    # interface
    def deliver(self, recipient):
        """
        Hand me to {recipient}
        """
        # it forks the members
        return recipient.recruit(request=self)

    def members(self):
        """
        Generate the ends of the channels of each member, in order: the channel it talks to its
        team over, and the one that carries its journal back, if there is one
        """
        # easy enough
        yield from zip(self.channels, self.journals)
        # all done
        return

    def load(self):
        """
        Load the class of the member, refusing one whose module did not come from where it came
        from in the team's process
        """
        # unpickle it, which imports its module
        crew = pickle.loads(self.crew)
        # if its module came from somewhere else
        if self.locate(crew=crew) != self.origin:
            # get the journal
            import journal

            # make a channel
            channel = journal.firewall("pyre.nexus.staffing")
            # complain
            channel.line(f"the crew class '{crew.__qualname__}' was loaded from")
            # set the two files apart
            channel.indent()
            # the one it came from here
            channel.line(f"{self.locate(crew=crew)} in the member, but from")
            # and the one it came from in the team's process
            channel.line(f"{self.origin} in the team's process")
            # done with the files
            channel.outdent()
            # flush
            channel.log()
        # hand it off
        return crew

    # implementation details
    @staticmethod
    def locate(crew):
        """
        Find the file the module that defines {crew} was loaded from
        """
        # get the module
        module = sys.modules[crew.__module__]
        # and resolve its file, so two spellings of the same file agree
        return os.path.realpath(module.__file__)

    # metamethods
    def __init__(self, crew, channels, journals=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the class of the members, pickled
        self.crew = pickle.dumps(crew)
        # the file its module was loaded from
        self.origin = self.locate(crew=crew)
        # the member's end of the channel each member talks to its team over
        self.channels = list(channels)
        # and of the channel that carries its journal back, where there is one
        self.journals = list(journals) if journals is not None else [None] * len(self.channels)
        # all done
        return


# end of file
