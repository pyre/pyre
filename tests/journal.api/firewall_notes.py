#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify access to the channel metadata
    """
    # access
    import journal

    # make a firewall channel
    channel = journal.firewall("test.channel")
    # get its metadata
    notes = channel.notes
    # adjust the application name
    notes["application"] = "firewall_notes"
    # add something
    notes["author"] = "michael"

    # make sure the adjustments stick by asking for the notes once again; this step is
    # non-trivial: if support is provided by the C++ library, it ensures that the notes are
    # mutable
    notes = channel.notes
    # and comparing against expectations
    assert notes["application"] == "firewall_notes"
    assert notes["author"] == "michael"
    assert notes["channel"] == "test.channel"
    assert notes["severity"] == "firewall"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
