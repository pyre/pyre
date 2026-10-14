#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dict of components takes instances one key at a time, whole tables of instances,
and the text form, with component specifications for values
"""

# support
import pyre


# a protocol for the entries
class Engine(pyre.protocol, family="pyre.tests.dict.components.engines"):
    """
    What powers a vehicle
    """


# an implementation
class Diesel(pyre.component, family="pyre.tests.dict.components.engines.diesel", implements=Engine):
    """
    An engine
    """

    # a setting
    power = pyre.properties.int(default=100)


# a component with a table of engines
class Fleet(pyre.component, family="pyre.tests.dict.components.fleet"):
    """
    A component with a dict of components
    """

    # the engines, by vehicle
    engines = pyre.properties.dict(schema=Engine())


def test() -> None:
    """
    Fill a table of components in the ways a client can
    """
    # make a fleet
    fleet = Fleet(name="fleet")
    # it starts out empty
    assert dict(fleet.engines) == {}

    # make an engine
    truck = Diesel(name="truck")
    # and add it under a key
    fleet.engines["truck"] = truck
    # it comes back as the same instance
    assert fleet.engines["truck"] is truck

    # assign a whole table of instances
    bus = Diesel(name="bus")
    fleet.engines = {"bus": bus}
    # which replaces the table
    assert dict(fleet.engines) == {"bus": bus}

    # assign the text form, with specifications for values
    fleet.engines = "van:pyre.tests.dict.components.engines.diesel#van"
    # the entry is an instance of the class the specification names
    van = fleet.engines["van"]
    assert isinstance(van, Diesel)
    # with the name it asked for
    assert van.pyre_name == "van"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
