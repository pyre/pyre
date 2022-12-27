// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_externals_h)
#define pyre_timers_externals_h


// externals
#include <time.h>
#include <string>
#include <map>
#include <ctime>
#include <chrono>
#include <sstream>


// aliases for fundamental types that define implementation choices
namespace pyre::timers {
    // sizes of things
    using size_t = std::size_t;
    // strings
    using string_t = std::string;
    // scratch buffers
    using buffer_t = std::stringstream;

    // timer names
    using name_t = string_t;

    // time durations
    using seconds_t = std::chrono::duration<double>;
    using milliseconds_t = std::chrono::duration<double, std::milli>;
    using microseconds_t = std::chrono::duration<double, std::micro>;
}


#endif

// end of file
