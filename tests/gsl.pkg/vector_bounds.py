#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that indices crossing into a vector are reflected and bounds-checked, so out of range
access raises {IndexError} rather than leaning on gsl's optional range check
"""


def raises(fn):
    """
    Return True if calling {fn} raises {IndexError}
    """
    # try the call
    try:
        # which is expected to fail
        fn()
    # if it raises the right thing
    except IndexError:
        # good
        return True
    # otherwise it did not guard
    return False


def test():
    # get the package
    import gsl

    # a vector with a known pattern
    v = gsl.vector(shape=5).fill(3.0)
    v[1] = 7.0

    # a negative index counts from the end
    assert v[-1] == v[4]
    assert v[-5] == v[0]
    assert v[-4] == v[1] == 7.0

    # reading or writing past the end raises, through the subscript and the raw accessors
    assert raises(lambda: v[5])
    assert raises(lambda: v.get(5))
    assert raises(lambda: v.__setitem__(5, 1.0))
    assert raises(lambda: v.set(5, 1.0))

    # a too-negative index raises rather than reflecting to a still-negative slot
    assert raises(lambda: v[-6])
    assert raises(lambda: v.get(-6))

    # the basis constructor checks its index too
    assert raises(lambda: v.basis(5))
    assert raises(lambda: v.basis(-6))

    # swap checks both of its indices, reflecting a negative one and raising past either edge
    assert raises(lambda: v.swap(0, 5))
    assert raises(lambda: v.swap(5, 0))
    assert raises(lambda: v.swap(0, -6))

    # and a valid basis index still works, including a reflected one
    assert v.clone().basis(-1)[4] == 1.0

    # accessing the very edges is fine
    assert v[0] == 3.0 and v[4] == 3.0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
