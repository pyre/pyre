# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Node import Node


class Configuration(Node):
    """
    Handler for the top level tag in pml documents
    """

    # constants
    elements = ("inventory", "bind")


    # interface
    def notify(self, parent, locator):
        """
        Let {parent} now that processing this configuration tag is complete
        """
        return parent.onConfiguration(self)


    def onBind(self, key, value):
        """
        Process a binding of a property to a value
        """
        self.assignments.append((key, value))
        return


    def onInventory(self, assignments):
        """
        Handle nested inventory tags
        """
        self.assignments += assignments
        return


    # meta methods
    def __init__(self, parent, attributes, locator):
        self.assignments = []
        return
    

# end of file
