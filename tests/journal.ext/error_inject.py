#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Exercise the simplest use case
    """
    # get the channel
    from journal.ext.journal import Error as error
    # and the trash can
    from journal.ext.journal import Trash as trash

    # make a channel
    channel = error(name="test.journal.error")
    # send the output to trash
    channel.device = trash()
    # make the error non-fatal
    channel.fatal = False

    # inject
    channel.log("hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
