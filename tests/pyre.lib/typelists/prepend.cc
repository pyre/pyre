// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// STL
#include <cstdint>
#include <utility>

// declarations
#include <pyre/typelists/prepend.h>


// driver
int
main()
{
    // make a type list
    using bytes_t = pyre::typelists::types_t<std::int8_t>;
    // add to it
    using words_t = pyre::typelists::prepend_t<bytes_t, std::int16_t>::type;
    // both ways
    using dwords_t = pyre::typelists::prepend_t<bytes_t, std::int32_t, std::int16_t>::type;

    // check
    static_assert(
        std::is_same_v<
            // check
            words_t, pyre::typelists::types_t<std::int16_t, std::int8_t>>,
        "mismatch in words_t");

    static_assert(
        std::is_same_v<
            // check
            dwords_t, pyre::typelists::types_t<std::int32_t, std::int16_t, std::int8_t>>,
        "mismatch in dwords_t");

    // all done
    return 0;
}


// end of file
