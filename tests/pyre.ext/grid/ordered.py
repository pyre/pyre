#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def heap():
    """
    Build heap grids over byte ordered cells and confirm their bytes sit in the declared order
    while their cells read as native values
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # a value whose two bytes differ
    value = 0x0102
    # in each explicit order
    for marker, expected, code in [("be", b"\x01\x02", ">H"), ("le", b"\x02\x01", "<H")]:
        # make a grid
        g = grid.heap(shape=[1], cell=f"uint16{marker}")
        # write through the erased class
        g[0] = value
        # read back; the value must come through the swap
        assert g[0] == value
        # the raw bytes must be in the declared order, whatever the host
        assert bytes(g) == expected
        # and the buffer protocol description carries the order marker, except when the
        # marker names the host's own order, in which case the cell is the native one
        assert memoryview(g).format in (code, code[1:])
    # all done
    return


def map():
    """
    Map a data product written in each byte order and confirm that declaring the right order
    yields the values, while declaring the wrong one yields their byte swapped shadows
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # for packing the product
    import struct

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "grid_ordered_test.dat"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # the shape
    shape = [2, 3]
    # the values, each with two distinct bytes
    values = [0x0100 * (i + 1) + (i + 1) for i in range(6)]
    # their byte swapped shadows
    shadows = [((v & 0xFF) << 8) | (v >> 8) for v in values]

    # for each byte order
    for marker, other, code in [("be", "le", ">"), ("le", "be", "<")]:
        # write the product in this order
        with open(uri, "wb") as product:
            # pack
            product.write(struct.pack(f"{code}{len(values)}H", *values))
        # map it read-only, declaring the matching order
        g = grid.map(uri=uri, shape=shape, cell=f"uint16{marker}", create=False, writable=False)
        # every cell reads as its value
        assert [g[i, j] for i in range(2) for j in range(3)] == values
        # map it again, declaring the other order
        h = grid.map(uri=uri, shape=shape, cell=f"uint16{other}", create=False, writable=False)
        # every cell reads as the shadow of its value
        assert [h[i, j] for i in range(2) for j in range(3)] == shadows
        # let go
        del g, h

        # map it for writing, declaring the matching order
        w = grid.map(uri=uri, shape=shape, cell=f"uint16{marker}", create=False)
        # change a cell
        w[1, 2] = 0xABCD
        # it reads right back
        assert w[1, 2] == 0xABCD
        # flush
        del w
        # the file must hold the new value in the declared order
        with open(uri, "rb") as product:
            # unpack
            stored = struct.unpack(f"{code}{len(values)}H", product.read())
        # check
        assert stored[5] == 0xABCD
        # and the rest are untouched
        assert list(stored[:5]) == values[:5]

    # all done
    return


def numpy():
    """
    Confirm that numpy, when available, honors the byte order marker in the buffer description
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

    # a value with distinct bytes
    value = 0x0102
    # in each explicit order
    for marker in ["be", "le"]:
        # make a grid
        g = grid.heap(shape=[2, 2], cell=f"uint16{marker}")
        # fill it
        for i in range(2):
            for j in range(2):
                g[i, j] = value + 2 * i + j
        # view it through numpy, without copying
        a = numpy.asarray(g)
        # numpy must see the same native values
        assert a[1, 1] == value + 3
        # write through numpy
        a[0, 0] = 0x0304
        # and the grid must see the write, through its own swap
        assert g[0, 0] == 0x0304
    # all done
    return


def bad():
    """
    Confirm that a marker on an unknown base cell is refused with the name the caller used
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # carefully
    try:
        # ask for a cell that does not exist
        grid.heap(shape=[1], cell="float6be")
    # the refusal
    except ValueError as error:
        # must name what was asked for
        assert "float6be" in str(error)
    # anything else
    else:
        # is a failure
        assert False, "unsupported cell name was accepted"
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
