#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the journal global state
def test():
    """
    Verify the default global settings
    """
    # get the console
    from journal.Console import Console as cout
    # and the chronicler
    from journal.Chronicler import Chronicler as chronicler

    # ask it for its metadata
    meta = chronicler().notes
    # verify that the table comes with only one setting
    assert len(meta) == 1
    # that is the default application name
    assert meta["application"] == "journal"

    # get the default device
    device = chronicler().device
    # verify it's an instance of {cout}
    assert isinstance(device, cout)
    # and that it is named correctly
    assert device.name == "cout"

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
