#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A dict with an entry set to a macro that refers to a name nobody defines fails to resolve it
(ints:E9)
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
    from pyre.calc.exceptions import UnresolvedNodeError

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
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_unresolved.yaml")
    # read it the way the configurator does
    with open(path) as stream:
        # and show each event as the setting it makes
        made = [
            f"{'.'.join(event.key)} <- {event.value!r}"
            for event in Parser().parse(uri=path, stream=stream, locator=None)
        ]
    # what the yaml reader must make of it
    expected = ["probe.ints <- {'b': '{x}'}"]
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
    # building the component and reading the trait must fail, since the macro names x, which
    # nobody defines
    try:
        # build the component
        probe = Probe(name="probe")
        # and read the trait
        held = probe.ints
    # if the setting is refused the right way
    except UnresolvedNodeError as error:
        # get the complaint
        complaint = str(error)
        # find what it leaves out
        missing = [text for text in ["'x'"] if text not in complaint]
        # if anything
        if missing:
            # say what went wrong
            channel.line("the dict refused the setting, but its error is incomplete")
            # and the details
            channel.indent()
            channel.line(f"error: {complaint}")
            channel.line(f"lacks: {', '.join(map(repr, missing))}")
            channel.line("look in: calc/Expression.py")
            channel.outdent()
    # if it is refused some other way
    except pyre.PyreError as error:
        # say what went wrong
        channel.line("the dict refused the setting with the wrong error")
        # and the details
        channel.indent()
        channel.line("expected: UnresolvedNodeError")
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
    # if it is not refused at all
    else:
        # say what went wrong
        channel.line("the dict accepted the setting")
        # and the details
        channel.indent()
        channel.line("expected: UnresolvedNodeError")
        channel.line(f"holds: {held!r}")
        channel.line("look in: calc/Expression.py")
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
