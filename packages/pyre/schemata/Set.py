# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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


    # interface
    def coerce(cls, value, **kwds):
        """
        Convert {value} into a set
        """
        # easy enough; resist the temptation to optimize this by skipping the call to super: we
        # have to coerce every item in the container!
        return set(super().coerce(value, **kwds))


    # meta-methods
    def __init__(self, default=set, **kwds):
        # adjust the default; carefully, so we don't all end up using the same global container
        # checking for {None} is not appropriate here; the user may want {None} as the default
        # value; we need a way to know that {default} was not supplied: use {set} as the
        # marker
        default = set() if default is set else default
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
