#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Send all output from {debug} channels to a log file
    """
    # get the channel
    from journal.ext.journal import Debug as debug

    # send all output to a log file
    debug.logfile(name="debug_file_mode.log", mode="a")

    # make a channel
    channel = debug(name="test.journal.debug")
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
    # run the test
    test()


# end of file
