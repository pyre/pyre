#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The chronicler can suppress all output
    """
    # get the chronicler
    import journal

    # grab the current device
    device = journal.chronicler.device
    # ask for quiet
    journal.chronicler.quiet()
    # verify the default device is now a trash can
    assert journal.chronicler.device.name == "trash"
    # restore the device
    journal.chronicler.device = device

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
