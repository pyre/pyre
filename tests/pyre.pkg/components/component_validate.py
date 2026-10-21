#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A component checks its configuration by reading every trait, its facilities included, and
records the values they refuse instead of raising them; it can show what it has recorded
"""


def test() -> None:
    """
    Misconfigure a component and its facility, check them, and look at what is recorded
    """
    # support
    import journal
    import pyre
    from pyre.components.exceptions import TraitValueError

    # a device that keeps the pages of the entries it receives
    class Capture(journal.device):
        """
        Keep the entries instead of showing them
        """

        # meta-methods
        def __init__(self, **kwds):
            # chain up
            super().__init__(name="capture", **kwds)
            # nothing received yet
            self.pages = []
            # all done
            return

        # interface
        def alert(self, entry):
            """
            Keep a user facing entry
            """
            # keep its page
            self.pages.append("\n".join(entry.page))
            # all done
            return self

        def memo(self, entry):
            """
            Keep a developer facing entry
            """
            # keep its page
            self.pages.append("\n".join(entry.page))
            # all done
            return self

        def help(self, entry):
            """
            Keep a help screen
            """
            # keep its page
            self.pages.append("\n".join(entry.page))
            # all done
            return self

    # the protocol of the facility
    class Parts(pyre.protocol, family="pyre.tests.components.validate.parts"):
        """
        The protocol of the facility
        """

    # its default implementation
    class Part(
        pyre.component, family="pyre.tests.components.validate.parts.part", implements=Parts
    ):
        """
        The component the facility holds
        """

        # an int
        n = pyre.properties.int()
        n.default = 0
        n.doc = "an int"

    # the component under study
    class Probe(pyre.component, family="pyre.tests.components.validate.probe"):
        """
        A component with a property and a facility
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

        # a str
        s = pyre.properties.str()
        s.default = "fine"
        s.doc = "a str"

        # a facility
        part = Parts()
        part.default = Part
        part.doc = "a facility"

    # get the executive
    executive = pyre.executive
    # capture the warnings about configuration errors
    warnings = Capture()
    # by sending them to my device
    journal.warning("pyre.configuration").device = warnings
    # and the reports of configuration errors
    reports = Capture()
    # by sending them to my device too
    journal.info("pyre.configuration").device = reports
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.validate")

    # a component that is configured correctly
    fine = Probe(name="fine")
    # has nothing to say
    if fine.pyre_validateConfiguration():
        # if it does, say so
        channel.line(f"'fine' found errors: {fine.pyre_validateConfiguration()}")

    # a component that is not
    probe = Probe(name="probe")
    # give it a value it refuses
    probe.i = [1, 2]
    # and its facility one too
    probe.part.n = [3, 4]
    # carefully
    try:
        # check it
        found = probe.pyre_validateConfiguration()
    # the check must not raise
    except pyre.PyreError as error:
        # say so
        channel.line(f"checking 'probe' raised {type(error).__name__}: {error}")
        # and pretend it found nothing
        found = []
    # the refusals it must have found, by the traits they name
    named = [error.trait for error in found if isinstance(error, TraitValueError)]
    # if they are not the two
    if sorted(named) != ["probe.i", "probe.part.n"]:
        # say what went wrong
        channel.line("checking 'probe' did not find the two refusals")
        # and the details
        channel.indent()
        channel.line(f"found: {[str(error) for error in found]}")
        channel.line("look in: components/Component.py, Component.pyre_validateConfiguration")
        channel.outdent()
    # each must be in the pile
    for error in found:
        # if one is not
        if error not in executive.errors:
            # say so
            channel.line(f"a refusal is not in the pile: {error}")
    # the component sees its own
    if [error.trait for error in probe.pyre_configurationErrors] != ["probe.i"]:
        # if not, say so
        channel.line(f"'probe' sees: {[str(error) for error in probe.pyre_configurationErrors]}")
    # and so does its facility
    if [error.trait for error in probe.part.pyre_configurationErrors] != ["probe.part.n"]:
        # if not, say so
        channel.line(
            f"'probe.part' sees: {[str(error) for error in probe.part.pyre_configurationErrors]}"
        )
    # each refusal must have been logged as it was recorded
    for trait in ["probe.i", "probe.part.n"]:
        # if not
        if not any(trait in page for page in warnings.pages):
            # say so
            channel.line(f"the refusal of '{trait}' was not logged")

    # show what the component recorded
    probe.pyre_showConfigurationErrors()
    # it must be one report
    if len(reports.pages) != 1:
        # if not, say so
        channel.line(f"'probe' wrote {len(reports.pages)} reports")
    # that mentions its refusal
    elif "probe.i" not in reports.pages[0] or "probe.part.n" in reports.pages[0]:
        # if not, say so
        channel.line(f"the report of 'probe' is wrong: {reports.pages[0]!r}")

    # a caller that has opinions about where the report goes
    elsewhere = Capture()
    # makes a channel of its own
    destination = journal.info("pyre.tests.components.validate.destination")
    # and sends it to my device
    destination.device = elsewhere
    # show what the component recorded there
    probe.pyre_showConfigurationErrors(channel=destination)
    # it must have landed there, and nowhere else
    if len(elsewhere.pages) != 1 or len(reports.pages) != 1:
        # if not, say so
        channel.line("the report of 'probe' did not go to the channel it was given")

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
