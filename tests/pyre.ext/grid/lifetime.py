#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A view must keep the grid's cells alive after the grid object itself is gone
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # the collector, so we can force the issue
    import gc

    # build a grid, fill it, and return only a view of it, dropping the grid object
    def viewOnly():
        # a grid that exists only inside this scope
        g = grid.heap(shape=[4, 4], cell="int32")
        # a view onto its cells, through the buffer protocol
        mv = memoryview(g)
        # stamp every cell
        for i in range(4):
            for j in range(4):
                mv[i, j] = 5
        # hand back the view; {g} is now unreferenced
        return mv

    # take the view
    v = viewOnly()
    # force a collection, so a premature reclamation of the storage would surface here
    gc.collect()

    # reading the cells must still be valid: the erased grid holds a copy of the source grid,
    # whose storage keeps its shared block alive, and the memoryview keeps the erased grid alive
    total = sum(v[i, j] for i in range(4) for j in range(4))
    assert total == 5 * 16
    # and the memory is still writable through the surviving view
    v[0, 0] = 99
    assert v[0, 0] == 99

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
