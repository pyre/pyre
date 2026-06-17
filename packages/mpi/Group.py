# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2026 all rights reserved
#


# base class
from .Object import Object
# meta-class
from pyre.patterns.Extent import Extent


# declaration
class Group(Object, metaclass=Extent):
    """
    Encapsulation of MPI communicator groups
    """

    # class level public data
    undefined = Object.mpi.undefined


    # per-instance public data
    rank = 0 # my rank in this group
    size = 0 # the size of this group


    # check whether a group is empty
    def isEmpty(self):
        """
        Check whether i am an empty group
        """
        return self.capsule.isEmpty


    # building groups using explicit ranklists
    def include(self, included):
        """
        Build a group out of the processes in {included}
        """
        # build a new group capsule
        capsule = self.capsule.include(list(included))
        # wrap it and return it
        return Group(capsule=capsule)


    def exclude(self, excluded):
        """
        Build a group out of all processes except those in {excluded}
        """
        # build a new group capsule
        capsule = self.capsule.exclude(list(excluded))
        # wrap it and return it
        return Group(capsule=capsule)


    # the set-like operations
    def union(self, g):
        """
        Build a new group whose processes are the union of mine and {g}'s
        """
        return Group(capsule=self.capsule + g.capsule)


    def intersection(self, g):
        """
        Build a new group whose processes are the intersection of mine and {g}'s
        """
        return Group(capsule=self.capsule & g.capsule)


    def difference(self, g):
        """
        Build a new group whose processes are the difference of mine and {g}'s
        """
        return Group(capsule=self.capsule - g.capsule)


    # meta methods
    def __init__(self, capsule, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)

        # store my attributes
        self.capsule = capsule
        # and precompute my rank and size
        self.rank = capsule.rank
        self.size = capsule.size

        # all done
        return


    # implementation details
    capsule = None


# end of file
