#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise a fatal warning channel with a realistic example
    """
    # get the trash can
    from journal.ext.journal import Trash as trash
    # and the channel
    from journal.ext.journal import Warning as warning

    # make a warning channel
    channel = warning(name="tests.journal.warning")
    # make it fatal
    channel.fatal = True
    # send the output to trash
    channel.device = trash()

    # add some metadata
    channel.notes["time"] = "now"

    # we asked for this to be fatal, so carefully
    try:
        # inject something
        channel.line("warning channel:")
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
