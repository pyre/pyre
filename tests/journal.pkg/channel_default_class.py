#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The severity wide defaults are accessible from the channel class and its instances
    """
    # get the trash can
    from journal.Trash import Trash as trash

    # and the channel
    from journal.Informational import Informational as info

    # the defaults are visible on the class
    assert info.defaultActive is True
    assert info.defaultFatal is False
    # the default device can be set on the class
    info.defaultDevice = trash()
    # read back from it
    device = info.defaultDevice
    assert device.name == "trash"
    # and seen by the instances
    channel = info(name="tests.journal.default")
    assert channel.defaultDevice is device
    assert channel.defaultActive is True
    assert channel.defaultFatal is False
    # the other spelling sees the same device
    assert info.getDefaultDevice() is device

    # the activation default is read only
    try:
        # so attempting to change it
        info.defaultActive = False
        # should fail
        assert False, "unreachable"
    # if all goes well
    except AttributeError:
        # no problem
        pass

    # clean up
    info.defaultDevice = None

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
