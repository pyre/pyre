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
    @pyre.provides
    def render(self, document):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # render the xml marker
        yield '<?xml version="1.0"?>'
        # and the rest
        for line in super().render(document):
            yield line
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(startBlock='<!--', commentMarker=' !', endBlock='-->', **kwds)
        return


    # constants
    doctypes = {
        'html5': '',

        'html4-strict':
            ' public "-//w3c//dtd html 4.01 transitional//en" "http://www.w3.org/TR/html4/strict.dtd"',

        'html4-transitional': ' public "-//w3c//dtd html 4.0 transitional//en"',
        }


# end of file 
