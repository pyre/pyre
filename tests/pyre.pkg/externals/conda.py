#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the conda engine against a fixture environment

The fake environment in {conda/} carries an install record for gsl, so this test runs on any
host, whether conda is present or not
"""


def test():
    """
    Interpret the gsl recipe against the fixture environment
    """
    # support
    import pyre

    # the engine
    from pyre.platforms.Conda import Conda

    # the category
    from pyre.externals.supported.gsl.GSL import GSL

    # make an engine pointing at the fixture environment
    engine = Conda(name="conda.fixture", environment="conda")
    # it must be functional: the fixture has install records
    assert engine.available()
    # and its provenance phrase must name the environment it interrogates
    assert "in 'conda'" in engine.about()

    # the index must know about gsl
    installed = engine.installed()
    # by name
    assert "gsl" in installed
    # with the version encoded in the record filename
    version, build = engine.info(package="gsl")
    # check both
    assert version == "2.7.1"
    assert build == "h1a2b3c_0"

    # the contents come from the record, absolutized against the environment
    contents = tuple(engine.contents(package="gsl"))
    # there are three entries in the fixture record
    assert len(contents) == 3

    # get the gsl recipe
    recipe, *_ = GSL.recipes()
    # the engine must resolve it to the native package
    assert engine.resolve(recipe=recipe) == "gsl"

    # interpret the recipe
    values = engine.configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # with the version from the record
    assert values["version"] == "2.7.1"
    # the headers live in the fixture include directory
    assert [str(folder) for folder in values["incdir"]] == ["conda/include"]
    # the libraries live in the fixture lib directory
    assert [str(folder) for folder in values["libdir"]] == ["conda/lib"]
    # both stems resolve
    assert values["libraries"] == ["gsl", "gslcblas"]
    # the compile time markers come from the recipe
    assert values["defines"] == ["WITH_GSL", "HAVE_INLINE"]
    # and the prefix is the common root
    assert str(values["prefix"]) == "conda"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
