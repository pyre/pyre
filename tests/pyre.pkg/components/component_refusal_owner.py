#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A refused value is attributed to the component or class that owns the trait; one whose slots
are not in the store, an instance without a name or a class without a family, is named in the
complaint along with where it was made
"""


def test() -> None:
    """
    Give the traits of named, nameless and familyless configurables values they refuse, and
    check whom each refusal names
    """
    # externals
    import os

    # support
    import journal
    import pyre
    from pyre.components.exceptions import TraitValueError

    # a component with a family
    class Probe(pyre.component, family="pyre.tests.components.owner.probe"):
        """
        A component whose slots are in the store when it has a name
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

    # a component without a family
    class Bare(pyre.component):
        """
        A component whose class slots are not in the store
        """

        # an int
        i = pyre.properties.int()
        i.default = 0
        i.doc = "an int"

    # the name of this file, which is where the configurables are made
    here = os.path.basename(__file__)
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.components.owner")

    # a named instance, a nameless one, a class with a family, and one without
    named = Probe(name="probe")
    nameless = Probe()
    # the refusals, as the configurable, and the text its complaint must contain
    cases = [
        (named, ["probe.i", here]),
        (nameless, ["'i' of an instance of 'pyre.tests.components.owner.probe', built at", here]),
        (Probe, ["pyre.tests.components.owner.probe.i"]),
        (Bare, ["'i' of component 'Bare', declared at", here]),
    ]
    # go through them
    for configurable, expected in cases:
        # give the trait a value it refuses
        configurable.i = [1, 2]
        # carefully
        try:
            # read it
            configurable.i
        # it must be refused
        except TraitValueError as error:
            # get the complaint
            complaint = str(error)
            # find what it leaves out
            missing = [text for text in expected if text not in complaint]
            # if anything, or if the refusal does not know its owner
            if missing or error.configurable is not configurable:
                # say what went wrong
                channel.line(f"the refusal by {configurable} is not attributed to it")
                # and the details
                channel.indent()
                channel.line(f"error: {complaint}")
                channel.line(f"lacks: {', '.join(map(repr, missing))}")
                channel.line(f"owner: {error.configurable}")
                channel.line("look in: traits/Slotted.py, components/exceptions.py")
                channel.outdent()
        # if it is not refused at all
        else:
            # say so
            channel.line(f"{configurable} accepted [1, 2]")
        # restore the value, so the instances made later are not refused
        configurable.i = 0

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
