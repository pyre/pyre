#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Suppress all helps
    """
    # get the channel
    from journal.Help import Help as help

    # suppress the output
    help.quiet()

    # make a help channel
    channel = help(name="tests.journal.help")
    # add some metadata
    channel.notes["time"] = "now"

    # inject
    channel.line("help channel:")
    channel.log("    hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
