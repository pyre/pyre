#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe records a configured dict trait as a table, entry by entry, and leaves
out the ones nobody configured
"""


def test() -> None:
    """
    Build the recipe of a component with a configured table
    """
    # support
    import pyre

    # a component with dicts of strings and of integers
    class Reader(pyre.component, family="pyre.tests.dict.recipe.reader"):
        """
        A component with dict traits
        """

        # a table of strings
        selection = pyre.properties.kv()
        # one of integers
        counts = pyre.properties.dict(schema=pyre.properties.int())
        # and one nobody configures
        labels = pyre.properties.kv()

    # make a reader
    reader = Reader(name="pyre.tests.dict.recipe.reader")
    # configure its tables
    reader.selection = "band:L, frequency:A"
    reader.counts = {"one": "1"}

    # build its recipe
    recipe = pyre.config.newRecipe().add(reader)
    # get its section
    section = recipe.section("pyre.tests.dict.recipe.reader")
    # the tables appear entry by entry
    assert section["selection"] == {"band": "L", "frequency": "A"}
    # with the values converted
    assert section["counts"] == {"one": 1}
    # while the table nobody configured is left out, like any other property left at its default
    assert "labels" not in section, section

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
