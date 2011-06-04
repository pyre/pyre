# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre


class Weaver(pyre.component, family="pyre.weaver"):
    """
    The base component for content generation
    """

    # types
    from .components.Stationery import Stationery

    # traits
    stationery = pyre.properties.facility(interface=Stationery, default=Stationery.default())
    stationery.doc = "the overall layout of the document"


    @pyre.export
    def weave(self):
        """
        Assemble the document
        """


# end of file 
