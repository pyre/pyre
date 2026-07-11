#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that indices crossing into a permutation are reflected and bounds-checked, so out of
range access raises {IndexError} rather than leaning on gsl's optional range check
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

    # the identity permutation of five elements
    p = gsl.permutation(shape=5).init()

    # a negative index counts from the end
    assert p[-1] == p.get(4)
    assert p[-5] == p.get(0)

    # reading past the end raises, through the subscript and the raw accessor
    assert raises(lambda: p[5])
    assert raises(lambda: p.get(5))

    # a too-negative index raises rather than reflecting to a still-negative slot
    assert raises(lambda: p[-6])
    assert raises(lambda: p.get(-6))

    # the swap checks both of its indices, and reflects a negative one
    assert raises(lambda: p.swap(0, 5))
    assert raises(lambda: p.swap(5, 0))
    # a valid swap, with a reflected index, does its job
    p.swap(0, -1)
    assert p[0] == 4 and p[4] == 0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
