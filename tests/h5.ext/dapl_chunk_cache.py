#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise opening a dataset with an access property list of one's own

    The raw data chunk cache is a property of the dataset access list, so a dataset opened
    with the library defaults gets whatever budget the file hands out. Handing an access list
    to the open is how a reader asks for something else: a budget sized for the chunks it
    means to revisit, rather than one sized for whoever happened to open the file.

    The cache belongs to the dataset rather than to the handle, and it is settled by the FIRST
    open. A second open of a dataset already in hand shares what the first one asked for,
    whichever way round they happen. Anyone tuning a cache therefore has to do it when the
    dataset is first reached, and this exercises the rule in both directions so that a change
    to it cannot pass unnoticed
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "dapl_chunk_cache.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # the layout
    chunk = [64, 64]

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=[256, 256])
    # the creation properties: chunked
    dcpl = libh5.properties.dcpl()
    dcpl.chunk = chunk
    # make the dataset
    f.create(path="product", type=libh5.types.native.double, space=space, dcpl=dcpl)
    # and let go of every handle, so the opens below start from nothing
    f.close()
    del f

    # the budget to ask for: room for sixteen chunks
    slots = 521
    budget = 16 * chunk[0] * chunk[1] * 8
    # an access list carrying it
    dapl = libh5.properties.dapl()
    dapl.chunkCache = libh5.properties.ChunkCache(slots, budget, 0.75)

    # take the dataset through it, on a file nobody else holds
    f = libh5.File(uri=uri, mode="r")
    tuned = f.dataset(path="product", dapl=dapl)
    # it reports the budget it was asked for
    cache = tuned.dapl.chunkCache
    assert cache.slots == slots
    assert cache.bytes == budget
    assert cache.preemption == 0.75
    # and the default it would otherwise have had is something else, or this proves nothing
    assert cache.bytes != libh5.properties.fapl().cache.bytes

    # a plain open of a dataset already in hand inherits what the first open asked for
    inherited = f.dataset(path="product")
    assert inherited.dapl.chunkCache.bytes == budget

    # let everything go
    f.close()
    del f, tuned, inherited, cache

    # and the same the other way round: a plain open first
    f = libh5.File(uri=uri, mode="r")
    plain = f.dataset(path="product")
    # takes the file's default
    assert plain.dapl.chunkCache.bytes == libh5.properties.fapl().cache.bytes
    # and a tuned open afterwards does NOT get what it asks for, because the dataset is
    # already open and its cache is already settled
    late = f.dataset(path="product", dapl=dapl)
    assert late.dapl.chunkCache.bytes != budget

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
