#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A channel that inherits the state of its parent keeps following the severity wide device
    """
    # get the trash can
    from journal.Trash import Trash as trash

    # and the channel
    from journal.Informational import Informational as info

    # install a severity wide device
    info.defaultDevice = trash()
    # make a parent while it is in place
    parent = info(name="tests.journal.cascade")
    # and a child that inherits its state
    child = info(name="tests.journal.cascade.child")
    # replace the severity wide device
    replacement = trash()
    info.defaultDevice = replacement
    # the child follows the new default
    assert child.device is replacement
    # and so does the parent
    assert parent.device is replacement

    # clean up
    info.defaultDevice = None

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
