// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// STL
#include <cstdint>
#include <utility>

// declarations
#include <pyre/typelists/concat.h>


// driver
int
main()
{
    // the empty list
    using nil_t = pyre::typelists::types_t<>;
    // and a couple of non empty lists
    using ints_t = pyre::typelists::types_t<char, int, long>;
    using uints_t = pyre::typelists::types_t<unsigned char, unsigned int, unsigned long>;
    using floats_t = pyre::typelists::types_t<float, double>;

    // no arguments
    using zero_t = pyre::typelists::concat_t<>::type;
    // verify
    static_assert(std::is_same_v<zero_t, nil_t>, "mismatch in zero_t");

    // one argument
    using one_t = pyre::typelists::concat_t<ints_t>::type;
    // verify
    static_assert(std::is_same_v<one_t, ints_t>, "mismatch in one_t");

    // list U nil
    using lUn_t = pyre::typelists::concat_t<ints_t, nil_t>::type;
    // verify
    static_assert(std::is_same_v<lUn_t, ints_t>, "mismatch in lUn_t");

    // nil U list
    using nUl_t = pyre::typelists::concat_t<nil_t, ints_t>::type;
    // verify
    static_assert(std::is_same_v<nUl_t, ints_t>, "mismatch in nUl_t");

    // list U list
    using lUl_t = pyre::typelists::concat_t<ints_t, floats_t>::type;
    // verify
    static_assert(
        std::is_same_v<lUl_t, pyre::typelists::types_t<char, int, long, float, double>>,
        "mismatch in lUl_t");

    // list U list U list
    using lUlUl_t = pyre::typelists::concat_t<ints_t, uints_t, floats_t>::type;
    // verify
    static_assert(
        std::is_same_v<
            lUlUl_t,
            pyre::typelists::types_t<
                char, int, long, unsigned char, unsigned int, unsigned long, float, double>>,
        "mismatch in lUlUl_t");

    // all done
    return 0;
}


// end of file
