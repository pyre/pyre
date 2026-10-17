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
        TraitNotFoundError,
    )

    class component(pyre.component):
        # a facility, for the errors about its specification
        tool = pyre.facility(protocol=pyre.protocol)

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

    # a facility whose specification can't be instantiated
    try:
        raise FacilitySpecificationError(
            configurable=c1, trait=component.pyre_trait(alias="tool"), value="nothing"
        )
    # names the component, the trait and the specification
    except FacilitySpecificationError as error:
        assert str(error) == f"{c1}.tool: could not instantiate 'nothing'", str(error)

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
