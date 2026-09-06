// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <cstdio>
#include <fstream>
// get the grid
#include <pyre/grid.h>
// and the storage strategies
#include <pyre/memory.h>


// the parts of the grid under test: a canonical layout over a file whose cells were written in
// the byte order the host lacks
using value_t = pyre::memory::uint16_t;
using cell_t = pyre::memory::foreign_t<value_t>;
using canonical_t = pyre::grid::canonical_t<2>;
using map_t = pyre::memory::map_t<cell_t>;
using constmap_t = pyre::memory::constmap_t<cell_t>;
using grid_t = pyre::grid::grid_t<canonical_t, map_t>;
using constgrid_t = pyre::grid::grid_t<canonical_t, constmap_t>;
// and the pieces used to address it
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;
// the bytes of one cell
using bytes_t = std::array<std::byte, sizeof(value_t)>;


// the bytes of a value as a machine of the other endianness would write them
static auto
swapped(value_t value) -> bytes_t
{
    // take the value apart
    auto bytes = std::bit_cast<bytes_t>(value);
    // and reverse it
    std::reverse(bytes.begin(), bytes.end());
    // all done
    return bytes;
}


// verify that a grid over byte ordered cells reads a foreign order data product in place, and
// writes back in the same order
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("grid_map_foreign");

    // the file that backs this grid
    const char * uri = "grid_map_foreign.data";
    // pick a shape
    constexpr shape_t shape { 3, 4 };
    // lay it out canonically
    const canonical_t packing { shape };

    // write the product the way a machine of the other endianness would: each cell holds its
    // own offset, with its bytes reversed relative to this host
    {
        // open the file
        std::ofstream product(uri, std::ios::binary);
        // go through the cells
        for (auto offset = 0; offset < packing.cells(); ++offset) {
            // the foreign bytes of this cell
            auto bytes = swapped(static_cast<value_t>(offset));
            // write them
            product.write(reinterpret_cast<const char *>(bytes.data()), bytes.size());
        }
    }

    // map the product read-only, over byte ordered cells
    {
        // open
        const constmap_t store = constmap_t::open(uri);
        // the file holds exactly the cells of the grid
        assert((store.cells() == packing.cells()));
        // make a grid over it
        const constgrid_t grid { packing, store };
        // every cell must read as its own offset, in native form
        for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
            // the value has to come through the swap
            assert((grid[*it] == static_cast<value_t>(packing.offset(*it))));
        }
        // spot check a cell whose two bytes differ
        assert((grid[index_t { 2, 3 }] == 11));
    }

    // map it for writing and change a cell
    {
        // open
        const map_t store = map_t::open(uri, true);
        // make a grid over it
        const grid_t grid { packing, store };
        // write a value with distinguishable bytes
        grid[index_t { 1, 1 }] = 0x1234;
        // and read it right back
        assert((grid[index_t { 1, 1 }] == 0x1234));
    }

    // the file must now hold the new value in the foreign order
    {
        // open the file
        std::ifstream product(uri, std::ios::binary);
        // seek to the cell
        product.seekg(packing.offset(index_t { 1, 1 }) * sizeof(value_t));
        // read its bytes
        bytes_t bytes;
        product.read(reinterpret_cast<char *>(bytes.data()), bytes.size());
        // they must be the swapped form of the value
        assert((bytes == swapped(0x1234)));
    }

    // done with the backing file
    std::remove(uri);

    // all done
    return 0;
}


// end of file
