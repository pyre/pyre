#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Content extractors feed the bare engine, which has no database to consult
"""


def test():
    """
    Resolve gsl through the bare engine and verify the header supplied the version
    """
    # the engine
    from pyre.platforms.Bare import Bare

    # the index class
    from pyre.externals.Index import Index

    # make a private index over an engine that probes only the fixture
    index = Index()
    # wire it
    index._engines = (Bare(name="bare.fixture.proof", searchpath=["prefix"]),)
    # resolve
    report = index.resolve(requested=["gsl"])
    # the fixture's version header supplied what no database could
    assert report.selections["gsl"].version == "2.8"
    # and satisfies version demands on another index over the same engine
    index = Index()
    # wire it
    index._engines = (Bare(name="bare.fixture.proof.demand", searchpath=["prefix"]),)
    # resolve with a version window the harvested version satisfies
    report = index.resolve(requested=["gsl>=2.5,<3"])
    # the demand was proven against the harvested version
    assert "gsl" in report.selections

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
