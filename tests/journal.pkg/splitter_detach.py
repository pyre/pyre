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
    import journal

    # make a few devices
    first = journal.trash()
    second = journal.trash()
    # make a splitter that holds the first one twice
    splitter = journal.splitter(outputs=[first, second, first])
    # detach the first one
    splitter.detach(device=first)
    # only the second one is left
    assert splitter.outputs == [second]
    # detaching a device that is not attached changes nothing
    splitter.detach(device=journal.trash())
    # so the second one is still there
    assert splitter.outputs == [second]

    # all done
    return


# main
if __name__ == "__main__":
    # skip the bindings, so the pure python implementation is exercised
    journal_no_libjournal = True
    # run the test
    test()


# end of file
