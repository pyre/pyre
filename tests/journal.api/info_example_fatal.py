#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the common case with a fatal channel
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.info(name="tests.journal.info")
    # make it fatal
    channel.fatal = True
    # send the output to the trash
    channel.device = journal.trash()

    # add some metadata
    channel.notes["time"] = "now"

    # we asked for this to be fatal, so carefully
    try:
        # to inject something
        channel.line("info channel:")
        channel.log("    hello world!")
        # this should be unreachable
        assert False, "unreachable"
    # if all goes well
    except channel.ApplicationError:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
