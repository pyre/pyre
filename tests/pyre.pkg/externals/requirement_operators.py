#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Each version comparison operator accepts and rejects correctly
"""


def test():
    """
    Exercise every comparison operator in isolation
    """
    # support
    import pyre.externals

    # get the parser
    parse = pyre.externals.requirement.parse

    # equality accepts the exact version only
    assert parse("gsl==2.8").accepts(version="2.8")
    # and nothing longer
    assert not parse("gsl==2.8").accepts(version="2.8.1")

    # inequality accepts everything else
    assert parse("gsl!=2.8").accepts(version="2.9")
    # and rejects the exact version
    assert not parse("gsl!=2.8").accepts(version="2.8")

    # at-least accepts the boundary
    assert parse("gsl>=2.8").accepts(version="2.8")
    # and anything above
    assert parse("gsl>=2.8").accepts(version="2.9")
    # but nothing below
    assert not parse("gsl>=2.8").accepts(version="2.7")

    # at-most accepts the boundary
    assert parse("gsl<=2.8").accepts(version="2.8")
    # and rejects anything longer, which sorts above
    assert not parse("gsl<=2.8").accepts(version="2.8.1")

    # strictly-above rejects the boundary
    assert not parse("gsl>2.8").accepts(version="2.8")
    # and accepts anything longer
    assert parse("gsl>2.8").accepts(version="2.8.1")

    # strictly-below accepts smaller versions
    assert parse("gsl<2.8").accepts(version="2.7")
    # and rejects the boundary
    assert not parse("gsl<2.8").accepts(version="2.8")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
