# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    @pyre.export
    def header(self):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # if I have doctype
        if self.doctype:
            # translate and render it
            yield "<!doctype html{}>".format(self.doctypes[self.doctype])
        # render the rest
        yield from super().header()
        # all done
        return


    # constants
    doctypes = {
        'html5': '',
        'html4-strict':
            ' public "-//w3c//dtd html 4.01//en" "http://www.w3.org/TR/html4/strict.dtd"',
        'html4-transitional': ' public "-//w3c//dtd html 4.01 transitional//en"',
        }


    # private data
    startBlock = '<!--'
    commentMarker = ' !'
    endBlock = '-->'


# end of file
