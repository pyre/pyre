// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// access the memory package
#include <pyre/memory.h>
// support
#include <cassert>
#include <cstdint>
#include <fstream>
#include <vector>


// type aliases
using cell_t = double;
using map_t = pyre::memory::map_t<cell_t>;
using constmap_t = pyre::memory::constmap_t<cell_t>;


// the product
const auto uri = "map_offset.dat";
// the number of cells past its header
const auto cells = 1024;


// write a product with a header of {header} bytes in front of its cells
void
write(std::size_t header)
{
    // make a stream
    std::ofstream product(uri, std::ios::binary | std::ios::trunc);
    // the header is a recognizable pattern
    auto preamble = std::vector<char>(header, '\xab');
    // write it
    product.write(preamble.data(), preamble.size());
    // then the cells, each holding its own index
    for (auto i = 0; i < cells; ++i) {
        // make the value
        cell_t value = i;
        // and write its bytes
        product.write(reinterpret_cast<const char *>(&value), sizeof(value));
    }
    // all done
    return;
}


// map a product whose cells sit past a header whose length is a multiple of the cell size
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("map_offset");

    // a short header, and one that pushes the cells past the first page
    for (std::size_t header : { 16, 4096 + 16 }) {
        // make the product
        write(header);

        // map it for reading, past its header
        {
            // open it
            constmap_t product(uri, false, header);
            // the block holds the cells and nothing else
            assert((product.cells() == cells));
            assert((product.bytes() == cells * sizeof(cell_t)));
            // the offset is a multiple of the cell size, so the cells are aligned
            assert((reinterpret_cast<std::uintptr_t>(product.data()) % alignof(cell_t) == 0));
            // every cell holds its index
            for (auto i = 0; i < cells; ++i) {
                // check
                assert((product[i] == i));
            }
        }

        // map it for writing, past its header
        {
            // open it
            map_t product(uri, true, header);
            // change a cell
            product[7] = -1;
        }

        // read the file back
        std::ifstream product(uri, std::ios::binary);
        // the header must be untouched
        auto preamble = std::vector<char>(header);
        // read it
        product.read(preamble.data(), preamble.size());
        // check every byte
        for (auto byte : preamble) {
            // against the pattern
            assert((byte == '\xab'));
        }
        // skip to the cell that changed
        product.seekg(header + 7 * sizeof(cell_t));
        // read it
        cell_t value = 0;
        product.read(reinterpret_cast<char *>(&value), sizeof(value));
        // it must hold the new value
        assert((value == -1));
    }

    // all done
    return 0;
}


// end of file
