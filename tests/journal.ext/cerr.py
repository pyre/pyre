#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the error console is available
    """
    # access
    from journal import libjournal

    # make a console that's tied to {cerr}
    console = libjournal.ErrorConsole()
    # verify its name is what we expect
    assert console.name == "cerr"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
