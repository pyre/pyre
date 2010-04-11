# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .ErrorNode import ErrorNode


class UnresolvedNode(ErrorNode):
    """
    Placeholders for nodes that are not yet resolvable by the Model.
    """


    # public data
    name = None
    clients = ()


    # interface
    def raiseException(self):
        """
        Raise an exception indicating a request for the value of an unresolved node
        """
        raise self.UnresolvedNodeError(name=self.name, node=self)


    # exceptions
    from . import UnresolvedNodeError


    # meta methods
    def __init__(self, name, client, **kwds):
        super().__init__(**kwds)
        self.name = name
        self.clients = set([client])
        return
        

# end of file 
