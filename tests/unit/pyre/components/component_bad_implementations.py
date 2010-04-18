#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
A more elaborate component declaration
"""

# acccess to the parts
import pyre.components
from pyre.components.Component import Component
from pyre.components.Interface import Interface
from pyre.components.Property import Property

# declare an interface
class interface(Interface):
    """a simple interface"""
    # properties
    name = Property()
    name.default = "my name"

    @pyre.components.provides
    def say(self):
        """say my name"""

# wrap the component declarations in functions so I can control when the exceptions get raised

def badImplementationSpec():
    class badspec(Component, implements=1):
        """bad implementation specification: not an Interface subclass"""
    return badspec


def missingProperty():
    class missing(Component, implements=interface):
        """missing property: diesn't have name"""
    # properties
    oops = Property()
    oops.default = "my name"

    @pyre.components.provides
    def say(self):
        """say my name"""
        return

    return missing


def missingBehavior():
    class missing(Component, implements=interface):
        """missing property: doesn't have name"""
    # properties
    name = Property()
    name.default = "my name"

    @pyre.components.provides
    def do(self):
        """say my name"""
        return

    return missing


def noExport():
    class missing(Component, implements=interface):
        """missing behavior decorator"""
    # properties
    name = Property()
    name.default = "my name"

    def say(self):
        """say my name"""
        return

    return missing


def test():
    # check that we catch bad implementation specifications
    try:
        badImplementationSpec()
        assert False
    except pyre.components.ImplementationSpecificationError as error:
        pass

    # check that we catch missing traits
    try:
        missingProperty()
        assert False
    except pyre.components.InterfaceError:
        pass

    # check that we catch missing behaviors
    try:
        missingBehavior()
        assert False
    except pyre.components.InterfaceError:
        pass

    # check that we catch missing exports
    try:
        noExport()
        assert False
    except pyre.components.InterfaceError:
        pass

    return interface


# main
if __name__ == "__main__":
    test()


# end of file 
