#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise value updates for slots
"""

def test():
    # get the constructor
    from pyre.config.Slot import Slot
    # build a few slots
    one = Slot.variable(value=1)
    two = Slot.variable(value=2)
    var = Slot.variable()

    three = one + two
    double = var + var

    # check that {var} has no value
    assert var.value is None
    # set it to {two)
    var.setValue(two)
    # this is supposed to happen via simple value transfer
    # so check that the cache has the right value
    assert var._value == 2
    # and that {var} knows it
    assert var.value == 2
    # and that double got updated
    assert double.value == 2 * var.value

    # verify {three} can compute correctly
    assert three.value == 3

    # now, replace {var} by {three} in {double}
    double.substitute(current=var, replacement=three)

    # check all expected invariants
    # operands
    assert len(one.operands) == 0
    assert len(two.operands) == 0
    assert len(var.operands) == 0
    assert len(three.operands) == 2
    assert identical(three.operands, [one, two])
    assert len(double.operands) == 2
    assert identical(double.operands, [three, three])

    # observers
    assert len(one.observers) == 1
    assert identical((ref() for ref in one.observers), [three])
    assert len(two.observers) == 1
    assert identical((ref() for ref in two.observers), [three])
    assert len(var.observers) == 0
    assert len(three.observers) == 1
    assert identical((ref() for ref in three.observers), [double])
    assert len(double.observers) == 0

    # all done
    return var, double


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
