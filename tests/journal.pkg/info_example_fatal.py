#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise a fatal info channel with a realistic example
    """
    # get the trash can
    from journal.Trash import Trash as trash
    # and the channel
    from journal.Informational import Informational as info

    # make an info channel
    channel = info(name="tests.journal.info")
    # make it fatal
    channel.fatal = True
    # send the output to trash
    channel.device = trash()

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
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
