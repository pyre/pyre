#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A facility set to the empty text refuses it, with an error that names the trait, the text, and
the protocol (part:E5, F12)
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

    # the protocol of the facility
    class Parts(pyre.protocol, family="pyre.coercions.components.parts"):
        """
        The protocol of the facility under study
        """

    # its default implementation
    class Part(pyre.component, family="pyre.coercions.components.parts.part", implements=Parts):
        """
        The component the facility holds unless configured otherwise
        """

        # something to configure
        s = pyre.properties.str()
        s.default = "part-default"
        s.doc = "a setting of the component the facility holds"

    # a component with a facility
    class Probe(pyre.component, family="pyre.coercions.components.facility"):
        """
        A component with a facility
        """

        # the trait under study
        part = Parts()
        part.default = Part
        part.doc = "a facility"

    # the setting
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "empty_text.yaml")
    # read it the way the configurator does
    with open(path) as stream:
        # and show each event as the setting it makes
        made = [
            f"{'.'.join(event.key)} <- {event.value!r}"
            for event in Parser().parse(uri=path, stream=stream, locator=None)
        ]
    # what the yaml reader must make of it
    expected = ["probe.part <- ''"]
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
    # building the component and reading the trait must fail, since the empty text names no
    # component
    try:
        # build the component
        probe = Probe(name="probe")
        # and read the trait
        held = probe.part
    # if the setting is refused the right way
    except Parts.ResolutionError as error:
        # get the complaint
        complaint = str(error)
        # find what it leaves out
        missing = [
            text
            for text in ["probe.part", "''", "pyre.coercions.components.parts"]
            if text not in complaint
        ]
        # if anything
        if missing:
            # say what went wrong
            channel.line("the facility refused the setting, but its error is incomplete")
            # and the details
            channel.indent()
            channel.line(f"error: {complaint}")
            channel.line(f"lacks: {', '.join(map(repr, missing))}")
            channel.line("look in: components/Protocol.py")
            channel.outdent()
    # if it is refused some other way
    except pyre.PyreError as error:
        # say what went wrong
        channel.line("the facility refused the setting with the wrong error")
        # and the details
        channel.indent()
        channel.line("expected: ResolutionError")
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
        channel.line("the facility accepted the setting")
        # and the details
        channel.indent()
        channel.line("expected: ResolutionError")
        channel.line(f"holds: {held!r}")
        channel.line("look in: components/Protocol.py")
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
