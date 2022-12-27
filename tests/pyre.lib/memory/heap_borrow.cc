// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get memory
#include <pyre/memory.h>
// support
#include <cassert>


// type alias
using heap_t = pyre::memory::heap_t<double>;
using constheap_t = pyre::memory::constheap_t<double>;


// an initializer that takes a {heap_t} by value
double initialize(heap_t block) {
    // make a channel
    pyre::journal::debug_t channel("pyre.memory.heap");
    // show me
    channel
        << "initialize: got a block at " << block.data()
        << pyre::journal::endl(__HERE__);

    // pick a value
    double value = 42;
    // iterate over the entire block
    for (auto & cell : block) {
        // and set every cell to my value;
        cell = value;
    }
    // all done
    return value;
}


void check(constheap_t block, double value) {
    // verify we can iterate and read
    for (auto cell : block) {
        // check that we have what we expect
        assert(( cell == value ));
    }

    // all done
    return;
}


// verify that we can construct and use heap blocks
int main(int argc, char *argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("heap_borrow");
    // make a channel
    pyre::journal::debug_t channel("pyre.memory.heap");

    // the number of cells
    std::size_t cells = 1024ul;
    // make a block on the heap
    heap_t block(cells);
    // show me
    channel
        << "main: made a block at " << block.data()
        << pyre::journal::endl(__HERE__);
    // send it to the initializer
    auto value = initialize(block);

    // make a const version
    constheap_t cblock { block.handle(), block.cells() };
    // and check it
    check(cblock, value);

    // all done
    return 0;
}


// end of file
