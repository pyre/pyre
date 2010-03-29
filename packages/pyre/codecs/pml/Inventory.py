# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Node import Node


class Inventory(Node):
    """
    Handler for the inventory tag in pml documents
    """

    # constants
    elements = ("inventory", "property",)


    # interface
    def notify(self, parent, locator):
        """
        Let {parent} now that processing this inventory tag is complete
        """
        return parent.onInventory(self)


    def onInventory(self, inventory):
        """
        """
        return


    def onProperty(self, property):
        """
        """
        return


    # meta methods
    def __init__(self, parent, attributes, locator):
        return
    

# end of file
