#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise a non-fatal error channel with a realistic example
    """
    # get the trash can
    from journal.ext.journal import Trash as trash
    # and the channel
    from journal.ext.journal import Error as error

    # make an error channel
    channel = error(name="tests.journal.error")
    # make it non-fatal
    channel.fatal = False
    # send the output to trash
    channel.device = trash()

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
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
