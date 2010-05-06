# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Error import Error


class UnresolvedNode(Error):
    """
    An evaluator that raises UnresolvedNodeError
    """


    # public data
    name = None # the unresolved name


    # interface
    def compute(self):
        """
        Compute my value
        """
        raise self.UnresolvedNodeError(name=self.name, node=self._owner)


    # meta methods
    def __init__(self, name, **kwds):
        super().__init__(**kwds)
        self.name = name
        return


    # exceptions
    from . import UnresolvedNodeError


# end of file 
