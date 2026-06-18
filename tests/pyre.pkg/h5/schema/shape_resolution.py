#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a {Root} resolves dataset shape references against the named dimensions of its
tree: providers are registered (unresolved) at their scoped paths, dataset references are
aliased to the nearest enclosing provider by walking up, a set dimension makes referencing
datasets compute, and an unset one raises {UnresolvedNodeError} at read time
"""


# the driver
def test():
    # support
    import pyre
    from pyre.calc.exceptions import UnresolvedNodeError

    # a per-frequency group: provides its own column dimension and a 2d dataset that also
    # references an enclosing dimension
    class Inner(pyre.h5.schema.group):
        """
        A scoping group with a local dimension
        """

        # a dimension scoped to this group
        ncols = pyre.h5.schema.dimension()
        # a dataset whose shape references an enclosing dimension and the local one
        data = pyre.h5.schema.array(
            schema=pyre.h5.schema.float(), shape=["nrows", "ncols"]
        )

    # a product root that provides the shared row dimension and two inner groups
    class Product(pyre.h5.schema.root, location="/science/LSAR"):
        """
        A product root with a shared dimension and two scoping subgroups
        """

        # a dimension shared across the inner groups
        nrows = pyre.h5.schema.dimension()
        # two independent inner groups
        a = Inner()
        b = Inner()

    # realize it; resolution runs eagerly in {Root.__init__}
    spec = Product(name="root")
    shapes = spec._pyre_shapes

    # providers are registered at their scoped paths
    assert "nrows" in shapes
    assert "a.ncols" in shapes
    assert "b.ncols" in shapes
    # dataset references are aliased to them
    assert "a.data.nrows" in shapes
    assert "a.data.ncols" in shapes

    # before any values are supplied, reading a referenced extent raises
    try:
        shapes.retrieve("a.data.nrows").value
        assert False, "expected an unresolved dimension"
    except UnresolvedNodeError:
        pass

    # set the shared row dimension; both inners' rows resolve to the same node
    shapes["nrows"] = 100
    assert shapes.retrieve("a.data.nrows").value == 100
    assert shapes.retrieve("b.data.nrows").value == 100

    # the per-group column dimension is independent: setting a's does not set b's
    shapes["a.ncols"] = 50
    assert shapes.retrieve("a.data.ncols").value == 50
    try:
        shapes.retrieve("b.data.ncols").value
        assert False, "expected b's column dimension to remain unresolved"
    except UnresolvedNodeError:
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
