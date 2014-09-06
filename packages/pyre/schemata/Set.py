# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from .Sequence import Sequence


# declaration
class Set(Sequence):
    """
    The set type declarator
    """


    # constants
    typename = 'set' # the name of my type
    container = set # the container I represent


    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a set
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
