# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Component(Node):
    """
    Handler for the inventory tag in pml documents
    """

    # constants
    elements = ("component", "bind")


    # interface
    def notify(self, parent, locator):
        """
        Transfer all the key,value bindings to my parent
        """
        # build conditional assignments if i have both a name and a family
        if self.name and self.family:
            for key, value, locator in self.bindings:
                parent.createConditionalAssignment(
                    component=self.name, family=self.family,
                    key=key, value=value, locator=locator)

            return

        # otherwise, build regular assignments out of my regular bindings
        for key, value, locator in self.bindings:
            # add my namespace to the key
            # if i have a name, use it as the namesapce qualifier
            if self.name:
                key.extendleft(reversed(self.name))
            # otherwise use my family name
            else:
                key.extendleft(reversed(self.family))
            # and store    
            parent.createAssignment(key=key, value=value, locator=locator)
        # build conditional assignments out of the others
        for component, family, key, value, locator in self.conditionals:
            parent.createConditionalAssignment(
                component=component, family=family, key=key, value=value, locator=locator)
        return


    # assignment handler
    def createAssignment(self, key, value, locator):
        """
        Process a binding of a property to a value
        """
        # store it with my other bindings
        # print("config.pml.Component: key={}, value={!r}".format(key, value))
        self.bindings.append((key, value, locator))
        return


    def createConditionalAssignment(self, component, family, key, value, locator):
        """
        Process a conditional assignment
        """
        # check whether it is supported
        if not self.name:
            raise self.DTDError(
                description="conditional binding in component with no name specification",
                locator=locator
                )
        if self.family:
            raise self.DTDError(
                description="conditional binding in component with a family specification",
                locator=locator
                )
        # add my name to the key
        component.extendleft(reversed(self.name))
        # store it with my other conditional bindings
        self.conditionals.append((component, family, key, value, locator))
        return


    # meta methods
    def __init__(self, parent, attributes, locator, **kwds):
        super().__init__(**kwds)
        # storage for my property bindings
        self.bindings = []
        self.conditionals = []
        # extract the attributes
        name = attributes.get('name')
        family = attributes.get('family')
        # split into fields and store
        self.name = name.split(self.separator) if name else None
        self.family = family.split(self.separator) if family else None
        # make sure that at least one of these attributes were given
        if not self.name and not self.family:
            raise self.DTDError(
                description="neither 'name' nor 'family' were specified",
                locator=locator
                )

        return
    

# end of file
