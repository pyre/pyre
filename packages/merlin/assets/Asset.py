# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Asset:
    """
    Base class for all objects tracked by merlin
    """


    # constants
    category = "asset"


    # meta methods
    def __init__(self, name, uri, **kwds):
        super().__init__(**kwds)

        self.name = name # my name
        self.uri = uri # the path relative to the relevant top level asset container
        
        return


    # implementation details
    __slots__ = 'name', 'uri'


    # debugging support
    def dump(self, indent=''):
        print('{}{}'.format(indent, self.name))
        return


# end of file 
