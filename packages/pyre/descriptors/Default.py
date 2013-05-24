# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Default:
    """
    Mix-in class that supports the notion of a default value
    """


    # framework requests
    def getValue(self):
        """
        Return my value
        """
        # easy enough
        return self.default


# end of file 
