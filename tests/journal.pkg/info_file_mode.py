#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Send all channel output to a log file
    """
    # get the channel
    from journal.Informational import Informational as info

    # send the output to a log file
    info.logfile(path="info_file_mode.log", mode="a")

    # make an info channel
    channel = info(name="tests.journal.info")
    # add some metadata
    channel.notes["time"] = "now"

    # inject
    channel.line("info channel:")
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
