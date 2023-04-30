#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that empty log messages get handled properly
    """
    # get the channel
    from journal.Warning import Warning as warning

    # make a warning channel
    channel = warning(name="tests.journal.warning")

    # inject an empty message
    channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
