#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the index can discard its caches and rediscover

The configuration file {reset.yaml} restricts the host to the bare engine over the fixture
installation; long running processes call {reset} after adjusting the configuration, so the
index must drop both its selections and its engine stack and rebuild them on demand
"""

# support
import pyre


# the application
class reset(pyre.application):
    """
    An application that resets the index between selections
    """


def test():
    """
    Select, reset, and select again
    """
    # instantiate the application; this loads {reset.yaml}
    app = reset(name="reset")
    # get the index
    index = pyre.externals.index()
    # and the gsl protocol
    gsl = index.protocol(category="gsl")
    # realize it
    first = index.select(protocol=gsl)
    # the fixture must have been found
    assert first is not None
    # and both caches must be warm
    assert index._selections
    assert index._engines is not None

    # discard the caches
    index.reset()
    # both must be cold
    assert not index._selections
    assert index._engines is None

    # realize the category again
    second = index.select(protocol=gsl)
    # rediscovery must succeed
    assert second is not None
    # and produce the same configuration
    assert [str(f) for f in second.incdir] == [str(f) for f in first.incdir]
    assert list(second.libraries) == list(first.libraries)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
