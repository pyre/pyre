// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// declarations
#include <pyre/typelists/list.h>


// driver
int
main()
{
    // make a type list
    using ints_t = typename pyre::typelists::list_t<int, 3>::type;

    // check
    static_assert(
        std::is_same_v<
            // check
            ints_t, pyre::typelists::types_t<int, int, int>>,
        "mismatch in ints_t");

    // all done
    return 0;
}


// end of file
