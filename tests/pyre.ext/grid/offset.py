#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the product
uri = "grid_offset_test.dat"


def product(header, values, code):
    """
    Write a product with a {header} of that many bytes in front of {values}, packed with the
    struct {code}
    """
    # for packing the values
    import struct

    # open the file
    with open(uri, "wb") as stream:
        # write a recognizable header
        stream.write(b"\xab" * header)
        # and the values after it
        stream.write(struct.pack(f"{code[0]}{len(values)}{code[1:]}", *values))
    # all done
    return


def aligned():
    """
    Map a product whose cells sit past a header whose length is a multiple of the cell size
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # the values
    values = [float(i) for i in range(6)]
    # past a header of 16 bytes
    product(header=16, values=values, code="=d")
    # map it
    g = grid.map(uri=uri, shape=[2, 3], cell="float64", create=False, offset=16)
    # every cell reads as its value
    assert [g[i, j] for i in range(2) for j in range(3)] == values
    # and the cells are the native ones, since the offset leaves them aligned
    assert memoryview(g).format == "d"
    # let go
    del g
    # all done
    return


def unaligned():
    """
    Map a product whose cells sit past a header whose length is not a multiple of the cell size,
    and confirm that they read and write correctly
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # for the host's byte order
    import sys

    # the values
    values = [float(i) for i in range(6)]
    # past a header of 3 bytes
    product(header=3, values=values, code="=d")
    # map it
    g = grid.map(uri=uri, shape=[2, 3], cell="float64", create=False, offset=3)
    # every cell reads as its value
    assert [g[i, j] for i in range(2) for j in range(3)] == values
    # the cells are read by copying their bytes, which the buffer description says by naming
    # the host's order, a spelling that implies no alignment
    assert memoryview(g).format == ("<d" if sys.byteorder == "little" else ">d")
    # change a cell
    g[1, 2] = -1.0
    # it reads right back
    assert g[1, 2] == -1.0
    # flush
    del g

    # read the file back
    with open(uri, "rb") as stream:
        # the whole thing
        contents = stream.read()
    # the header is untouched
    assert contents[:3] == b"\xab" * 3
    # and the change is where it belongs
    import struct

    # unpack the cells
    stored = struct.unpack("=6d", contents[3:])
    # check
    assert list(stored) == values[:5] + [-1.0]
    # all done
    return


def foreign():
    """
    Map a big endian product at an offset that leaves its cells misaligned
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # the values, each with two distinct bytes
    values = [0x0100 * (i + 1) + (i + 1) for i in range(6)]
    # past a header of 1 byte
    product(header=1, values=values, code=">H")
    # map it read-only, declaring its order
    g = grid.map(uri=uri, shape=[2, 3], cell="uint16be", create=False, writable=False, offset=1)
    # every cell reads as its value
    assert [g[i, j] for i in range(2) for j in range(3)] == values
    # the description carries the order
    assert memoryview(g).format == ">H"
    # let go
    del g
    # all done
    return


def numpy():
    """
    Confirm that numpy, when available, reads misaligned cells correctly
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

    # the values
    values = [float(i) for i in range(6)]
    # past a header of 5 bytes
    product(header=5, values=values, code="=d")
    # map it
    g = grid.map(uri=uri, shape=[2, 3], cell="float64", create=False, offset=5)
    # view it through numpy, without copying
    a = numpy.asarray(g)
    # numpy must see the same values
    assert a.tolist() == [values[:3], values[3:]]
    # let go
    del a, g
    # all done
    return


def bad():
    """
    Confirm that offsets that make no sense are refused
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # a fresh product has no header to skip, and no offset can be negative
    for create, offset in [(True, 8), (False, -1)]:
        # carefully
        try:
            # ask for the impossible
            grid.map(uri=uri, shape=[2, 3], cell="float64", create=create, offset=offset)
        # the refusal
        except ValueError as error:
            # must mention the offset
            assert "offset" in str(error)
        # anything else
        else:
            # is a failure
            assert False, f"create={create}, offset={offset} was accepted"
    # all done
    return


def empty():
    """
    Confirm that a map with nothing in it is refused: an offset at the end of the file, an empty
    file, and a fresh product with no cells
    """
    # support
    import os
    import journal

    # the grid bindings
    from pyre.extensions.pyre import grid

    # the refusals are expected, so keep them off the screen
    journal.error("pyre.memory.map").device = journal.trash()
    # a product with a header of 16 bytes and nothing after it
    product(header=16, values=[], code="=d")
    # an empty file
    blank = "grid_offset_empty.dat"
    # make it
    open(blank, "wb").close()
    # a fresh product that must never appear
    fresh = "grid_offset_fresh.dat"
    # the requests
    requests = [
        # an offset right at the end of the file
        dict(uri=uri, shape=[1], create=False, offset=16),
        # an empty file
        dict(uri=blank, shape=[1], create=False, offset=0),
        # a fresh product with no cells
        dict(uri=fresh, shape=[0, 3], create=True, offset=0),
    ]
    # go through them
    for request in requests:
        # carefully
        try:
            # ask for a map with nothing in it
            grid.map(cell="float64", **request)
        # the refusal
        except journal.ApplicationError:
            # is the expected outcome
            pass
        # anything else
        else:
            # is a failure
            assert False, f"{request} was accepted"
    # the refused product was never made
    assert not os.path.exists(fresh)
    # clean up
    os.remove(blank)
    # all done
    return


# main
if __name__ == "__main__":
    # run the tests
    aligned()
    unaligned()
    foreign()
    numpy()
    bad()
    empty()


# end of file
