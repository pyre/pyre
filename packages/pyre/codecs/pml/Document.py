# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from pyre.xml.Document import Document as Base


class Document(Base):
    """
    The anchor point for the handlers of the pml document tags
    """

    # constants
    root = "inventory" # the op level element tag

    # get access to the element descriptor factory
    import pyre.xml
    # and the handlers
    from .Inventory import Inventory
    from .Package import Package
    from .Property import Property

    # the element descriptors
    inventory = pyre.xml.element(tag="inventory", handler=Inventory)
    package = pyre.xml.element(tag="package", handler=Package)
    property = pyre.xml.element(tag="property", handler=Property)


    # interface
    def onInventory(self, inventory):
        """
        """
        return


# end of file
