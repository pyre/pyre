#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Exercise the channel with a realistic example
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.warning(name="tests.journal.warning")
    # send the output to the trash
    channel.device = journal.trash()
    # add some metadata
    channel.notes["time"] = "now"

    # inject
    channel.line("warning channel:")
    # and flush with some additional metadata
    channel.log("    hello world!", code=7)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
