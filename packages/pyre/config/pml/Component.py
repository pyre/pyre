# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Component(Node):
    """
    Handler for the component tag in pml documents
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
            # if i have a name, use it as the namespace qualifier
            if self.name:
                path = self.name + key
            # otherwise use my family name
            else:
                path = self.family + key
            # and store    
            parent.createAssignment(key=path, value=value, locator=locator)

        # build conditional assignments out of the others
        for component, family, key, value, locator in self.conditionals:
            parent.createConditionalAssignment(
                component=component, family=family, key=key, value=value, locator=locator)
        return


    def createAssignment(self, key, value, locator):
        """
        Process a binding of a property to a value
        """
        # store it with my other bindings
        self.bindings.append((key, value, locator))
        # and return
        return


    def createConditionalAssignment(self, component, family, key, value, locator):
        """
        Process a conditional assignment
        """
        # print("pyre.config.pml.Component: name={.name!r}".format(self))
        # print("    component: {!r}".format(component))
        # print("    family: {!r}".format(family))
        # print("    key: {!r}".format(key))
        # print("    value: {!r}".format(value))
        # print("    locator: {}".format(locator))
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
        path = self.name + component
        # store it with my other conditional bindings
        self.conditionals.append((component, family, path, value, locator))
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
        self.name = name.split(self.separator) if name else []
        self.family = family.split(self.separator) if family else []

        # make sure that at least one of these attributes were given
        if not self.name and not self.family:
            raise self.DTDError(
                description="neither 'name' nor 'family' were specified",
                locator=locator
                )

        return
    

# end of file
