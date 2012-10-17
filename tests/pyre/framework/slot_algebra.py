#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Check the slot algebra
"""

def test():
    # get the constructor
    from pyre.config.Slot import Slot
    # build a few slots
    zero = Slot.variable(value=0)
    one = Slot.variable(value=1)
    two = Slot.variable(value=2)
    # verify their values
    assert zero.value == 0
    assert one.value == 1
    assert two.value == 2

    # add them
    s = one + two
    # check that the new slot has an invalid cache
    assert s._value is None
    # force it to evaluate
    assert s.value == 3
    # check that the cache has been updated properly
    assert s._value == 3

    # check that variables have no operands
    assert len(zero.operands) == 0
    assert len(one.operands) == 0
    assert len(two.operands) == 0
    # check that {zero} has no observers
    assert len(zero.observers) == 0
    # but {one} and {two} have one each
    assert len(one.observers) == 1
    assert len(two.observers) == 1
    # the right one
    assert identical((ref() for ref in one.observers), [s])
    assert identical((ref() for ref in two.observers), [s])
    
    # check that {s} has two operands
    assert len(s.operands) == 2
    assert identical(s.operands, [one, two])

    # all done
    return zero, one, two, s


def identical(s1, s2):
    """
    Verify that the nodes in {s1} and {s2} are identical. This has to be done carefully since
    we must avoid triggering __eq__
    """
    # for the pairs
    for n1, n2 in zip(s1, s2):
        # check them for _identity_, not _equality_
        if n1 is not n2: return False
    # all done
    return True
            

# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
