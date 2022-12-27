// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// access the memory package
#include <pyre/memory.h>
// support
#include <cassert>


// type aliases
using filemap_t = pyre::memory::filemap_t;


// create a new filemap
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("filemap_create");

    // create a new file-backed memory block
    // N.B.: the {ul} suffix is necessary to disambiguate the constructor
    filemap_t product("filemap.dat", 4*1024ul);

    // get the actual size
    auto bytes = product.bytes();
    // we expect a 4k block
    assert(( bytes == 4*1024ul ));

    // make a byte
    char value = 0xff;
    // access the block as an array of bytes
    auto data = static_cast<char *>(product.data());

    // go through the entire block
    for (std::size_t offset = 0; offset < bytes; ++offset) {
        // and fill it with our byte
        data[offset] = value;
    }

    // all done
    return 0;
}


// end of file
