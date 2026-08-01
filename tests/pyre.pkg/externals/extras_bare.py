#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Optional markers extend the bare engine's include path without vetoing discovery
"""


def test():
    """
    Interpret ad hoc recipes with optional markers against the fixture installation
    """
    # the engine
    from pyre.platforms.Bare import Bare

    # the recipe description
    from pyre.externals.Recipe import Recipe

    # the placeholder factory; engines never touch it
    from pyre.externals.supported.gsl.Default import Default

    # make an engine that probes only the fixture
    engine = Bare(name="bare.fixture.extras", searchpath=["prefix"])

    # a recipe whose optional marker is present in the fixture: eigen's nested headers
    present = Recipe(
        # of a scratch category
        category="gsl",
        # with a placeholder factory
        factory=Default,
        # the hard marker
        headers=("gsl/gsl_version.h",),
        # and an optional one the fixture provides
        extras=("Eigen/Core",),
    )
    # interpret it
    values = engine.configure(recipe=present)
    # the discovery must succeed
    assert values is not None
    # with the optional marker's folder appended to the include path
    assert [str(f) for f in values["incdir"]] == ["prefix/include", "prefix/include/eigen3"]

    # a recipe whose optional marker is nowhere to be found
    absent = Recipe(
        # of a scratch category
        category="gsl",
        # with a placeholder factory
        factory=Default,
        # the hard marker
        headers=("gsl/gsl_version.h",),
        # and an optional one the fixture lacks
        extras=("nosuch/header.h",),
    )
    # interpret it
    values = engine.configure(recipe=absent)
    # the discovery must still succeed: optional markers never veto
    assert values is not None
    # with just the hard marker's folder
    assert [str(f) for f in values["incdir"]] == ["prefix/include"]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
