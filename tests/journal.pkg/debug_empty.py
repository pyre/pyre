#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that empty log messages get handled properly
    """
    # and the channel
    from journal.Debug import Debug as debug

    # make a debug channel
    channel = debug(name="tests.journal.debug")
    # activate it
    channel.activate()

    # inject an empty message
    channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
