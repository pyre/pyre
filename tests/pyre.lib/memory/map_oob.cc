// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// access the memory package
#include <pyre/memory.h>


// type aliases
using cell_t = double;
using map_t = pyre::memory::map_t<cell_t>;


// create a map over an existing product in read-only mode
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("map_oob");

    // silence the firewall
    pyre::journal::firewall_t::quiet();

    // open an existing file-backed memory block
    map_t product("map.dat");

    // gingerly
    try {
        // make an out-of-bounds access
        product.at(product.cells());
        // unreachable
        throw std::logic_error("unreachable");
    // catch the firewall
    } catch (const pyre::journal::firewall_t::exception_type &) {
        // all good
    }

    // all done
    return 0;
}


// end of file
