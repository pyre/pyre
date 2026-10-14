#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the tables of dict traits can be set on the component class, by assignment or
through its family in the configuration store, and that instances start from them
"""


def test() -> None:
    """
    Set the tables of a component class and build instances
    """
    # support
    import pyre

    # access the store
    nameserver = pyre.executive.nameserver
    # place a table under the family of a component class, the way a configuration file would
    nameserver.insert(
        name="pyre.tests.dict.class.reader.selection",
        value="band:L, frequency:A",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )
    # and a key of the table of an instance, likewise
    nameserver.insert(
        name="own.selection.band",
        value="X",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )

    # a component with a table
    class Reader(pyre.component, family="pyre.tests.dict.class.reader"):
        """
        A component with a dict trait
        """

        # a table of strings
        selection = pyre.properties.kv()

    # the class picks up the table configured for its family
    assert dict(Reader.selection) == {"band": "L", "frequency": "A"}
    # and so do its instances
    assert dict(Reader(name="configured").selection) == {"band": "L", "frequency": "A"}

    # assign a table to the class
    Reader.selection = {"band": "S"}
    # which replaces its own
    assert dict(Reader.selection) == {"band": "S"}
    # instances built from now on start from it
    reader = Reader(name="assigned")
    assert dict(reader.selection) == {"band": "S"}
    # and can change their own
    reader.selection = {"band": "L"}
    # which they hold
    assert dict(reader.selection) == {"band": "L"}
    # without changing the class
    assert dict(Reader.selection) == {"band": "S"}
    # an instance whose own key is configured
    own = Reader(name="own")
    # keeps it over the table of the class
    assert own.selection["band"] == "X"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
