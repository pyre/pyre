#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The conda cuda fragments assemble, and the {targets/<arch>} layout is absorbed

The fixture environment in {conda/} carries the runtime under the conda-forge
{targets/<arch>} tree and the compiler in its own {cuda-nvcc} fragment
"""


def test():
    """
    Interpret the cuda recipe against the fixture environment
    """
    # the engine
    from pyre.platforms.Conda import Conda

    # the category
    from pyre.externals.supported.cuda.CUDA import CUDA

    # make an engine pointing at the fixture environment
    engine = Conda(name="conda.fixture.cuda", environment="conda")
    # it must be functional
    assert engine.available()

    # get the cuda recipe
    recipe, *_ = CUDA.recipes()
    # interpret it
    values = engine.configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # the version comes from the runtime fragment, the lead of the union
    assert values["version"] == "12.4.127"
    # the headers were found under the conda-forge targets tree
    assert [str(folder) for folder in values["incdir"]] == ["conda/targets/fake-arch/include"]
    # so was the runtime
    assert [str(folder) for folder in values["libdir"]] == ["conda/targets/fake-arch/lib"]
    # with its stem resolved
    assert values["libraries"] == ["cudart"]
    # and the compiler came from its own fragment
    assert values["compiler"] == "nvcc"
    assert [str(folder) for folder in values["bindir"]] == ["conda/bin"]
    # the prefix collapses to the environment root, the common root of all the pieces
    assert str(values["prefix"]) == "conda"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
