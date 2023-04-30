#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Check that the color tables respond well when asked for color names that don't exist
    """
    # access the color map
    from journal.ANSI import ANSI

    # ask for a very strange color name
    assert ANSI.x11("a-very-unlikely-color-name") == ""

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
