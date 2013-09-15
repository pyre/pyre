# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .BlockMill import BlockMill


# my declaration
class SVG(BlockMill):
    """
    Support for SVG, the scalable vector graphics format
    """


    # user configurable state
    standalone = pyre.properties.bool(default=True)


    # interface
    @pyre.provides
    def render(self, document):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # if this is a stand-alone document
        if self.standalone:
            # render the xml marker
            yield '<?xml version="1.0"?>'
            # the document header
            for line in self.header(): yield line
            # and a blank line
            yield ''

        # render the svg tag
        yield '<svg version="1.1" xmlns="http://www.w3.org/2000/svg">'
        # a blank line
        yield ''
        # the document body
        for line in document: yield line
        # a blank line
        yield ''
        # close the svg tag
        yield '</svg>'

        # if this is a stand-alone document
        if self.standalone:
            # render a blank line
            yield ''
            # and the document footer
            for line in self.footer(): yield line

        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(startBlock='<!--', commentMarker=' !', endBlock='-->', **kwds)
        return


# end of file 
