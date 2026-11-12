#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def heap():
    """
    Build heap grids of radar samples and confirm that their cells read and write as the pair of
    their counts, in either byte order, with each count stored in the declared order
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # a sample whose counts have distinct bytes
    sample = (0x0102, 0x0304)
    # with native counts, and with counts in each explicit order
    for marker, expected in [
        ("", None),
        ("be", b"\x01\x02\x03\x04"),
        ("le", b"\x02\x01\x04\x03"),
    ]:
        # make a grid
        g = grid.heap(shape=[2], cell=f"iquint16{marker}")
        # write through the erased class
        g[0] = sample
        # twice, so the two cells are told apart
        g[1] = (5, 6)
        # read back; the counts come through the swap
        assert g[0] == sample
        assert g[1] == (5, 6)
        # with an explicit order, the bytes of each count sit in that order, the counts in place
        if expected is not None:
            assert bytes(g)[:4] == expected
    # all done
    return


def map():
    """
    Map a data product of samples and confirm that it reads as the pairs it holds
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # for packing the product
    import struct

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "grid_iq_test.dat"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # three samples of big endian signed counts
    samples = [(1, -1), (2, -2), (300, -300)]
    # write them as a product
    with open(uri, "wb") as product:
        # each sample is its two counts back to back
        product.write(struct.pack(">6h", *(count for sample in samples for count in sample)))

    # map it read-only
    g = grid.map(uri=uri, shape=[3], cell="iqint16be", create=False, writable=False)
    # every cell reads as its sample
    assert [g[i] for i in range(3)] == samples
    # let go
    del g

    # all done
    return


def numpy():
    """
    Confirm that numpy, when available, sees a grid of samples as a record of two counts
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # numpy is optional
    try:
        # get it
        import numpy
    # if it's not there
    except ImportError:
        # there is nothing to check
        return

    # make a grid of samples
    g = grid.heap(shape=[2, 2], cell="iqint16")
    # fill it
    for i in range(2):
        for j in range(2):
            g[i, j] = (i, -j)
    # view it through numpy, without copying
    a = numpy.asarray(g)
    # numpy sees the fields of the sample
    assert a.dtype.names == ("i", "q")
    # and the counts
    assert int(a["i"][1, 0]) == 1
    assert int(a["q"][0, 1]) == -1
    # write through numpy
    a["q"][1, 1] = 7
    # and the grid sees it
    assert g[1, 1] == (1, 7)
    # all done
    return


def bad():
    """
    Confirm that a sample of counts that are not integers is refused with the name the caller used
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # names that look like samples but are not
    for cell in ["iqfloat32", "iqcomplex64", "iquint16xx"]:
        # carefully
        try:
            # ask for it
            grid.heap(shape=[1], cell=cell)
        # the refusal
        except ValueError as error:
            # must name what was asked for
            assert cell in str(error)
        # anything else
        else:
            # is a failure
            assert False, f"unsupported cell name '{cell}' was accepted"
    # all done
    return


# main
if __name__ == "__main__":
    # run the tests
    heap()
    map()
    numpy()
    bad()


# end of file
