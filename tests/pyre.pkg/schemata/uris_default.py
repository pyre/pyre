#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Without a declared default, a uri holds {None}, both as a schema and as a trait
"""


def test() -> None:
    """
    Check what a uri holds when nobody chose a value for it
    """
    # support
    import pyre

    # a uri schema without a default
    schema = pyre.schemata.uri()
    # has none
    assert schema.default is None, repr(schema.default)

    # a component with a uri trait whose default is not declared
    class Sensor(pyre.component, family="pyre.tests.schemata.uris.default.sensor"):
        """
        A component with a uri trait
        """

        # the source of the data
        source = pyre.properties.uri()

    # the trait has no default
    assert Sensor.pyre_trait(alias="source").default is None
    # so the class
    assert Sensor.source is None, repr(Sensor.source)
    # and its instances hold none
    assert Sensor(name="sensor").source is None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
