# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


class Unresolved:
    """
    A node that raises {UnresolvedNodeError} when its value is read
    """


    # exceptions
    from .exceptions import UnresolvedNodeError


    # public data
    request = None # the unresolved name


    @property
    def getValue(self):
        """
        Compute my value
        """
        raise self.UnresolvedNodeError(node=self, name=self.request)


    # meta methods
    def __init__(self, request, **kwds):
        super().__init__(**kwds)
        self.request = request
        return


    def __str__(self):
        return self.request


    # debugging support
    def dump(self, name, indent):
        print('{}{}: <unresolved>'.format(indent, name))
        return self


# end of file
