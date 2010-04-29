# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Node import Node


class Component(Node):
    """
    Handler for the inventory tag in pml documents
    """

    # constants
    elements = ("bind",)


    # interface
    def notify(self, parent, locator):
        """
        Transfer all the key,value bindings to my parent
        """
        for key, value, locator in self.bindings:
            parent.createAssignment(key=key, value=value, locator=locator)
        return


    # assignment handler
    def createAssignment(self, key, value, locator):
        """
        Process a binding of a property to a value
        """
        # add my namespace to the key
        # NYI: conditional bindings
        key.append(self.family)
        # store it with my other bindings
        self.bindings.append((key, value, locator))
        return


    # meta methods
    def __init__(self, parent, attributes, locator):
        self.family = attributes['family']
        self.bindings = []
        return
    

# end of file
