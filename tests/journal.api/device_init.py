#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the device base class is published as {device}, and not as {Device}
    """
    # access
    import journal

    # the device base class is published
    assert isinstance(journal.device, type)
    # but not under its implementation name, which may only name the module that holds it
    assert not isinstance(getattr(journal, "Device", None), type)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
