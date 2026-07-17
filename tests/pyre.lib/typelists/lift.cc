// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// STL
#include <cstdint>
#include <type_traits>

// declarations
#include <pyre/typelists/lift.h>
#include <pyre/typelists/lower.h>
#include <pyre/typelists/cartesian.h>


// driver
int
main()
{
    // a boolean axis as a value list
    using bools_t = pyre::typelists::values_t<true, false>;
    // lift it into a type list
    using liftedBools_t = pyre::typelists::lift_t<bools_t>::type;
    // it should be a {types_t} of boolean constants
    static_assert(
        std::is_same_v<
            liftedBools_t,
            pyre::typelists::types_t<std::bool_constant<true>, std::bool_constant<false>>>,
        "mismatch in liftedBools_t");

    // an integer axis as a value list
    using nums_t = pyre::typelists::values_t<1, 2, 3, 4>;
    // lift it into a type list
    using liftedNums_t = pyre::typelists::lift_t<nums_t>::type;
    // it should be a {types_t} of integral constants, each carrying its own value
    static_assert(
        std::is_same_v<
            liftedNums_t, pyre::typelists::types_t<
                              std::integral_constant<int, 1>, std::integral_constant<int, 2>,
                              std::integral_constant<int, 3>, std::integral_constant<int, 4>>>,
        "mismatch in liftedNums_t");

    // lowering a lifted list should recover the original values
    using recovered_t = pyre::typelists::lower_t<liftedNums_t>::type;
    // verify the round trip
    static_assert(std::is_same_v<recovered_t, nums_t>, "mismatch in recovered_t");

    // the reason for the bridge: mix a value axis with a type axis
    using constness_t = pyre::typelists::lift_t<pyre::typelists::values_t<false, true>>::type;
    // against a couple of base types
    using bases_t = pyre::typelists::types_t<std::int8_t, std::int16_t>;
    // multiply them out
    using product_t = pyre::typelists::cartesian_t<constness_t, bases_t>::type;
    // {false} pairs with every base before {true} does, so the mutable variants come first
    static_assert(
        std::is_same_v<
            product_t, pyre::typelists::types_t<
                           pyre::typelists::types_t<std::bool_constant<false>, std::int8_t>,
                           pyre::typelists::types_t<std::bool_constant<false>, std::int16_t>,
                           pyre::typelists::types_t<std::bool_constant<true>, std::int8_t>,
                           pyre::typelists::types_t<std::bool_constant<true>, std::int16_t>>>,
        "mismatch in product_t");

    // all done
    return 0;
}


// end of file
