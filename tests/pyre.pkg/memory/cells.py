#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import itertools


# the driver
def intCells() -> None:
    """
    Sanity test: make sure the bindings for integral type cells exist
    """
    # access the cell types
    from pyre.memory import cells

    # access rights
    rights = ["", "Const"]
    # integral types: signed and unsigned
    signs = ["", "u"]
    # in every width
    sizes = [8, 16, 32, 64]

    # build the integral type names
    for access, sign, size in itertools.product(rights, signs, sizes):
        # assemble the python name of the cell
        name = f"{sign}int{size}{access}"
        # assemble the name the cell reports
        cellName = f"{sign.upper()}Int{size}{access}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name
        assert cellName == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert access == ("" if cell.mutable else "Const")

    # all done
    return


def floatCells() -> None:
    """
    Sanity test: make sure the bindings for float type cells exist
    """
    # access the cell types
    from pyre.memory import cells

    # access rights
    rights = ["", "Const"]
    # float types
    sizes = [("float", 32), ("double", 64)]

    # build the float type names
    for access, (marker, size) in itertools.product(rights, sizes):
        # assemble the name in the module
        name = f"{marker}{access}"
        # assemble the name the cell reports
        cellName = f"{marker.capitalize()}{access}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name
        assert cellName == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert access == ("" if cell.mutable else "Const")

    # all done
    return


def complexCells() -> None:
    """
    Sanity test: make sure the bindings for complex type cells exist
    """
    # access the cell types
    from pyre.memory import cells

    # access rights
    rights = ["", "Const"]
    # complex types
    sizes = [
        ("complexFloat", "ComplexFloat", 64),
        ("complexDouble", "ComplexDouble", 128),
    ]

    # build the complex type names
    for access, (marker, tag, size) in itertools.product(rights, sizes):
        # assemble the name in the module
        name = f"{marker}{access}"
        # assemble the name the cell reports
        cellName = f"{tag}{access}"
        # verify that the bindings exist
        cell = getattr(cells, name)
        # check the name
        assert cellName == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert access == ("" if cell.mutable else "Const")

    # all done
    return


def orderedCells() -> None:
    """
    Sanity test: make sure the byte ordered cells are published under their python names
    """
    # access the cell types
    from pyre.memory import cells

    # the host's byte order
    import sys

    # the marker that names the host's order
    native = "LE" if sys.byteorder == "little" else "BE"
    # access rights
    rights = ["", "Const"]
    # byte order markers
    markers = ["BE", "LE"]
    # the scalars wide enough to have a byte order, with the names they report
    scalars = [
        ("int16", "Int16", 16),
        ("int32", "Int32", 32),
        ("int64", "Int64", 64),
        ("uint16", "UInt16", 16),
        ("uint32", "UInt32", 32),
        ("uint64", "UInt64", 64),
        ("float", "Float", 32),
        ("double", "Double", 64),
        ("complexFloat", "ComplexFloat", 64),
        ("complexDouble", "ComplexDouble", 128),
    ]

    # go through them
    for access, marker, (scalar, tag, size) in itertools.product(rights, markers, scalars):
        # assemble the name in the module
        name = f"{scalar}{marker}{access}"
        # the name the cell reports: the host's own order is the native cell
        cellName = f"{tag}{access}" if marker == native else f"{tag}{marker}{access}"
        # verify that the cell exists
        cell = getattr(cells, name)
        # check the name
        assert cellName == cell.__name__
        # check the size, in bits
        assert size == cell.bits
        # check the size, in bytes
        assert size == 8 * cell.bytes
        # check the access rights
        assert access == ("" if cell.mutable else "Const")

    # all done
    return


# main
if __name__ == "__main__":
    # check the integral cells
    intCells()
    # the float ones
    floatCells()
    # the complex ones
    complexCells()
    # and the byte ordered ones
    orderedCells()


# end of file
