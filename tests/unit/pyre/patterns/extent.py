#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that extent awareness tracks the extent of classes correctly
"""
    

from pyre.patterns.ExtentAware import ExtentAware

class base(metaclass=ExtentAware):
    """base"""

class derived(base):
    """derived"""


def create_instances():
    """build some instances"""

    b1 = base()
    b2 = base()
    d1 = derived()
    d2 = derived()

    # print("b1:", b1)
    # print("b2:", b2)
    # print("d1:", d1)
    # print("d2:", d2)
    # print({ref for ref in base._pyre_extent})
    # print({ref for ref in derived._pyre_extent})
    assert set(base._pyre_extent) == { b1, b2, d1, d2 }
    assert set(derived._pyre_extent) == { d1, d2 }

    return


def test():
    # make some instances
    create_instances()

    # verify that they were destroyed when they went out of scope
    # print(set(base._pyre_extent))
    # print(set(derived._pyre_extent))
    assert set(base._pyre_extent) == set()
    assert set(derived._pyre_extent) == set()

    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
