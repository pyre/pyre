# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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


    # types
    from .Stationery import Stationery


    # traits
    stationery = pyre.facility(interface=Stationery)
    stationery.doc = "the overall layout of the document"

    languageMarker = pyre.properties.str()
    languageMarker.doc = "the string to use as the language marker"


    # interface
    @pyre.provides
    def render(self, document):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # create the header
        for line in self.header():
            yield line
        # and a blank line
        yield ''
        # iterate over the document
        for line in document:
            yield line
        # another blank line
        yield ''
        # and the footer
        for line in self.footer():
            yield line
        # all done
        return


    # the lower level interface
    def header(self):
        """
        Build the header of the document
        """
        # the low level guy does all the work; just wrap everything in a comment block
        for line in self.commentBlock(self._header()):
            # pass it on
            yield line
        # all done
        return

                                          
    def footer(self):
        """
        Build the footer of the document
        """
        # cache my stationery
        stationery = self.stationery
        # if we have a footer
        if stationery.footer:
            # render the footer
            yield self.commentLine(stationery.footer)
        # all done
        return


    # implementation details
    def _header(self):
        """
        Workhorse for the header generator
        """
        # cache my stationery
        stationery = self.stationery
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


# end of file 
