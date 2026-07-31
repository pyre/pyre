#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The conda mkl headers live in {mkl-include}, folded in as a companion

The fixture environment in {conda/} splits mkl the way conda does: the libraries under
the {mkl} package, the headers under {mkl-include}
"""


def test():
    """
    Interpret the mkl recipe against the fixture environment
    """
    # the engine
    from pyre.platforms.Conda import Conda

    # the category
    from pyre.externals.supported.mkl.MKL import MKL

    # make an engine pointing at the fixture environment
    engine = Conda(name="conda.fixture.mkl", environment="conda")
    # it must be functional
    assert engine.available()

    # get the mkl recipe
    recipe, *_ = MKL.recipes()
    # interpret it
    values = engine.configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # the version comes from the lead
    assert values["version"] == "2024.1.0"
    # the headers were found in the {mkl-include} companion
    assert [str(folder) for folder in values["incdir"]] == ["conda/include"]
    # the runtime in the lead
    assert [str(folder) for folder in values["libdir"]] == ["conda/lib"]
    # with its stem resolved
    assert values["libraries"] == ["mkl_rt"]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
