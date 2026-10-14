#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the command line sets dict traits in their text form and one key at a time, and that
it outranks configuration files
"""


def test() -> None:
    """
    Parse a command line and build the components it configures
    """
    # support
    import pyre
    import pyre.config

    # access the executive
    executive = pyre.executive
    # and the store
    nameserver = executive.nameserver
    # a key set in a file, which the command line overrides with a whole table
    nameserver.insert(
        name="replaced.selection.band",
        value="S",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )

    # a component with dicts of strings and of integers
    class Reader(pyre.component, family="pyre.tests.dict.commandline.reader"):
        """
        A component with dict traits
        """

        # a table of strings
        selection = pyre.properties.kv()
        # and one of integers
        counts = pyre.properties.dict(schema=pyre.properties.int())

    # a command line
    commandline = [
        # a whole table, in its text form
        "--whole.selection=band:L, frequency:A, polarization:HH",
        # the same table, one key at a time
        "--keys.selection.band=L",
        "--keys.selection.frequency=A",
        "--keys.selection.polarization=HH",
        # a whole table and then one of its keys
        "--mixed.selection=band:L, frequency:A",
        "--mixed.selection.band=S",
        # a whole table over a key set in a file
        "--replaced.selection=band:L",
        # the keys of a table of integers
        "--keys.counts.one=1",
        "--keys.counts.two=1+1",
    ]
    # parse it
    events = pyre.config.newCommandLineParser().parse(commandline)
    # and process the assignments it holds
    executive.configurator.processEvents(events=events, priority=executive.priority.command)

    # the whole table
    assert dict(Reader(name="whole").selection) == {
        "band": "L",
        "frequency": "A",
        "polarization": "HH",
    }
    # is the same as the one built a key at a time
    keys = Reader(name="keys")
    assert dict(keys.selection) == {"band": "L", "frequency": "A", "polarization": "HH"}
    # whose integers are converted
    assert dict(keys.counts) == {"one": 1, "two": 2}
    # the key that comes after the whole table wins
    assert dict(Reader(name="mixed").selection) == {"band": "S", "frequency": "A"}
    # and the command line wins over the file
    assert dict(Reader(name="replaced").selection) == {"band": "L"}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
