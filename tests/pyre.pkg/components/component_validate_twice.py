#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Checking a configuration again does not record again what it recorded before: a refusal of
the same slot, for the same reason, is already in the pile; a new assignment, or a value that
an expression now evaluates to differently, is a new refusal
"""


def test() -> None:
    """
    Check a misconfigured instance and class repeatedly, changing what they refuse in between
    """
    # support
    import journal
    import pyre

    # a component with a family
    class Probe(pyre.component, family="pyre.tests.components.twice.probe"):
        """
        A component with a property
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

    # a component without a family
    class Bare(pyre.component):
        """
        A component whose class is checked
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

    # get the executive
    executive = pyre.executive
    # and its store
    nameserver = executive.nameserver
    # the refusals are logged as they are recorded; keep the log out of the way
    journal.warning("pyre.configuration").device = journal.trash()
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.twice")

    # a misconfigured instance
    probe = Probe(name="probe")
    # whose trait refers to a setting that it refuses
    nameserver["pyre.tests.components.twice.x"] = "one"
    # by an expression
    probe.i = "{pyre.tests.components.twice.x}"
    # and a misconfigured class
    Bare.i = [1, 2]

    # the checks, the instance one and the class one
    checks = [
        ("probe", probe, probe.pyre_validateConfiguration),
        ("Bare", Bare, Bare.pyre_classValidateConfiguration),
    ]
    # go through them
    for name, configurable, check in checks:
        # check once
        first = check()
        # count the pile
        recorded = len(executive.errors)
        # and again
        second = check()
        # the second check must find the same refusals
        if second != first:
            # if not, say so
            channel.line(f"checking '{name}' again found other refusals")
            # and the details
            channel.indent()
            channel.line(f"first: {[str(error) for error in first]}")
            channel.line(f"second: {[str(error) for error in second]}")
            channel.line("look in: components/Component.py, Component.pyre_recordRefusal")
            channel.outdent()
        # without recording them again
        if len(executive.errors) != recorded:
            # if not, say so
            channel.line(f"checking '{name}' again recorded its refusals again")
        # and the component sees one
        if len(first) != 1 or len(executive.configurationErrors(configurable=configurable)) != 1:
            # if not, say so
            channel.line(f"'{name}' does not see exactly one refusal")

    # the setting the expression refers to changes
    nameserver["pyre.tests.components.twice.x"] = "two"
    # so the same slot refuses for another reason
    changed = probe.pyre_validateConfiguration()
    # which is a new refusal
    if (
        len(probe.pyre_configurationErrors) != 2
        or changed[0] is not probe.pyre_configurationErrors[-1]
    ):
        # if not, say so
        channel.line("a slot that refuses for another reason is not a new refusal")
        # and the details
        channel.indent()
        channel.line(f"sees: {[str(error) for error in probe.pyre_configurationErrors]}")
        channel.outdent()

    # a new assignment
    Bare.i = [3, 4]
    # is a new slot
    reassigned = Bare.pyre_classValidateConfiguration()
    # whose refusal is new
    if len(Bare.pyre_classConfigurationErrors()) != 2 or reassigned[0] is not (
        Bare.pyre_classConfigurationErrors()[-1]
    ):
        # if not, say so
        channel.line("a new assignment that is refused is not a new refusal")
        # and the details
        channel.indent()
        channel.line(f"sees: {[str(error) for error in Bare.pyre_classConfigurationErrors()]}")
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
