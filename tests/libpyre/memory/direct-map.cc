// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// given a file named "grid.dat" in the current directory, use the low level interface to map
// it into memory

// portability
#include <portinfo>
// externals
#include <unistd.h>
// support
#include <pyre/memory.h>
#include <pyre/geometry.h>

// entry point
int main() {
    // desired size
    size_t page = ::getpagesize();
    // the name of the file
    pyre::memory::uri_t name {"grid.dat"};

    // turn on the info channel
    // pyre::journal::debug_t("pyre.memory.direct").activate();
    // map a buffer over the file
    void * buffer = pyre::memory::direct_t::map(name, page, 0, true);
    // and undo it
    pyre::memory::direct_t::unmap(buffer, page);

    // all done
    return 0;
}

// end of file
