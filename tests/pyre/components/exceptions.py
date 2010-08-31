#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""

def test():
    from pyre.components.Component import Component
    from pyre.components.exceptions import (
        ComponentError, 
        CategoryMismatchError, ImplementationSpecificationError, InterfaceError,
        TraitNotFoundError)

    class component(Component): pass

    c1 = component(name="c1")
    c2 = component(name="c2")

    try:
        raise ComponentError(description=None)
    except ComponentError as error:
        pass

    try:
        raise CategoryMismatchError(configurable=c1, target=c2, name="test")
    except CategoryMismatchError as error:
        pass

    try:
        raise ImplementationSpecificationError(name="test", errors=[])
    except ImplementationSpecificationError as error:
        pass

    try:
        raise InterfaceError(component=c1, interface=c2, report=None)
    except InterfaceError as error:
        pass

    try:
        raise TraitNotFoundError(configurable=c1, name=None)
    except TraitNotFoundError as error:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
