#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the info channel with a realistic example
    """
    # get the trash can
    from journal.ext.journal import Trash as trash

    # and the channel
    from journal.ext.journal import Informational as info

    # make an info channel
    channel = info(name="tests.journal.info")
    # send the output to trash
    channel.device = trash()

    # add some metadata
    channel.notes["time"] = "now"
    # inject
    channel.line("info channel:")
    # and flush with some additional metadata
    channel.log("    hello world!", code=7)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
