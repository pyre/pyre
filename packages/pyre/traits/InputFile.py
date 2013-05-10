# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import weakref
# superclass
from .Property import Property


# declaration
class InputFile(Property):
    """
    A class declarator for input files
    """


    # class data
    mode = "r"
    default = "stdin"


    # framework support
    def macro(self, model):
        """
        Return my preferred macro converter
        """
        # build interpolations
        return model.interpolation


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a file
        """
        # N.B.: no chaining upwards here: output files are their own schema, which would cause
        # infinite recursion...
        # if the value is a string
        if isinstance(value, str):
            # check whether it is one of the special names
            if value == "stdin":
                import sys
                return sys.stdin
            # otherwise, assume it is a valid file name and open it
            return self.pyre_fileserver.open(value, mode=self.mode)
        # if not, just pass it through
        return value


    # meta-methods
    def __init__(self, mode=mode, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # save my mode
        self.mode = mode
        # i am my own schema
        self.schema = self
        # all done
        return


# end of file 
