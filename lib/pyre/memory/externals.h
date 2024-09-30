// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#if !defined(pyre_memory_externals_h)
#define pyre_memory_externals_h


// standard library
#include <stdexcept>
#include <array>
#include <fstream>
#include <utility>

// low level stuff
#include <complex>    // for {complex}
#include <cstdint>    // for type aliases for the basic types
#include <cstring>    // for {strerror}
#include <fcntl.h>    // for {open}
#include <unistd.h>   // for {close}
#include <sys/mman.h> // for {mmap}
#include <sys/stat.h> // for the mode flags

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

    // the basic types
    // unsigned
    using uint8_t = std::uint8_t;
    using uint16_t = std::uint16_t;
    using uint32_t = std::uint32_t;
    using uint64_t = std::uint64_t;
    // signed
    using int8_t = std::int8_t;
    using int16_t = std::int16_t;
    using int32_t = std::int32_t;
    using int64_t = std::int64_t;
    // floating point
    using float32_t = float;
    using float64_t = double;
    // complex
    using complex64_t = std::complex<float>;
    using complex128_t = std::complex<double>;
} // namespace pyre::memory


#endif

// end of file
