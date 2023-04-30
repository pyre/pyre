#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the usual test case with an non-fatal channel
    """
    # get the journal
    import journal

    # make an error channel
    channel = journal.error(name="tests.journal.error")
    # make it non-fatal
    channel.fatal = False
    # send the output to the trash
    channel.device = journal.trash()

    # add some metadata
    channel.notes["time"] = "now"

    # carefully
    try:
        # inject
        channel.line("error channel:")
        channel.log("    hello world!")
    # if the correct exception was raised
    except channel.ApplicationError as error:
        # shouldn't get here
        assert False, "unreachable"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
