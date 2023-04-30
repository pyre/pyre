#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify we can suppress all channel output
    """
    # get the channel
    from journal.ext.journal import Help as help

    # suppress all output
    help.quiet()

    # make a help channel
    channel = help(name="tests.journal.help")
    # add some metadata
    channel.notes["time"] = "now"

    # inject
    channel.line("help channel:")
    channel.log("    hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
