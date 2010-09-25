# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..calc.Node import Node


class Slot(Node):
    """
    Storage for trait values
    """


    # constants
    DEFAULT_PRIORITY = (-1,-1)


    # meta methods
    def __init__(self, priority=DEFAULT_PRIORITY, **kwds):
        super().__init__(**kwds)
        self._priority = priority
        return


    # private data
    _priority = None


# end of file 
