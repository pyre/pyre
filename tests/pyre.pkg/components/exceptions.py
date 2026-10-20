#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Tests for all the exceptions raised by this package
"""


def test():
    import pyre
    from pyre.components.exceptions import (
        ComponentError,
        CategoryMismatchError,
        FacilitySpecificationError,
        ImplementationSpecificationError,
        ProtocolError,
        ResolutionError,
        TraitNotFoundError,
    )

    class component(pyre.component):
        pass

    class protocol(pyre.protocol):
        pass

    c1 = component(name="c1")
    c2 = component(name="c2")

    try:
        raise ComponentError()
    except ComponentError as error:
        pass

    try:
        raise CategoryMismatchError(configurable=c1, target=c2, name="test")
    except CategoryMismatchError as error:
        pass

    # text that is not a component specification
    try:
        raise FacilitySpecificationError(protocol=protocol, value="")
    # is a failure to resolve it, that names the text and the protocol
    except ResolutionError as error:
        assert isinstance(error, FacilitySpecificationError), error
        assert str(error) == (
            f"could not resolve '' into a component that implements {protocol}, "
            "since it is not a component specification"
        ), str(error)

    try:
        raise ImplementationSpecificationError(name="test", errors=[])
    except ImplementationSpecificationError as error:
        pass

    try:
        raise ProtocolError(component=c1, protocol=protocol, report=None)
    except ProtocolError as error:
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
