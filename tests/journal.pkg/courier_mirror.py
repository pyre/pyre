#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A mirror sees every entry through its own sink, in order, whether or not the far end is there
    """
    # externals
    import os

    # access
    import journal

    # a capturing device
    class Capture(journal.device):
        # start with an empty log
        def __init__(self, **kwds):
            # chain up
            super().__init__(name="capture", **kwds)
            # nothing recorded yet
            self.calls = []

        # record which sink each entry reached, and what it said
        def alert(self, entry):
            # a user-facing alert
            self.calls.append(("alert", list(entry.page)))
            # all done
            return self

        def memo(self, entry):
            # a developer-facing memo
            self.calls.append(("memo", list(entry.page)))
            # all done
            return self

        def help(self, entry):
            # a help screen
            self.calls.append(("help", list(entry.page)))
            # all done
            return self

    # make a pipe
    reader, writer = os.pipe()
    # a mirror
    mirror = Capture()
    # a courier that also delivers to it
    courier = journal.courier(descriptor=writer, mirror=mirror)
    journal.chronicler.device = courier

    # log through three sinks
    journal.info("test.courier.mirror").log("one")
    debug = journal.debug("test.courier.mirror")
    debug.active = True
    debug.log("two")
    journal.help("test.courier.mirror").log("three")

    # the mirror saw all three, in order, through the right sinks
    assert mirror.calls == [("alert", ["one"]), ("memo", ["two"]), ("help", ["three"])]
    # and so did the far end
    assert courier.shipped == 3
    lines = os.read(reader, 64 * 1024).splitlines()
    assert [journal.record.decode(line).page for line in lines] == [["one"], ["two"], ["three"]]

    # take the far end away
    os.close(reader)
    # log again
    journal.info("test.courier.mirror").log("four")
    # the courier went quiet
    assert courier.dead
    # but the mirror still hears everything
    assert mirror.calls[-1] == ("alert", ["four"])

    # clean up
    courier.close()

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
