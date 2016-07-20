// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// given a file named "grid.dat" in the current directory, use the low level interface to map
// it into memory

// portability
#include <portinfo>

// support
#include <pyre/geometry.h>

// entry point
int main() {
    // units
    auto k = 1024;
    // declare the type of a pixel
    typedef double pixel_t;
    // fix the rep
    typedef std::array<int, 3> rep_t;
    // build the parts
    typedef pyre::geometry::index_t<rep_t> index_t;
    typedef pyre::geometry::layout_t<rep_t> layout_t;
    typedef pyre::geometry::tile_t<index_t, layout_t> tile_t;

    // the name of the file
    pyre::geometry::uri_t name {"grid.dat"};
    // make a layout
    tile_t::layout_type layout {2, 1, 0};
    // make a shape
    tile_t::index_type shape {1*k, 3*k, 3};
    // make a tile
    tile_t tile {shape, layout};

    // compute the size of the payload
    size_t size = sizeof(pixel_t) * tile.size();

    // turn on the info channel
    // pyre::journal::debug_t("pyre.geometry.direct").activate();
    // map a buffer over the file
    void * buffer = pyre::geometry::direct_t::map("grid.dat", size, 0, true);
    // and undo it
    pyre::geometry::direct_t::unmap(buffer, size);

    // all done
    return 0;
}

// end of file
