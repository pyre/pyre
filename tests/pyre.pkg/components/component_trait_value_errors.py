#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A trait that refuses a value raises a {TraitValueError} that names the trait, says where its
value was set, and carries the error that refused it
"""


def test() -> None:
    """
    Give the traits of a component values they refuse, and check what their errors say
    """
    # externals
    import os

    # support
    import journal
    import pyre
    from pyre.components.exceptions import ResolutionError, TraitValueError
    from pyre.constraints.exceptions import ConstraintViolationError
    from pyre.schemata.exceptions import CastingError

    # a validator that refuses odd numbers the way users are encouraged to
    def even(value, **kwds):
        """
        Refuse odd numbers with a {TraitValueError}
        """
        # odd numbers
        if value % 2:
            # are refused
            raise TraitValueError(value=value, reason="must be even")
        # everything else is fine
        return value

    # a validator that refuses large numbers with an error of its own
    def small(value, **kwds):
        """
        Refuse large numbers with a {ValueError}
        """
        # large numbers
        if value > 10:
            # are refused
            raise ValueError("too large")
        # everything else is fine
        return value

    # a protocol
    class Parts(pyre.protocol, family="pyre.tests.components.refusals.parts"):
        """
        The protocol of the facility
        """

    # its default implementation
    class Part(
        pyre.component, family="pyre.tests.components.refusals.parts.part", implements=Parts
    ):
        """
        The component the facility holds unless configured otherwise
        """

    # a component with traits that refuse values
    class Probe(pyre.component, family="pyre.tests.components.refusals.probe"):
        """
        The component under study
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

        # a positive int
        positive = pyre.properties.int()
        positive.default = 1
        positive.validators = pyre.constraints.isPositive()
        positive.doc = "a positive int"

        # an even int
        parity = pyre.properties.int()
        parity.default = 0
        parity.validators = even
        parity.doc = "an even int"

        # a small int
        size = pyre.properties.int()
        size.default = 0
        size.validators = small
        size.doc = "a small int"

        # a facility
        part = Parts()
        part.default = Part
        part.doc = "a facility"

    # the name of this file, which is where the refused values are set
    here = os.path.basename(__file__)
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.refusals")
    # build the component
    probe = Probe(name="probe")

    # the refusals, as the trait, the value, the type of the error that refused it, and the text
    # the report must contain
    cases = [
        ("i", [1, 2], CastingError, "could not coerce"),
        ("positive", -1, ConstraintViolationError, "is not greater than 0"),
        ("part", "pyre.tests.components.refusals.nowhere", ResolutionError, "could not resolve"),
        ("parity", 3, type(None), "must be even"),
    ]
    # go through them
    for trait, value, refusal, reason in cases:
        # set the trait
        setattr(probe, trait, value)
        # carefully
        try:
            # read it
            getattr(probe, trait)
        # it must be refused
        except TraitValueError as error:
            # get the complaint
            complaint = str(error)
            # find what it leaves out
            missing = [text for text in [f"probe.{trait}", here, reason] if text not in complaint]
            # if anything, or if the error that refused the value is not the expected one
            if missing or not isinstance(error.error, refusal):
                # say what went wrong
                channel.line(f"'{trait}' refused {value!r}, but its error is incomplete")
                # and the details
                channel.indent()
                channel.line(f"error: {complaint}")
                channel.line(f"lacks: {', '.join(map(repr, missing))}")
                channel.line(f"refused by: {type(error.error).__name__}")
                channel.line(f"expected: {refusal.__name__}")
                channel.line("look in: traits/SlotFactory.py, components/exceptions.py")
                channel.outdent()
        # if it is refused some other way
        except pyre.PyreError as error:
            # say what went wrong
            channel.line(f"'{trait}' refused {value!r} with the wrong error")
            # and the details
            channel.indent()
            channel.line(f"error: {type(error).__name__}: {error}")
            channel.line("look in: traits/SlotFactory.py")
            channel.outdent()
        # if it is not refused at all
        else:
            # say so
            channel.line(f"'{trait}' accepted {value!r}")

    # a validator that raises an error of its own
    probe.size = 11
    # carefully
    try:
        # read it
        probe.size
    # must see its error unchanged
    except ValueError as error:
        # unless its text is lost
        if str(error) != "too large":
            # in which case, say so
            channel.line(f"'size' refused 11 with an altered error: {error}")
    # if it is refused some other way
    except pyre.PyreError as error:
        # say what went wrong
        channel.line(f"'size' refused 11 with {type(error).__name__}, not ValueError: {error}")
    # if it is not refused at all
    else:
        # say so
        channel.line("'size' accepted 11")

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
