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
    // the name of the file
    pyre::memory::uri_t name {"grid.dat"};

    // map the file
    // turn on the info channel
    // pyre::journal::debug_t("pyre.memory.direct").activate();
    // map a buffer over the file; it gets unmapped on destruction
    pyre::memory::direct_t map {name, page, page};

    // ask the map for its size and compare against our calculation
    if (map.size() != page) {
        // make a channel
        pyre::journal::firewall_t firewall("pyre.memory.direct");
        // complain
        firewall
            << pyre::journal::at(__HERE__)
            << "size mismatch for file '" << name << "': " << pyre::journal::newline
            << "  expected " << page << " bytes, got " << map.size() << " bytes"
            << pyre::journal::endl;
        // and bail
        return 1;
    }

    // all done
    return 0;
}

// end of file
