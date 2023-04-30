#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the channel buffers get flushed properly after {log}
    """
    # get the trash can
    from journal.Trash import Trash as trash
    # and the channel
    from journal.Debug import Debug as debug

    # make a debug channel
    channel = debug(name="tests.journal.debug")
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
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
