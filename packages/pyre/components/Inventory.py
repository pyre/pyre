# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ..framework.Dashboard import Dashboard


# declaration
class Inventory(Dashboard):
    """
    Base class for the state storage strategies for component classes and instances
    """

    # public data
    name = None  # by default, components have no name
    fragments = ()  # by default, components have no family name
    package = None  # by default, components don't belong to a package

    # factories
    @classmethod
    def initializeClass(cls):
        """
        Build inventory for a component class
        """
        # implementation dependent -- override in subclasses
        raise NotImplementedError(
            "class {.__name__!r} must implement 'initializeClass'".format(cls)
        )

    @classmethod
    def configureClass(cls):
        """
        Configure a newly minted class record
        """
        # implementation dependent -- override in subclasses
        raise NotImplementedError("class {.__name__!r} must implement 'configureClass'".format(cls))

    @classmethod
    def initializeInstance(cls):
        """
        Build inventory for a component instance
        """
        # implementation dependent -- override in subclasses
        raise NotImplementedError(
            "class {.__name__!r} must implement 'initializeInstance'".format(cls)
        )

    @classmethod
    def configureInstance(cls):
        """
        Configure a newly minted instance
        """
        # implementation dependent -- override in subclasses
        raise NotImplementedError(
            "class {.__name__!r} must implement 'configureInstance'".format(cls)
        )

    # trait and slot access
    def getTraits(self):
        """
        Return an iterable over my traits
        """
        # easy: i already support the iteration protocol
        return iter(self)

    def getSlots(self):
        """
        Return an iterable over the trait value storage
        """
        # i don't know how to do it, but my children had better
        raise NotImplementedError("class {.__name__!r} must implement 'getSlots'".format(cls))

    # support for giving up values
    @classmethod
    def inheritedSlot(cls, component, trait):
        """
        Find the slot of {trait} in the nearest ancestor of {component} that has it; {None} when
        {component} declares {trait} itself, or when that ancestor is marked {internal} and so
        has no inventory
        """
        # a trait that {component} declares
        if trait in component.pyre_localTraits:
            # is its own
            return None
        # go through the ancestors of {component}, nearest first
        for ancestor in component.pyre_pedigree[1:]:
            # the ones without {trait}
            if trait not in ancestor.pyre_configurables():
                # are of no interest
                continue
            # get the inventory of the nearest one with it
            inventory = ancestor.pyre_inventory
            # ancestors marked {internal} have none
            if inventory is None:
                # so {component} acts as if it owned {trait}
                return None
            # the others hold the slot
            return inventory[trait]

        # an inherited trait that no ancestor has is a bug, so access the journal
        import journal

        # and complain
        raise journal.firewall("pyre.components").log(
            f"{component}: could not locate the slot of '{trait.name}'"
        )

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my table
        self.traits = {}
        # all done
        return

    def __getitem__(self, trait):
        # ask my table
        return self.traits[trait]

    def __setitem__(self, trait, item):
        # punt
        self.traits[trait] = item
        # all done
        return

    def __iter__(self):
        # iterate over my keys
        return iter(self.traits)

    # implementation details
    def populate(self, slots):
        """
        Populate my trait map
        """
        # update my map
        self.traits.update(slots)
        # all done
        return


# end of file
