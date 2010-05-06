# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Function import Function


class Unary(Function):
    """
    Base class for evaluators that are functions of one other node
    """


    # interface
    def getDomain(self):
        """
        Return an iterable over my domain
        """
        yield self._op
        return


    # meta methods
    def __init__(self, node, **kwds):
        super().__init__(**kwds)
        self._op = node
        return


    # implementation details
    def _replace(self, name, old, new):
        """
        Patch my domain by replacing {old} with {new}.

        This is used by the model during node resolution. Please don't use directly unless you
        have thought the many and painful implications through
        """
        self._op = new
        return


# end of file 
