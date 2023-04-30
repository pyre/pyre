#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the developer facing renderer
    """
    # get the renderer
    from journal.Bland import Bland as bland
    # the color spaces
    from journal.ANSI import ANSI
    # and a channel
    from journal.Debug import Debug as debug

    # get the chronicler metadata
    gmeta = debug.chronicler.notes
    # add some
    gmeta["application"] = "bland"
    gmeta["author"] = "michael"

    # make a channel
    channel = debug(name="tests.journal.debug")
    # generate a fake stack trace
    channel.notes["filename"] = "bland_sanity"
    channel.notes["line"] = 29
    channel.notes["function"] = "test"
    # add some metadata
    channel.notes["time"] = "now"
    channel.notes["device"] = "null"
    # inject
    channel.line("debug channel:")
    channel.line("    hello world!")

    # make a palette
    palette = {
        "reset": ANSI.x11("normal"),
        "channel": ANSI.x11("light slate gray"),
        "debug": ANSI.x11("steel blue"),
        "body": "",
        }

    # instantiate the renderer
    renderer = bland()
    # ask it to do its thing
    page = '\n'.join(renderer.render(palette=palette, entry=channel.entry))
    # and show me
    # print(page)

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
