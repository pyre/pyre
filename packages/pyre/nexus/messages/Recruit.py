# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import pickle
import socket
import sys

# support
import pyre

# my superclass
from .Message import Message


# declaration
class Recruit(Message):
    """
    A request for a new crew member: the class to build it from, and the member's ends of the
    channels it talks to its team over

    The class travels pickled, so the staffing agency passes it along without loading it: the
    member is the one that imports its module, after the fork, and the agency stays as clean as
    it started. It travels with the file its module was loaded from in the team's process, which
    is where the member must load it from too
    """

    # interface
    def deliver(self, recipient):
        """
        Hand me to {recipient}
        """
        # it forks the member
        return recipient.recruit(request=self)

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
            channel.indent()
            channel.line(f"{self.locate(crew=crew)} in the member, but from")
            channel.line(f"{self.origin} in the team's process")
            channel.outdent()
            # flush; firewalls are fatal
            channel.log()
        # hand it off
        return crew

    def dress(self):
        """
        Dress the descriptors i carried as the member's ends of its crew channel and, when there
        is one, its journal channel
        """
        # get the transport the channels were made with
        transport = self.transports[self.transport]()
        # split the descriptors
        crew, journal = self.descriptors[: self.split], self.descriptors[self.split :]
        # dress the crew channel
        channel = self.wrap(transport=transport, descriptors=crew)
        # and the journal channel, if there is one
        journal = self.wrap(transport=transport, descriptors=journal) if journal else None
        # hand them off
        return channel, journal

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

    @staticmethod
    def kind(channel):
        """
        Name the kind of {channel}, so the agency can dress its descriptors the same way
        """
        # a socket is one descriptor, and anything else a pair of pipes
        return "socket" if isinstance(channel, socket.socket) else "pipe"

    @staticmethod
    def unpack(channel):
        """
        Collect the descriptors of {channel}
        """
        # a socket is one descriptor
        if isinstance(channel, socket.socket):
            # its own
            return [channel.fileno()]
        # a pair of pipes is two
        return [channel.inbound, channel.outbound]

    @staticmethod
    def wrap(transport, descriptors):
        """
        Dress {descriptors} as a channel of {transport}
        """
        # a socket is one descriptor
        if len(descriptors) == 1:
            # dress it
            return transport.wrap(descriptor=descriptors[0])
        # a pair of pipes is two
        return transport.wrap(infd=descriptors[0], outfd=descriptors[1])

    # metamethods
    def __init__(self, crew, channel, journal=None, **kwds):
        # collect the descriptors of the member's ends
        crewDescriptors = self.unpack(channel=channel)
        journalDescriptors = self.unpack(channel=journal) if journal is not None else []
        # chain up, with the descriptors that travel with me
        super().__init__(descriptors=crewDescriptors + journalDescriptors, **kwds)
        # the class of the member, pickled
        self.crew = pickle.dumps(crew)
        # the file its module was loaded from
        self.origin = self.locate(crew=crew)
        # the kind of channel it talks over
        self.transport = self.kind(channel=channel)
        # and how many of the descriptors belong to the crew channel
        self.split = len(crewDescriptors)
        # all done
        return

    # the transports, by the name they travel under
    transports = {
        "pipe": pyre.ipc.pipe(),
        "socket": pyre.ipc.socket(),
    }


# end of file
