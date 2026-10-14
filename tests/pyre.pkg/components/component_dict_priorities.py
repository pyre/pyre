#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the entries of a dict trait compete with the settings of its individual keys by
priority: a whole map carries the priority of its assignment, and replaces the map it overrides
"""


def test() -> None:
    """
    Combine whole maps and individual keys, set at user, command and explicit priority
    """
    # support
    import pyre

    # access the store
    nameserver = pyre.executive.nameserver
    # and its priorities
    priority = nameserver.priority

    # a component with dicts of strings and of integers
    class Reader(pyre.component, family="pyre.tests.dict.priorities.reader"):
        """
        A component with dict traits
        """

        # a map of strings
        selection = pyre.properties.kv()
        # and a map of integers
        counts = pyre.properties.dict(schema=pyre.properties.int())

    # settings, as a configuration file and the command line would leave them in the store
    settings = [
        # a key from a file, and the whole map from the command line
        ("file.selection.band", "S", priority.user),
        ("file.selection", "band:L", priority.command),
        # the whole map from a file, and a key from the command line
        ("line.selection", "band:S, frequency:A", priority.user),
        ("line.selection.band", "L", priority.command),
        # a key from the command line, later replaced by a whole map
        ("edit.selection.band", "L", priority.command),
        # the whole map from the command line, later replaced by another
        ("swap.selection", "band:L, frequency:A", priority.command),
        # a key of a map of integers from the command line
        ("count.counts.one", "1", priority.command),
    ]
    # go through them
    for name, value, rank in settings:
        # and place each one in the store
        nameserver.insert(
            name=name, value=value, priority=rank(), locator=pyre.tracking.simple("the test")
        )

    # the command line outranks a file, whether it sets the whole map
    assert dict(Reader(name="file").selection) == {"band": "L"}
    # or one of its keys
    assert dict(Reader(name="line").selection) == {"band": "L", "frequency": "A"}

    # a whole map assigned at command priority after a key was set at command priority
    edit = Reader(name="edit")
    # wins, and replaces the map
    edit.pyre_setTrait(
        alias="selection",
        value={"band": "S", "frequency": "B"},
        priority=priority.command(),
        locator=pyre.tracking.simple("the test"),
    )
    # so it holds the new value of the key, and the new key
    assert dict(edit.selection) == {"band": "S", "frequency": "B"}

    # a whole map assigned at command priority after another whole map at command priority
    swap = Reader(name="swap")
    # replaces it
    swap.pyre_setTrait(
        alias="selection",
        value={"band": "S"},
        priority=priority.command(),
        locator=pyre.tracking.simple("the test"),
    )
    # so the keys that are not in the new map are gone
    assert dict(swap.selection) == {"band": "S"}
    # and the entries remember where the map was set
    assert "the test" in str(nameserver.getInfo(nameserver.hash("swap.selection.band")).locator)

    # a key assigned explicitly
    pinned = Reader(name="pinned")
    pinned.selection["band"] = "L"
    # does not survive a later explicit assignment of the whole map
    pinned.selection = {"band": "S"}
    # which wins
    assert dict(pinned.selection) == {"band": "S"}

    # a key set on the command line of a map of integers
    count = Reader(name="count")
    # is converted by the schema of the entries
    assert dict(count.counts) == {"one": 1}

    # a whole map with a reference
    nameserver["pyre.tests.dict.priorities.band"] = "L"
    linked = Reader(name="linked")
    linked.selection = {"band": "{pyre.tests.dict.priorities.band}"}
    # resolves it
    assert dict(linked.selection) == {"band": "L"}
    # and follows it when it changes
    nameserver["pyre.tests.dict.priorities.band"] = "S"
    # so it holds the new value
    assert dict(linked.selection) == {"band": "S"}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
