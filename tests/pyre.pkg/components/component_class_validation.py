#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the trait defaults get validated properly
"""


def test():
    import pyre

    # declare a component
    class raw(pyre.component):
        """the base component"""

        number = pyre.properties.int(default=1)
        number.validators = pyre.constraints.isGreater(value=0)

    # and another that assigns the validators in an iterable
    class canonical(pyre.component):
        """the base component"""

        number = pyre.properties.int(default=1)
        number.validators = (pyre.constraints.isGreater(value=0),)

    # make an illegal assignment
    raw.number = 0
    # attempting to
    try:
        # reading it should throw an exception
        raw.number
        # so this statement should be unreachable
        assert False
    # if the error got detected properly
    except raw.TraitValueError:
        # all good
        pass

    # another illegal assignment
    canonical.number = 0
    # attempting to
    try:
        # reading this value should also raise an exception
        canonical.number
        # so this statement should be unreachable
        assert False
    # if the error got detected properly
    except canonical.TraitValueError:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
