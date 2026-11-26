# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .NamedTuple import NamedTuple


# declaration
class Mutable(NamedTuple):
    """
    Storage for and access to the values of mutable record instances

    This class assumes that its items are {pyre.calc} nodes.
    """

    # interface
    def pyre_observe(self, index, observer):
        """
        Let {observer} know of changes to the value at {index}
        """
        # get the node that holds the value
        node = super().__getitem__(index)
        # and add {observer} to the ones it notifies
        node.addObserver(observer)
        # all done
        return self

    # meta-methods
    def __getitem__(self, index):
        """
        Retrieve the item at {index} and return its value
        """
        # get the item
        item = super().__getitem__(index)
        # return the value
        return item.value

    def __setitem__(self, index, value):
        """
        Set the item at {index} to the indicated value
        """
        # get the node
        node = super().__getitem__(index)
        # and set its value
        node.value = value
        # all done
        return

    def __iter__(self):
        """
        Build an iterator over my values
        """
        # ask my tuple for an iterator
        iterator = super().__iter__()
        # for each item
        for item in iterator:
            # return its value
            yield item.value
        # all done
        return

    # private data
    __slots__ = ()


# end of file
