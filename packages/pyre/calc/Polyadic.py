# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Function import Function


class Polyadic(Function):
    """
    Base class for evaluators whose value depends on a sequence of nodes
    """


    # interface
    @property
    def domain(self):
        """
        Return an iterator over the set of nodes in my domain
        """
        return iter(self._domain)


    def patch(self, old, new):
        """
        Patch my domain by replacing {old} with {new}.

        This is used by the model during node resolution. Please don't use directly unless you
        have thought the many and painful implications through
        """
        # out with the old
        self._domain.remove(old)
        # in with the new
        self._domain.add(new)
        # all done
        return new


    # meta methods
    def __init__(self, domain, **kwds):
        super().__init__(**kwds)
        self._domain = domain
        return


    # private data
    _domain = None


# end of file 
