#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import struct
import sys

# the marker that names the order the host lacks
foreign = "BE" if sys.byteorder == "little" else "LE"
# and the struct code for it
code = ">" if foreign == "BE" else "<"


def heap():
    """
    Verify that the heap factory allocates over byte ordered cells, in both spellings
    """
    # get the package
    import pyre
    from pyre.memory import cells

    # a cell in the order the host lacks
    cell = getattr(cells, f"uint16{foreign}")()
    # allocate
    heap = pyre.memory.heap(type=cell, cells=4)
    # the class is the foreign order one
    assert type(heap).__name__ == f"HeapUInt16{foreign}"
    # fill and read back as native values
    heap.fill(0x0102)
    assert list(heap) == [0x0102] * 4
    # while the bytes sit in the declared order
    assert bytes(heap) == struct.pack(f"{code}4H", *([0x0102] * 4))

    # a cell in the host's own order is the native cell
    native = "LE" if foreign == "BE" else "BE"
    cell = getattr(cells, f"uint16{native}")()
    # so the factory hands back the native heap
    heap = pyre.memory.heap(type=cell, cells=4)
    assert type(heap).__name__ == "HeapUInt16"

    # all done
    return


def map():
    """
    Verify that the map factory opens a product in the order the host lacks, read-only and
    writable
    """
    # get the package
    import pyre
    from pyre.memory import cells

    # the scratch product
    uri = pyre.primitives.path("memory_ordered_test.dat")
    # the values
    values = [1, 2, 3, 0x1234]
    # write the product in the foreign order
    with open(uri, "wb") as product:
        product.write(struct.pack(f"{code}4H", *values))

    # open it read-only
    const = pyre.memory.map(uri=uri, type=getattr(cells, f"uint16{foreign}Const")())
    # the cells read as their native values
    assert list(const) == values
    # let go
    del const

    # a writable map over an existing product goes through the bindings directly
    from pyre.extensions.pyre.memory import maps

    writable = getattr(maps, f"MapUInt16{foreign}")(str(uri), True)
    # change a cell
    writable[3] = 0xABCD
    # flush
    del writable
    # and the file must hold it in the foreign order
    with open(uri, "rb") as product:
        stored = struct.unpack(f"{code}4H", product.read())
    assert list(stored) == values[:3] + [0xABCD]

    # all done
    return


def numpy():
    """
    Verify that numpy, when available, honors the order marker on a heap over byte ordered cells
    """
    # numpy is optional
    try:
        # get it
        import numpy
    # if it's not there
    except ImportError:
        # there is nothing to check
        return

    # get the package
    import pyre
    from pyre.memory import cells

    # allocate over foreign order complex cells
    heap = pyre.memory.heap(type=getattr(cells, f"complexFloat{foreign}")(), cells=2)
    # fill
    heap[0] = 1.5 - 2j
    heap[1] = 3 + 4j
    # view through numpy, without copying
    a = numpy.asarray(heap)
    # numpy sees the marker
    assert a.dtype == numpy.dtype(f"{code}c8")
    # and the values
    assert a.tolist() == [1.5 - 2j, 3 + 4j]
    # a write through numpy
    a[1] = 5 + 6j
    # is seen by the heap
    assert heap[1] == 5 + 6j

    # all done
    return


# main
if __name__ == "__main__":
    # run the tests
    heap()
    map()
    numpy()


# end of file
