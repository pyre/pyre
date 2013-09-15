# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
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


    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a list
        """
        # easy enough; resist the temptation to optimize this by skipping the call to {super}:
        # we have to coerce every item in the container!
        return list(super().coerce(value, **kwds))


    # meta-methods
    def __init__(self, default=list, **kwds):
        # adjust the default; carefully, so we don't all end up using the same global container
        # checking for {None} is not appropriate here; the user may want {None} as the default
        # value; we need a way to know that {default} was not supplied: use {list} as the
        # marker
        default = list() if default is list else default
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
