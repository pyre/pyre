#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Set the application name
    """
    # get the library
    import journal

    # make up a name
    name = "app"
    # register it
    journal.application(name)

    # get the chronicler's notes
    notes = journal.chronicler.notes
    # verify that the key is registered and has the correct value
    assert notes["application"] == name

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
