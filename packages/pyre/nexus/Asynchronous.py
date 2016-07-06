# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# support
import pyre


# declaration
class Asynchronous(pyre.protocol, family='pyre.nexus.peers'):
    """
    A protocol that specifies the two ingredients necessary for building event driven
    applications
    """

    # user configurable state
    marshaler = pyre.ipc.marshaler()
    marshaler.doc = "the serializer that enables the transmission of objects among peers"

    dispatcher = pyre.ipc.dispatcher()
    dispatcher.doc = "the manager of the event loop"


# end of file
