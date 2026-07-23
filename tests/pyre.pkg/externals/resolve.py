#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the dependency resolver

The configuration file {resolve.yaml} restricts the host to the bare engine over the fixture
installation; requesting parmetis must pull in metis and mpi through the recipe dependency
edges, and the report must list the selections in link order
"""

# support
import pyre


# the application
class resolve(pyre.application):
    """
    An application that resolves its requirements explicitly
    """


def test():
    """
    Resolve the transitive closure of parmetis and check the link order
    """
    # instantiate the application; this loads {resolve.yaml}
    app = resolve(name="resolve")
    # resolve a request with dependencies, an unknown category, and a known category that the
    # fixture does not provide
    report = pyre.externals.resolve(requested=["parmetis", "nosuchpackage", "petsc"])
    # the unknown category must be flagged
    assert report.unsupported == ["nosuchpackage"]
    # petsc is supported but not installed in the fixture, so it must be flagged as such
    assert report.unavailable == ["petsc"]
    # and must not appear among the selections
    assert "petsc" not in report.selections
    # the closure must have been realized in full
    order = list(report.selections)
    assert set(order) == {"parmetis", "metis", "mpi"}
    # in link order: every package precedes its dependencies
    assert order.index("parmetis") < order.index("metis")
    assert order.index("parmetis") < order.index("mpi")
    # and every selection must be validly configured
    for category, installation in report.selections.items():
        # no complaints
        assert not installation.pyre_configurationErrors, f"'{category}' misconfigured"
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
