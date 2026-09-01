#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise direct chunk access: moving a chunk in the form it is stored in

    The ordinary read hands over cells, which means inflating the chunk and converting it. The
    direct read hands over the chunk exactly as it sits in the file, filter pipeline and all,
    and the direct write puts such bytes back without filtering them again. Between them they
    let a chunk be moved, or held somewhere, without ever being decoded.

    The library insists that these two calls be given the chunk's own corner, unlike the chunk
    table, which accepts any cell of a chunk. Pinning that difference matters, because we hide
    it: {readChunk} and {writeChunk} snap the cell for the caller so the whole chunk family
    can be addressed the same way
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and a payload
    import os
    import array

    # and for muzzling the complaints the guarded calls below are meant to raise
    import journal

    # a scratch data product
    uri = "direct_chunk.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # the layout: an extent that is not a whole number of chunks, so the tiling has an edge
    extent = [200, 200]
    chunk = [64, 64]
    cells = chunk[0] * chunk[1]
    # what a chunk would occupy if nothing were done to it
    raw = cells * 8

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=extent)
    # the creation properties: chunked and compressed, so that stored form and cell form
    # genuinely differ and a test cannot pass by confusing the two
    dcpl = libh5.properties.dcpl()
    dcpl.chunk = chunk
    dcpl.addShuffle()
    dcpl.addDeflate(4)
    # a dataset to write, and an identical one to move a chunk into
    src = f.create(path="src", type=libh5.types.native.double, space=space, dcpl=dcpl)
    dst = f.create(path="dst", type=libh5.types.native.double, space=space, dcpl=dcpl)
    # and a contiguous one, for the question that is ill posed
    flat = f.create(path="flat", type=libh5.types.native.double, space=space)

    # something that does not compress away to nothing; a regular sequence would be crushed
    # and the stored size would stop being interesting
    def noise():
        """
        Generate {cells} pseudo random values, deterministically
        """
        # a seed
        state = 0x2545F4914F6CDD1D
        # go through the cells
        for _ in range(cells):
            # advance the sequence
            state = (state * 6364136223846793005 + 1442695040888963407) % (2**64)
            # and hand back its high bits
            yield float(state >> 32)

    payload = array.array("d", noise())
    # write one interior chunk the ordinary way
    src.write(payload, libh5.types.native.double, [0, 0], chunk)

    # now take that chunk out in the form it is stored in
    mask, stored = src.readChunk(origin=[0, 0])
    # what came back is the compressed form, not the cells: the chunk table agrees with its
    # length, and it is smaller than the cells would be
    assert len(stored) == src.chunkAt(origin=[0, 0]).bytes
    assert len(stored) < raw
    # nothing in the pipeline was skipped for this chunk
    assert mask == 0

    # the library would refuse a cell that is not the chunk's corner; we snap it, so any cell
    # of the chunk names it, exactly as it does for the chunk table
    interiorMask, interior = src.readChunk(origin=[5, 5])
    assert interior == stored
    assert interiorMask == mask

    # put those bytes down in the other dataset without ever decoding them
    dst.writeChunk(origin=[0, 0], filterMask=mask, data=stored)

    # and read it back the ordinary way: the cells have to survive the trip
    check = array.array("d", bytes(raw))
    dst.read(check, libh5.types.native.double, [0, 0], chunk)
    assert check[0] == payload[0]
    assert check[cells // 2] == payload[cells // 2]
    assert check[cells - 1] == payload[cells - 1]

    # a chunk nobody wrote has no stored form to hand over, and that is the answer rather
    # than a failure
    assert src.readChunk(origin=[128, 128]) is None

    # the question is ill posed for a dataset that is not stored as chunks
    assert flat.readChunk(origin=[0, 0]) is None

    # a cell outside the extent is refused rather than mistaken for an empty chunk; muzzle
    # the complaint so the suite stays silent on success
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

    assert declined(lambda: src.readChunk(origin=[999, 999]))

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
