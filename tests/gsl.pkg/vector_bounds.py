#!/usr/bin/env python3
# -*- python -*-
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

    # a vector with a known pattern: all threes
    v = gsl.vector(shape=5).fill(3.0)
    # except for one cell
    v[1] = 7.0

    # a negative index counts from the end: the last cell
    assert v[-1] == v[4]
    # the first
    assert v[-5] == v[0]
    # and the odd one
    assert v[-4] == v[1] == 7.0

    # reading past the end raises, through the subscript
    assert raises(lambda: v[5])
    # and through the raw accessor
    assert raises(lambda: v.get(5))
    # and so does writing, through the subscript
    assert raises(lambda: v.__setitem__(5, 1.0))
    # and through the raw accessor
    assert raises(lambda: v.set(5, 1.0))

    # a too-negative index raises rather than reflecting to a still-negative slot, through the
    # subscript
    assert raises(lambda: v[-6])
    # and through the raw accessor
    assert raises(lambda: v.get(-6))

    # the basis constructor checks its index too, past the end
    assert raises(lambda: v.basis(5))
    # and before the beginning
    assert raises(lambda: v.basis(-6))

    # swap checks its second index past the end
    assert raises(lambda: v.swap(0, 5))
    # its first
    assert raises(lambda: v.swap(5, 0))
    # and a negative one that reflects before the beginning
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
