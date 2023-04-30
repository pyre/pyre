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
    from journal.ext.journal import Informational as info

    # suppress all output
    info.quiet()

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
    # run the test
    test()


# end of file
