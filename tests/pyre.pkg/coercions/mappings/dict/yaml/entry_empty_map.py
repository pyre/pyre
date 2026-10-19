#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A dict leaves out an entry it cannot convert, and records it against the instance (ints:E8,
decision A)
"""


def test() -> None:
    """
    Check what the yaml reader makes of the setting, then what the trait holds
    """
    # externals
    import os
    import traceback

    # support
    import journal
    import pyre
    from pyre.config.yaml.Parser import Parser

    # a component with a dict of int
    class Probe(pyre.component, family="pyre.coercions.mappings.dict"):
        """
        A component with a dict of int
        """

        # the trait under study
        ints = pyre.properties.dict(schema=pyre.properties.int())
        ints.default = {"a": 1}
        ints.doc = "a dict of int"

    # the setting
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_empty_map.yaml")
    # read it the way the configurator does
    with open(path) as stream:
        # and show each event as the setting it makes
        made = [
            f"{'.'.join(event.key)} <- {event.value!r}"
            for event in Parser().parse(uri=path, stream=stream, locator=None)
        ]
    # what the yaml reader must make of it
    expected = ["probe.ints <- {'b': {}}"]
    # if it made something else
    if made != expected:
        # make a channel
        channel = journal.firewall("pyre.coercions")
        # say what went wrong
        channel.line("the yaml reader misread the setting")
        # and the details
        channel.indent()
        channel.line(f"in: {path}")
        channel.line(f"expected: {expected}")
        channel.line(f"made: {made}")
        channel.line("look in: config/yaml/Parser.py, Parser.harvest")
        channel.outdent()
        # and complain
        channel.log()

    # load the setting
    pyre.loadConfiguration(path)
    # make a channel for what goes wrong from here on; it fires only after any error is
    # handled, so the report is not buried under the traceback it explains
    channel = journal.firewall("pyre.coercions")
    # what the trait must hold: the good entries, since an empty map is not an int
    expected = {}
    # carefully
    try:
        # build the component
        probe = Probe(name="probe")
        # and read the trait
        held = probe.ints
    # if anything is refused
    except pyre.PyreError as error:
        # say what went wrong
        channel.line("the dict raised an error instead of holding a value")
        # and the details
        channel.indent()
        channel.line(f"expected: {expected!r}")
        channel.line(f"got: {type(error).__name__}: {error}")
        # and where it was raised, as far as four frames out inside pyre
        channel.line("raised:")
        channel.indent()
        # go through the frames inside pyre, innermost first
        for frame in [
            frame
            for frame in reversed(traceback.extract_tb(error.__traceback__))
            if "/packages/pyre/" in frame.filename
        ][:4]:
            # the file, relative to the package
            where = frame.filename.split("/packages/pyre/")[-1]
            # one per line, with the line and the function
            channel.line(f"{where}:{frame.lineno} in {frame.name}")
        # done with the frames
        channel.outdent()
        # and with the details
        channel.outdent()
    # otherwise
    else:
        # as a plain dict
        held = held if held is None else dict(held)
        # if it holds something else
        if held != expected:
            # say what went wrong
            channel.line("the dict holds the wrong value")
            # and the details
            channel.indent()
            channel.line(f"expected: {expected!r}")
            channel.line(f"holds: {held!r}")
            channel.line("look in: traits/Dict.py")
            channel.outdent()
        # gather what was recorded against the instance
        said = "\n".join(str(entry) for entry in probe.pyre_configurationErrors)
        # find what it leaves out
        missing = [text for text in ["probe.ints.b"] if text not in said]
        # if anything
        if missing:
            # say what went wrong
            channel.line("the dict did not record the bad entry against the instance")
            # and the details
            channel.indent()
            channel.line(f"recorded: {said!r}")
            channel.line(f"lacks: {', '.join(map(repr, missing))}")
            channel.line("look in: schemata/Mapping.py")
            channel.outdent()

    # if anything went wrong
    if channel.page:
        # complain
        channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
