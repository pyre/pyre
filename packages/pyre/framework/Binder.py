# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections


class Binder(object):
    """
    Binder converts trait values from configuration settings to the trait native types
    """


    # public data
    shelves = None # the index of component sources


    # interface
    def retrieveSymbol(self, codec, source, symbol, locator):
        """
        Get {codec} to resolve {symbol} either by processing {source} or by retrieving from a
        previously cached shelf
        """
        # check whether we have seen this {source} before
        try:
            shelf = self.shelves[source]
        except KeyError:
            # if not, get the codec to build a new shelf
            shelf = codec.decode(source=source, locator=locator)
            # and cache it
            self.shelves[source] = shelf
        # extract the requested symbol
        descriptor = codec.retrieveSymbol(shelf=shelf, symbol=symbol)
        # and return it
        return descriptor


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
            print("{._pyre_name!r}: binding {.name!r}".format(component, trait))
            trait.pyre_assign(getattr(inventory, trait.name))
        # all done
        return component


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.shelves = {}

        return


# end of file 
