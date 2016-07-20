// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// portability
#include <portinfo>

// support
#include <pyre/grid.h>

// entry point
int main() {
    // units
    auto k = 1024;
    // declare the type of a pixel
    typedef double pixel_t;
    // the name of the file
    pyre::grid::string_t name {"grid.dat"};
    // specify the shape of the data
    pyre::grid::shape_t shape {1*k, 3*k, 3};
    // make a tile
    pyre::grid::tile_t tile {shape, pyre::grid::layout::pixel};

    // compute the size of the payload
    size_t size = sizeof(pixel_t) * tile.pixels();

    // map the file
    // turn on the info channel
    pyre::journal::debug_t("pyre.grid.direct").activate();
    // map a buffer over the file; it gets unmapped on destruction
    pyre::grid::direct_t map {name, size};
    // and make a copy
    pyre::grid::direct_t clone {map};

    // all done
    return 0;
}

// end of file
