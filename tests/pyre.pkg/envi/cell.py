#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Lay a grid over a product written in each byte order, using nothing but its header
    """
    # access the package
    import pyre

    # and the grid factories
    import pyre.grid

    # for packing the product
    import struct

    # the layout
    lines, samples = 2, 3
    # the values, each with two distinct bytes
    values = [0x0100 * (i + 1) + (i + 1) for i in range(lines * samples)]

    # for each byte order the header can declare
    for order, code in [(0, "<"), (1, ">")]:
        # the product and its sidecar
        uri = f"envi_cell_test_{order}.dat"
        hdr = f"envi_cell_test_{order}.hdr"
        # write the product in that order
        with open(uri, "wb") as product:
            product.write(struct.pack(f"{code}{len(values)}H", *values))
        # describe it
        header = pyre.envi.header(
            samples=samples, lines=lines, bands=1, dataType=12, interleave="bsq", byteOrder=order
        )
        # write the sidecar
        pyre.envi.writer().write(header=header, uri=hdr)

        # read the sidecar back
        header = pyre.envi.reader().read(uri=hdr)
        # lay a grid over the product using only what the header says
        grid = pyre.grid.map(
            uri=uri, shape=header.shape, cell=header.cell, create=False, writable=False
        )
        # every cell must read as its value, whatever the order of the bytes on disk
        assert [grid[i, j] for i in range(lines) for j in range(samples)] == values
        # let go
        del grid

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
