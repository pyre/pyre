#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the common use case with a cpu timer
    """
    # access the timer bindings
    from pyre.extensions.pyre.timers import ProcessTimer

    # make a timer
    t = ProcessTimer(name="tests.timer")
    # start it
    t.start()

    # do something
    s = sum(range(10**6))

    # stop the timer
    t.stop()

    # get the journal
    import journal
    # make a channel
    channel = journal.debug(name="pyre.timers")
    # activate it
    # channel.activate()
    # log the elapsed time
    channel.log(f"elapsed: {t.ms()}ms")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
