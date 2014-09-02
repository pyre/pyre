# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .BlockMill import BlockMill


# my declaration
class XML(BlockMill):
    """
    Support for XML
    """


    # interface
    @pyre.export
    def header(self):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # render the xml marker
        yield '<?xml version="1.0"?>'
        # and the rest
        yield from super().header()
        # all done
        return


    # private data
    startBlock = '<!--'
    commentMarker = ' !'
    endBlock = '-->'


# end of file 
