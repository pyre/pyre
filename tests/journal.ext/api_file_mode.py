#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Send all output from journal channels to a log file
    """
    # get the library
    import journal.ext.journal as libjournal

    # send all output to a log file
    libjournal.logfile(name="api_file_mode.log", mode="a")

    # make a channel
    channel = libjournal.Debug(name="test.journal.debug")
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
