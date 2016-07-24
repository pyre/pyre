// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// given a file named "grid.dat" in the current directory, use the high level interface to map
// it into memory

// portability
#include <portinfo>

// support
#include <pyre/memory.h>
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
    pyre::memory::uri_t name {"grid.dat"};
    // make a layout
    tile_t::layout_type layout {2, 1, 0};
    // make a shape
    tile_t::index_type shape {1*k, 3*k, 3};
    // make a tile
    tile_t tile {shape, layout};

    // compute the expected size of the payload
    size_t size = sizeof(pixel_t) * tile.size();

    // map the file
    // turn on the info channel
    // pyre::journal::debug_t("pyre.memory.direct").activate();
    // map a buffer over the file; it gets unmapped on destruction
    pyre::memory::direct_t map {name};

    // ask the map for its size and compare against our calculation
    if (map.size() != size) {
        // make a channel
        pyre::journal::firewall_t firewall("pyre.memory.direct");
        // and complain
            firewall
                << pyre::journal::at(__HERE__)
                << "size mismatch for file '" << name << "': " << pyre::journal::newline
                << "  expected " << size << " bytes, got " << map.size() << " bytes"
                << pyre::journal::endl;
            // and bail
            return 1;
    }

    // all done
    return 0;
}

// end of file
