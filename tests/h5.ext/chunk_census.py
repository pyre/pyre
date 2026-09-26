#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the census of the chunk table: every chunk that was written, in one pass

    The census has to agree with the lookups that name one chunk at a time: the same chunks,
    at the same origins, addresses, and sizes, and none of the ones nobody wrote. The chunks go
    down out of logical order, so an origin reported in the wrong units, or a census that
    lists chunks by the order they were written, cannot pass unnoticed
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and a payload
    import os
    import array

    # a scratch data product
    uri = "chunk_census.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        # by removing it
        os.remove(uri)

    # the layout: a raster diced into twelve chunks that are not square
    extent = [256, 192]
    chunk = [64, 48]
    cells = chunk[0] * chunk[1]

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=extent)
    # the creation properties: chunked
    dcpl = libh5.properties.dcpl()
    dcpl.chunk = chunk
    # make the chunked dataset
    chunked = f.create(path="chunked", type=libh5.types.native.double, space=space, dcpl=dcpl)
    # another one, chunked the same way, that nobody writes into
    empty = f.create(path="empty", type=libh5.types.native.double, space=space, dcpl=dcpl)
    # and a contiguous one, which has no chunk table at all
    flat = f.create(path="flat", type=libh5.types.native.double, space=space)

    # something to write
    payload = array.array("d", (float(cell) for cell in range(cells)))
    # the chunks to write, deliberately not in the order of their origins
    written = [[192, 144], [0, 48], [128, 0]]
    # write them
    for origin in written:
        # one at a time
        chunked.write(payload, libh5.types.native.double, origin, chunk)

    # take the census
    census = chunked.chunkTable()
    # it holds exactly the chunks that were written
    assert len(census) == len(written) == chunked.chunks
    # at the origins they were written at, in cells rather than in chunks
    assert sorted(entry.origin for entry in census) == sorted(written)
    # and each entry agrees with the lookup that names that one chunk
    for entry in census:
        # look it up by its origin
        single = chunked.chunkAt(origin=entry.origin)
        # it is the same chunk
        assert single.address == entry.address
        assert single.bytes == entry.bytes
        assert single.filterMask == entry.filterMask

    # a chunked dataset nobody wrote into has a table, and it is empty
    assert empty.chunkTable() == []
    # a dataset that is not stored as chunks has no table at all
    assert flat.chunkTable() is None

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
