#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# access to the global device
def test():
    """
    Exercise getting/setting the global device
    """
    # get the chronicler
    from journal.Chronicler import Chronicler as chronicler
    # and the trash can
    from journal.Trash import Trash as trash

    # make a new device
    custom = trash()
    # install it
    chronicler.device = custom

    # verify that it was installed correctly
    assert chronicler.device is custom

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
