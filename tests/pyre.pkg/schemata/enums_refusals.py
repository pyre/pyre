#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
An enum refuses a name and a value that belong to none of its members, and its complaint names
the members
"""


def test() -> None:
    """
    Give an enum a name and a value it must refuse, and check the complaint
    """
    # support
    import enum
    import pyre

    # a few colors
    class color(enum.Enum):
        """
        The members of the enum
        """

        # one member
        red = 1
        # and another
        green = 2

    # make an enum schema
    schema = pyre.schemata.enum(enum=color)

    # the members are accepted by their names
    assert schema.coerce(value="green") is color.green
    # and by their values
    assert schema.coerce(value=1) is color.red

    # a name and a value of no member
    for value in ["blue", 3]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.EnumError as error:
            # with a complaint that names the members
            assert str(error) == f"could not coerce {value!r} into one of 'red', 'green'", str(
                error
            )
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
