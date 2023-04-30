#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can send channel output to a log file
    """
    # pick a file name
    filename = "file_example.log"

    # get the device
    from journal.File import File
    # and a channel
    from journal.Debug import Debug

    # instantiate
    device = File(path=filename)

    # make a debug channel
    channel = Debug(name="tests.journal.debug")
    # activate it
    channel.activate()
    # send the output to the file
    channel.device = device

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
