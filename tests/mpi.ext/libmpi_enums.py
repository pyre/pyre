#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that every enumeration the bindings publish carries the members the collectives and the
comparisons name, and that the members of each are distinct
"""


def test():
    # access the bindings directly, without bringing mpi up
    from mpi import libmpi

    # the reduction operators, grouped as the c++ layer groups them
    ops = [
        # arithmetic
        libmpi.Op.sum,
        libmpi.Op.product,
        libmpi.Op.maximum,
        libmpi.Op.minimum,
        # logical
        libmpi.Op.logicalAnd,
        libmpi.Op.logicalOr,
        libmpi.Op.logicalXor,
        # bitwise
        libmpi.Op.bitwiseAnd,
        libmpi.Op.bitwiseOr,
        libmpi.Op.bitwiseXor,
        # the extrema paired with the rank that supplied them
        libmpi.Op.maxloc,
        libmpi.Op.minloc,
        # last one wins
        libmpi.Op.replace,
    ]
    # no two operators may share a value, or a reduction would silently do the wrong thing
    assert len(set(ops)) == len(ops)

    # the outcomes of a comparison
    comparisons = [
        libmpi.Comparison.identical,
        libmpi.Comparison.congruent,
        libmpi.Comparison.similar,
        libmpi.Comparison.unequal,
    ]
    # likewise distinct
    assert len(set(comparisons)) == len(comparisons)

    # the levels of thread support
    threads = [
        libmpi.Thread.single,
        libmpi.Thread.funneled,
        libmpi.Thread.serialized,
        libmpi.Thread.multiple,
    ]
    # and these too
    assert len(set(threads)) == len(threads)

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
