#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Without a declared default, an internet address holds {None}, both as a schema and as a trait
"""


def test() -> None:
    """
    Check what an internet address holds when nobody chose a value for it
    """
    # support
    import pyre

    # an internet address schema without a default
    schema = pyre.schemata.inet()
    # has none
    assert schema.default is None, repr(schema.default)

    # a component with an internet address trait whose default is not declared
    class Server(pyre.component, family="pyre.tests.schemata.inets.default.server"):
        """
        A component with an internet address trait
        """

        # the address it listens at
        address = pyre.properties.inet()

    # the trait has no default
    assert Server.pyre_trait(alias="address").default is None
    # so the class
    assert Server.address is None, repr(Server.address)
    # and its instances hold none
    assert Server(name="server").address is None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
