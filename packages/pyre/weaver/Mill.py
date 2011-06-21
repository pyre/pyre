# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the pyre package
import pyre


# my ancestors
from .Indenter import Indenter
# my interface
from .Language import Language


# turn my subclasses into components
class Mill(pyre.component, Indenter, implements=Language):
    """
    The base class for text renderers
    """


    # traits
    languageMarker = pyre.properties.str()
    languageMarker.doc = "the string to use as the language marker"


    # interface
    @pyre.provides
    def render(self, document, stationery):
        """
        Layout the {document} using {stationery} for the header and footer
        """
        # create the header
        for line in self.commentBlock(self.header(stationery)):
            yield line
        # and a blank line
        yield ''
        # iterate over the document
        for line in document:
            yield line
        # another blank line
        yield ''
        # and the footer
        for line in self.footer(stationery):
            yield self.commentLine(line)
        # all done
        return


    # implementation details
    def header(self, stationery):
        """
        Build the header of the document
        """
        # if we have a language marker
        if self.languageMarker:
            # render it
            yield "-*- " + self.languageMarker + " -*-"
        # a blank, commented line
        yield ''
        # render the author
        if stationery.author:
            yield stationery.author
        # render the affiliation
        if stationery.affiliation:
            yield stationery.affiliation
        # render the copyright note
        if stationery.copyright:
            yield stationery.copyright
        # a blank, commented line
        yield ''
        # all done
        return


    def footer(self, stationery):
        """
        Build the footer of the document
        """
        # if we have a footer
        if stationery.footer:
            # render the footer
            yield stationery.footer
        # all done
        return


# end of file 
