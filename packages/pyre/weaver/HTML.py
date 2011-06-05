# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .BlockMill import BlockMill


# my declaration
class HTML(BlockMill):
    """
    Support for HTML
    """


    # traits
    doctype = pyre.properties.str(default='html5')
    doctype.doc = "the doctype variant to use on the first line"


    # interface
    @pyre.provides
    def render(self, document, stationery):
        """
        Layout the {document} using {stationery} for the header and footer
        """
        # render the doctype
        if self.doctype:
            yield "<!doctype html{}>".format(self.doctypes[self.doctype])
        # and the rest
        for line in super().render(document, stationery):
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
