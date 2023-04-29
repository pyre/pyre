// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_externals_h)
#define pyre_memory_externals_h


// standard library
#include <stdexcept>
#include <array>
#include <fstream>
#include <utility>

// low level stuff
#include <cstring>     // for {strerror}
#include <fcntl.h>     // for {open}
#include <unistd.h>    // for {close}
#include <sys/mman.h>  // for {mmap}
#include <sys/stat.h>  // for the mode flags

// support
#include <pyre/journal.h>


// aliases that define implementation choices
namespace pyre::memory {
    // sizes of things
    using size_t = std::size_t;
    // distances
    using ptrdiff_t = std::ptrdiff_t;

    // strings
    using string_t = std::string;
    // names of things
    using name_t = string_t;
    // filenames
    using uri_t = std::string;
    // file information
    using info_t = struct stat;
}


#endif

// end of file
