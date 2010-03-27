# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Node import Node


class Property(Node):
    """
    Handler for the property tag in pml documents
    """

    # constants
    elements = ()


    # interface
    def notify(self, parent, locator):
        """
        Let {parent} now that processing this property tag is complete
        """
        return parent.onProperty(self)


    # meta methods
    def __init__(self, parent, attributes, locator):
        return


# end of file
