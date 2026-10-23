#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dict of components whose default names a component class holds the class in the
component class, and an instance named after the entry's key in each instance
"""

# support
import pyre


# a protocol for the entries
class Engine(pyre.protocol, family="pyre.tests.dict.defaults.engines"):
    """
    What powers a vehicle
    """


# an implementation
class Diesel(pyre.component, family="pyre.tests.dict.defaults.engines.diesel", implements=Engine):
    """
    An engine
    """


# a component with a table of engines whose default names a class
class Fleet(pyre.component, family="pyre.tests.dict.defaults.fleet"):
    """
    A component with a dict of components
    """

    # the engines, by vehicle
    engines = pyre.properties.dict(schema=Engine())
    engines.default = {"truck": Diesel}


def test() -> None:
    """
    Read the table of the class and of an instance
    """
    # the class holds the class it was handed
    assert Fleet.engines["truck"] is Diesel

    # make an instance
    fleet = Fleet(name="fleet")
    # get its entry
    truck = fleet.engines["truck"]
    # which is an instance of the class
    assert isinstance(truck, Diesel)
    # named after its key, as a facility names its component
    assert truck.pyre_name == "fleet.engines.truck"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
