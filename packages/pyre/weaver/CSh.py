# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .LineMill import LineMill


# my declaration
class CSh(LineMill):
    """
    Support for the c shell
    """


    # traits
    variant = pyre.properties.str(default='/bin/csh')
    variant.doc = "the shell variant to use on the hash-bang line"


    # interface
    @pyre.provides
    def render(self, document, stationery):
        """
        Layout the {document} using {stationery} for the header and footer
        """
        # render the hash-bang line
        if self.variant:
            yield "#!" + self.variant
        # and the rest
        for line in super().render(document, stationery):
            yield line
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(comment='#', **kwds)
        return


# end of file 
