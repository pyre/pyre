# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# declaration
class Asynchronous(pyre.protocol, family="pyre.nexus.peers"):
    """
    A protocol that specifies the two ingredients necessary for building event driven
    applications
    """

    # user configurable state
    marshaler = pyre.ipc.marshaler()
    marshaler.doc = (
        "the serializer that enables the transmission of objects among peers"
    )

    dispatcher = pyre.ipc.dispatcher()
    dispatcher.doc = "the manager of the event loop"

    # required interface
    @pyre.provides
    def run(self):
        """
        Start processing requests
        """

    @pyre.provides
    def prepare(self):
        """
        Carry out any necessary start up steps
        """

    @pyre.provides
    def watch(self):
        """
        Activate my event loop
        """

    @pyre.provides
    def shutdown(self):
        """
        Shut down and exit gracefully
        """


# end of file
