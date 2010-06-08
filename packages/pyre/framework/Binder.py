# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Binder(object):
    """
    Binder converts trait values from configuration settings to the trait native types
    """


    # interface
    def bindComponentInstance(self, component, executive):
        """
        Resolve and convert the current values of the traits of {component} into the native
        types described by the trait descriptors.

        Properties get cast to the native types. Facilities require more complex processing
        that involves resolving the component requests into actual class records, instantiating
        them and binding them to the {component} trait.
        """
        # access the component inventory
        inventory = component._pyre_inventory
        # iterate over the traits
        for trait, source in component.pyre_traits(categories=component._pyre_CONFIGURABLE_TRAITS):
            trait.pyre_assign(getattr(inventory, trait.name))
        # all done
        return component


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        return


# end of file 
