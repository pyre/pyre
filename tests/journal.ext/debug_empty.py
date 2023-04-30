#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that injecting an empty message is handled correctly
    """
    # get the channel
    from journal.ext.journal import Debug

    # make a channel
    channel = Debug(name="test.journal.debug")
    # activate it
    channel.activate()

    # inject an empty message
    channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
