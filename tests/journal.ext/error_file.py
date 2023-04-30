#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Send all error channel output to a log file
    """
    # get the channel
    from journal.ext.journal import Error as error

    # send output to a log file
    error.logfile("error_file.log")

    # make a channel
    channel = error(name="test.journal.error")
    # add some metadata
    channel.notes["time"] = "now"

    # carefully
    try:
        # inject
        channel.line("error:")
        channel.log("    a nasty bug was detected")
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
