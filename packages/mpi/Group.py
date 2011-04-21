# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# base classes
from .Object import Object


# declaration
class Group(Object):
    """
    Encapsulation of MPI communicator groups
    """


    # per-instance public data
    rank = 0 # my rank in this group
    size = 1 # the size of this group


    # class interface
    def include(self, included):
        """
        Build a group out of the processes in {included}
        """
        # build a new group handle
        handle = self.mpi.groupInclude(self._handle, included)
        # wrap it and return it
        return Group(handle=handle)


    def exclude(self, excluded):
        """
        Build a group out of all processes except those in {excluded}
        """
        # build a new group handle
        handle = self.mpi.groupExclude(self._handle, excluded)
        # wrap it and return it
        return Group(handle=handle)


    # meta methods
    def __init__(self, handle, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)

        # all done
        return


    # implementation details
    _handle = None


# end of file 
