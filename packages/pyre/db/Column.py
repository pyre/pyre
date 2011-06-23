# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..schema.Descriptor import Descriptor


class Column(Descriptor):
    """
    The base class for database table descriptors
    """


    # interface
    def setDefault(self, value):
        """
        Set a new default value
        """
        # install the new value
        self.default = value
        # enable chaining
        return self


# end of file 
