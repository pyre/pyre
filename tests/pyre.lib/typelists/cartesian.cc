// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// STL
#include <complex>
#include <cstdint>
#include <utility>

// declarations
#include <pyre/typelists/cartesian.h>


// driver
int
main()
{
    // the empty type list
    using nil_t = pyre::typelists::types_t<>;

    // nil x nil
    using nxn_t = pyre::typelists::cartesian_t<nil_t, nil_t>::type;
    // verify
    static_assert(std::is_same_v<nxn_t, nil_t>, "mismatch in nxn_t");
    // make a non empty list of length one
    using bytes_t = pyre::typelists::types_t<std::uint8_t>;

    // one x nil
    using oxn_t = pyre::typelists::cartesian_t<bytes_t, nil_t>::type;
    // verify
    static_assert(std::is_same_v<oxn_t, nil_t>, "mismatch in oxn_t");

    // nil x one
    using nxo_t = pyre::typelists::cartesian_t<nil_t, bytes_t>::type;
    // verify
    static_assert(std::is_same_v<nxo_t, nil_t>, "mismatch in nxo_t");

    // make a non empty list of length two
    using real_t = pyre::typelists::types_t<std::float_t, std::double_t>;

    // one x nil
    using oxn_t = pyre::typelists::cartesian_t<real_t, nil_t>::type;
    // verify
    static_assert(std::is_same_v<oxn_t, nil_t>, "mismatch in oxn_t");

    // nil x one
    using nxo_t = pyre::typelists::cartesian_t<nil_t, real_t>::type;
    // verify
    static_assert(std::is_same_v<nxo_t, nil_t>, "mismatch in nxo_t");

    // one x list
    using oxl_t = pyre::typelists::cartesian_t<bytes_t, real_t>::type;
    // verify
    static_assert(
        std::is_same_v<
            oxl_t, pyre::typelists::types_t<
                       pyre::typelists::types_t<std::uint8_t, std::float_t>,
                       pyre::typelists::types_t<std::uint8_t, std::double_t>>>,
        "mismatch in oxl_t");

    // list x one
    using lxo_t = pyre::typelists::cartesian_t<real_t, bytes_t>::type;
    // verify
    static_assert(
        std::is_same_v<
            lxo_t, pyre::typelists::types_t<
                       pyre::typelists::types_t<std::float_t, std::uint8_t>,
                       pyre::typelists::types_t<std::double_t, std::uint8_t>>>,
        "mismatch in lxo_t");

    // a deeper example
    using ints_t = pyre::typelists::types_t<std::int8_t, std::int16_t, std::int32_t>;
    using complex_t = pyre::typelists::types_t<std::complex<float>, std::complex<double>>;

    // multiply out
    using mixed_t = pyre::typelists::cartesian_t<ints_t, complex_t>::type;
    // verify
    static_assert(
        std::is_same_v<
            mixed_t, pyre::typelists::types_t<
                         pyre::typelists::types_t<std::int8_t, std::complex<float>>,
                         pyre::typelists::types_t<std::int8_t, std::complex<double>>,
                         pyre::typelists::types_t<std::int16_t, std::complex<float>>,
                         pyre::typelists::types_t<std::int16_t, std::complex<double>>,
                         pyre::typelists::types_t<std::int32_t, std::complex<float>>,
                         pyre::typelists::types_t<std::int32_t, std::complex<double>>>>,
        "mismatch in mixed_t");

    // one x one x one
    using oxoxo_t = pyre::typelists::cartesian_t<
        pyre::typelists::types_t<char>, pyre::typelists::types_t<int>,
        pyre::typelists::types_t<float>>::type;
    // verify
    static_assert(
        std::is_same_v<
            oxoxo_t, pyre::typelists::types_t<pyre::typelists::types_t<char, int, float>>>,
        "mismatch in oxoxo_t");

    // list x list x list
    using lxlxl_t = pyre::typelists::cartesian_t<real_t, real_t, real_t>::type;
    // verify
    static_assert(
        std::is_same_v<
            lxlxl_t, pyre::typelists::types_t<
                         pyre::typelists::types_t<float, float, float>,
                         pyre::typelists::types_t<float, float, double>,
                         pyre::typelists::types_t<float, double, float>,
                         pyre::typelists::types_t<float, double, double>,
                         pyre::typelists::types_t<double, float, float>,
                         pyre::typelists::types_t<double, float, double>,
                         pyre::typelists::types_t<double, double, float>,
                         pyre::typelists::types_t<double, double, double>>>,
        "mismatch in lxlxl_t");

    // all done
    return 0;
}


// end of file
