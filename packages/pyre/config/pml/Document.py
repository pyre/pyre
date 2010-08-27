# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from pyre.xml.Document import Document as Base


# import the handlers
from .Bind import Bind
from .Component import Component
from .Configuration import Configuration
from .Inventory import Inventory


class Document(Base):
    """
    The anchor point for the handlers of the pml document tags
    """

    # constants
    root = "config" # the top level element tag

    # get access to the element descriptor factory
    import pyre.xml
    # the element descriptors
    bind = pyre.xml.element(tag="bind", handler=Bind)
    component = pyre.xml.element(tag="component", handler=Component)
    config = pyre.xml.element(tag="config", handler=Configuration)
    inventory = pyre.xml.element(tag="inventory", handler=Inventory)


    # interface
    def onConfiguration(self, configuration):
        """
        Handle the top level tag
        """
        self.dom = configuration.events
        return


# end of file
