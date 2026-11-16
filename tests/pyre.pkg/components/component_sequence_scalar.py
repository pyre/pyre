#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A sequence trait given a value that is neither a sequence nor text takes it, and refuses it
when it is read, with an error that names the trait
"""


def test() -> None:
    """
    Give each kind of sequence trait a number, and read it back
    """
    # support
    import journal
    import pyre
    from pyre.components.exceptions import TraitValueError

    # a component with a trait of each kind of sequence
    class Probe(pyre.component, family="pyre.tests.components.sequence.scalar"):
        """
        A component with sequences
        """

        # a list
        list = pyre.properties.list(schema=pyre.properties.str())
        list.doc = "a list of str"

        # a set
        set = pyre.properties.set(schema=pyre.properties.str())
        set.doc = "a set of str"

        # a tuple
        tuple = pyre.properties.tuple(schema=pyre.properties.str())
        tuple.doc = "a tuple of str"

        # an array
        array = pyre.properties.array()
        array.doc = "an array"

    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.sequence")
    # build the component
    probe = Probe(name="probe")

    # go through the sequences
    for trait in ["list", "set", "tuple", "array"]:
        # carefully
        try:
            # give it a number
            setattr(probe, trait, 5)
        # the assignment must succeed
        except pyre.PyreError as error:
            # if not, say so
            channel.line(f"'{trait}' refused 5 when it was assigned: {type(error).__name__}")
            # and the details
            channel.indent()
            channel.line(f"error: {error}")
            channel.line("look in: traits/Property.py, Property.sequences.native")
            channel.outdent()
            # and move on
            continue
        # carefully
        try:
            # read it
            held = getattr(probe, trait)
        # it must be refused, by name
        except TraitValueError as error:
            # unless its complaint does not name the trait
            if f"probe.{trait}" not in str(error):
                # in which case, say so
                channel.line(f"the refusal of 5 by '{trait}' does not name it: {error}")
        # if it is refused some other way
        except pyre.PyreError as error:
            # say so
            channel.line(f"'{trait}' refused 5 with {type(error).__name__}: {error}")
        # if it is not refused at all
        else:
            # say so
            channel.line(f"'{trait}' accepted 5 as {held!r}")

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
