// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// access the memory package
#include <pyre/memory.h>
// support
#include <cassert>
#include <filesystem>
#include <stdexcept>


// type aliases
using cell_t = double;
using map_t = pyre::memory::map_t<cell_t>;


// create a product with no cells
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("map_create_empty");

    // the product
    auto uri = "map_create_empty.dat";

    // silence the error channel
    pyre::journal::error_t::quiet();
    // gingerly
    try {
        // make a product with no room for anything
        auto product = map_t::create(uri, 0);
        // unreachable
        throw std::logic_error("unreachable");
    }
    // the complaint
    catch (const pyre::journal::error_t::exception_type &) {
        // is the expected outcome
    }
    // and the refusal leaves no file behind
    assert((!std::filesystem::exists(uri)));

    // all done
    return 0;
}


// end of file
