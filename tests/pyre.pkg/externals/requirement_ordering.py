#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Version comparison is componentwise numeric, not lexicographic
"""


def test():
    """
    Exercise the version ordering semantics
    """
    # support
    import pyre.externals

    # get the parser
    parse = pyre.externals.requirement.parse

    # components compare as numbers: lexicographically {1.9} > {1.12}, numerically it is below
    assert not parse("gsl>=1.12").accepts(version="1.9")
    # and {1.100} sorts above {1.12}, not between {1.1} and {1.2}
    assert parse("gsl>=1.12").accepts(version="1.100")

    # an alphabetic tail sorts a component above its bare base
    assert parse("gsl>1.14.6").accepts(version="1.14.6b")
    # a purely alphabetic component sorts below any numbered one
    assert not parse("gsl>=1.14.6").accepts(version="1.14.rc1")

    # a longer version sorts above its prefix
    assert parse("gsl>1.14").accepts(version="1.14.0")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
