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


# end of file
