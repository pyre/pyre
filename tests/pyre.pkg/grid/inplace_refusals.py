#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic refuses the operands numpy would refuse
"""


def test():
    # support
    import numpy
    import pyre.grid

    # check that {action} raises {error}
    def refuses(error, action):
        # try it
        try:
            action()
        # the expected complaint
        except error:
            # means the refusal worked
            return True
        # anything else means it did not
        return False

    # a grid of integers
    i = pyre.grid.heap(shape=(4,), cell="int32")
    # and one of reals
    f = pyre.grid.heap(shape=(4,), cell="float64")
    # integer cells cannot hold a quotient
    assert refuses(TypeError, lambda: i.__itruediv__(2))
    # or a fraction
    assert refuses(TypeError, lambda: i.__iadd__(1.5))
    # real cells cannot hold a complex number
    assert refuses(TypeError, lambda: f.__iadd__(1j))
    # integers must fit the cells
    assert refuses(ValueError, lambda: pyre.grid.heap(shape=(4,), cell="uint8").__iadd__(300))
    # grids must agree in shape
    assert refuses(ValueError, lambda: f.__iadd__(pyre.grid.heap(shape=(5,), cell="float64")))
    # and in cell type
    assert refuses(TypeError, lambda: f.__iadd__(pyre.grid.heap(shape=(4,), cell="float32")))
    # views that share cells in different places would read what they already wrote
    v = pyre.grid.heap(shape=(8,), cell="float64")
    assert refuses(ValueError, lambda: v[1:].__iadd__(v[:-1]))
    # and operands that are neither numbers nor buffers are left for python to refuse
    assert f.__iadd__("a") is NotImplemented

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
