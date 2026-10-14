#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dict traits of a component without a name, whose tables live outside the
configuration store, accept the same values as those of named components
"""


def test() -> None:
    """
    Assign whole tables, text, and individual keys to the dict traits of an anonymous component
    """
    # support
    import pyre

    # a component with dicts of strings and of integers
    class Reader(pyre.component, family="pyre.tests.dict.anonymous.reader"):
        """
        A component with dict traits
        """

        # a table of strings
        selection = pyre.properties.kv()
        # and one of integers
        counts = pyre.properties.dict(schema=pyre.properties.int())

    # make a reader without a name
    reader = Reader()
    # it starts out empty
    assert dict(reader.selection) == {}

    # assign a table
    reader.selection = {"band": "L", "frequency": "A"}
    # and it is there
    assert dict(reader.selection) == {"band": "L", "frequency": "A"}
    # assign another
    reader.selection = {"band": "S"}
    # which replaces it
    assert dict(reader.selection) == {"band": "S"}
    # assign text
    reader.selection = "band:L, polarization:HH"
    # which is split into entries
    assert dict(reader.selection) == {"band": "L", "polarization": "HH"}
    # set a key
    reader.selection["band"] = "S"
    # which replaces its value
    assert dict(reader.selection) == {"band": "S", "polarization": "HH"}

    # the values of a table of integers
    reader.counts = "one:1, two:1+1"
    # are converted by the schema of the entries
    assert dict(reader.counts) == {"one": 1, "two": 2}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
