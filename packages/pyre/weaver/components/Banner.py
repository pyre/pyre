# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre


class Banner(pyre.component, family="pyre.weaver.banner"):
    """
    The base component for content generation
    """

    author = pyre.properties.str(default=None)
    author.doc = "the name of the entity to blame for this content"

    affiliation = pyre.properties.str(default=None)
    affiliation.doc = "the author's institutional affiliation"


    @pyre.export
    def foo(self):
        """
        A behavior
        """


# end of file 
