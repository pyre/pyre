# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Inventory(Node):
    """
    Handler for the package tag in pml documents
    """

    # constants
    elements = ("component", "package", "bind")


    # interface
    def notify(self, parent, locator):
        """
        Transfer all the key,value bindings to my parent
        """
        # process my bindings
        for key, value, locator in self.bindings:
            # add my namespace to the key
            path = self.name + key
            # dispatch the event to my parent
            parent.createAssignment(key=path, value=value, locator=locator)
        return


    # assignment handler
    def createAssignment(self, key, value, locator):
        """
        Process a binding of a property to a value
        """
        # store it with my other bindings
        self.bindings.append((key, value, locator))
        # and return
        return


    # meta methods
    def __init__(self, parent, attributes, locator, **kwds):
        super().__init__(**kwds)

        self.name = attributes['name'].split(self.separator)
        self.bindings = []
        return
    

# end of file
