# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Function import Function


class Polyadic(Function):
    """
    Base class for evaluators whose value depends on a sequence of nodes
    """


    # interface
    def getDomain(self):
        """
        Return an iterator over the set of nodes in my domain
        """
        return iter(self._domain)


    # meta methods
    def __init__(self, domain, **kwds):
        super().__init__(**kwds)
        self._domain = domain
        return


    def _replace(self, old, new):
        """
        Patch my domain by replacing {old} with {new}.

        This is used by the model during node resolution. Please don't use directly unless you
        have thought the many and painful implications through
        """
        self._domain.remove(old)
        self._domain.add(new)
        return new


    # private data
    _domain = None


# end of file 
