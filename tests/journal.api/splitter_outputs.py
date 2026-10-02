#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that a splitter built with {outputs} forwards to each of them
    """
    # access
    import journal

    # make two devices
    first = journal.trash()
    second = journal.trash()
    # and a splitter that forwards to both
    splitter = journal.splitter(outputs=[first, second])
    # check that it knows about them, in order
    assert list(splitter.outputs) == [first, second], splitter.outputs

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
