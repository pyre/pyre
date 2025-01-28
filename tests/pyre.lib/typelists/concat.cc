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
    // make two type lists
    using narrow_t = pyre::typelists::types_t<std::int8_t, std::int16_t>;
    using wide_t = pyre::typelists::types_t<std::int32_t, std::int64_t>;
    using real_t = pyre::typelists::types_t<std::float_t, std::double_t>;

    // splice two together
    using lcl_t = pyre::typelists::concat_t<narrow_t, wide_t>::type;
    // splice three together
    using lclcl_t = pyre::typelists::concat_t<narrow_t, wide_t, real_t>::type;

    // edge cases
    using nil_t = pyre::typelists::concat_t<>::type;
    using one_t = pyre::typelists::concat_t<narrow_t>::type;
    using lcn_t = pyre::typelists::concat_t<narrow_t, pyre::typelists::types_t<>>::type;
    using ncl_t = pyre::typelists::concat_t<pyre::typelists::types_t<>, narrow_t>::type;

    // check
    // the common two list case
    static_assert(
        std::is_same_v<
            // check
            lcl_t, pyre::typelists::types_t<std::int8_t, std::int16_t, std::int32_t, std::int64_t>>,
        "mismatch in lcl_t");

    // the common three list case
    static_assert(
        std::is_same_v<
            // check
            lclcl_t, pyre::typelists::types_t<
                         std::int8_t, std::int16_t, std::int32_t, std::int64_t, std::float_t,
                         std::double_t>>,
        "mismatch in lcl_t");

    // edge cases
    static_assert(
        std::is_same_v<
            // check
            nil_t, pyre::typelists::types_t<>>,
        "mismatch in nil_t");

    static_assert(
        std::is_same_v<
            // check
            one_t, narrow_t>,
        "mismatch in one_t");

    static_assert(
        std::is_same_v<
            // check
            lcn_t, narrow_t>,
        "mismatch in lcn_t");

    static_assert(
        std::is_same_v<
            // check
            ncl_t, narrow_t>,
        "mismatch in ncl_t");

    // all done
    return 0;
}


// end of file
