#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a component specification that does not resolve is left alone by coercion, so that
the rest of the value processing, and ultimately the validators, get to decide what to do with it
"""


def test():
    """
    Coerce a specification that names no component
    """
    # access the framework
    import pyre

    # a protocol with no implementations anywhere
    class gadgets(pyre.protocol, family="test.schemata.gadgets"):
        """
        The requirements of a gadget
        """

    # make a schema for components that implement it
    schema = pyre.schemata.component(protocol=gadgets)
    # a specification that names a component that does not exist
    spec = "nosuch#thing"
    # coerce it
    value = schema.coerce(spec)
    # the failure to resolve it is not an error at this stage: the string comes back untouched
    assert value == spec

    # all done
    return schema


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
