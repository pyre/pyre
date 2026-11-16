#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a channel whose hints do not name a kind of channel cannot be rebuilt
"""


def test():
    # access the package
    import pyre.ipc

    # hints that name a module that does not exist, a class that does not exist, and a class
    # that is not a channel
    for kind in ("nowhere.channels:Pipe", "pyre.ipc.Pipe:Tube", "pyre.ipc.Manifest:Manifest"):
        # carefully
        try:
            # attempt to rebuild a channel from them
            pyre.ipc.channel.arrive(hints={"kind": kind}, descriptors=[])
        # it cannot be done
        except pyre.ipc.exceptions.TravelError as error:
            # and the complaint names the kind
            assert error.kind == kind
        # anything else
        else:
            # is a failure
            assert False, f"a channel was rebuilt from '{kind}'"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
