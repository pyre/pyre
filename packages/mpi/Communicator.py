# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# base classes
from .Object import Object


# declaration
class Communicator(Object):
    """
    An encapsulation of MPI communicators
    """


    # per-instance public data
    rank = 0
    size = 1


    # communicator factories
    def include(self, processes):
        """
        Build a new communicator with the processes in the iterable {processes} as its members
        """
        # get my group
        mine = self.group()
        # create a new group out of {processes}
        group = mine.include(tuple(processes))
        # use it to build a new communicator handle
        handle = self.mpi.communicatorCreate(self._handle, group._handle)
        # if successful
        if handle is not None:
            # wrap it and return it
            return Communicator(handle=handle)
        # otherwise
        return None
        

    def exclude(self, processes):
        """
        Build a new communicator with all my processes except those in {processes}
        """
        # create a new group out of the processes not in {processes}
        group = self.group().exclude(tuple(processes))
        # use it to build a new communicator handle
        handle = self.mpi.communicatorCreate(self._handle, group._handle)
        # if successful
        if handle is not None:
            # wrap it and return it
            return Communicator(handle=handle)
        # otherwise
        return None


    def cartesian(self, axes, periods, reorder=1):
        """
        Build a cartesian communicator; see the MPI documentation for details
        """
        # access the factory
        from .Cartesian import Cartesian
        # build one and return it
        return Cartesian(handle=self._handle, axes=axes, periods=periods, reorder=reorder)
        

    # interface
    def barrier(self):
        """
        Establish a synchronization point: all processes in this communicator must call this
        method, and they all block until the last one makes the call
        """
        # invoke the low level routine
        return self.mpi.communicatorBarrier(self._handle)


    def group(self):
        """
        Build a group that contains all my processes
        """
        # create a new group handle out of my processes
        handle = self.mpi.groupCreate(self._handle)
        # wrap it up and return it
        from .Group import Group
        return Group(handle)


    def port(self, peer, tag):
        """
        Establish a point-to-point communication conduit with {peer}; all messages sent through
        this port will be tagged with {tag}
        """
        # access the factory
        from .Port import Port
        # make a port and return it
        return Port(communicator=self, peer=peer, tag=tag)


    # meta methods
    def __init__(self, handle, **kwds):
        """
        This constructor is not public, and it is unlikely to be useful to you. To make
        communicators, access the predefined {world} communicator in the {mpi} package and use
        its interface to build new communicators
        """
        # chain to my ancestors
        super().__init__(**kwds)

        # set the per-instance variables
        self._handle = handle
        self.rank = self.mpi.communicatorRank(handle)
        self.size = self.mpi.communicatorSize(handle)

        # all done
        return


    # implementation details
    _handle = None


# end of file 
