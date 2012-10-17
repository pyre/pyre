# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from .Property import Property


class OutputFile(Property):
    """
    A class declarator for output files
    """


    # class data
    mode = "w"
    default = "stdout"


    # interface
    def pyre_cast(self, value, **kwds):
        """
        Attempt to convert {value} into a file
        """
        # if the value is a string
        if isinstance(value, str):
            # check whether it is one of the special names
            if value == "stdout":
                import sys
                return sys.stdout
            if value == "stderr":
                import sys
                return sys.stderr
            # otherwise, assume it is a valid file name and open it
            return open(value, mode=self.mode)
        # if not, just pass it through
        return value


# end of file 
