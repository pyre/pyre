#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that {choices}, a dict of sets, takes whole tables and sets one key at a time
"""


def test() -> None:
    """
    Fill a table of choices in the ways a client can
    """
    # support
    import pyre

    # a component with a table of choices
    class Picker(pyre.component, family="pyre.tests.dict.choices.picker"):
        """
        A component with a table of choices
        """

        # the legal values of each axis
        axes = pyre.properties.choices()

    # a table of choices is a dict of sets of strings
    assert Picker.pyre_trait("axes").type == "dict[set[str]]"

    # make a picker
    picker = Picker(name="picker")
    # it starts out empty
    assert dict(picker.axes) == {}
    # assign a whole table
    picker.axes = {"band": ["L", "S", "L"], "frequency": ("A",)}
    # and its values become sets
    assert dict(picker.axes) == {"band": {"L", "S"}, "frequency": {"A"}}
    # set the choices of one key from their text form
    picker.axes["polarization"] = "HH, HV, HH"
    # and they become a set
    assert picker.axes["polarization"] == {"HH", "HV"}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
