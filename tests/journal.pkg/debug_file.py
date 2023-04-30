#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Send all channel output to a log file
    """
    # access the channel
    from journal.Debug import Debug as debug

    # send the output to a log file
    debug.logfile("debug_file.log")

    # make a channel
    channel = debug(name="tests.journal.debug")
    # activate it
    channel.activate()
    # add some metadata
    channel.notes["time"] = "now"

    # inject
    channel.line("debug channel:")
    channel.log("    hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
