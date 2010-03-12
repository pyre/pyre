# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from . import _metaclass_Node
from ..patterns.Observable import Observable


class ErrorNode(Observable, metaclass=_metaclass_Node):
    """
    Base class for nodes that raise exceptions when their value is requested
    """


    # public data
    @property
    def value(self):
        """
        Raise an exception
        """
        return self.raiseException()


    # interface
    def raiseException(self):
        """
        Raise an exception that corresponds to the type of error i represent
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'raiseException'".format(self))


# end of file 
