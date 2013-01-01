# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from ..patterns.Named import Named


# class declaration
class Package(Named):
    """
    The resting place of information collected while loading packages
    """


    # public data
    sources = None
    protocols = None
    components = None


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize my attributes
        self.sources = []
        self.protocols = set()
        self.components = set()
        # all done
        return


    def __str__(self):
        return 'package {.name!r}'.format(self)


# end of file 
