# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the pyre package
import pyre


# my ancestors
from .Indenter import Indenter
# my protocol
from .Language import Language


# turn my subclasses into components
class Mill(pyre.component, Indenter, implements=Language):
    """
    The base class for text renderers
    """


    # types
    # the protocols of my traits
    from .Stationery import Stationery


    # traits
    stationery = Stationery()
    stationery.doc = "the overall layout of the document"

    languageMarker = pyre.properties.str()
    languageMarker.doc = "the string to use as the language marker"


    # interface
    @pyre.export
    def render(self):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # create the header
        yield from self.header()
        # and a blank line
        yield ''

        # process it
        yield from self.body()
        # another blank line
        yield ''

        # and the footer
        yield from self.footer()
        # all done
        return


    # the lower level interface
    @pyre.export
    def header(self):
        """
        Build the header of the document
        """
        # the low level guy does all the work; just wrap everything in a comment block
        yield from self.commentBlock(self._header())
        # all done
        return


    @pyre.export
    def body(self):
        """
        The body of the document
        """
        # empty, by default
        return ()

                                          
    @pyre.export
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
