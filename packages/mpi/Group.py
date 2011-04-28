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

    # class level public data
    undefined = None # patched by the bootstrapping code with the value from the extension module


    # per-instance public data
    rank = 0 # my rank in this group
    size = 0 # the size of this group

    
    # check whether a group is empty
    def isEmpty(self):
        """
        Check whether i am an empty group
        """
        return self.mpi.groupIsEmpty(self._handle)


    # building groups using explicit ranklists
    def include(self, included):
        """
        Build a group out of the processes in {included}
        """
        # build a new group handle
        handle = self.mpi.groupInclude(self._handle, tuple(included))
        # check whether it is a valid group
        if handle:
            # wrap it and return it
            return Group(handle=handle)
        # otherwise return an invalid group
        return None


    def exclude(self, excluded):
        """
        Build a group out of all processes except those in {excluded}
        """
        # build a new group handle
        handle = self.mpi.groupExclude(self._handle, tuple(excluded))
        # check whether it is a valid group
        if handle:
            # wrap it and return it
            return Group(handle=handle)
        # otherwise return an invalid group
        return None


    # the set-like operations
    def union(self, g):
        """
        Build a new group whose processes are the union of mine and {g}'s
        """
        # build the new group handle
        handle = self.mpi.groupUnion(self._handle, g._handle)
        # check whether it is a valid group
        if handle:
            # wrap it and return it
            return Group(handle=handle)
        # otherwise
        return None


    def intersection(self, g):
        """
        Build a new group whose processes are the intersection of mine and {g}'s
        """
        # build the new group handle
        handle = self.mpi.groupIntersection(self._handle, g._handle)
        # check whether it is a valid group
        if handle:
            # wrap it and return it
            return Group(handle=handle)
        # otherwise
        return None


    def difference(self, g):
        """
        Build a new group whose processes are the difference of mine and {g}'s
        """
        # build the new group handle
        handle = self.mpi.groupDifference(self._handle, g._handle)
        # check whether it is a valid group
        if handle:
            # wrap it and return it
            return Group(handle=handle)
        # otherwise
        return None


    # meta methods
    def __init__(self, handle, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)

        # store my attributes
        self._handle = handle
        # and precompute my rank and size
        self.rank = self.mpi.groupRank(handle)
        self.size = self.mpi.groupSize(handle)

        # all done
        return


    # implementation details
    _handle = None


# end of file 
