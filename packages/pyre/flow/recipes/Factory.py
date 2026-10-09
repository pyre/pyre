# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Node import Node

# the protocol of the products, which tells slots from settings
from ..Specification import Specification


# the factories of a recipe
class Factory(Node):
    """
    A factory of a recipe: its slots are the ones its protocol declares, or, once it is pinned,
    the ones its pin has, which include them and may add more
    """

    # public data
    @property
    def slots(self) -> dict:
        """
        My slots, by name, in the order they are declared
        """
        # the declarations come from my pin when i have one, since it may add slots of its own
        source = self.protocol if self.pin is None else self.pin
        # the slots are the facilities typed by a specification
        return {
            trait.name: trait
            for trait in source.pyre_facilities()
            if issubclass(trait.protocol, Specification)
        }

    @property
    def inputs(self) -> list:
        """
        My slots that read products, in the order they are declared
        """
        # filter my slots
        return [trait for trait in self.slots.values() if trait.input]

    @property
    def outputs(self) -> list:
        """
        My slots that write products, in the order they are declared
        """
        # filter my slots
        return [trait for trait in self.slots.values() if trait.output]

    # metamethods
    def __init__(self, protocol=None, pin=None, settings: dict | None = None, **kwds):
        # a factory with no protocol of its own takes the one its pin implements
        if protocol is None and pin is not None:
            # which every class and instance can name
            protocol = pin.pyre_implements
        # chain up
        super().__init__(protocol=protocol, pin=pin, **kwds)
        # the settings to apply once the factory is made; an instance carries its own
        self.settings = {} if settings is None else dict(settings)
        # all done
        return


# end of file
