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
    root = "config" # the top level element tag

    # get access to the element descriptor factory
    import pyre.xml
    # and the handlers
    from .Configuration import Configuration
    from .Inventory import Inventory
    from .Property import Property

    # the element descriptors
    config = pyre.xml.element(tag="config", handler=Configuration)
    inventory = pyre.xml.element(tag="inventory", handler=Inventory)
    property = pyre.xml.element(tag="property", handler=Property)


    # interface
    def onConfiguration(self, configuration):
        """
        """
        return


# end of file
