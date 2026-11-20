#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Without a declared default, a timestamp holds {None}, both as a schema and as a trait
"""


def test() -> None:
    """
    Check what a timestamp holds when nobody chose a value for it
    """
    # support
    import pyre

    # a timestamp schema without a default
    schema = pyre.schemata.timestamp()
    # has none
    assert schema.default is None, repr(schema.default)

    # a component with a timestamp trait whose default is not declared
    class Sensor(pyre.component, family="pyre.tests.schemata.timestamps.default.sensor"):
        """
        A component with a timestamp trait
        """

        # the moment of interest
        moment = pyre.properties.timestamp()

    # the trait has no default
    assert Sensor.pyre_trait(alias="moment").default is None
    # so the class
    assert Sensor.moment is None, repr(Sensor.moment)
    # and its instances hold none
    assert Sensor(name="sensor").moment is None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
