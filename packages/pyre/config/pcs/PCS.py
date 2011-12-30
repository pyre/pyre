# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from ..Codec import Codec


class PCS(Codec):
    """
    This package contains the implementation of the pcs reader and writer
    """


    # constants
    encoding = "pcs"


    # interface
    def decode(self, source, locator=None):
        """
        Parse {source} and return the configuration events it contains
        """
        return []


# end of file
