// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// given a file named "grid.dat" in the current directory, use the high level interface to map
// it into memory

// portability
#include <portinfo>

// support
#include <pyre/memory.h>
#include <pyre/geometry.h>

// entry point
int main() {
    // units
    auto k = 1024;
    // desired size
    size_t page = 4*k;

    // allocate a buffer
    void * buffer = ::operator new(page);

    // if this succeeded
    if (buffer) {
        // turn on the info channel
        // pyre::journal::debug_t("pyre.memory.direct").activate();
        // create a view over the buffer
        pyre::memory::view_t v1 {buffer};
        // make a copy
        pyre::memory::view_t v2 {v1};
        // check that they point to the same memory location
        if (v1.buffer() != v2.buffer()) {
            // make a channel
            pyre::journal::firewall_t firewall("pyre.memory.view");
            // complain
            firewall
                << pyre::journal::at(__HERE__)
                << "view not properly copied:" << pyre::journal::newline
                << "  expected " << v1.buffer() << ", got " << v2.buffer()
                << pyre::journal::endl;
            // and bail
            return 1;
        }
    }

    // if all goes well, the following deallocation will not raise any exceptions...
    ::operator delete(buffer);

    // all done
    return 0;
}

// end of file
