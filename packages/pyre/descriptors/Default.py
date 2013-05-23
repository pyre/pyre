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


    # public data
    default = None


    # framework requests
    def getValue(self):
        """
        Return my value
        """
        # easy enough
        return self.default


    # meta methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(**kwds)
        # set my default value
        self.default = default
        # all done
        return


# end of file 
