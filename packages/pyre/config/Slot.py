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


    # meta methods
    def __init__(self, priority, **kwds):
        super().__init__(**kwds)
        self._priority = priority
        return


    # private data
    _priority = None


# end of file 
