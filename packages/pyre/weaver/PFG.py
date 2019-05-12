# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .LineMill import LineMill


# my declaration
class PFG(LineMill):
    """
    Support for pyre configuration files
    """


    # meta-methods
    def component(self, name):
        """
        Render a component
        """
        # easy enough
        return self.place(f"{name}:")


    def trait(self, name, value):
        """
        Render a trait
        """
        # easy enough
        return self.place(f"{name} = {value}")


    def value(self, value):
        """
        Renderer a value for a multi-line trait
        """
        # easy
        return self.place(value)


    # private data
    comment = ';'


# end of file
