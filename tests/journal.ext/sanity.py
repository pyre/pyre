#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Sanity test: make sure the journal extension is accessible
    """
    # access
    import journal
    # verify the extension module exists
    assert journal.libjournal, "extension module not found"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
