# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre
# my meta-class
from .FlowMaster import FlowMaster


# declaration
class Node(pyre.component, metaclass=FlowMaster, internal=True):
    """
    Base class for entities that participate in workflows
    """


    # public data
    # the object that watches over my traits
    pyre_status = None


    # public data
    @property
    def pyre_stale(self):
        """
        Retrieve my status
        """
        # delegate to my status manager
        return self.pyre_status.stale

    @pyre_stale.setter
    def pyre_stale(self, value):
        """
        Set my status
        """
        # delegate to my status manager
        self.pyre_status.stale = value
        # all done
        return


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build my status tracker
        self.pyre_status = self.pyre_newStatus(node=self)
        # all done
        return


    # debugging support
    def pyre_dump(self, channel, indent, level):
        """
        Display information about me
        """
        # compute the margin
        margin = indent * level
        # sign on
        channel.line(f"{margin}{self}")

        # my status monitor
        channel.line(f"{margin}{indent}status: {self.pyre_status}")
        # my observers
        observers = tuple(self.pyre_status.observers)
        if observers:
            channel.line(f"{margin}{indent}observers:")
            for observer in observers:
                channel.line(f"{margin}{indent*2}{observer}")

        # all done
        return self


# end of file
