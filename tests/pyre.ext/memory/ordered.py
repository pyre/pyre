#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import itertools
import struct
import sys

# the scalars wide enough to have a byte order
scalars = [
    # ints
    "Int16",
    "Int32",
    "Int64",
    "UInt16",
    "UInt32",
    "UInt64",
    # floats
    "Float",
    "Double",
    # complex
    "ComplexFloat",
    "ComplexDouble",
]
# the marker that names the order the host lacks
foreign = "BE" if sys.byteorder == "little" else "LE"
# and the struct code for it
code = ">" if foreign == "BE" else "<"


def presence():
    """
    Verify that the buffer, heap, map, and view expansions over the foreign order cells are all
    present, in both access modes
    """
    # get the memory bindings
    from pyre.extensions.pyre import memory

    # the storage strategies
    strategies = ["Buffer", "Heap", "Map", "View"]
    # given access rights
    permissions = ["", "Const"]
    # go through all combinations
    for strategy, scalar, permission in itertools.product(strategies, scalars, permissions):
        # the module that holds the class
        module = getattr(memory, f"{strategy.lower()}s")
        # the class name
        name = f"{strategy}{scalar}{foreign}{permission}"
        # verify it is present
        cls = getattr(module, name)
        # and that it reports its name
        assert cls.__name__ == name

    # all done
    return


def heaps():
    """
    Verify that a heap over foreign order cells reads and writes native values while its bytes sit
    in the declared order
    """
    # get the heap bindings
    from pyre.extensions.pyre.memory import heaps

    # a value whose two bytes differ
    value = 0x0102
    # the number of cells
    cells = 4
    # make a heap over foreign order cells
    heap = getattr(heaps, f"HeapUInt16{foreign}")(cells=cells)
    # it reports its size
    assert len(heap) == cells
    # fill it
    heap.fill(value)
    # every cell reads as the value
    assert list(heap) == [value] * cells
    # write a different value
    heap[3] = 0x0304
    # and read it back
    assert heap[3] == 0x0304
    # the buffer description carries the order marker
    assert memoryview(heap).format == f"{code}H"
    # and the raw bytes are in the declared order
    assert bytes(heap) == struct.pack(f"{code}4H", value, value, value, 0x0304)
    # a slice is a view over the same cells, in the same order
    view = heap[1:3]
    assert type(view).__name__ == f"ViewUInt16{foreign}"
    assert list(view) == [value, value]
    assert memoryview(view).format == f"{code}H"
    # and writes through the view land in the heap
    view[0] = 7
    assert heap[1] == 7

    # all done
    return


def complexHeaps():
    """
    Verify that a heap over foreign order complex cells swaps each component on its own
    """
    # get the heap bindings
    from pyre.extensions.pyre.memory import heaps

    # make a heap over foreign order complex cells
    heap = getattr(heaps, f"HeapComplexFloat{foreign}")(cells=2)
    # write
    heap[0] = 1.5 - 2j
    heap[1] = 3 + 4j
    # read back
    assert list(heap) == [1.5 - 2j, 3 + 4j]
    # the buffer description carries the order marker
    assert memoryview(heap).format == f"{code}Zf"
    # and the raw bytes are the components, each in the declared order
    assert bytes(heap) == struct.pack(f"{code}4f", 1.5, -2, 3, 4)

    # all done
    return


def maps():
    """
    Verify that a map over foreign order cells reads a product written in that order and writes
    back in the same order
    """
    # get the map bindings
    from pyre.extensions.pyre.memory import maps

    # the scratch product
    uri = "memory_ordered_test.dat"
    # the values
    values = [1, 2, 3, 0x1234]
    # write the product in the foreign order
    with open(uri, "wb") as product:
        product.write(struct.pack(f"{code}4H", *values))

    # map it read-only
    const = getattr(maps, f"MapUInt16{foreign}Const")(uri)
    # every cell reads as its value
    assert list(const) == values
    # and the description says so
    assert memoryview(const).format == f"{code}H"
    assert memoryview(const).readonly
    # let go
    del const

    # map it for writing
    writable = getattr(maps, f"MapUInt16{foreign}")(uri, True)
    # change a cell
    writable[0] = 0xABCD
    # and read it back
    assert writable[0] == 0xABCD
    # flush
    del writable
    # the file must hold the new value in the foreign order
    with open(uri, "rb") as product:
        stored = struct.unpack(f"{code}4H", product.read())
    assert list(stored) == [0xABCD] + values[1:]

    # all done
    return


# main
if __name__ == "__main__":
    # run the tests
    presence()
    heaps()
    complexHeaps()
    maps()


# end of file
