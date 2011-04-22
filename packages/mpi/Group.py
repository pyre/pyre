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


    # class public data
    null = None # the null group singleton; patched by the module initialization code
    empty = None # the empty group singleton; patched by the module initialization code


    # per-instance public data
    rank = 0 # my rank in this group
    size = 0 # the size of this group


    # class interface
    def include(self, included):
        """
        Build a group out of the processes in {included}
        """
        # build a new group handle
        handle = self.mpi.groupInclude(self._handle, included)
        # check whether it is the empty group
        if handle == self.mpi.emptyGroup:
            return self.empty
        # otherwise, wrap it and return it
        return Group(handle=handle)


    def exclude(self, excluded):
        """
        Build a group out of all processes except those in {excluded}
        """
        # build a new group handle
        handle = self.mpi.groupExclude(self._handle, excluded)
        # check whether it is the empty group
        if handle == self.mpi.emptyGroup:
            return self.empty
        # wrap it and return it
        return Group(handle=handle)


    # meta methods
    def __init__(self, handle, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)

        # store my attributes
        self._handle = handle

        # am i wrapped around the null group?
        if handle is self.mpi.nullGroup:
            self.rank = self.mpi.undefined
            self.size = self.mpi.undefined
        # or the empty group?
        elif handle is self.mpi.emptyGroup:
            self.rank = self.mpi.undefined
            self.size = 0
        # otherwise, precompute my size and the process rank
        else:
            self.rank = self.mpi.groupRank(handle)
            self.size = self.mpi.groupSize(handle)

        # all done
        return


    # implementation details
    _handle = None


# end of file 
