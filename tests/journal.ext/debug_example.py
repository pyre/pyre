#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Exercise the common use case
    """
    # get the channel
    from journal.ext.journal import Debug as debug

    # and the trash can
    from journal.ext.journal import Trash as trash

    # make a channel
    channel = debug(name="test.journal.debug")
    # activate it
    channel.activate()
    # but send the output to trash
    channel.device = trash()

    # add some metadata
    channel.notes["time"] = "now"

    # inject
    channel.line("debug channel:")
    # and flush with some additional metadata
    channel.log("    hello world!", code=7)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
