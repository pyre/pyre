#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Permutation} directly, through the extension rather than the
{gsl.permutation} shim, so a failure isolates the c++ layer
"""


def raises(fn, kind):
    """
    Return True if calling {fn} raises {kind}
    """
    # try the call
    try:
        # which is expected to fail
        fn()
    # if it raises the right thing
    except kind:
        # good
        return True
    # otherwise it did not guard
    return False


def test():
    # the bindings
    from gsl import libgsl

    # make a permutation of five elements
    p = libgsl.Permutation(shape=5)
    # which knows its size
    assert p.shape == 5 and len(p) == 5
    # is valid
    assert bool(p) is True
    # and starts out as the identity
    assert p.get(3) == 3

    # a negative index reflects
    assert p.get(-1) == 4
    # an index past the end is refused
    assert raises(lambda: p.get(5), IndexError)
    # and so is a negative one that reflects past the beginning
    assert raises(lambda: p.get(-6), IndexError)

    # make a clone
    q = p.clone()
    # change it
    q.swap(0, 4)
    # and check that the original did not change
    assert q.get(0) == 4 and p.get(0) == 0

    # swap checks both of its indices
    assert raises(lambda: p.swap(0, 5), IndexError)
    # and reflects a negative one
    p.swap(0, -1)
    # so the first and last elements trade places
    assert p.get(0) == 4 and p.get(4) == 0

    # reset to the identity
    p.init()
    # and check that it took
    assert p.get(0) == 0
    # step to the next permutation in the sequence
    assert p.next() is True
    # which swaps the last two
    assert p.get(3) == 4 and p.get(4) == 3
    # step back
    assert p.prev() is True
    # which returns to the identity
    assert p.get(3) == 3

    # reset to the identity
    p.init()
    # swap two elements
    p.swap(0, 2)
    # and invert
    inv = p.inverse()
    # the inverse of a swap is the same swap
    assert inv.get(0) == 2 and inv.get(2) == 0

    # reset to the identity and reverse it
    p.init().reverse()
    # which yields the descending permutation
    assert p.get(0) == 4 and p.get(4) == 0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
