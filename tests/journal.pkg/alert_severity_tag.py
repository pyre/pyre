#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    When no application name is registered, the alert header tags the message with the channel
    severity rather than the sentinel default
    """
    # get the renderer
    from journal.Alert import Alert as alert

    # and a channel
    from journal.Informational import Informational as info

    # reach the global metadata
    notes = info.chronicler.notes
    # leave the application unset, i.e. at the sentinel default the chronicler seeds
    notes["application"] = "journal"

    # make an info channel whose name differs from its severity, so the tag and the channel
    # name cannot be confused
    channel = info(name="tests.journal.flow")
    # put something on its page, since an empty page renders nothing
    channel.line("hello world!")

    # a palette with no color decorations, so the rendered text is the bare content
    palette = {"reset": "", "info": "", "body": ""}

    # render the header
    header = next(alert().header(palette=palette, entry=channel.entry))
    # the tag precedes the first space; the header has the form "{tag} ({channel}):"
    tag = header.split(" ", 1)[0]
    # with no application registered, the tag is the severity
    assert tag == "info", f"expected the severity 'info' as the tag, got '{tag}'"

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
