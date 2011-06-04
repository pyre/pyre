# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the pyre package
import pyre


# my interface
from .Stationery import Stationery


class Banner(pyre.component, family="pyre.weaver.banner", implements=Stationery):
    """
    The base component for content generation
    """

    author = pyre.properties.str(default="{pyre.user.name}")
    author.doc = "the name of the entity to blame for this content"

    affiliation = pyre.properties.str(default="{pyre.user.affiliation}")
    affiliation.doc = "the author's institutional affiliation"

    copyright = pyre.properties.str()
    copyright.doc = "the copyright note"


    footer = pyre.properties.str()
    footer.doc = "the marker to drop at the bottom of the document"


    @pyre.export
    def foo(self):
        """
        A behavior
        """


# end of file 
