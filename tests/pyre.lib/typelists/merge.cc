// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// STL
#include <cstdint>
#include <utility>

// declarations
#include <pyre/typelists/merge.h>


// driver
int
main()
{
    // the empty list
    using nil_t = pyre::typelists::types_t<>;

    // nil U nil
    using nUn = pyre::typelists::merge_t<nil_t, nil_t>::type;
    // check
    static_assert(std::is_same_v<nUn, nil_t>, "mismatch in nUn");

    // type U type
    using tUt = pyre::typelists::merge_t<int, double>::type;
    // check
    static_assert(std::is_same_v<tUt, pyre::typelists::types_t<int, double>>, "mismatch in tut_t");

    // a list of length one
    using one_t = pyre::typelists::types_t<int>;

    // one U nil
    using oUn = pyre::typelists::merge_t<one_t, pyre::typelists::types_t<>>::type;
    // check
    static_assert(std::is_same_v<oUn, one_t>, "mismatch in nUn");

    // nil U one
    using nUo = pyre::typelists::merge_t<pyre::typelists::types_t<>, one_t>::type;
    // check
    static_assert(std::is_same_v<nUo, one_t>, "mismatch in nUn");


#if NYI
    // a list of length one
    using one_t = types_t<std::float_t>;
    // merge
    using ox1_t = merge_t<std::uint8_t, one_t>::type;
    // check
    static_assert(
        std::is_same_v<ox1_t, types_t<types_t<std::uint8_t, std::float_t>>>, "mismatch in ox1_t");

    // a list of length two
    using two_t = types_t<std::float_t, std::double_t>;
    // merge
    using ox2_t = merge_t<std::uint8_t, two_t>::type;
    // check
    static_assert(
        std::is_same_v<
            ox2_t,
            types_t<types_t<std::uint8_t, std::float_t>, types_t<std::uint8_t, std::double_t>>>,
        "mismatch in ox2_t");

    // a list of length three
    using three_t = types_t<std::uint64_t, std::float_t, std::double_t>;
    // merge
    using ox3_t = merge_t<std::uint8_t, three_t>::type;
    // check
    static_assert(
        std::is_same_v<
            ox3_t, types_t<
                       types_t<std::uint8_t, std::uint64_t>, types_t<std::uint8_t, std::float_t>,
                       types_t<std::uint8_t, std::double_t>>>,
        "mismatch in ox3_t");
#endif

    // all done
    return 0;
}


// end of file
