// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// STL
#include <cstdint>
#include <utility>

// declarations
#include <pyre/typelists/typelist.h>


// driver
int
main()
{
    // make a type list
    using ints_t = pyre::typelists::types_t<std::int8_t, std::int16_t>;

    // check
    static_assert(
        std::is_same_v<
            // check
            ints_t, pyre::typelists::types_t<std::int8_t, std::int16_t>>,
        "mismatch in ints_t");

    // all done
    return 0;
}


// end of file
