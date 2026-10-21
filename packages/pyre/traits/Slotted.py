# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Trait import Trait


# declaration
class Slotted(Trait):
    """
    Intermediate class that knows that trait values are held by framework slots
    """

    # types
    from .SlotFactory import SlotFactory as factory
    from ..components.exceptions import TraitValueError
    from ..framework.exceptions import PyreError

    # framework data
    isConfigurable = True  # slotted traits have configurable values
    classSlot = None  # the factory for class slots
    instanceSlot = None  # the factory of instance slots

    # meta-methods
    def __get__(self, instance, cls):
        """
        Retrieve the value of this trait
        """
        # find out whose inventory we are supposed to access
        configurable = instance or cls
        # get the slot from the client's inventory
        slot = configurable.pyre_inventory[self]
        # attempt to
        try:
            # compute its value
            value = slot.value
        # if the value is refused
        except self.TraitValueError as error:
            # and the refusal is not about my {value} but about where it is stored
            if error.slot is slot:
                # associate it with my client
                error.configurable = configurable
            # either way, let it through
            raise
        # if computing it fails in any other way of the framework's, e.g. an expression that
        # refers to a name that does not exist, or that can't be evaluated
        except self.PyreError as error:
            # the value is refused because of it
            refusal = self.TraitValueError(error=error)
            # by the slot that holds it
            refusal.slot = slot
            # whose factory, the one for my client's kind of slots
            slots = self.classSlot if instance is None else self.instanceSlot
            # knows how to attribute the refusal to my trait
            slots.attribute(error=refusal, node=slot)
            # associate the refusal with my client
            refusal.configurable = configurable
            # and raise it in place of the error
            raise refusal from error
        # if all goes well, return the {value}
        return value


# end of file
