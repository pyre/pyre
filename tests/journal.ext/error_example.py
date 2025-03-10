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
    from journal.ext.journal import Error as error

    # and the trash can
    from journal.ext.journal import Trash as trash

    # make a channel
    channel = error(name="test.journal.error")
    # send the output to trash
    channel.device = trash()
    # add some metadata
    channel.notes["time"] = "now"

    # carefully
    try:
        # inject
        channel.line("error:")
        # and flush with some additional metadata
        channel.log("    a nasty bug was detected", code=7)
        # shouldn't get here
        assert False, "unreachable"
    # if the correct exception was raised
    except channel.ApplicationError as error:
        # check the description
        assert str(error) == "test.journal.error: application error"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
