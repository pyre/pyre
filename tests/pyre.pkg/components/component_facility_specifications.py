#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A facility reads its specification with the blanks around the marker of the instance name
dropped, and honors the {#name} shorthand for an instance of its default
"""


def test() -> None:
    """
    Set a facility to specifications that name an instance, and check what it holds
    """
    # support
    import journal
    import pyre

    # a protocol
    class Parts(pyre.protocol, family="pyre.tests.components.specifications.parts"):
        """
        The protocol of the facility
        """

    # its default implementation
    class Part(
        pyre.component, family="pyre.tests.components.specifications.parts.part", implements=Parts
    ):
        """
        The component the facility holds unless configured otherwise
        """

    # a component with a facility
    class Probe(pyre.component, family="pyre.tests.components.specifications.probe"):
        """
        The component under study
        """

        # a facility with a default of its own
        part = Parts()
        part.default = Part
        part.doc = "a facility"

    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.specifications")

    # the specifications, and the name of the instance each must make
    cases = [
        ("pyre.tests.components.specifications.parts.part # mine", "mine"),
        ("pyre.tests.components.specifications.parts.part#ours", "ours"),
        ("#yours", "yours"),
        ("  #  theirs  ", "theirs"),
    ]
    # go through them
    for spec, name in cases:
        # build a fresh component
        probe = Probe(name=f"probe-{name}")
        # set its facility
        probe.part = spec
        # carefully
        try:
            # read it
            part = probe.part
        # if it is refused
        except pyre.PyreError as error:
            # say what went wrong
            channel.line(f"the facility refused {spec!r}")
            # and the details
            channel.indent()
            channel.line(f"error: {type(error).__name__}: {error}")
            channel.line("look in: framework/Executive.py, schemata/Component.py")
            channel.outdent()
            # and move on
            continue
        # if it holds something other than an instance of its default with the right name
        if not isinstance(part, Part) or part.pyre_name != name:
            # say what went wrong
            channel.line(f"the facility misread {spec!r}")
            # and the details
            channel.indent()
            channel.line(f"expected: a Part named {name!r}")
            channel.line(f"holds: {part!r}, named {getattr(part, 'pyre_name', None)!r}")
            channel.line("look in: framework/Executive.py, schemata/Component.py")
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
