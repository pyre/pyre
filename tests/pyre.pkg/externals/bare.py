#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bare engine against the fixture installation in {prefix/}
"""


def test():
    """
    Probe the fixture prefix for gsl and openmpi
    """
    # support
    import pyre

    # the engine
    from pyre.platforms.Bare import Bare

    # the categories
    from pyre.externals.supported.gsl.GSL import GSL
    from pyre.externals.supported.mpi.MPI import MPI

    # make an engine that probes only the fixture
    engine = Bare(name="bare.fixture", searchpath=["prefix"])
    # probing is always possible
    assert engine.available()

    # get the gsl recipe
    recipe, *_ = GSL.recipes()
    # interpret it
    values = engine.configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # the headers live in the canonical include directory
    assert [str(folder) for folder in values["incdir"]] == ["prefix/include"]
    # the libraries live in the canonical lib directory
    assert [str(folder) for folder in values["libdir"]] == ["prefix/lib"]
    # both stems resolve
    assert values["libraries"] == ["gsl", "gslcblas"]
    # bare engines can't know versions from a database, but the recipe's content
    # extractor harvests it from the version header
    assert values["version"] == "2.8"

    # get the eigen recipe
    from pyre.externals.supported.eigen.Eigen import Eigen

    # its headers nest one level below the canonical include directory
    eigen, *_ = Eigen.recipes()
    # interpret it
    values = engine.configure(recipe=eigen)
    # the discovery must succeed
    assert values is not None
    # with the nested include directory
    assert [str(folder) for folder in values["incdir"]] == ["prefix/include/eigen3"]

    # get the openmpi recipe
    openmpi, *_ = MPI.recipes()
    # interpret it
    values = engine.configure(recipe=openmpi)
    # the discovery must succeed: the fixture has mpi.h, libmpi, and a launcher
    assert values is not None
    # the launcher was resolved to an actual executable name
    assert values["launcher"].startswith("mpirun")
    # and the bin directory was recorded
    assert [str(folder) for folder in values["bindir"]] == ["prefix/bin"]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
