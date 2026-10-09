#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that python reaches the cells of a tile through a type-erased grid: read only when it
reads, writable when it writes, and that asking to write marks what depends on the tile as stale
"""


def test():
    # the flow bindings
    from pyre.extensions.pyre import flow

    # get the catalog
    catalog = flow.catalog()
    # find the normalizer
    (entry,) = [e for e in catalog.factories.values() if e.className == "Parametric"]
    # make one, and the tiles it takes
    normalizer = catalog.makeFactory(decl=entry.decl, name="normalizer")
    signal = catalog.makeProduct(decl=entry.slots[0].product, name="signal", shape=(2, 2))
    normalized = catalog.makeProduct(decl=entry.slots[1].product, name="normalized", shape=(2, 2))
    # wire them
    normalizer.bind(slot="signal", product=signal)
    normalizer.bind(slot="normalized", product=normalized)
    # map [0,4] onto [0,1]
    normalizer.set(setting="interval", value=(0, 4))

    # the catalog makes tiles with every cell zero
    assert all(normalized.read()[i, j] == 0 for i in range(2) for j in range(2))
    # pulling made the output fresh
    assert not normalized.stale

    # asking to write the signal
    cells = signal.write()
    # marks the output stale
    assert normalized.stale
    # and hands out cells python can write
    assert cells.writable
    # so fill them
    for i in range(2):
        # one line at a time
        for j in range(2):
            # with 0, 1, 2, 3
            cells[i, j] = 2 * i + j
    # pull the output
    view = normalized.read()
    # which python can only read
    assert not view.writable
    # and holds the normalized signal
    assert [view[i, j] for i in range(2) for j in range(2)] == [0, 0.25, 0.5, 0.75]

    # take the graph apart
    normalizer.unbind(slot="signal")
    normalizer.unbind(slot="normalized")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
