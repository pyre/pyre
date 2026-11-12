#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import itertools
import struct
import sys

# the counts a radar sample can have
counts = ["Int8", "Int16", "Int32", "Int64", "UInt8", "UInt16", "UInt32", "UInt64"]
# the ones wide enough to have a byte order
wide = ["Int16", "Int32", "Int64", "UInt16", "UInt32", "UInt64"]
# the marker that names the order the host lacks
foreign = "BE" if sys.byteorder == "little" else "LE"
# and the struct code for it
code = ">" if foreign == "BE" else "<"


def presence():
    """
    Verify that the buffer, heap, map and view expansions over radar samples are all present, in
    both access modes, for native counts and for counts in the order the host lacks
    """
    # get the memory bindings
    from pyre.extensions.pyre import memory

    # the storage strategies
    strategies = ["Buffer", "Heap", "Map", "View"]
    # given access rights
    permissions = ["", "Const"]
    # the cell names: samples of native counts, and samples of foreign order counts
    cells = [f"IQ{count}" for count in counts] + [f"IQ{count}{foreign}" for count in wide]
    # go through all combinations
    for strategy, cell, permission in itertools.product(strategies, cells, permissions):
        # the module that holds the class
        module = getattr(memory, f"{strategy.lower()}s")
        # the class name
        name = f"{strategy}{cell}{permission}"
        # verify it is present and reports its name
        assert getattr(module, name).__name__ == name

    # all done
    return


def heaps():
    """
    Verify that a heap of samples hands out and takes in the pair of counts, and lays its cells
    out as the two counts back to back
    """
    # get the heap bindings
    from pyre.extensions.pyre.memory import heaps

    # make a heap of samples
    heap = heaps.HeapIQUInt16(cells=3)
    # fill it with one sample
    heap.fill((1, 2))
    # every cell reads as the pair
    assert list(heap) == [(1, 2)] * 3
    # write a different sample, from any sequence of two counts
    heap[2] = [3, 65535]
    # and read it back as a pair
    assert heap[2] == (3, 65535)
    # the buffer description is a record of two counts, named after the fields of the sample
    assert memoryview(heap).format == "T{H:i:H:q:}"
    # and its bytes are the counts in order
    assert bytes(heap) == struct.pack("=6H", 1, 2, 1, 2, 3, 65535)

    # make a heap of samples with signed counts
    signed = heaps.HeapIQInt8(cells=1)
    # store one with a negative count
    signed[0] = (-3, 4)
    # the counts keep their sign
    assert signed[0] == (-3, 4)
    # and the record describes signed bytes
    assert memoryview(signed).format == "T{b:i:b:q:}"

    # all done
    return


def foreignHeaps():
    """
    Verify that a heap of samples in the order the host lacks swaps each count on its own
    """
    # get the heap bindings
    from pyre.extensions.pyre.memory import heaps

    # make a heap of samples with foreign order counts
    heap = getattr(heaps, f"HeapIQUInt16{foreign}")(cells=2)
    # write a sample whose counts have distinct bytes
    heap[0] = (0x0102, 0x0304)
    # and another one
    heap[1] = (5, 6)
    # read back the values
    assert list(heap) == [(0x0102, 0x0304), (5, 6)]
    # the description marks each count with its order
    assert memoryview(heap).format == f"T{{{code}H:i:{code}H:q:}}"
    # and the bytes are each count in the declared order, the counts in place
    assert bytes(heap) == struct.pack(f"{code}4H", 0x0102, 0x0304, 5, 6)

    # all done
    return


def refusals():
    """
    Verify that anything other than a pair of counts that fit is refused
    """
    # get the heap bindings
    from pyre.extensions.pyre.memory import heaps

    # make a heap of samples
    heap = heaps.HeapIQUInt16(cells=1)
    # go through things that are not samples
    for value in ["ab", (1, 2, 3), (1,), (1, "x"), (70000, 1), (-1, 1), 5]:
        # try
        try:
            # to store it
            heap[0] = value
        # which must fail
        except TypeError:
            # and move on to the next one
            continue
        # if it did not, complain
        raise AssertionError(f"{value!r} was taken for a sample")

    # all done
    return


# main
if __name__ == "__main__":
    # the classes
    presence()
    # heaps of samples in the host's order
    heaps()
    # heaps of samples in the other order
    foreignHeaps()
    # and values that are not samples
    refusals()


# end of file
