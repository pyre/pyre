# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from .Sequence import Sequence


# declaration
class List(Sequence):
    """
    The list type declarator
    """


    # constants
    typename = 'list' # the name of my type
    container = list # the container i represent


    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a list
        """
        # easy enough; resist the temptation to optimize this by skipping the call to {super}:
        # we have to coerce every item in the container!
        return self.container(super().coerce(value, **kwds))


    # meta-methods
    def __init__(self, default=container, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
