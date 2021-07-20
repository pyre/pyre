#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Exercise adding multiple lines at once
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.debug(name="test.journal.debug")
    # activate it
    channel.activate()
    # but send the output to trash
    channel.device = journal.trash()

    # content in a tuple
    reptuple = (
        "report from tuple:",
        "  tuple line 1",
        "  tuple line 2",
    )

    # content in a list
    replist = [
        "report from list:",
        "  list line 1",
        "  list line 2",
    ]

    # content in a generator
    def repgen():
        yield "report from generator:"
        yield "  generator line 1"
        yield "  generator line 2"
        return

    # inject
    channel.report(report=reptuple)
    channel.report(report=replist)
    channel.report(report=repgen())
    # flush
    channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
