#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the keys of a dict trait can be set, replaced and removed one at a time, and that
each value is converted by the schema of the entries
"""


def test() -> None:
    """
    Work with the individual keys of dict traits
    """
    # support
    import pyre

    # a component with dicts of strings and of integers
    class Reader(pyre.component, family="pyre.tests.dict.keys.reader"):
        """
        A component with dict traits
        """

        # a table of strings
        selection = pyre.properties.kv()
        # and one of integers
        counts = pyre.properties.dict(schema=pyre.properties.int())

    # make a reader
    reader = Reader(name="reader")

    # add a key
    reader.selection["band"] = "L"
    # and another
    reader.selection["frequency"] = "A"
    # both are there
    assert dict(reader.selection) == {"band": "L", "frequency": "A"}
    # replace one
    reader.selection["band"] = "S"
    # which changes it alone
    assert dict(reader.selection) == {"band": "S", "frequency": "A"}
    # remove one
    del reader.selection["frequency"]
    # which leaves the others
    assert dict(reader.selection) == {"band": "S"}

    # keys added one at a time to a table of integers
    reader.counts["one"] = "1"
    reader.counts["two"] = 2
    reader.counts["three"] = "1+2"
    # are converted by the schema of the entries
    assert dict(reader.counts) == {"one": 1, "two": 2, "three": 3}

    # a key added after the table was assigned whole
    reader.selection = {"band": "L"}
    reader.selection["polarization"] = "HH"
    # joins it
    assert dict(reader.selection) == {"band": "L", "polarization": "HH"}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
