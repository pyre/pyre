# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the exceptions i raise
from ..exceptions import IncompatiblePinError


# the base of the nodes of a recipe
class Node:
    """
    A node of a recipe: a name, the protocol whatever stands here must satisfy, and what it is
    pinned to, if anything: a class, or an instance
    """

    # public data
    @property
    def level(self) -> str:
        """
        How far down i am pinned: to my protocol only, to a class, or to an instance
        """
        # get my pin
        pin = self.pin
        # a node with no pin
        if pin is None:
            # stands for any implementation of its protocol
            return "protocol"
        # a node pinned to a class
        if isinstance(pin, type):
            # stands for any instance of it
            return "class"
        # otherwise, it is the instance itself
        return "instance"

    # metamethods
    def __init__(self, name: str, protocol=None, pin=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # a pin that does not satisfy my protocol
        if (
            pin is not None
            and protocol is not None
            and not pin.pyre_isCompatible(spec=protocol).isClean
        ):
            # cannot stand here
            raise IncompatiblePinError(node=name, pin=pin, protocol=protocol)
        # save my name
        self.name = name
        # my protocol
        self.protocol = protocol
        # and my pin
        self.pin = pin
        # all done
        return

    def __str__(self) -> str:
        # render my name and my level
        return f"{type(self).__name__.lower()} '{self.name}' ({self.level})"


# end of file
