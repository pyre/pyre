#!/usr/bin/env python3
# -*- python -*-
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

    # the property namespace, which is where the records live
    p = libh5.properties

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "h5_ext_gcpl.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        # by removing it
        os.remove(uri)

    # a fresh group creation property list
    gcpl = libh5.properties.gcpl()

    # it inherits the settings that govern anything one creates
    assert isinstance(gcpl, libh5.properties.ocpl)
    # among them, whether modification times are recorded; they are, by default
    assert gcpl.timeTracking is True
    # turning them off is what makes two runs produce identical bytes
    gcpl.timeTracking = False
    # and the list remembers
    assert gcpl.timeTracking is False

    # the attribute storage thresholds are inherited as well
    assert (gcpl.attributePhaseChange.maxCompact, gcpl.attributePhaseChange.minDense) == (8, 6)
    # and they are settable as a pair
    gcpl.attributePhaseChange = p.PhaseChange(maxCompact=16, minDense=12)
    # and the list remembers
    assert gcpl.attributePhaseChange.maxCompact == 16

    # its own settings start at the library defaults: the link storage thresholds
    assert (gcpl.linkPhaseChange.maxCompact, gcpl.linkPhaseChange.minDense) == (8, 6)
    # and the estimate of its membership
    assert (gcpl.estimatedLinkInfo.links, gcpl.estimatedLinkInfo.nameLength) == (4, 8)
    # a group expecting many members says so, so its object header is sized for them: it
    # keeps more links in compact form
    gcpl.linkPhaseChange = p.PhaseChange(maxCompact=32, minDense=24)
    # and expects more of them
    gcpl.estimatedLinkInfo = p.LinkEstimate(links=64, nameLength=12)
    # the list remembers the thresholds
    assert gcpl.linkPhaseChange.maxCompact == 32
    # and the estimate
    assert gcpl.estimatedLinkInfo.links == 64

    # the order of my members is not remembered, by default
    assert gcpl.linkCreationOrder == libh5.CreationOrder.none
    # ask for it to be recorded and indexed; hdf5 will not index an order it does not
    # track, so the two travel together as one state rather than as combinable flags
    gcpl.linkCreationOrder = libh5.CreationOrder.indexed
    # and the list remembers
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
    # and another
    g.create(path="beta")
    # they are both there: the first
    assert "alpha" in g
    # and the second
    assert "beta" in g

    # creating a group without a property list still works, and takes the library defaults
    f.create(path="plain")
    # so the group is there
    assert "plain" in f

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
