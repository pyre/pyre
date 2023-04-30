#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the simplest use case
    """
    # get the trash can
    from journal.Trash import Trash as trash
    # and the channel
    from journal.Warning import Warning as warning

    # make a warning channel
    channel = warning(name="tests.journal.warning")
    # send the output to trash
    channel.device = trash()

    # inject
    channel.log("hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
