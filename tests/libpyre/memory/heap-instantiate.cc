// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// given a file named "grid.dat" in the current directory, use the high level interface to map
// it into memory

// portability
#include <portinfo>
// externals
#include <unistd.h>
// support
#include <pyre/journal.h>
#include <pyre/memory.h>
#include <pyre/geometry.h>

// entry point
int main() {
    // desired size
    size_t page = ::getpagesize();

    // make an allocation
    pyre::memory::heap_t heap(page);
    // remember the allocation location
    void * data = heap.buffer();

    // use it to initialize another one
    pyre::memory::heap_t clone {std::move(heap)};
    // check that it got the same memory location
    if (clone.buffer() != data) {
        // make a channel
        pyre::journal::firewall_t firewall("pyre.memory.heap");
        // complain
        firewall
            << pyre::journal::at(__HERE__)
            << "heap copy not at expected location:" << pyre::journal::newline
            << "  expected " << data << ", got " << clone.buffer()
            << pyre::journal::endl;
        // and bail
        return 1;
    }

    // check that the source is now "empty"
    // check that it got the same memory location
    if (heap.buffer()) {
        // make a channel
        pyre::journal::firewall_t firewall("pyre.memory.heap");
        // complain
        firewall
            << pyre::journal::at(__HERE__)
            << "heap not properly moved:" << pyre::journal::newline
            << "  expected " << (void*)0 << ", got " << heap.buffer()
            << pyre::journal::endl;
        // and bail
        return 1;
    }

    // if all goes well, no exceptions will be thrown when these objects get destroyed
    return 0;
}

// end of file
