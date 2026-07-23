#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Smoke test against the real host

Exercise the actual engine stack; hosts differ, so nothing is asserted about the outcome
beyond basic consistency: whatever is found must validate
"""


def test():
    """
    Ask the real engine stack for a few common packages
    """
    # support
    import pyre
    import pyre.externals

    # get the index
    index = pyre.externals.index()
    # the engine stack reflects the host description
    engines = index.engines()
    # every functional engine has a tag
    assert all(engine.name for engine in engines)

    # a few common categories
    for category in ("python", "gsl", "hdf5"):
        # get the protocol
        protocol = index.protocol(category=category)
        # realize it, if possible on this host
        installation = index.select(protocol=protocol)
        # if nothing was found
        if installation is None:
            # that's a legitimate outcome
            continue
        # whatever was found must have a home
        assert installation.prefix, f"'{category}' has no prefix"
        # and must survive validation
        assert not installation.pyre_configurationErrors, f"'{category}' misconfigured"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
