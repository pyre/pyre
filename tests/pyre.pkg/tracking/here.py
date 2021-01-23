#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify that the location of the caller of a function is recorded correctly
    """
    # access the package
    import pyre.tracking

    # make a locator for this statement
    locator = pyre.tracking.here()

    # verify we got the correct type of locator
    assert isinstance(locator, pyre.tracking.script)
    # and that everything was recorded correctly
    assert locator.source == __file__
    assert locator.line == 16
    assert locator.function == 'test'

    # now, look up my caller
    locator = pyre.tracking.here(level=1)
    # verify we got the correct type of locator
    assert isinstance(locator, pyre.tracking.script)
    # and that everything was recorded correctly
    assert locator.source == __file__
    assert locator.line == 41
    assert locator.function == '<module>'

    # all done
    return locator


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
