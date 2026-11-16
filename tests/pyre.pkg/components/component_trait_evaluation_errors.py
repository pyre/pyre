#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A pyre error raised while the value of a trait is computed, such as the failed evaluation of
an expression, refuses the value with a {TraitValueError} that names the trait and carries the
error; errors that are not pyre's go through as they are; the configuration check records the
refusals
"""


def test() -> None:
    """
    Give the traits of a component values whose computation fails, and read them
    """
    # support
    import journal
    import pyre
    from pyre.calc.exceptions import EvaluationError, UnresolvedNodeError
    from pyre.components.exceptions import TraitValueError

    # a validator that is not pyre's
    def odd(value, **kwds) -> int:
        """
        Refuse even numbers with an error that is not pyre's
        """
        # if {value} is even
        if value % 2 == 0:
            # refuse it
            raise ValueError(f"{value} is even")
        # otherwise, accept it
        return value

    # a component with a family
    class Probe(pyre.component, family="pyre.tests.components.evaluation.probe"):
        """
        A component with traits whose values are expressions
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

        # another
        j = pyre.properties.int()
        j.default = 0
        j.doc = "another int"

        # one with a validator that is not pyre's
        k = pyre.properties.int()
        k.default = 1
        k.validators = odd
        k.doc = "an odd int"

    # the refusals are logged as they are recorded; keep the log out of the way
    journal.warning("pyre.configuration").device = journal.trash()
    # get the store
    nameserver = pyre.executive.nameserver
    # make a setting to refer to
    nameserver["pyre.tests.components.evaluation.x"] = "1"
    # build the component
    probe = Probe(name="probe")
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.evaluation")

    # the traits, the expressions whose computation fails, and the error each one raises
    cases = [
        ("i", "{pyre.tests.components.evaluation.nothing}", UnresolvedNodeError),
        ("j", "{pyre.tests.components.evaluation.x} / 0", EvaluationError),
    ]
    # go through them
    for name, expression, reason in cases:
        # set the trait
        setattr(probe, name, expression)
        # carefully
        try:
            # read it
            getattr(probe, name)
        # it must be refused as a value of the trait
        except TraitValueError as error:
            # with the error that refused it
            if not isinstance(error.error, reason):
                # say so
                channel.line(f"'{name}' was refused because of {error.error!r}, not {reason}")
            # naming the trait
            if f"probe.{name}" not in str(error):
                # say so
                channel.line(f"the refusal of '{name}' does not name it: {error}")
            # and knowing whose it is
            if error.configurable is not probe:
                # say so
                channel.line(f"the refusal of '{name}' is about {error.configurable}")
        # if it is refused some other way
        except pyre.PyreError as error:
            # say so
            channel.line(f"'{name}' was refused with {type(error).__name__}: {error}")
            # and the details
            channel.indent()
            channel.line("look in: traits/Slotted.py, Slotted.__get__")
            channel.outdent()
        # if it is not refused at all
        else:
            # say so
            channel.line(f"'{name}' accepted {expression!r}")

    # an even value
    probe.k = 2
    # carefully
    try:
        # read it
        probe.k
    # the validator refuses it with an error that is not pyre's
    except ValueError:
        # which must go through as it is
        pass
    # if it is refused some other way
    except pyre.PyreError as error:
        # say so
        channel.line(f"'k' was refused with {type(error).__name__}: {error}")
    # restore it, so the check below sees only the two refusals
    probe.k = 1

    # check the configuration
    refusals = probe.pyre_validateConfiguration()
    # it must record both refusals
    if len(refusals) != 2:
        # if not, say so
        channel.line(f"the check recorded {len(refusals)} refusals, not 2")
        # and the details
        channel.indent()
        # go through them
        for refusal in refusals:
            # show each one
            channel.line(f"{refusal}")
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
