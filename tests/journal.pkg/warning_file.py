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
    from journal.Warning import Warning as warning

    # send the output to a log file
    warning.logfile("warning_file.log")

    # make a warning channel
    channel = warning(name="tests.journal.warning")
    # add some metadata
    channel.notes["time"] = "now"

    # inject
    channel.line("warning channel:")
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
