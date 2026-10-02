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
// a native cell, read wherever it sits
using native_t = pyre::memory::unaligned_t<double>;
// a big endian cell, read wherever it sits
using big_t = pyre::memory::unaligned_t<pyre::memory::big_t<std::uint32_t>>;


// the product
const auto uri = "map_unaligned.dat";
// the number of cells past its header
const auto cells = 1024;


// write a product with a header of {header} bytes in front of {cells} values, in the host's order
// or, when {big} is set, as big endian unsigned integers
void
write(std::size_t header, bool big)
{
    // make a stream
    std::ofstream product(uri, std::ios::binary | std::ios::trunc);
    // the header is a recognizable pattern
    auto preamble = std::vector<char>(header, '\xab');
    // write it
    product.write(preamble.data(), preamble.size());
    // go through the cells
    for (auto i = 0; i < cells; ++i) {
        // big endian integers
        if (big) {
            // a value with four distinct bytes
            std::uint32_t value = 0x01020300 + i;
            // spelled most significant byte first
            char bytes[] = { char(value >> 24), char(value >> 16), char(value >> 8), char(value) };
            // write them
            product.write(bytes, sizeof(bytes));
            // and move on
            continue;
        }
        // otherwise, the native value
        double value = i;
        // and its bytes
        product.write(reinterpret_cast<const char *>(&value), sizeof(value));
    }
    // all done
    return;
}


// map products whose cells sit past a header whose length is not a multiple of the cell size
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("map_unaligned");

    // unaligned cells can sit anywhere
    static_assert(alignof(native_t) == 1);
    static_assert(alignof(big_t) == 1);
    // and take up exactly as much room as the scalars they stand in for
    static_assert(sizeof(native_t) == sizeof(double));
    static_assert(sizeof(big_t) == sizeof(std::uint32_t));

    // a short header, and one that pushes the cells past the first page
    for (std::size_t header : { 3, 4096 + 5 }) {
        // make a product of native values
        write(header, false);

        // map it for reading, past its header
        {
            // open it
            pyre::memory::constmap_t<native_t> product(uri, false, header);
            // the block holds the cells and nothing else
            assert((product.cells() == cells));
            // the cells are misaligned
            assert((reinterpret_cast<std::uintptr_t>(product.data()) % alignof(double) != 0));
            // but every one of them reads as its index
            for (auto i = 0; i < cells; ++i) {
                // check
                assert((product[i] == i));
            }
        }

        // map it for writing, past its header
        {
            // open it
            pyre::memory::map_t<native_t> product(uri, true, header);
            // change a cell
            product[7] = -1;
        }
        // and map it again
        {
            // for reading
            pyre::memory::constmap_t<native_t> product(uri, false, header);
            // the change must have stuck
            assert((product[7] == -1));
            // and left its neighbors alone
            assert((product[6] == 6 && product[8] == 8));
        }

        // make a product of big endian integers
        write(header, true);
        // map it for reading, past its header
        pyre::memory::constmap_t<big_t> product(uri, false, header);
        // the block holds the cells and nothing else
        assert((product.cells() == cells));
        // go through the cells
        for (auto i = 0; i < cells; ++i) {
            // each must read as its value, swapped into the host's order
            assert((product[i] == std::uint32_t(0x01020300 + i)));
        }
    }

    // all done
    return 0;
}


// end of file
