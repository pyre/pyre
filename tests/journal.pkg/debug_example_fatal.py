#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise a fatal debug channel with a realistic example
    """
    # access the parts
    from journal.Trash import Trash as trash
    from journal.Debug import Debug as debug

    # make a debug channel
    channel = debug(name="tests.journal.debug")
    # activate it
    channel.active = True
    # make it fatal
    channel.fatal = True
    # but send the output to trash
    channel.device = trash()

    # add some metadata
    channel.notes["time"] = "now"

    # we asked for this to be fatal, so carefully
    try:
        # inject something
        channel.line("debug channel:")
        channel.log("    hello world!")
        # this should be unreachable
        assert False, "unreachable"
    # if all goes well, the channel raised an error
    except channel.DebugError:
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
