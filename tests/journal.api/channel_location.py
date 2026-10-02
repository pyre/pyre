#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that an entry made through the bindings records where it was made without reading
    any source files
    """
    # externals
    import os
    import sys

    # get the journal
    import journal

    # make a pipe
    reader, writer = os.pipe()
    # make a courier on its write end
    courier = journal.courier(descriptor=writer)
    # and make it the default device
    journal.chronicler.device = courier
    # make a channel
    channel = journal.info("test.journal.location")

    # the files the test opens
    opened = []

    # record the files that get opened
    def hook(event, args):
        """
        Watch for file opens
        """
        # if a file is being opened
        if event == "open":
            # record it
            opened.append(args[0])
        # all done
        return

    # watch
    sys.addaudithook(hook)
    # the line of the entry below
    line = sys._getframe().f_lineno + 2
    # make an entry
    channel.log("hello world!")

    # read the record
    record = journal.record.decode(os.read(reader, 64 * 1024))
    # check that it recorded where it was made
    assert record.notes["filename"] == __file__
    assert record.notes["line"] == str(line)
    assert record.notes["function"] == "test"
    # and that nothing was read to find out
    assert not opened, opened

    # clean up
    courier.close()
    os.close(reader)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
