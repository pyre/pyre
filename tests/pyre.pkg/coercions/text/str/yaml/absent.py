#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A str that nothing configures holds its default (s:E1)
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

    # a component with a str
    class Probe(pyre.component, family="pyre.coercions.text.str"):
        """
        A component with a str
        """

        # the trait under study
        s = pyre.properties.str()
        s.default = "c-default"
        s.doc = "a str"

    # the setting
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "absent.yaml")
    # read it the way the configurator does
    with open(path) as stream:
        # and show each event as the setting it makes
        made = [
            f"{'.'.join(event.key)} <- {event.value!r}"
            for event in Parser().parse(uri=path, stream=stream, locator=None)
        ]
    # what the yaml reader must make of it
    expected = ["other <- 1"]
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
    # what the trait must hold: the default
    expected = "c-default"
    # carefully
    try:
        # build the component
        probe = Probe(name="probe")
        # and read the trait
        held = probe.s
    # if anything is refused
    except pyre.PyreError as error:
        # say what went wrong
        channel.line("the str raised an error instead of holding a value")
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
        # if it holds something else
        if held != expected:
            # say what went wrong
            channel.line("the str holds the wrong value")
            # and the details
            channel.indent()
            channel.line(f"expected: {expected!r}")
            channel.line(f"holds: {held!r}")
            channel.line("look in: schemata/String.py")
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
