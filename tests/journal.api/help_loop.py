#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Verify that repeated access to the same channel does not accumulate extraneous material
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.help(name="tests.journal.help")
    # send the output to the trash
    channel.device = journal.trash()

    # for a few times
    for _ in range(10):
        # inject
        channel.log("hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
