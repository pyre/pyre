#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dict of tuples takes whole tables and tuples one key at a time, and that the table
of one component can be assigned to another
"""


def test() -> None:
    """
    Fill tables of tuples, and copy them between components
    """
    # support
    import pyre

    # a component with a table of tuples
    class Reader(pyre.component, family="pyre.tests.dict.tuples.reader"):
        """
        A component with a table of tuples
        """

        # the legal values of each selector
        selectors = pyre.properties.dict(
            schema=pyre.properties.tuple(schema=pyre.properties.str(), default=())
        )

    # a dict of tuples says so
    assert Reader.pyre_trait("selectors").type == "dict[tuple[str]]"

    # make a reader
    reader = Reader(name="reader")
    # assign a whole table
    reader.selectors = {"band": ("L", "S"), "frequency": ["A", "B"]}
    # and its values become tuples
    assert dict(reader.selectors) == {"band": ("L", "S"), "frequency": ("A", "B")}
    # set the tuple of one key from its text form
    reader.selectors["polarization"] = "HH, HV"
    # and it is split into items
    assert reader.selectors["polarization"] == ("HH", "HV")

    # make another reader
    other = Reader(name="other")
    # and give it the table of the first one
    other.selectors = reader.selectors
    # it now has the same table
    assert dict(other.selectors) == dict(reader.selectors)
    # but its own copy of it
    other.selectors["band"] = ("L",)
    # so changing it leaves the first one alone
    assert reader.selectors["band"] == ("L", "S")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
