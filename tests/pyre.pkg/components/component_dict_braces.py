#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that braces in the values of dict traits are read exactly once, whichever way the map is
set: the text {}, the way an empty dictionary renders, is an empty map, and an escaped brace is
a literal one, in code, in configuration files and on the command line, as it is for strings
"""


def test() -> None:
    """
    Set maps with braces in every way a client can, and read them back
    """
    # support
    import pyre
    import pyre.config

    # a component with a map and a string
    class Reader(pyre.component, family="pyre.tests.dict.braces.reader"):
        """
        A component with a dict trait and a string trait
        """

        # a map of strings, whose default is not empty, so an empty map is told apart from it
        selection = pyre.properties.kv(default={"band": "S"})
        # and a string, which reads braces the way the entries of the map should
        label = pyre.properties.str()

    # load the configuration files
    pyre.loadConfiguration("component_dict_braces.pfg")
    pyre.loadConfiguration("component_dict_braces.yaml")
    # and process a command line
    commandline = [
        # an empty map
        "--cmdempty.selection={}",
        # a value that holds braces
        "--cmdkeys.selection.band={{L}}",
    ]
    # by parsing it
    events = pyre.config.newCommandLineParser().parse(commandline)
    # and processing the assignments it holds
    pyre.executive.configurator.processEvents(
        events=events, priority=pyre.executive.priority.command
    )

    # the empty maps
    for name in ("pfgempty", "yamlempty", "cmdempty"):
        # are empty
        assert dict(Reader(name=name).selection) == {}, name
    # the maps whose value holds an escaped brace
    for name in ("pfgtext", "pfgkeys", "yamltext", "yamlkeys", "cmdkeys"):
        # hold a literal one
        assert dict(Reader(name=name).selection) == {"band": "{L}"}, name
    # just like the strings
    for name in ("pfgtext", "yamltext"):
        # in the same files
        assert Reader(name=name).label == "{L}", name

    # in code
    reader = Reader(name="code")
    # the text of an empty map
    reader.selection = "{}"
    # is an empty map
    assert dict(reader.selection) == {}
    # a table whose value holds an escaped brace
    reader.selection = {"band": "{{L}}"}
    # holds a literal one
    assert dict(reader.selection) == {"band": "{L}"}
    # and so does the text form of the same table
    reader.selection = "band:{{L}}"
    assert dict(reader.selection) == {"band": "{L}"}
    # and a key set by itself
    reader.selection["band"] = "{{S}}"
    assert dict(reader.selection) == {"band": "{S}"}
    # just like a string
    reader.label = "{{L}}"
    assert reader.label == "{L}"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
