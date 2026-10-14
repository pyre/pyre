#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dict trait whose default is {None} holds {None} until it is given a table, and that
the store can set it to {None}
"""


def test() -> None:
    """
    Use {None} as the value of dict traits
    """
    # support
    import pyre

    # access the store
    nameserver = pyre.executive.nameserver
    # the text form of {None}, the way a configuration file would set it
    nameserver.insert(
        name="cleared.selection",
        value="none",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )

    # a component with tables
    class Reader(pyre.component, family="pyre.tests.dict.none.reader"):
        """
        A component with dict traits
        """

        # a table that is not there unless it is set
        selection = pyre.properties.kv(default=None)
        # and a catalog likewise
        languages = pyre.properties.catalog(default=None)

    # make a reader
    reader = Reader(name="reader")
    # its tables are {None}
    assert reader.selection is None
    assert reader.languages is None
    # until they are given one
    reader.selection = {"band": "L"}
    # which they hold
    assert dict(reader.selection) == {"band": "L"}
    # and can be cleared again
    reader.selection = None
    # back to {None}
    assert reader.selection is None

    # a table the store sets to {None}
    assert Reader(name="cleared").selection is None

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
