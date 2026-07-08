#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Booting pyre with the pure-python journal installs a real console through the boot handoff,
    replacing the bootstrap buffer journal used while the framework was still coming up
    """
    # force the pure-python journal before anything imports it
    import __main__

    __main__.journal_no_libjournal = True

    # booting the framework drives the whole sequence: while {pyre.executive} is None journal
    # collects into a boot device, then pyre hands off to a real console and publishes the
    # executive
    import pyre
    import journal

    # the console and the boot device, to check which one we ended up with
    from journal.Console import Console
    from journal.BootDevice import BootDevice

    # we exercised the pure-python journal, the path the bootstrapper uses
    assert journal.without_libjournal is True
    # pyre finished booting, so the executive is published
    assert pyre.executive is not None
    # and the handoff swapped the bootstrap buffer for a real console
    device = journal.chronicler.device
    assert isinstance(device, Console)
    assert not isinstance(device, BootDevice)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
