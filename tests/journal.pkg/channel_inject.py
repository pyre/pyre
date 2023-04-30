#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# make sure the injection interface works as expected
def test():
    """
    Exercise a simple use case
    """
    # get the channel base class
    from journal.Channel import Channel

    # make one
    d1 = Channel(name="test.channel")

    # build a message
    d1.line("hello world!")
    d1.log()

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
