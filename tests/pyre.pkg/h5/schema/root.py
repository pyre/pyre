#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a schema {Root} is a group that carries an absolute mount point and an
instance-level index of named shape dimensions, one per realization
"""


# the driver
def test():
    # support
    import pyre

    # a product root: a {Root} subclass with an absolute mount point
    class Product(pyre.h5.schema.root, location="/science/LSAR"):
        """
        A product root
        """

        # a member, to confirm {Root} still harvests descriptors like any group
        count = pyre.h5.schema.int()

    # a root is a group
    assert issubclass(Product, pyre.h5.schema.group)

    # two independent realizations
    a = Product(name="root")
    b = Product(name="root")

    # each carries the absolute mount, inherited like any root
    assert a._pyre_location == "/science/LSAR"
    assert b._pyre_location == "/science/LSAR"

    # each has its own shape index; the nodes are structural but their values bind per
    # realization, so the indices must be distinct objects
    assert a._pyre_shapes is not b._pyre_shapes

    # the index is a named container: set a dimension on {a} and read it back
    a._pyre_shapes["nlines"] = 9000
    assert a._pyre_shapes["nlines"] == 9000

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
