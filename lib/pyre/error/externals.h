// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_error_externals_h)
#define pyre_error_externals_h


// prefer STL <source_location> (since C++20)
#if __has_include(<source_location>)
#include <source_location>

namespace pyre::error {
    using source_location_t = std::source_location;
}

// fallback on Library Fundamentals TS v2 <experimental/source_location>
#elif __has_include(<experimental/source_location>)
#include <experimental/source_location>

namespace pyre::error {
    using source_location_t = std::experimental::source_location;
}

// no support for source_location
#else
#error could not find source_location header
#endif


#endif

// end of file
