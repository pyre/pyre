// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the memory
#include <pyre/memory.h>


// type alias
using view_t = pyre::memory::view_t<double>;


// create a view over a foreign block of data
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("view_oob");

    // silence the firewall
    pyre::journal::firewall_t::quiet();

    // the number of cells
    std::size_t cells = 1024ul;
    // allocate a memory block
    double * block = new double[cells];

    // convert it into a view
    view_t product(block, cells);

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

    // clean up
    delete [] block;

    // all done
    return 0;
}


// end of file
