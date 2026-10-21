#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The executive checks the configuration of every class and instance it knows, and shows the
errors it has recorded and the configuration files it guessed at and did not find; it calls
none of these on its own
"""


def test() -> None:
    """
    Misconfigure a class and an instance, check everything, and look at the reports
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

    # get the executive
    executive = pyre.executive
    # capture the warnings about configuration errors
    warnings = Capture()
    # by sending them to my device
    journal.warning("pyre.configuration").device = warnings
    # the reports of configuration errors
    reports = Capture()
    # by sending them to my device too
    journal.info("pyre.configuration").device = reports
    # and the reports of the guesses
    candidates = Capture()
    # likewise
    journal.info("pyre.configuration.candidates").device = candidates
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.framework.validate")

    # nothing pyre builds while booting is misconfigured
    clean = executive.validateConfiguration()
    # so the pile is empty
    if clean:
        # if not, say so
        channel.line("checking right after booting found errors")
        # and the details
        channel.indent()
        channel.report(report=(f"{type(error).__name__}: {error}" for error in clean))
        channel.line("look in: framework/Executive.py, Executive.validateConfiguration")
        channel.outdent()
    # booting must not have shown anything
    if warnings.pages or reports.pages or candidates.pages:
        # if not, say so
        channel.line("booting or checking showed something")

    # a class without a family
    class Bare(pyre.component):
        """
        A component whose class slots are not in the store
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

    # a class with a family
    class Probe(pyre.component, family="pyre.tests.framework.validate.probe"):
        """
        A component whose instances are checked
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

    # misconfigure the class
    Bare.i = [1, 2]
    # build an instance
    probe = Probe(name="probe")
    # and misconfigure it
    probe.i = [3, 4]

    # check everything
    pile = executive.validateConfiguration()
    # it must be the pile
    if pile is not executive.errors:
        # if not, say so
        channel.line("the check does not return the pile")
    # whom the refusals in it are attributed to
    owners = [error.configurable for error in pile if isinstance(error, TraitValueError)]
    # must be the class and the instance, each once
    if sorted(map(str, owners)) != sorted(map(str, [Bare, probe])):
        # if not, say what went wrong
        channel.line("the check did not find the two refusals, each once")
        # and the details
        channel.indent()
        channel.report(report=(f"{type(error).__name__}: {error}" for error in pile))
        channel.line("look in: framework/Executive.py, Executive.validateConfiguration")
        channel.outdent()
    # the class sees its own
    if [error.configurable for error in Bare.pyre_classConfigurationErrors()] != [Bare]:
        # if not, say so
        channel.line(f"'Bare' sees: {Bare.pyre_classConfigurationErrors()}")

    # show the pile
    executive.showConfigurationErrors()
    # it must be one report
    if len(reports.pages) != 1:
        # if not, say so
        channel.line(f"the executive wrote {len(reports.pages)} reports of errors")
    # that mentions both refusals
    elif "'i' of component 'Bare'" not in reports.pages[0] or "probe.i" not in reports.pages[0]:
        # if not, say so
        channel.line(f"the report of errors is wrong: {reports.pages[0]!r}")

    # show the guesses
    executive.showConfigurationCandidates()
    # it must be one report
    if len(candidates.pages) != 1:
        # if not, say so
        channel.line(f"the executive wrote {len(candidates.pages)} reports of guesses")
    # that lists every one of them
    elif any(str(guess.uri) not in candidates.pages[0] for guess in executive.guesses):
        # if not, say so
        channel.line(f"the report of guesses is incomplete: {candidates.pages[0]!r}")

    # a caller that has opinions about where the reports go
    elsewhere = Capture()
    # makes a channel of its own
    destination = journal.info("pyre.tests.framework.validate.destination")
    # and sends it to my device
    destination.device = elsewhere
    # show the pile there
    executive.showConfigurationErrors(channel=destination)
    # and the guesses
    executive.showConfigurationCandidates(channel=destination)
    # both must have landed there, and nowhere else
    if len(elsewhere.pages) != 2 or len(reports.pages) != 1 or len(candidates.pages) != 1:
        # if not, say so
        channel.line("the reports did not go to the channel they were given")
        # and the details
        channel.indent()
        channel.line(f"given: {len(elsewhere.pages)} reports, expected 2")
        channel.line(f"default: {len(reports.pages) + len(candidates.pages)} reports, expected 2")
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
