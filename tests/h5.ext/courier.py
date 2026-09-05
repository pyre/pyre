#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    An entry flushed by compiled code reaches a courier installed from python

    The h5 bindings refuse a stride that does not speak for every axis by flushing an error
    channel from C++. That entry has to reach whatever device the chronicler holds, so a
    courier installed on the chronicler must ship it like any other
    """
    # get the bindings
    from pyre.extensions import libh5

    # for the pipe, a scratch path, and a payload
    import os
    import array

    # the journal
    import journal

    # a scratch data product
    uri = "courier.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)
    # make the file
    f = libh5.File(uri=uri, mode="w")
    # with a small raster
    extent = [8, 8]
    space = libh5.DataSpace(shape=extent)
    src = f.create(path="src", type=libh5.types.native.double, space=space)
    # laid down the ordinary way
    payload = array.array("d", (float(cell) for cell in range(extent[0] * extent[1])))
    src.write(payload, libh5.types.native.double, [0, 0], extent)

    # make a pipe
    reader, writer = os.pipe()
    # a courier on its write end
    courier = journal.courier(descriptor=writer)
    # installed as the default device
    journal.chronicler.device = courier
    # the complaint is on an error channel, which is fatal; let it speak but not abort
    channel = journal.error("pyre.h5")
    channel.fatal = False

    # ask for a stride that does not speak for every axis
    scratch = array.array("d", bytes(4 * 8))
    # the complaint may still be raised across the language boundary
    try:
        src.read(scratch, libh5.types.native.double, [0, 0], [2, 2], [2])
    except journal.ApplicationError:
        pass
    # nothing was read
    assert scratch[0] == 0.0

    # the entry made it out
    assert courier.shipped == 1
    # read it back
    line = os.read(reader, 64 * 1024)
    record = journal.record.decode(line)
    # it came from the C++ channel
    assert record.channel == "pyre.h5"
    assert record.severity == "error"
    assert record.sink == "alert"
    # with the page the compiled code wrote
    assert record.page[0] == "the stride does not match the shape of the tile"
    # and a location inside the compiled code
    assert record.notes["filename"].endswith("DataSet.cc")
    assert "line" in record.notes
    # stamped by this process
    assert record.pid == os.getpid()

    # clean up
    courier.close()
    os.close(reader)
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
