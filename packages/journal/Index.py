# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# declaration
class Index:
    """
    Wrapper around the C++ diagnostic indices from the journal extension module
    """


    # meta methods
    def __init__(self, lookup, setter, getter, **kwds):
        # chain to the ancestors
        super().__init__(**kwds)
        # attach the lookup strategy
        self.lookup = lookup
        # and the state accessors
        self.setter = setter
        self.getter = getter
        # all done
        return


    def __getitem__(self, name):
        """
        Retrieve the state associated with the given {name}
        """
        return self._State(inventory=self.lookup(name), setter=self.setter, getter=self.getter)
        

    # implementation details
    class _State:

        # public state
        device = None

        @property
        def state(self):
            return self.getter(self.inventory)

        @state.setter
        def state(self, value):
            self.setter(self.inventory, value)
            return

        # meta methods
        def __init__(self, inventory, setter, getter):
            self.setter = setter
            self.getter = getter
            self.inventory = inventory
            return


# end of file 
