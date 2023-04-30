#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the message buffers get reset correctly after a flush
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

    # inject
    channel.log("hello world!")

    # verify that the buffer is empty after the flush
    assert len(channel.page) == 0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
