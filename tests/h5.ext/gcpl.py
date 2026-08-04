#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the group creation property list: its own settings, the object creation settings
    it inherits, and the group creation call that now accepts one
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "h5_ext_gcpl.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # a fresh group creation property list
    gcpl = libh5.properties.gcpl()

    # it inherits the settings that govern anything one creates
    assert isinstance(gcpl, libh5.properties.ocpl)
    # among them, whether modification times are recorded; they are, by default
    assert gcpl.trackTimes is True
    # turning them off is what makes two runs produce identical bytes
    gcpl.trackTimes = False
    assert gcpl.trackTimes is False

    # the attribute storage thresholds are inherited as well
    assert gcpl.attributePhaseChange == (8, 6)
    # and they are settable as a pair
    gcpl.attributePhaseChange = (16, 12)
    assert gcpl.attributePhaseChange == (16, 12)

    # its own settings start at the library defaults
    assert gcpl.linkPhaseChange == (8, 6)
    assert gcpl.estimatedLinkInfo == (4, 8)
    # a group expecting many members says so, so its object header is sized for them
    gcpl.linkPhaseChange = (32, 24)
    gcpl.estimatedLinkInfo = (64, 12)
    assert gcpl.linkPhaseChange == (32, 24)
    assert gcpl.estimatedLinkInfo == (64, 12)

    # the order of my members is not remembered, by default
    assert gcpl.linkCreationOrder == libh5.CreationOrder.none
    # ask for it to be recorded and indexed; hdf5 will not index an order it does not
    # track, so the two travel together as one state rather than as combinable flags
    gcpl.linkCreationOrder = libh5.CreationOrder.indexed
    assert gcpl.linkCreationOrder == libh5.CreationOrder.indexed

    # the shared default is reachable; it wraps hdf5's sentinel rather than a live list, so
    # it is something to hand to a create call, not something to interrogate
    assert libh5.properties.gcpl.default is not None

    # make a file
    f = libh5.File(uri=uri, mode="w")
    # create a group with my property list
    g = f.create(path="configured", gcpl=gcpl)
    # give it a couple of members, so the settings have something to govern
    g.create(path="alpha")
    g.create(path="beta")
    # they are both there
    assert "alpha" in g
    assert "beta" in g

    # creating a group without a property list still works, and takes the library defaults
    plain = f.create(path="plain")
    assert "plain" in f

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
