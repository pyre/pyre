# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import typing


# declaration
class TrivialCommunicator:
    """
    A single process stand-in for an mpi communicator

    This is what {mpi.world} names on a machine with no mpi at all, and before anybody calls
    {mpi.init}. It answers the same questions a real communicator of size one would, so that
    code written against the parallel interface runs unchanged in serial.

    Every collective here is an identity: with a single process there is nobody to exchange
    anything with, and the answer each of them computes is already in hand. What is missing is
    the point to point interface, which a lone process cannot exercise without deadlocking, and
    the structural factories, which have no serial meaning.
    """

    # public data
    @property
    def rank(self) -> int:
        """
        My place among the processes i hold
        """
        # there is only one process, so it is the first
        return 0

    @property
    def size(self) -> int:
        """
        How many processes i hold
        """
        # just the one
        return 1

    @property
    def isNull(self) -> bool:
        """
        Whether i name no communicator at all
        """
        # i always name the lone process, so never
        return False

    # collective operations
    def barrier(self) -> None:
        """
        Block until every one of my processes arrives here
        """
        # the only process is the one asking, and it is already here
        return

    def bcast(self, item: typing.Any = None, source: int = 0) -> typing.Any:
        """
        Broadcast {item} from {source} to every one of my processes
        """
        # the source is the only process there is
        self._only(source)
        # so it already holds what it would have been sent
        return item

    def reduce(self, item: typing.Any, op: typing.Any, root: int = 0) -> typing.Any:
        """
        Combine the {item} of every process with {op}, delivering the answer to {root}
        """
        # the root is the only process there is
        self._only(root)
        # with a single contribution there is nothing for {op} to fold, so it goes unused
        return item

    def allreduce(self, item: typing.Any, op: typing.Any) -> typing.Any:
        """
        Combine the {item} of every process with {op}, delivering the answer to all
        """
        # as above, the lone contribution is already the answer
        return item

    def scan(self, item: typing.Any, op: typing.Any) -> typing.Any:
        """
        Combine the {item} of every process that precedes me, myself included
        """
        # i precede myself, and nobody else does
        return item

    def exscan(self, item: typing.Any, op: typing.Any) -> None:
        """
        Combine the {item} of every process that strictly precedes me
        """
        # nobody strictly precedes rank zero; mpi leaves the answer undefined there, and the
        # bindings report it as {None}
        return None

    def gather(self, item: typing.Any, root: int = 0) -> list:
        """
        Collect the {item} of every process at {root}, in rank order
        """
        # the root is the only process there is
        self._only(root)
        # and its contribution is the whole collection
        return [item]

    def allgather(self, item: typing.Any) -> list:
        """
        Collect the {item} of every process, in rank order, and deliver it to all
        """
        # as above
        return [item]

    def scatter(self, items: typing.Sequence, root: int = 0) -> typing.Any:
        """
        Hand the nth cell of {items} to the nth process; only {root}'s {items} matters
        """
        # the root is the only process there is
        self._only(root)
        # so it brought exactly one cell, and that cell is addressed to it
        return self._one(items)

    def alltoall(self, items: typing.Sequence) -> list:
        """
        Hand the nth cell of every process's {items} to the nth process
        """
        # the lone process hands its only cell to itself
        return [self._one(items)]

    # the collectives that move arbitrary objects rather than numbers; with a single process
    # nothing ever gets flattened, so each is exactly its numeric counterpart
    def gatherObject(self, item: typing.Any, root: int = 0) -> list:
        """
        Collect the {item} of every process at {root}, in rank order
        """
        # delegate
        return self.gather(item=item, root=root)

    def allgatherObject(self, item: typing.Any) -> list:
        """
        Collect the {item} of every process, in rank order, and deliver it to all
        """
        # delegate
        return self.allgather(item=item)

    def scatterObject(self, items: typing.Sequence = None, root: int = 0) -> typing.Any:
        """
        Hand the nth object of {items} to the nth process; only {root}'s {items} matters
        """
        # delegate
        return self.scatter(items=items, root=root)

    def alltoallObject(self, items: typing.Sequence) -> list:
        """
        Hand the nth object of every process's {items} to the nth process
        """
        # delegate
        return self.alltoall(items=items)

    # communicator factories
    def duplicate(self) -> "TrivialCommunicator":
        """
        Build a communicator with my membership but a fresh context
        """
        # my membership is the lone process, and there are no messages for a context to isolate
        return type(self)()

    # process control
    def abort(self, code: int = 1) -> typing.NoReturn:
        """
        Bring down every process i hold, handing {code} to the environment
        """
        # the only process i hold is the one asking
        raise SystemExit(code)

    # implementation details
    def _only(self, rank: int) -> None:
        """
        Assert that {rank} names the lone process i hold
        """
        # anything but the first rank names a process that does not exist
        if rank != 0:
            # so say so, rather than quietly compute the wrong answer
            raise ValueError(
                f"rank {rank} is out of range: a trivial communicator holds one process"
            )
        # all done
        return

    def _one(self, items: typing.Sequence) -> typing.Any:
        """
        Extract the single cell that {items} must hold, one per process
        """
        # a collective that hands a cell to each process needs as many cells as i hold processes
        if items is None or len(items) != 1:
            # so anything else is a shape error, and mpi would have said as much
            raise ValueError(
                "a trivial communicator holds one process, so it expects exactly one cell"
            )
        # hand back the only cell there is
        return items[0]

    # meta-methods
    def __bool__(self) -> bool:
        """
        I always name a communicator
        """
        # namely the one that holds this process alone
        return True

    def __repr__(self) -> str:
        """
        A human readable summary of this communicator
        """
        # say what i am
        return "<mpi.TrivialCommunicator: rank 0 of 1>"


# end of file
