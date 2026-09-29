#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Lay a grid over a product with an embedded header, in each byte order, using nothing but its
    sidecar
    """
    # access the package
    import pyre

    # and the grid factories
    import pyre.grid

    # for packing the product
    import struct

    # the layout
    lines, samples = 2, 3
    # the values, each with four distinct bytes
    values = [0x01020300 + i for i in range(lines * samples)]
    # an embedded header whose length leaves the cells misaligned
    embedded = b"ENVI embedded header"

    # for each byte order the header can declare
    for order, code in [(0, "<"), (1, ">")]:
        # the product and its sidecar
        uri = f"envi_offset_test_{order}.dat"
        hdr = f"envi_offset_test_{order}.hdr"
        # write the product in that order, behind its embedded header
        with open(uri, "wb") as product:
            # the header
            product.write(embedded)
            # and the cells
            product.write(struct.pack(f"{code}{len(values)}I", *values))
        # describe it
        header = pyre.envi.header(
            samples=samples,
            lines=lines,
            bands=1,
            dataType=13,
            interleave="bsq",
            byteOrder=order,
            headerOffset=len(embedded),
        )
        # write the sidecar
        pyre.envi.writer().write(header=header, uri=hdr)

        # read the sidecar back
        header = pyre.envi.reader().read(uri=hdr)
        # it knows how far into the product the cells start
        assert header.offset == len(embedded)
        # lay a grid over the product using only what the header says
        grid = pyre.grid.map(
            uri=uri,
            shape=header.shape,
            cell=header.cell,
            create=False,
            writable=False,
            offset=header.offset,
        )
        # every cell must read as its value, wherever it sits and whatever its byte order
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
