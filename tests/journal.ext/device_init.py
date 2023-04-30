#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the device base class constructor is unavailable
    """
    # access
    from journal import libjournal

    # attempt to
    try:
        # instantiate a device
        libjournal.Device()
        # which is not allowed
        assert False, "unreachable"
    # if it fails
    except TypeError:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
