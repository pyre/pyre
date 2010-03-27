# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Node import Node


class Package(Node):
    """
    Handler for the package tag in pml documents
    """

    elements = ("package", "property")


    # interface
    def notify(self, parent, locator):
        """
        Let {parent} know that processing this package tag is complete
        """
        return parent.onPackage(self)


    # hooks for my nested tags
    def onPackage(self, package):
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
