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
    from journal.Error import Error as error

    # make an error channel
    channel = error(name="tests.journal.error")

    # carefully
    try:
        # inject an empty message
        channel.log()
        # shouldn't get here
        assert False, "unreachable"
    # if the correct exception was raised
    except channel.ApplicationError as error:
        # all  good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
