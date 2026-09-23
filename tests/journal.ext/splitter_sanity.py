#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that a splitter can be made and devices attached to it
    """
    # access
    import journal

    # make a splitter
    splitter = journal.splitter()
    # check its name
    assert splitter.name == "splitter"
    # it starts out with no devices
    assert len(splitter.outputs) == 0
    # attach a couple
    splitter.attach(journal.trash()).attach(journal.trash())
    # and they are there
    assert len(splitter.outputs) == 2
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
