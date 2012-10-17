# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .Container import Container


class List(Container):
    """
    The list type declarator
    """


    # interface
    def coerce(cls, value, **kwds):
        """
        Convert {value} into a list
        """
        # easy enough; resist the temptation to optimize this by skipping the call to super: we
        # have to coerce every item in the container!
        return list(super().coerce(value, **kwds))


# end of file 
