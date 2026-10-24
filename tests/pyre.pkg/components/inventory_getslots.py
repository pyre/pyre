#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an inventory that does not know how to reach its slots says which class must implement
the access
"""


def test() -> None:
    """
    Ask the base inventory for its slots
    """
    # access the inventory base class
    from pyre.components.Inventory import Inventory

    # make one
    inventory = Inventory()
    # attempt to
    try:
        # get its slots
        inventory.getSlots()
        # which should be unreachable
        assert False, "unreachable"
    # if it fails as expected
    except NotImplementedError as error:
        # check that the message names the class
        assert str(error) == "class 'Inventory' must implement 'getSlots'"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
