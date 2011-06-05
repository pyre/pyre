# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# declaration
class Language(pyre.interface, family="pyre.weaver.languages"):
    """
    The interface specification for output languages
    """


    # interface
    @pyre.provides
    def render(self, document, stationery):
        """
        Layout the {document} using {stationery} for the header and footer
        """


# end of file 
