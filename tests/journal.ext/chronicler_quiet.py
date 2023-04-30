#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can suppress all journal output
    """
    # get the chronicler
    from journal.ext.journal import Chronicler as chronicler
    # get the channel
    from journal.ext.journal import Debug as debug

    # quiet all channels
    chronicler.quiet()

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
