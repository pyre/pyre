#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Verify that repeated access to the same channel does not accumulate extraneous material
    """
    # get the trash can
    from journal.Trash import Trash as trash
    # and the channel
    from journal.Error import Error as error

    # make an error channel
    channel = error(name="tests.journal.error")
    # send the output to trash
    channel.device = trash()

    # a few times
    for _ in range(10):
        # carefully
        try:
            # inject
            channel.log("hello world!")
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
