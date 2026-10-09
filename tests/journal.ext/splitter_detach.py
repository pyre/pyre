#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test() -> None:
    """
    Verify that detaching a device from a splitter removes every one of its attachments
    """
    # access
    from journal import libjournal

    # make a few devices
    first = libjournal.Trash()
    second = libjournal.Trash()
    # make a splitter that holds the first one twice
    splitter = libjournal.Splitter(outputs=[first, second, first])
    # detach the first one
    splitter.detach(device=first)
    # only the second one is left
    assert list(splitter.outputs) == [second]
    # detaching a device that is not attached changes nothing
    splitter.detach(device=libjournal.Trash())
    # so the second one is still there
    assert list(splitter.outputs) == [second]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
