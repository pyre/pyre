#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


def test():
    """
    Verify that repeated use of the same channel instance works correctly
    """
    # get the channel
    from journal.ext.journal import Error as error
    # and the trash can
    from journal.ext.journal import Trash as trash

    # make a channel
    channel = error(name="test.journal.error")
    # make it non-fatal
    channel.fatal = False
    # send the output to trash
    channel.device = trash()

    # a few times
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
