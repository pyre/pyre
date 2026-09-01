#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the chunk table of a chunked dataset

    A chunked dataset is diced into tiles, but only the tiles somebody wrote are stored. The
    chunk table is the library's record of which ones those are, and asking it is far cheaper
    than reading: a region whose chunks are absent is pure fill, and a reader that knows this
    can skip the work entirely rather than inflate a chunk of fill values.

    The table lists only the chunks that exist, so an index into it is a cursor and not a
    durable address, and it is ordered by chunk origin rather than by the order the chunks
    were written. This writes its two chunks out of logical order so that a change to either
    of those properties cannot pass unnoticed
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and a payload
    import os
    import array

    # and for muzzling the complaints the guarded calls below are meant to raise
    import journal

    # a scratch data product
    uri = "chunk_table.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # the layout: a raster diced into sixteen chunks, of which we will write two
    extent = [256, 256]
    chunk = [64, 64]
    cells = chunk[0] * chunk[1]
    # a double is eight bytes, and nothing here is filtered, so a stored chunk is exactly
    # this big; anything else means the pipeline changed under us
    footprint = cells * 8

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=extent)
    # the creation properties: chunked
    dcpl = libh5.properties.dcpl()
    dcpl.chunk = chunk
    # make the chunked dataset
    chunked = f.create(path="chunked", type=libh5.types.native.double, space=space, dcpl=dcpl)
    # and a contiguous one beside it, so the questions that are ill posed for it can be asked
    flat = f.create(path="flat", type=libh5.types.native.double, space=space)

    # something to write
    payload = array.array("d", (float(cell) for cell in range(cells)))
    # write two chunks, and deliberately in the wrong order: the one further along the raster
    # goes down first, so that write order and logical order disagree
    chunked.write(payload, libh5.types.native.double, [64, 64], chunk)
    chunked.write(payload, libh5.types.native.double, [0, 0], chunk)

    # two of the sixteen tiles have been written, and only those are in the table
    assert chunked.chunks == 2

    # the table is ordered by origin, not by the order the chunks were laid down; if it were
    # write order, these two would come back the other way round
    first = chunked.chunk(index=0)
    second = chunked.chunk(index=1)
    assert first.origin == [0, 0]
    assert second.origin == [64, 64]
    # both are really there
    assert first.bytes == footprint
    assert second.bytes == footprint
    # nothing was filtered, so no stage was skipped
    assert first.filterMask == 0

    # a chunk can be named by any of its cells, not just its corner, and it reports its own
    # origin rather than the cell it was asked about
    interior = chunked.chunkAt(origin=[70, 70])
    assert interior.origin == [64, 64]
    assert interior.address == second.address

    # a tile nobody wrote has no entry, and that is the answer rather than a failure: it says
    # the region is pure fill
    assert chunked.chunkAt(origin=[128, 128]) is None

    # the questions are ill posed for a dataset that is not stored as chunks, and both of them
    # say so rather than letting the library raise
    assert flat.chunks is None
    assert flat.chunkAt(origin=[0, 0]) is None

    # the lookups that are given something unusable complain and decline to answer; muzzle
    # the complaint so the rest of this can run, and so the suite stays silent on success
    channel = journal.error("pyre.h5")
    channel.device = journal.trash()
    channel.fatal = False

    # the guarded calls below complain on the {pyre.h5} error channel and decline to answer.
    # whether such a complaint also stops the application is a policy the application sets,
    # not part of what the guard promises, and the muzzle above does not reach the c++ side
    # of every build. so treat a refusal and a raised complaint as the same outcome: what is
    # being tested is that the guard saw the bad input, not what the application does about it
    def declined(call):
        """
        Report whether the guard turned {call} away
        """
        # make the call
        try:
            # a guard that declined hands back nothing
            return call() is None
        # and one whose complaint was fatal never returns at all
        except journal.ApplicationError:
            # which is the same news
            return True

    # an index past the end of the table names nothing; the table is as long as the number of
    # chunks written, not as long as the tiling, so this is a moving target and worth saying
    assert declined(lambda: chunked.chunk(index=2))

    # the library does not bounds check the by-coordinate lookup: it answers a coordinate that
    # cannot exist exactly the way it answers a chunk nobody wrote, which would make "outside
    # the raster" and "pure fill" indistinguishable. so we check for it ourselves
    assert declined(lambda: chunked.chunkAt(origin=[999, 999]))
    # and a coordinate of the wrong rank cannot even be checked, let alone used
    assert declined(lambda: chunked.chunkAt(origin=[0]))

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
