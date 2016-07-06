# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# support
import pyre
# my protocol
from .Asynchronous import Asynchronous


# declaration
class Peer(pyre.component, family='pyre.nexus.peers.peer', implements=Asynchronous):
    """
    A component base class that supplies the two ingredients necessary for building event
    driven applications
    """

    # user configurable state
    marshaler = pyre.ipc.marshaler()
    marshaler.doc = "the serializer that enables the transmission of objects among peers"

    dispatcher = pyre.ipc.dispatcher()
    dispatcher.doc = "the manager of the event loop"


    # meta-methods
    def __init__(self, timer=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # if i were handed a timer to use
        if timer is not None:
            # save it
            self.timer = timer
        # otherwise
        else:
            # make a new one and start it
            self.timer = self.pyre_executive.newTimer(name=self.pyre_family()).start()

        # journal channels
        import journal
        self.info = journal.info(self.pyre_family())
        self.debug = journal.debug(self.pyre_family())

        # all done
        return


    # implementation details
    def serve(self):
        """
        Start processing requests
        """
        # enter the event loop of my dispatcher
        status = self.dispatcher.watch()
        # shut everything down
        self.shutdown()
        # and report the status
        return status


    def shutdown(self):
        """
        Shut the peer down and exit gracefully
        """
        # no clean up, by default
        return


    # private data
    timer = None


# end of file
