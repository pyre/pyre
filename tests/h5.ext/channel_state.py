#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that channel state set from python is seen inside another extension module: a channel
    deactivated here must stay quiet when the h5 bindings log to it

    The journal keeps the state of a channel in a static owned by the library; a build that lets
    every extension module carry its own copy of that static splits the state, and a channel
    quieted here would still fire inside the module
    """
    # the h5 bindings
    from pyre.extensions import libh5

    # the journal
    import journal

    # the bindings complain on this channel when asked for a mode they do not support; the
    # channel is fatal by default, so the request would raise; quiet it from python
    channel = journal.error("pyre.h5.file")
    channel.active = False
    # ask for a file in a mode the bindings do not support; no file is touched
    f = libh5.File(uri="channel_state.h5", mode="bogus")
    # if the deactivation reached the channel inside the module, the bindings returned a stub
    # rather than raising
    assert isinstance(f, libh5.File)
    # restore the channel
    channel.active = True

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
