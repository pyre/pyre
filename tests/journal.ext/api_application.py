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
    from journal import libjournal

    # make up a name
    name = "app"
    # register it
    libjournal.application(name)

    # get the chronicler's notes
    notes = libjournal.chronicler.notes
    # verify that the key is registered and has the correct value
    assert notes["application"] == name

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
