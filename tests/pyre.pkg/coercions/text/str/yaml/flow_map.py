#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A str set to a non-empty flow map refuses it, with an error that names the trait (s:E3, R4)
"""


def test() -> None:
    """
    Check what the yaml reader makes of the setting, then how the trait refuses it
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
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flow_map.yaml")
    # read it the way the configurator does
    with open(path) as stream:
        # and show each event as the setting it makes
        made = [
            f"{'.'.join(event.key)} <- {event.value!r}"
            for event in Parser().parse(uri=path, stream=stream, locator=None)
        ]
    # what the yaml reader must make of it
    expected = ["probe.s <- {'k': 'v'}"]
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
    # building the component and reading the trait must fail, since no scalar accepts a non-
    # empty map
    try:
        # build the component
        probe = Probe(name="probe")
        # and read the trait
        held = probe.s
    # if the setting is refused the right way
    except pyre.PyreError as error:
        # get the complaint
        complaint = str(error)
        # find what it leaves out
        missing = [text for text in ["probe.s"] if text not in complaint]
        # if anything
        if missing:
            # say what went wrong
            channel.line("the str refused the setting, but its error is incomplete")
            # and the details
            channel.indent()
            channel.line(f"error: {complaint}")
            channel.line(f"lacks: {', '.join(map(repr, missing))}")
            channel.line("look in: traits/Property.py")
            channel.outdent()
    # if it is not refused at all
    else:
        # say what went wrong
        channel.line("the str accepted the setting")
        # and the details
        channel.indent()
        channel.line("expected: an error")
        channel.line(f"holds: {held!r}")
        channel.line("look in: traits/Property.py")
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
