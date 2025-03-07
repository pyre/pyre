#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import itertools


# the drivers
def intCells() -> None:
    """
    Sanity test: make sure the bindings for integral type cells
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
    Sanity test: make sure the bindings for float type cells
    """
    # access the memory bindings
    from pyre.extensions.pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # float types
    sizes = [("Float", 32), ("Double", 64)]

    # build the integral type names
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
    Sanity test: make sure the bindings for complex type cells
    """
    # access the memory bindings
    from pyre.extensions.pyre.memory import cells

    # access rights
    const = ["", "Const"]
    # float types
    sizes = [("ComplexFloat", 64), ("ComplexDouble", 128)]

    # build the integral type names
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


# main
if __name__ == "__main__":
    # run the tests
    intCells()
    floatCells()
    complexCells()


# end of file
