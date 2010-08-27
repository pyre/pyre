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
        # buld the configuration target out of the family and instance name
        # this mechanism enables configuration settings for multiple possible bindings of a
        # given property to coëxist in the same file
        marker = '#'.join(tag for tag in [self.family, self.name] if tag)
        # add my namespace to the key
        key.append(marker)
        # store it with my other bindings
        self.bindings.append((key, value, locator))
        return


    # meta methods
    def __init__(self, parent, attributes, locator, **kwds):
        super().__init__(**kwds)
        # storage for my property bindings
        self.bindings = []
        # extract the attributes
        self.name = attributes.get('name')
        self.family = attributes.get('family')

        # make sure that at least one of these attributes were given
        if not self.name and not self.family:
            raise self.DTDError(
                description="neither 'name' not 'family' were specified",
                locator=locator
                )

        return
    

# end of file
