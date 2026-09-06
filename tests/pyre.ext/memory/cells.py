#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import itertools


# the drivers
def intCells() -> None:
    """
    Sanity test: make sure the bindings for integral type cells are present
    """
    # access the memory bindings
    from pyre.extensions.pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # integral types
    signs = ["", "U"]
    sizes = [8, 16, 32, 64]

    # build the integral type names
    for perm, sign, size in itertools.product(const, signs, sizes):
        # assemble the name
        name = f"{sign}Int{size}{perm}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name of the class
        assert name == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert perm == ("" if cell.mutable else "Const")

    # all done
    return


def floatCells() -> None:
    """
    Sanity test: make sure the bindings for float type cells are present
    """
    # access the memory bindings
    from pyre.extensions.pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # float types
    sizes = [("Float", 32), ("Double", 64)]

    # build the float type names
    for perm, (marker, size) in itertools.product(const, sizes):
        # assemble the name
        name = f"{marker}{perm}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name of the class
        assert name == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert perm == ("" if cell.mutable else "Const")

    # all done
    return


def complexCells() -> None:
    """
    Sanity test: make sure the bindings for complex type cells are present
    """
    # access the memory bindings
    from pyre.extensions.pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # complex types
    sizes = [("ComplexFloat", 64), ("ComplexDouble", 128)]

    # build the complex type names
    for perm, (marker, size) in itertools.product(const, sizes):
        # assemble the name
        name = f"{marker}{perm}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name of the class
        assert name == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert perm == ("" if cell.mutable else "Const")

    # all done
    return


def orderedCells() -> None:
    """
    Sanity test: make sure the bindings for byte ordered cells are present, that the spelling
    that matches the host is the native cell, and that the other one is a distinct class
    """
    # access the memory bindings
    from pyre.extensions.pyre.memory import cells

    # the host's byte order
    import sys

    # the marker that names the host's order, and the one that names the other
    native, foreign = ("LE", "BE") if sys.byteorder == "little" else ("BE", "LE")
    # access rights
    const = ["", "Const"]
    # the scalars wide enough to have a byte order
    scalars = [
        ("Int16", 16),
        ("Int32", 32),
        ("Int64", 64),
        ("UInt16", 16),
        ("UInt32", 32),
        ("UInt64", 64),
        ("Float", 32),
        ("Double", 64),
        ("ComplexFloat", 64),
        ("ComplexDouble", 128),
    ]

    # go through them
    for perm, (scalar, size) in itertools.product(const, scalars):
        # the native cell
        plain = getattr(cells, f"{scalar}{perm}")
        # the spelling that matches the host is another name for it
        assert getattr(cells, f"{scalar}{native}{perm}") is plain
        # the other spelling is its own class
        name = f"{scalar}{foreign}{perm}"
        cell = getattr(cells, name)
        # that is not the native cell
        assert cell is not plain
        # with the right name
        assert name == cell.__name__
        # the same size
        assert size == cell.bits
        assert size == 8 * cell.bytes
        # the same access rights
        assert perm == ("" if cell.mutable else "Const")
        # and a declaration that spells out the order
        marker = "big_t" if foreign == "BE" else "little_t"
        assert marker in cell.declValue

    # all done
    return


# main
if __name__ == "__main__":
    # run the tests
    intCells()
    floatCells()
    complexCells()
    orderedCells()


# end of file
