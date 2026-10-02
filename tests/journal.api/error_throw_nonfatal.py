#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A non-fatal error channel hands back the exception it would have raised
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.error(name="tests.journal.error")
    # send the output to the trash
    channel.device = journal.trash()
    # make it non-fatal
    channel.fatal = False

    # carefully
    try:
        # raise what the channel hands back
        raise channel.log("the input is unusable")
    # if it is the right exception
    except channel.ApplicationError:
        # all good
        pass

    # the entry was flushed after it was recorded
    assert len(channel.page) == 0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
