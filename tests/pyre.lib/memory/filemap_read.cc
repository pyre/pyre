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


// open an existing filemap in read-only mode
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("filemap_read");

    // open an existing file-backed memory block for read
    filemap_t product("filemap.dat");

    // get the block size
    auto bytes = product.bytes();
    // we expect a 4k block
    assert(( bytes == 4*1024ul ));

    // our value expectation
    char value = 0x20;
    // get the block as an array of bytes
    auto data = static_cast<char *>(product.data());

    // go through the entire block
    for (std::size_t offset = 0; offset < bytes; ++offset) {
        // make sure the value is what we expect
        assert(( data[offset] == value ));
    }

    // all done
    return 0;
}


// end of file
