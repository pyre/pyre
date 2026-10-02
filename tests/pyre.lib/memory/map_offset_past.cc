// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// access the memory package
#include <pyre/memory.h>
// support
#include <cassert>
#include <fstream>
#include <stdexcept>


// type aliases
using cell_t = double;
using constmap_t = pyre::memory::constmap_t<cell_t>;


// map a product with an offset right at its end, and with one past it
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("map_offset_past");

    // the product
    auto uri = "map_offset_past.dat";
    // make one that holds a header and nothing else
    {
        // make a stream
        std::ofstream product(uri, std::ios::binary | std::ios::trunc);
        // and write a header of 64 bytes
        product.write("0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef", 64);
    }

    // silence the error channel
    pyre::journal::error_t::quiet();
    // offsets right at the end of the file, and past it, leave nothing to map
    for (auto offset : { 64, 65 }) {
        // so, gingerly
        try {
            // map it
            constmap_t product(uri, false, offset);
            // unreachable
            throw std::logic_error("unreachable");
        }
        // the complaint
        catch (const pyre::journal::error_t::exception_type &) {
            // is the expected outcome
        }
    }

    // all done
    return 0;
}


// end of file
