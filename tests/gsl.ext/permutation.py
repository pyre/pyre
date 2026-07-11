#!/usr/bin/env python3
# -*- Python -*-
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

    # allocation is the identity, and it is valid
    p = libgsl.Permutation(shape=5)
    assert p.shape == 5 and len(p) == 5
    assert bool(p) is True
    assert p.get(3) == 3

    # a negative index reflects; out of range and too-negative raise
    assert p.get(-1) == 4
    assert raises(lambda: p.get(5), IndexError)
    assert raises(lambda: p.get(-6), IndexError)

    # a clone is independent
    q = p.clone()
    q.swap(0, 4)
    assert q.get(0) == 4 and p.get(0) == 0

    # swap checks both of its indices, and reflects a negative one
    assert raises(lambda: p.swap(0, 5), IndexError)
    p.swap(0, -1)
    assert p.get(0) == 4 and p.get(4) == 0

    # reset to the identity, then walk the sequence
    p.init()
    assert p.get(0) == 0
    # the next permutation swaps the last two
    assert p.next() is True
    assert p.get(3) == 4 and p.get(4) == 3
    # and stepping back returns to the identity
    assert p.prev() is True
    assert p.get(3) == 3

    # the inverse of a swap is the same swap
    p.init()
    p.swap(0, 2)
    inv = p.inverse()
    assert inv.get(0) == 2 and inv.get(2) == 0

    # reverse turns the identity into the descending permutation
    p.init().reverse()
    assert p.get(0) == 4 and p.get(4) == 0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
