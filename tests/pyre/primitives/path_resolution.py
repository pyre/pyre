#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


"""
Exercise the path primitive
"""


def test():
    # the home of the factory
    import pyre.primitives

    # the location of this test
    cwd = pyre.primitives.path.cwd()
    # the location with the crazy links that {mm} prepared
    scratch = cwd / 'scratch'

    # a couple of easy ones
    # this is guaranteed by posix
    # assert cwd == cwd.resolve()
    # this is an absolute path with no links
    # assert scratch == scratch.resolve()

    # another good link
    here = scratch / 'here'
    # check
    # assert scratch == here.resolve()

    # another good link
    up = scratch / 'up'
    # check
    # assert cwd == up.resolve()

    # a cycle
    cycle = scratch / 'cycle'
    # check that
    try:
        # this fails
        print(cycle.resolve())
        # so we can't reach here
        assert False
    # further, check that
    except RuntimeError as error:
        # that it generates the correct report
        assert str(error) == "while resolving 'cycle': symbolic link loop at '{}'".format(cycle)

    # a loop
    loop = scratch / 'loop'
    # check that
    try:
        # this fails
        loop.resolve()
        # so we can't reach here
        assert False
    # further, check that
    except RuntimeError as error:
        # that it generates the correct report
        assert str(error) == "while resolving '{0}': symbolic link loop at '{0}'".format(loop)

    # a ramp
    ramp = scratch / 'ramp'
    # check that
    try:
        # this fails
        ramp.resolve()
        # so we can't reach here
        assert False
    # further, check that
    except RuntimeError as error:
        # that it generates the correct report
        assert str(error) == "while resolving 'cycle': symbolic link loop at '{0}'".format(cycle)

    # a two link cycle
    tic = scratch / 'tic'
    # check that
    try:
        # this fails
        tic.resolve()
        # so we can't reach here
        assert False
    # further, check that
    except RuntimeError as error:
        # that it generates the correct report
        assert str(error) == "while resolving 'tic': symbolic link loop at '{0}'".format(tic)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
