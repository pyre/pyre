// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the memory
#include <pyre/memory.h>


// type alias
using heap_t = pyre::memory::heap_t<double>;


// verify that we can construct and use heap blocks
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("heap_oob");

    // silence the firewall
    pyre::journal::firewall_t::quiet();

    // the number of cells
    std::size_t cells = 1024ul;
    // make a block on the heap
    heap_t product(cells);

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
