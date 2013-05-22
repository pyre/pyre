# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import time
# superclass
from .Type import Type


# my declaration
class Time(Type):
    """
    A type declarator for timestamp
    """

    # the default format
    format = "%H:%M:%S"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a timestamp
        """
        # attempt to cast {value} into a time
        return time.strptime(value, self.format)


    # meta-methods
    def __init__(self, format=format, **kwds):
        # chain up
        super().__init__(**kwds)
        # store the format
        self.format = format
        # all done
        return


# end of file 
